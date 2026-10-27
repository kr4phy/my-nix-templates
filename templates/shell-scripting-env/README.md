# Shell scripting environment

Run this flake from the repository working copy; its imports use paths relative to this template directory.

```sh
cd templates/shell-scripting-env
nix develop
```

On shell entry, the Bash and PowerShell modules create their configuration files if those files do not exist:

- **Zsh:** Running `omz` creates `.nix/config/zsh/.zshrc` (or uses `ZDOTDIR`) with Oh My Zsh, the `cypher` theme, the `git` plugin, syntax highlighting, and autosuggestions. It then starts Zsh with that `ZDOTDIR`.
- **Bash:** The shell hook creates `.nix/config/bash/.bashrc` (or uses `BASHDOTDIR`) with the Oh My Bash `font` theme and `git` plugin. `omb` starts Bash with that file via `--rcfile`.
- **PowerShell:** The shell hook creates `.nix/config/powershell/Microsoft.PowerShell_profile.ps1` (or uses `PWSH_PROFILE`) with Oh My Posh's `if_tea` theme initialization. `omp` starts `pwsh` and loads that profile.

The default profile locations are relative to the current working directory. This flake does not contain the marker pairs required by `scripts/create_template.py`, so that generator cannot create this preset. See [`default-template`](../default-template/README.md) for the generator's usage.
