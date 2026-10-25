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
