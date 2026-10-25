{
  description = "A development environment with AstroNvim";
  
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

    astronvim-template = {
      url = "github:AstroNvim/template";
      flake = false;
    };
  };

  outputs = { self, nixpkgs, astronvim-template }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };

      modules = [
        (import ../../nix-modules/editors/astronvim.nix {
          inherit pkgs;
          templateSrc = astronvim-template;
        })
      ];

      modulePackages = builtins.concatLists (
        map (module: module.packages or []) modules
      );
      moduleShellHooks = map (module: module.shellHook or "") modules;

    in {
      devShells.${system}.default = pkgs.mkShell {
        packages = [
          # Add your own packages here
        ]
          ++ modulePackages;
        shellHook = ''
          ${builtins.concatStringsSep "\n" moduleShellHooks}
          # Add your own shell hook commands here
        '';
      };
    };
}