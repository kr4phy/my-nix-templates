/*
METADATA_BLOCK_START
{
  "author": "kr4phy",
  "description": "Nix module for Python 3.14 development packages",
  "inputs": {},
  "moduleArgs": {}
}
METADATA_BLOCK_END
*/
{ pkgs }:

let
in {
  packages = with pkgs; [
    python314
    python314Packages.pydevd
    uv
    pyright
  ];
}
