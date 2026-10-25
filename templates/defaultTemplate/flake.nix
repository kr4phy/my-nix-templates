{
  description = "A default template for this repo that can be used to create new flakes using modules from this repo";
  
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };

      modules = [
        # (import ../../nix-modules/path/to/module.nix {
        #   inherit pkgs;
        #   otherModuleInputs = ...;
        # })
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