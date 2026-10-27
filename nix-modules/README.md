# Nix modules

Each `.nix` file defines a function that returns an attribute set. Modules expose `packages`, may expose a `shellHook`, and may declare flake `inputs` and module arguments in a JSON metadata comment. The template generator uses that metadata to add inputs, pass arguments, and copy selected modules.

Categories in this directory:

- [`editors/`](editors/README.md)
- [`languages/`](languages/README.md)
- [`shells/`](shells/README.md)
- `utilities/`
