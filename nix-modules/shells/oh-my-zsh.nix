{ pkgs }:

let
  omz = pkgs.writeShellScriptBin "omz" ''
    zsh_config_dir="''${ZDOTDIR:-$PWD/.nix/config/zsh}"
    zshrc="$zsh_config_dir/.zshrc"

    mkdir -p "$zsh_config_dir"

    if [ ! -f "$zshrc" ]; then
      printf '%s\n' \
        'export ZSH="${pkgs.oh-my-zsh}/share/oh-my-zsh"' \
        'ZSH_THEME="cypher"' \
        'plugins=(git)' \
        'source "$ZSH/oh-my-zsh.sh"' \
        'source "${pkgs.zsh-syntax-highlighting}/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh"' \
        'source "${pkgs.zsh-autosuggestions}/share/zsh-autosuggestions/zsh-autosuggestions.zsh"' \
        > "$zshrc"
    fi

  export ZDOTDIR="$zsh_config_dir"
    exec ${pkgs.zsh}/bin/zsh "$@"
  '';
in {
  packages = [
    omz
  ] ++ (with pkgs; [
    oh-my-zsh
    zsh-syntax-highlighting
    zsh-autosuggestions
  ]);
}