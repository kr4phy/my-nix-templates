{
  description = "A Node.js project template using pnpm";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  }

  outputs = { self, nixpkgs }: {
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs {
        inherit system;
      };

    zsh-shell-nix = import ../../snippets/shells/oh-my-zsh.nix {
      inherit pkgs;
    };
    pnpm-nix = import ../../snippets/nodejs/pnpm.nix {
      inherit pkgs;
    };

    in {
      devShells.${system}.default = pkgs.mkShell {
        packages = [
          pnpm-nix.packages;
          zsh-shell-nix.packages
        ];
      };
    };
  };
}