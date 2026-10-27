# my-nix-templates

Nix flake templates and reusable Nix modules for development shells. The flake files target `x86_64-linux`.

## Repository layout

- `templates/` contains flake examples.
- `nix-modules/` contains modules for editors, languages, shells, and utilities.
- `scripts/` contains Python tools for creating projects and handling module metadata.

## Generate a project

From the repository root, run:

```sh
python3 scripts/create_template.py \
  --use-template default-template \
  --include-module languages/python/python314.nix \
  --output-dir ../my-project

cd ../my-project
nix develop
```

`--include-module` paths are relative to `nix-modules/` and can be repeated. The generator writes `flake.nix` and copies selected modules under the output's `nix-modules/` directory. It refuses to overwrite existing output files. Without a module, the generated shell has no module packages or hooks.

## Templates

The repository contains `default-template`, `cl-dev`, `dev-essentials`, `dev-env-with-AstroNvim`, `shell-scripting-env`, and `nodejs/with-pnpm-and-oh-my-zsh`.

The Node.js template currently refers to `nix-modules/nodejs/pnpm.nix`, which is not present. The module is at `nix-modules/languages/nodejs/pnpm.nix`.

See [`nix-modules/README.md`](nix-modules/README.md) for module details and [`scripts/README.md`](scripts/README.md) for script usage. The repository is licensed under the [MIT License](LICENSE).
