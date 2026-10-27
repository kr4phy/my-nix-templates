# Default Template

A minimal `x86_64-linux` Nix development shell. Add modules to the generated flake to include their packages and shell hooks.

## Create a project

From the repository root, run `scripts/create_template.py`. `--use-template` takes the directory name under `templates/`; `--include-module` takes a path relative to `nix-modules/` and can be repeated; `--output-dir` sets the destination (default: the current directory).

```sh
python3 scripts/create_template.py \
  --use-template default-template \
  --include-module languages/python/python314.nix \
  --output-dir ../my-project
cd ../my-project
nix develop
```

The script creates `flake.nix` and copies each selected module under `nix-modules/`. It refuses to overwrite existing output files. With no `--include-module`, the generated shell has no module packages or hooks.
