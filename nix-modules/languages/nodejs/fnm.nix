{ pkgs }:

let
in {
    packages = with pkgs; [
        fnm
        pnpm
    ];

    shellHook = ''
        fnm install
        fnm use

        echo "fnm and nodejs are ready to use."
    '';
}