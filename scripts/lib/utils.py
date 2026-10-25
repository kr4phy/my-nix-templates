import json
import re
from pathlib import Path


def find_repo_root() -> Path:
    # Find the template repo root.
    script_dir = Path(__file__).resolve().parent

    for directory in (script_dir, *script_dir.parents):
        if (directory / "templates").is_dir() and (directory / "nix-modules").is_dir():
            return directory

    raise RuntimeError("Could not find the template repo root.")


IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_'-]*$")


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
        raise TypeError(f"{module_path}: Metadata block must be a JSON object.")

    inputs = metadata.get("inputs", {})
    module_args = metadata.get("moduleArgs", {})

    if not isinstance(inputs, dict):
        raise TypeError(
            f"{module_path}: 'inputs' in metadata block must be a JSON object."
        )

    if not isinstance(module_args, dict):
        raise TypeError(
            f"{module_path}: 'moduleArgs' in metadata block must be a JSON object."
        )

    for input_name, config in inputs.items():
        if not isinstance(input_name, str):
            raise TypeError(f"{module_path}: Invalid Nix input name: {input_name!r}")

        if input_name in {"self", "nixpkgs"}:
            raise ValueError(
                f"{module_path}: '{input_name}' is already provided by the template."
            )

        if not isinstance(config, dict):
            raise TypeError(
                f"{module_path}: Input '{input_name}' configuration must be a JSON object."
            )

        if not isinstance(config.get("url"), str):
            raise TypeError(
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


def validate_module_arguments(selected, inputs):
    known_values = set(inputs) | {"pkgs", "self", "nixpkgs"}

    for source, metadata in selected:
        for arg_name, input_name in metadata.get("moduleArgs", {}).items():
            if input_name not in known_values:
                raise ValueError(
                    f"{source}: Module argument {arg_name!r} references unknown input {input_name!r}."
                )
