#!/usr/bin/env python3
"""
Create a new Nix module with metadata.
"""

import argparse
import json
import sys
from pathlib import Path

from lib.utils import (
    IDENTIFIER_RE,
    find_repo_root,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a new Nix module with metadata."
    )
    parser.add_argument(
        "path",
        help="Path to the new module file relative to the 'nix-modules' directory, with or without the .nix extension.",
    )
    parser.add_argument(
        "--input",
        action="append",
        default=[],
        metavar="NAME=URL",
        help="Define an input for the new module. Can be used multiple times.",
    )
    parser.add_argument(
        "--author",
        default="",
        help="Author of the module. Defaults to an empty string.",
    )
    parser.add_argument(
        "--description",
        default="",
        help="Description of the module. Defaults to an empty string.",
    )
    return parser.parse_args()


def parse_inputs(values: list[str]) -> dict:
    inputs = {}

    for value in values:
        if "=" not in value:
            raise ValueError(f"Invalid input format: '{value}'. Expected 'NAME=URL'.")
        name, url = value.split("=", 1)
        name = name.strip()
        url = url.strip()

        if not IDENTIFIER_RE.fullmatch(name):
            raise ValueError(f"Invalid input name: '{name!r}'.")

        if name in {"self", "nixpkgs"}:
            raise ValueError(f"Input name '{name!r}' is reserved and cannot be used.")

        if not url:
            raise ValueError(f"Input URL for '{name!r}' cannot be empty.")

        if name in inputs:
            raise ValueError(f"Duplicate input name: '{name!r}'.")

        inputs[name] = {"url": url}

    return inputs


def build_module_source(args, inputs: dict) -> str:
    metadata = {
        "author": args.author,
        "description": args.description,
        "inputs": inputs,
        "moduleArgs": {},
    }

    metadata_json = json.dumps(metadata, indent=2, ensure_ascii=False)

    return f"""# METADATA_BLOCK_START
# {metadata_json.replace(chr(10), chr(10) + "# ")}
# METADATA_BLOCK_END

{{ pkgs }}:

let
  packages = [
    # Add packages here, for example:
    # pkgs.cmake
  ];
in
{{
  inherit packages;
}}
"""


def main() -> int:
    args = parse_args()
    modules_dir = (find_repo_root() / "nix-modules").resolve()

    requested = Path(args.path)

    if requested.is_absolute() or ".." in requested.parts:
        raise ValueError("Module path must stay inside the 'nix-modules' directory.")

    if requested.suffix == "":
        requested = requested.with_suffix(".nix")

    destination = (modules_dir / requested).resolve()

    if not destination.is_relative_to(modules_dir):
        raise ValueError("Module path must stay inside the 'nix-modules' directory.")

    if destination.exists():
        raise FileExistsError(f"Module file already exists: {destination}")

    inputs = parse_inputs(args.input)
    source = build_module_source(args, inputs)

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(source, encoding="utf-8")

    print(f"Created new module at: {destination}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
