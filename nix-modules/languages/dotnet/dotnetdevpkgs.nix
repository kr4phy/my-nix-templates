{ pkgs }:

let
in {
  packages = with pkgs; [
    dotnet-sdk_10
  ];
}