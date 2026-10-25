# Default Template

This is the base template for creating Nix development environments. Use this template as a starting point and add modules as needed.

## Usage

Copy this template and add modules from `nix-modules/` to the `modules` list in `flake.nix`.

## Customization

### Option A: Use the `create_template.py` script to create a new project with this template and include modules.

### Option B: Manually copy this template and add modules to the `flake.nix` file.
1. Copy modules to your project directory
2. Import them in flake.nix:
   ```nix
   modules = [
     (import ./modules/python314.nix { inherit pkgs; })
     (import ./modules/oh-my-zsh.nix { inherit pkgs; })
   ];
   ```
3. Run `nix develop`
