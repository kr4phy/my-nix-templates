# My Nix Templates
Reusable, simple Nix templates and snippets for quickly setting up dev environments.

## Structure
- `templates/`: Standalone dev environment templates
- `nix-modules/languages/`: pkg configs for programming languages and SDKs
- `nix-modules/build-tools/`: pkg configs for build tools and dev utils
- `nix-modules/shells/`: Shell pkgs and related configs

## Usage
Copy templates or import nix modules you need into your project and modify things like import path to make it fit for your environment.