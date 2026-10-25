# My Nix Templates

Reusable Nix templates and modules for setting up development environments.

## Purpose

This project provides Nix flake templates and reusable modules to quickly create development environments. Each template uses a combination of modules to provide a complete setup.

## Structure

- `templates/`: Ready-to-use development environment templates
- `nix-modules/`: Reusable modules organized by category
  - `editors/`: Editor configurations
  - `languages/`: Language-specific packages and tools
  - `shells/`: Shell configurations
  - `utilities/`: Utility packages and build tools
- `scripts/`: Python scripts for managing templates and modules

## Usage

### Method A: Using the create_template.py script

```bash
python scripts/create_template.py \
  --use-template default-template \
  --include-module nix-modules/languages/python/python314.nix \
  --include-module nix-modules/shells/oh-my-zsh.nix \
  --output-dir my-project

cd my-project
nix develop
```

### Method B: Manual setup

```bash
git clone https://github.com/kr4phy/my-nix-templates.git

# Copy a template
cp -r my-nix-templates/templates/default-template my-project

# Copy modules as needed
cp my-nix-templates/nix-modules/languages/python/python314.nix my-project/

# Edit flake.nix to import the modules
cd my-project
nix develop
```

## Available Templates

- `default-template`: Minimal template for custom configurations
- `dev-env-with-astronvim`: Development environment with AstroNvim editor
- `shell-scripting-env`: Shell scripting environment with oh-my-zsh, oh-my-posh, oh-my-bash
- `dev-essentials`: General development environment with essential tools
- `cl-dev`: Common Lisp development environment

## Available Modules

### Editors
- `editors/astronvim.nix`: Neovim with AstroNvim configuration

### Languages
- `languages/python/python314.nix`: Python 3.14 with pip, pydevd, pyright
- `languages/nodejs/fnm.nix`: Node.js version manager
- `languages/nodejs/pnpm.nix`: Node.js with pnpm
- `languages/nodejs/yarn.nix`: Node.js with Yarn
- `languages/nix/nix.nix`: Nix development tools
- `languages/lisp/common-lisp.nix`: Common Lisp with clisp and quicklisp
- `languages/lisp/scheme.nix`: Scheme with racket and guile
- `languages/dotnet/dotnetdevpkgs.nix`: .NET SDK and runtime

### Shells
- `shells/oh-my-zsh.nix`: Zsh with oh-my-zsh, syntax highlighting, auto-suggestions
- `shells/oh-my-posh.nix`: PowerShell with oh-my-posh
- `shells/oh-my-bash.nix`: Bash with oh-my-bash

### Utilities
- `utilities/dev-essentials.nix`: git, curl, wget, htop, tmux, neovim, ripgrep
- `utilities/cmake.nix`: cmake, ninja, pkg-config

## Scripts

The `scripts/` directory contains tools for managing the project:

- `create-template.py`: Create a new project from a template with modules
- `list_modules.py`: List all available modules
- `validate_modules.py`: Validate module structure
- `new_module.py`: Create a new module skeleton

## Requirements

- Nix 2.4 or later
- Git
- Python 3.8+ (for scripts)

## Platform Support

- Linux (x86_64): Supported
- macOS (aarch64): Not tested, but likely supported
- Windows (WSL2): Supported
- Windows (Native): Not supported (due to lack of Nix support)

## License

MIT License. See LICENSE for details.
