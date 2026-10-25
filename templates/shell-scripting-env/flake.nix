{
  description = "A flake for setting up a shell scripting environment";
  
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

    oh-my-bash = {
      url = "github:ohmybash/oh-my-bash";
      flake = false;
    };
  };

  outputs = { self, nixpkgs, oh-my-bash }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };

      modules = [
        (import ../../nix-modules/shells/oh-my-zsh.nix {
          inherit pkgs;
        })

        (import ../../nix-modules/shells/oh-my-bash.nix {
          inherit pkgs;
          templateSrc = oh-my-bash;
        })

        (import ../../nix-modules/shells/oh-my-posh.nix {
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
          echo "Shell scripting environment is ready."
          echo "Run \`omz\` to start the oh-my-zsh shell, \`omp\` to start the oh-my-posh shell, or \`omb\` to start the oh-my-bash shell."
        '';
      };
    };
}