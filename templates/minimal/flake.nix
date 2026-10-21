{
    description = "A minimal Nix flake template";

    inputs = {
        nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    }

    outputs = { self, nixpkgs }: {
        let
            system = "x86_64-linux";
            pkgs = import nixpkgs {
                inherit system;
            };
        in {
            devShells.${system} = pkgs.mkShell {
                packages = with pkgs; [
                    git
                ];
            };
        };
    };
}