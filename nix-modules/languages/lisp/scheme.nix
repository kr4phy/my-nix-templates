/*
METADATA_BLOCK_START
{
  "author": "kr4phy",
  "description": "Nix module for Scheme development packages",
  "inputs": {},
  "moduleArgs": {}
}
METADATA_BLOCK_END
*/
{ pkgs }:

let
in {
  packages = with pkgs; [
    # Scheme implementations
    chez
    guile
    chicken
    # racket # Is this scheme..? I don't know, but it is from scheme.
  ];
}