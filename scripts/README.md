# Scripts

Run the scripts with Python 3.9 or later from the repository root. They use only the Python standard library.

## `create_template.py`

Creates `flake.nix` from a template and copies selected modules under the output's `nix-modules/` directory. Module paths are relative to `nix-modules/`; paths may omit the `.nix` suffix. The script refuses to overwrite files.

```sh
python3 scripts/create_template.py \
  --use-template default-template \
  --include-module languages/python/python314.nix \
  --output-dir ../my-project
```

Options:

- `--use-template`: directory name under `templates/`; default `default-template`.
- `--include-module PATH`: module to add; repeat to select more than one.
- `--output-dir DIR`: destination directory; default is the current directory.

The selected template must contain one pair of marker comments for each block the generator fills. The checked-in `default-template` has these markers; the AstroNvim and shell-scripting templates do not.

## `list_modules.py`

Scans `nix-modules/` recursively for `.nix` files, reads each module's metadata block, and prints its path, flake inputs, and module arguments. It reports metadata errors and exits with a nonzero status if any are found.

```sh
python3 scripts/list_modules.py
```

## `validate_modules.py`

Reads metadata for all `.nix` modules, checks metadata structure, detects conflicting flake input definitions, and checks that declared module arguments refer to known inputs or `pkgs`, `self`, or `nixpkgs`. It does not parse or evaluate Nix code.

```sh
python3 scripts/validate_modules.py
```

## `new_module.py`

Creates a module file under `nix-modules/`. The positional path is relative to that directory, may omit `.nix`, and must not escape it. Existing files are not overwritten. The generated module has a metadata block and an empty `packages` list.

```sh
python3 scripts/new_module.py languages/rust/rust --author "Example" --description "Rust tools"
```

Options are `--input NAME=URL` (repeatable), `--author`, and `--description`. The path argument is required; the script has no interactive mode.
