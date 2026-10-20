{ pkgs }:

let
  zsh = pkgs.writeShellScriptBin "zsh" ''
    export ZDOTDIR="$HOME/.nix/config/zsh"
    
    mkdir -p "$ZDOTDIR"

    if [ ! -f "$ZDOTDIR/.zshrc" ]; then
      cat > "$ZDOTDIR/.zshrc" << 'ZSHRC'
export ZSH="${pkgs.oh-my-zsh}/share/oh-my-zsh"

# Configure oh-my-zsh plugins and theme
ZSH_THEME="robbyrussell"

plugins=(
  git
  zsh-syntax-highlighting
  zsh-autosuggestions
)

source "$ZSH/oh-my-zsh.sh"
ZSHRC

    exec ${pkgs.zsh}/bin/zsh "$@"
    fi


    exec ${pkgs.zsh}/bin/zsh "$@"
  '';
in {
  packages = [
    zsh
  ] ++ (with pkgs; [
    oh-my-zsh
    zsh-syntax-highlighting
    zsh-autosuggestions
  ]
}