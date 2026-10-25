{ pkgs }:

let
  omp = pkgs.writeShellScriptBin "omp" ''
    profile="''${PWSH_PROFILE_PATH:-$PWD/.nix/config/powershell/Microsoft.PowerShell_profile.ps1}"

    exec ${pkgs.powershell}/bin/pwsh -NoLogo -NoExit -Command ". '$profile'"
  '';

in {
  packages = [
    omp
  ] ++ (with pkgs; [
    powershell
    oh-my-posh
  ]);

  shellHook = ''
    config_dir="''${PWSH_PROFILE:-$PWD/.nix/config/powershell}"
    profile="$config_dir/Microsoft.PowerShell_profile.ps1"

    mkdir -p "$config_dir"

    if [ ! -f "$profile" ]; then
      printf '%s\n' \
        'oh-my-posh init pwsh --config "${pkgs.oh-my-posh}/share/oh-my-posh/themes/if_tea.omp.json" | Invoke-Expression' \
        > "$profile"
    fi

    export PWSH_PROFILE_PATH="$profile"
  '';
}