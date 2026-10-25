{ pkgs }:

let
in {
  packages = with pkgs; [
    nodejs
    corepack
    pnpm
  ];
}