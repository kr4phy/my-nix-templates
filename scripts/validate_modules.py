#!/usr/bin/env python3
"""
Validate all Nix modules in the nix-modules directory and their metadata.
"""

import sys
from pathlib import Path

from lib.utils import (
    find_repo_root,
    load_metadata,
    merge_inputs,
    validate_module_arguments,
)


def validate_all_modules(repo_root: Path):
    # Validate all Nix modules in the nix-modules/ directory.
    modules_root = repo_root / "nix-modules"
    module_files = sorted(modules_root.rglob("*.nix"))

    if not module_files:
        print("No Nix modules found in nix-modules/ directory.")
        return 0

    valid_modules = []
    error_count = 0

    for path in module_files:
        relative = path.relative_to(repo_root).as_posix()

        try:
            metadata = load_metadata(path)
            valid_modules.append((path, metadata))
            print(f"OK {relative}")
        except (OSError, ValueError) as e:
            print(f"FAIL {relative}: {e}")
            error_count += 1

    if valid_modules:
        try:
            merged_inputs = merge_inputs(valid_modules)
        except ValueError as error:
            error_count += 1
            print("FAIL Cross-module input validation")
            print(f"  - {error}")
        else:
            try:
                validate_module_arguments(valid_modules, merged_inputs)
            except ValueError as error:
                error_count += 1
                print("FAIL Module argument validation")
                print(f"  - {error}")

    print()
    print(
        f"Checked {len(module_files)} modules: {len(valid_modules)} valid, {error_count} errors."
    )

    return error_count


def main() -> int:
    repo_root = find_repo_root()
    return 1 if validate_all_modules(repo_root) else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)
