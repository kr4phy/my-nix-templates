/*
METADATA_BLOCK_START
{
  "author": "kr4phy",
  "description": "Nix module for build utilities",
  "inputs": {},
  "moduleArgs": {}
}
METADATA_BLOCK_END
*/
{ pkgs }:

let
in {
  packages = with pkgs; [
    cmake
    ninja
    pkg-config
  ];
}