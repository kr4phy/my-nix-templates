{ pkgs }:

with pkgs; [
  python314
  python314Packages.pydevd
  uv
  pyright

  #editor for python
  jetbrains.pycharm
  #uncomment this to use vscode instead
  #vscode
  #vscode-fhs
]
