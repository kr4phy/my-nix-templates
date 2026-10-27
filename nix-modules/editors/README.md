# Editor module

- `astronvim.nix` provides an `astronvim` command that starts Neovim with project-local XDG config, data, state, and cache directories under `.nix/astronvim`. On shell entry, it copies the supplied AstroNvim template into that config directory if `init.lua` is absent. It also adds Git, Neovim, Tree-sitter, GCC, ripgrep, lazygit, gdu, bottom, Python, and Node.js to the shell.

  The module takes `pkgs` and `templateSrc` arguments. Its corresponding flake input is `astronvim-template`.
