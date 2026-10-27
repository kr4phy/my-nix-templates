# Development Environment with AstroNvim

This flake imports `nix-modules/editors/astronvim.nix` and the AstroNvim template input. Use it from this repository so its relative module path resolves.

```sh
cd templates/dev-env-with-AstroNvim
nix develop
astronvim
```

On shell entry, the AstroNvim template is copied into `.nix/astronvim/xdg-config/astronvim` if that directory does not already contain `init.lua`. The `astronvim` command sets project-local XDG config, data, state, and cache directories under `.nix/astronvim`, then launches Neovim.

The template directory name is exactly `dev-env-with-AstroNvim`. `scripts/create_template.py` cannot currently generate this preset: its flake does not contain the marker pairs required by that script. The generator path and supported options are documented in [`default-template`](../default-template/README.md).
