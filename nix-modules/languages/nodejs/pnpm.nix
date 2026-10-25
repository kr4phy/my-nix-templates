{ pkgs }:

with pkgs; [
  nodejs
  corepack
  pnpm

  #editor for js/ts
  vscode
  vscode-fhs
  #Uncomment this to use JetBrains WebStorm
  # webstorm
]
