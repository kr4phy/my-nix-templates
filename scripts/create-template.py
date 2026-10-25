#!/usr/bin/env python3

import re
from pathlib import Path
import shutil
import subprocess
import sys
import argparse
import json

MARKERS = ("INPUTS_BLOCK", "ARGS_BLOCK", "MODULES_BLOCK")

IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_'-]*$")


def find_repo_root() -> Path:
    # Find the template repo root.
    script_dir = Path(__file__).resolve().parent

    for directory in (script_dir, *script_dir.parents):
        if (directory / "templates").is_dir() and (directory / "nix-modules").is_dir():
            return directory

    raise RuntimeError("Could not find the template repo root.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a new Nix module from a template."
    )
    parser.add_argument(
        "--use-template",
        default="default-template",
        help="Template directory name to use. (default: default-template)",
    )
    parser.add_argument(
        "--include-module",
        action="append",
        default=[],
        metavar="PATH",
        help="Module path relative to nix-modules/.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path.cwd(),
        help="The output directory for the new flake.nix file. (default: current working directory)",
    )
    return parser.parse_args()


def load_metadata(module_path: Path) -> dict:
    # Read and validate the JSON metadata in Nix comments at the top of the module file.
    nix_source = module_path.read_text(encoding="utf-8")

    pattern = re.compile(
        r"METADATA_BLOCK_START\s*(.*?)\s*METADATA_BLOCK_END",
        re.DOTALL,
    )
    matches = pattern.findall(nix_source)

    if len(matches) != 1:
        raise ValueError(
            f"{module_path}: Expected exactly one metadata block, found {len(matches)}."
        )

    try:
        metadata = json.loads(
            matches[0],
            parse_constant=lambda value: (_ for _ in ()).throw(
                ValueError(f"Invalid JSON value: {value}")
            ),
        )
    except (json.JSONDecodeError, ValueError) as e:
        raise ValueError(f"{module_path}: Invalid JSON in metadata block: {e}") from e

    if not isinstance(metadata, dict):
        raise ValueError(f"{module_path}: Metadata block must be a JSON object.")

    inputs = metadata.get("inputs", {})
    module_args = metadata.get("moduleArgs", {})

    if not isinstance(inputs, dict):
        raise ValueError(
            f"{module_path}: 'inputs' in metadata block must be a JSON object."
        )

    if not isinstance(module_args, dict):
        raise ValueError(
            f"{module_path}: 'moduleArgs' in metadata block must be a JSON object."
        )

    for input_name, config in inputs.items():
        if not isinstance(input_name, str):
            raise ValueError(f"{module_path}: Invalid Nix input name: {input_name!r}")

        if input_name in {"self", "nixpkgs"}:
            raise ValueError(
                f"{module_path}: '{input_name}' is already provided by the template."
            )

        if not isinstance(config, dict):
            raise ValueError(
                f"{module_path}: Input '{input_name}' configuration must be a JSON object."
            )

        if not isinstance(config.get("url"), str):
            raise ValueError(
                f"{module_path}: Input '{input_name}' requires a string 'url'."
            )

    for arg_name, input_name in module_args.items():
        if not isinstance(arg_name, str) or not IDENTIFIER_RE.fullmatch(arg_name):
            raise ValueError(
                f"{module_path}: Invalid Nix module argument name: {arg_name!r}"
            )

        if not isinstance(input_name, str) or not IDENTIFIER_RE.fullmatch(input_name):
            raise ValueError(
                f"{module_path}: Invalid Nix input reference for '{arg_name}': {input_name!r}"
            )

    return metadata


def nix_string(value: str) -> str:
    # Serialize a Python string to a Nix double-quoted string literal.
    value = (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("${", "\\${")
        .replace("\n", "\\n")
        .replace("\r", "\\r")
        .replace("\t", "\\t")
    )
    return f'"{value}"'


def nix_attr_name(name: str) -> str:
    # Return a Nix attribute name, quoting it if necessary.
    if IDENTIFIER_RE.fullmatch(name):
        return name
    return nix_string(name)


def to_nix(value, indent: int = 0) -> str:
    # Recursively convert JSON-compatible values to Nix expressions.
    if value is None:
        return "null"

    if isinstance(value, bool):
        return "true" if value else "false"

    if isinstance(value, str):
        return nix_string(value)

    if isinstance(value, int):
        return str(value)

    if isinstance(value, float):
        if value != value or value in (float("inf"), float("-inf")):
            raise ValueError(f"NaN and Infinity are not supported in Nix metadata.")
        return repr(value)

    if isinstance(value, list):
        if not value:
            return "[]"

        items = [to_nix(item, indent + 2) for item in value]
        return "[" + " ".join(items) + "]"

    if isinstance(value, dict):
        if not value:
            return "{}"

        lines = []
        for key, item in value.items():
            if not isinstance(key, str):
                raise ValueError(f"Nix attribute name must be a string: {key!r}")

            lines.append(
                " " * (indent + 2)
                + f"{nix_attr_name(key)} = {to_nix(item, indent + 2)};"
            )

        return "{\n" + "\n".join(lines) + "\n" + " " * indent + "}"

    raise ValueError(
        f"Unsupported value type for Nix conversion: {type(value).__name__}"
    )


