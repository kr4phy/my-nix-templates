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

      astronvim = import ./snippets/editors/astronvim.nix {
        inherit pkgs;
        templateSrc = astronvim-template;
      };
    in {
      devShells.${system}.default = pkgs.mkShell {
        packages = astronvim.packages;
        shellHook = astronvim.shellHook;
      };
    }
}