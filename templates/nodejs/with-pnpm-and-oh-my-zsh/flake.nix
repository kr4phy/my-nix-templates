{
  description = "A Node.js project template using pnpm and oh-my-zsh";
  
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };

      modules = [
        (import ../../nix-modules/shells/oh-my-zsh.nix {
          inherit pkgs;
        }),
        (import ../../nix-modules/nodejs/pnpm.nix {
          inherit pkgs;
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
          echo "Node.js project template with pnpm and oh-my-zsh is ready."
          echo "Run \`omz\` to start the oh-my-zsh shell."
        '';
      };
    };
}