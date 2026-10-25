{ pkgs }:

let
in {
  packages = with pkgs; [
    git
    curl
    cacert
    ripgrep
    fd
    jq
    yq-go
    file
    unzip
    which
  ];
}