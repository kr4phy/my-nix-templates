{ pkgs }:

in {
  with pkgs; [
    nodejs
    corepack
    yarn
  ];
}