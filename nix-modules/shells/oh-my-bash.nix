{ pkgs, templateSrc }:

let
  omb = pkgs.writeShellScriptBin "omb" ''
    bashrc="''${BASHRC_PATH:-$PWD/.nix/config/bash/.bashrc}"

    export OSH="${templateSrc}"

    exec ${pkgs.bash}/bin/bash --rcfile "$bashrc" "$@"
  '';
in
{
  packages = [
    omb
  ] ++ (with pkgs; [
    bash
    git
    curl
  ]);

  shellHook = ''
    config_dir="''${BASHDOTDIR:-$PWD/.nix/config/bash}"
    bashrc="$config_dir/.bashrc"

    mkdir -p "$config_dir"

    if [ ! -f "$bashrc" ]; then
      printf '%s\n' \
        'OSH_THEME="font"' \
        'plugins=(git)' \
        'source "$OSH/oh-my-bash.sh"' \
        > "$bashrc"
    fi

    export OSH="${templateSrc}"
    export BASHRC_PATH="$bashrc"
  '';
}