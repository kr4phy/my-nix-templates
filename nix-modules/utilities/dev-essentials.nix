/*
METADATA_BLOCK_START
{
  "author": "kr4phy",
  "description": "Nix module for basic development packages",
  "inputs": {},
  "moduleArgs": {}
}
METADATA_BLOCK_END
*/
{ pkgs }:

let
in {
  packages = with pkgs; [
    git
    curl
    cacert
    ripgrep
    fd
    jq
    yq-go
    file
    unzip
    which
  ];
}