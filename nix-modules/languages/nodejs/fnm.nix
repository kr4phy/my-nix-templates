{ pkgs }:

in {
    packages = [
        pkgs.fnm
        pkgs.pnpm

        # editor for js/ts
        pkgs.vscode
        pkgs.vscode-fhs
        # Uncomment this to use JetBrains WebStorm
        # pkgs.webstorm
    ];

    shellHook = ''
        fnm install
        fnm use

        echo "fnm and nodejs are ready to use."
    ''
}