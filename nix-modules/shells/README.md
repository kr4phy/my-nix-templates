# Shell modules

- `oh-my-bash.nix` takes `pkgs` and `templateSrc`. It provides `omb`, Bash, Git, and curl. Its shell hook creates a project-local `.bashrc` if absent and sets `BASHRC_PATH` and `OSH`.
- `oh-my-posh.nix` provides `omp`, PowerShell, and Oh My Posh. Its shell hook creates a project-local PowerShell profile if absent and sets `PWSH_PROFILE_PATH`.
- `oh-my-zsh.nix` provides `omz`, Oh My Zsh, zsh-syntax-highlighting, and zsh-autosuggestions. Running `omz` creates a project-local `.zshrc` if absent, sets `ZDOTDIR`, and starts Zsh.
