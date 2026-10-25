# {
#     description = "";

#     inputs = {
#         nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
#     };

#     outputs = { self, nixpkgs }: {
#         let
#             system = "x86_64-linux";
#             pkgs = import nixpkgs {
#                 inherit system;
#             };
#         in {
#             devShells.${system} = pkgs.mkShell {
#                 packages = with pkgs; [
#                     git
#                 ];
#             };
#         };
#     };
# }
{
  description = "A minimal Nix flake template";
  
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };

      modules = [
        (import ../../nix-modules/utilities/dev-essentials.nix {
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
        '';
      };
    };
}