/*
METADATA_BLOCK_START
{
  "author": "kr4phy",
  "description": "Nix module for Nix development packages",
  "inputs": {},
  "moduleArgs": {}
}
METADATA_BLOCK_END
*/
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