/*
METADATA_BLOCK_START
{
  "author": "kr4phy",
  "description": "Nix module for Oh My Bash shell",
  "inputs": {
    "oh-my-bash": {
      "url": "github:ohmybash/oh-my-bash",
      "flake": false
    }
  },
  "moduleArgs": {
    "templateSrc": "oh-my-bash"
  }
}
METADATA_BLOCK_END
*/
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