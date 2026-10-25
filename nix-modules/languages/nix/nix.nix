{ pkgs }:

let
in {
  packages = with pkgs; [
    # Assuming you have installed the Nix because this is a Nix flake.
    nixd
    # or use nil as nix lsp
    # nil
    nixfmt
  ];
}