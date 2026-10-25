/*
METADATA_BLOCK_START
{
  "author": "kr4phy",
  "description": "Nix module for Node.js development packages",
  "inputs": {},
  "moduleArgs": {}
}
METADATA_BLOCK_END
*/
{ pkgs }:

let   
in {
  packages = with pkgs; [
    nodejs
    corepack
    pnpm
  ];
}