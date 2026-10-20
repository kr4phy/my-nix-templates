{ pkgs }:

in {
    packages = [
        pkgs.fnm
    ];

    shellHook = ''
        fnm install
        fnm use

        echo "fnm and nodejs are ready to use."
    ''
}