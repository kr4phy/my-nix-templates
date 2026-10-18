# My Nix Templates
Reusable, simple Nix templates and snippets for quickly setting up dev environments.

## Structure
- `templates/`: Standalone dev environment templates
- `snippets/languages/`: pkg configs for programming languages and SDKs
- `snippets/build-tools/`: pkg configs for build tools and dev utils
- `snippets/shells/`: Shell pkgs and related configs

## Usage
Copy templates or snippets you need into your project and modify things like import path to make it fit for your environment.
The snippets currently expose package lists as Nix functions accepting pkgs.