{
  description = "A flake for this project";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
  let
    system = "x86_64-linux";
    pkgs = import nixpkgs {
      inherit system;
    };

    nix-config = import ../../snippets/languages/nix/nix.nix {
      inherit pkgs;
    };

  in {
    devShells.${system}.default = pkgs.mkshell {
      packages = nix-config.packages;
    };
  };
}