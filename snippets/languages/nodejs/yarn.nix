{ pkgs }:

with pkgs; [
  nodejs
  corepack
  yarn

  #editor for js/ts
  vscode
  vscode-fhs
  #Uncomment this to use JetBrains WebStorm
  # webstorm
]