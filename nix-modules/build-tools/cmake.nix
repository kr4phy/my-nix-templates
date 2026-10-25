{ pkgs }:

in {
  with pkgs; [
    cmake
    ninja
    pkg-config
  ];
}