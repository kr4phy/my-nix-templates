{ pkgs, templateSrc }:

let
  astronvim = pkgs.writeShellScriptBin "astronvim" ''
    project_root="''${ASTRONVIM_PROJECT_ROOT:-$PWD}"
    config_root="$project_root/.nix/config"

    export NVIM_APPNAME="astronvim"
    export XDG_CONFIG_HOME="$config_root/xdg-config"
    export XDG_DATA_HOME="$config_root/xdg-data"
    export XDG_STATE_HOME="$config_root/xdg-state"
    export XDG_CACHE_HOME="$config_root/xdg-cache"

    exec ${pkgs.neovim}/bin/nvim "$@"
  '';
  
in
{
  packages = [
    astronvim
  ] ++ (with pkgs; [
    git

    # Essential dependencies
    neovim
    tree-sitter
    gcc

    # Optional dependencies
    ripgrep
    lazygit
    gdu
    bottom
    python3
    nodejs
  ]);

  shellHook = ''
    export ASTRONVIM_PROJECT_ROOT="$PWD"

    config_dir="$ASTRONVIM_PROJECT_ROOT/.nix/astronvim/xdg-config/astronvim"

    if [ ! -f "$config_dir/init.lua" ]; then
      mkdir -p "$config_dir"
      cp -R "${templateSrc}/." "$config_dir/"
      rm -r "$config_dir/.git"
    fi

    echo "AstroNvim is ready to use."
    echo "Run 'astronvim' to start editor."
  '';
}
