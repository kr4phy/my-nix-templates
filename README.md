# My Nix Templates

Reusable, simple Nix templates and snippets for quickly setting up dev environments.

## What is this project for

When you go outside and need to use other computer for coding or you need to set up your development environment quickly, you can do that with simply copy this template and run `nix develop`

## Structure

- `templates/`: Standalone dev environment templates
- `nix-modules/languages/`: pkg configs for programming languages and SDKs
- `nix-modules/build-tools/`: pkg configs for build tools and dev utils
- `nix-modules/shells/`: Shell pkgs and related configs

## Usage

### 1. Clone this repository
```
git clone https://github.com/kr4phy/my-nix-templates.git
```

### 2. Copy templates and modules you need
```
cp -r /path/to/cloned/repo/nix-modules /path/to/your/project/
cp /path/to/wanted/template/flake.nix /path/to/your/project/
```
Remove modules that you don't need.

### 3. Correct import paths
You need to fix import paths in template's modules list. In most templates, you need to replace `../../` in import path to `./` or something.

### 4. Activate nix flake
Run `nix develop` to activate flake.nix.