def resolve_module_path(modules_root: Path, requested: str) -> Path:
    # Resolve a module path relative to the module root.
    relative = Path(requested)

    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"Invalid module path: {requested!r}")

    if relative.suffix == "":
        relative = relative.with_suffix(".nix")

    source = (modules_root / relative).resolve()

    if not source.is_relative_to(modules_root.resolve()):
        raise ValueError(f"Module path escapes nix-modules/: {requested!r}")

    if not source.is_file():
        raise FileNotFoundError(f"Module not found: {requested}")

    return source


def merge_inputs(modules: list[tuple[Path, dict]]) -> dict:
    # Merge the inputs from multiple modules, checking for conflicts.
    merged = {}

    for path, metadata in modules:
        for name, config in metadata.get("inputs", {}).items():
            if name in merged and merged[name] != config:
                raise ValueError(
                    f"Conflicting definitions for flake input {name!r} "
                    f"(found in {path})."
                )
            merged[name] = config

    return merged


def generate_inputs_block(inputs: dict) -> str:
    return "\n".join(
        f"{nix_attr_name(name)} = {to_nix(config)};" for name, config in inputs.items()
    )


def generate_args_block(inputs: dict) -> str:
    return "\n".join(f"{name}," for name in inputs)


def generate_modules_block(modules: list[tuple[Path, dict]], modules_root: Path) -> str:
    lines = []

    for source, metadata in modules:
        relative = source.relative_to(modules_root.resolve()).as_posix()
        module_args = metadata.get("moduleArgs", {})

        lines.append(f"(import ./nix-modules/{relative} {'{'}")
        lines.append("  inherit pkgs;")

        for arg_name, input_name in module_args.items():
            lines.append(f"  {arg_name} = {input_name};")

        lines.append("})")

    return "\n".join(lines)


def replace_marker(template: str, name: str, content: str) -> str:
    # Replace one marker pair, preserving the surrounding indentation.
    pattern = re.compile(
        rf"(?m)^(?P<indent>[ \t]*)# {re.escape(name)}_START[ \t]*\r?\n"
        rf".*?"
        rf"^(?P=indent)# {re.escape(name)}_END[ \t]*$",
        re.DOTALL,
    )

    matches = list(pattern.finditer(template))
    if len(matches) != 1:
        raise ValueError(
            f"Templates must contain exactly one {name}_START/END marker pair, found {len(matches)}."
        )

    match = matches[0]
    indent = match.group("indent")

    if content:
        replacement = "\n".join(indent + line for line in content.splitlines())
    else:
        replacement = ""

    return template[: match.start()] + replacement + template[match.end() :]


def find_git_root(directory: Path) -> Path | None:
    result = subprocess.run(
        ["git", "-C", str(directory), "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        return None

    return Path(result.stdout.strip()).resolve()


def main() -> int:
    args = parse_args()
    repo_root = find_repo_root()
    templates_root = repo_root / "templates"
    modules_dir = (repo_root / "nix-modules").resolve()
    output_dir = args.output_dir.resolve()

    template_dir = (templates_root / args.use_template).resolve()

    if not template_dir.is_relative_to(templates_root.resolve()):
        raise ValueError(f"Invalid template path: {args.use_template!r}")

    template_file = template_dir / "flake.nix"
    if not template_file.is_file():
        raise FileNotFoundError(f"Template not found: {template_file}")

    selected = []
    seen = set()

    for requested in args.include_module:
        source = resolve_module_path(modules_dir, requested)

        if source in seen:
            continue

        seen.add(source)
        selected.append((source, load_metadata(source)))

    inputs = merge_inputs(selected)

    known_values = set(inputs) | {"pkgs", "self", "nixpkgs"}

    for source, metadata in selected:
        for arg_name, input_name in metadata.get("moduleArgs", {}).items():
            if input_name not in known_values:
                raise ValueError(
                    f"{source}: Module argument {arg_name!r} references unknown input {input_name!r}."
                )

    flake = template_file.read_text(encoding="utf-8")

    generated_blocks = {
        "INPUTS_BLOCK": generate_inputs_block(inputs),
        "ARGS_BLOCK": generate_args_block(inputs),
        "MODULES_BLOCK": generate_modules_block(selected, modules_dir),
    }

    for marker in MARKERS:
        flake = replace_marker(flake, marker, generated_blocks[marker])

    output_files = {output_dir / "flake.nix": flake}

    for source, _metadata in selected:
        relative = source.relative_to(modules_dir)
        output_files[output_dir / "nix-modules" / relative] = None

    collisions = [path for path in output_files if path.exists()]
    if collisions:
        raise FileExistsError(
            "Refusing to overwrite existing files:\n"
            + "\n".join(str(path) for path in collisions)
        )

    output_dir.mkdir(parents=True, exist_ok=True)

    for destination, content in output_files.items():
        destination.parent.mkdir(parents=True, exist_ok=True)

        if content is not None:
            destination.write_text(content, encoding="utf-8")
        else:
            source = next(
                source
                for source, _metadata in selected
                if destination
                == (output_dir / "nix-modules" / source.relative_to(modules_dir))
            )
            shutil.copy2(source, destination)

    git_root = find_git_root(output_dir)

    if git_root:
        relative_files = [
            str(path.resolve().relative_to(git_root).as_posix()) for path in output_files
        ]

        result = subprocess.run(
            ["git", "-C", str(git_root), "add", "-N", "--", *relative_files], check=False
        )

        if result.returncode != 0:
            print(
                "Warning: Files were created, but `git add -N` failed. You may need to add the files manually.",
                file=sys.stderr,
            )

    print(
        f"Successfully created {output_dir / 'flake.nix'} and copied {len(selected)} module(s) to {output_dir / 'nix-modules'}."
    )

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
