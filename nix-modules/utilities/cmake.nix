{ pkgs }:

let
in {
  packages = with pkgs; [
    cmake
    ninja
    pkg-config
  ];
}