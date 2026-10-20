{
  description = "A flake for setting up a oh-my-zsh shell environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };

      oh-my-zsh-setups = import ../../snippets/shells/oh-my-zsh.nix {
        inherit pkgs;
      };
    in {
      devShells.${system}.default = pkgs.mkShell {
        packages = oh-my-zsh-setups.packages;
        shellHook = oh-my-zsh-setups.shellHook;
      };
    };
}