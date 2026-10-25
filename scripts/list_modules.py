#!/usr/bin/env python3
"""
List all Nix modules in the nix-modules directory and display their metadata.
"""

import sys

from lib.utils import (
    find_repo_root,
    load_metadata,
)


def main() -> int:
    repo_root = find_repo_root()
    modules_dir = repo_root / "nix-modules"
    module_files = sorted(modules_dir.rglob("*.nix"))

    if not module_files:
        print("No Nix modules found in the 'nix-modules' directory.", file=sys.stderr)
        return 1

    error_count = 0

    for path in module_files:
        relative = path.relative_to(modules_dir).as_posix()

        try:
            metadata = load_metadata(path)
        except (OSError, ValueError) as e:
            print(f"FAIL {relative}: {e}", file=sys.stderr)
            error_count += 1
            continue

        inputs = metadata.get("inputs", {})
        module_args = metadata.get("moduleArgs", {})

        print(f"Module: {relative}")
        if inputs:
            print("\tInputs:")
            for name, config in inputs.items():
                print(f"\t\t{name}: {config.get('url', 'N/A')}")
        else:
            print("\tInputs: None")

        if module_args:
            print("\tModule Arguments:")
            for arg_name, input_name in module_args.items():
                print(f"\t\t{arg_name} <- {input_name}")
        else:
            print("\tModule Arguments: None")

        print()

    print(f"Found {len(module_files)} module(s) with {error_count} error(s).")

    return 0 if error_count == 0 else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)
