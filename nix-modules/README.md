# nix-modules/

This directory contains reusable Nix modules organized by category. Each module provides packages and shell configuration for specific functionality.

## Structure

- `editors/`: Editor and IDE configurations
- `languages/`: Language-specific packages and development tools
- `shells/`: Shell configurations with frameworks
- `utilities/`: Utility packages and build tools

## Module Requirements

Each module must expose at least one of:
- `packages`: List of Nix packages to include in the development shell
- `shellHook`: Shell commands to run when the development shell is entered
