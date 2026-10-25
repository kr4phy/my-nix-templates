/*
METADATA_BLOCK_START
{
  "author": "kr4phy",
  "description": "Nix module for .NET development packages",
  "inputs": {},
  "moduleArgs": {}
}
METADATA_BLOCK_END
*/
{ pkgs }:

let
in {
  packages = with pkgs; [
    dotnet-sdk_10
  ];
}