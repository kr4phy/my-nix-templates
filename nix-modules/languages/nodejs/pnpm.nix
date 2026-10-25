{ pkgs }:


in {
  packages = with pkgs; [
    nodejs
    corepack
    pnpm
  ];
}