/*
METADATA_BLOCK_START
{
  "author": "kr4phy",
  "description": "Nix module for Common Lisp development packages",
  "inputs": {},
  "moduleArgs": {}
}
METADATA_BLOCK_END
*/
{ pkgs }:

let
in {
  packages = with pkgs; [
    # Common Lisp Implementations
    sbcl
    sbclPackages.coalton
    # clisp
    # ccl
    # ecl

    rlwrap

    # Utilities
    asdf
    # quicklisp
    # roswell
  ];
}