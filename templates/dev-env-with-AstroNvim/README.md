# Development Environment with AstroNvim

This template provides a development environment with AstroNvim (Neovim with AstroNvim configuration).

## Features

- Neovim with AstroNvim configuration
- LSP support
- Tree-sitter syntax highlighting
- Autocompletion
- Git integration

## Usage

```bash
python scripts/create-template.py \
  --use-template dev-env-with-astronvim \
  --output-dir my-project

cd my-project
nix develop
astronvim
```

## Commands

- `astronvim`: Launch Neovim with AstroNvim configuration
- `nvim`: Launch Neovim with AstroNvim configuration
