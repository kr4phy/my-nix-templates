# 🤖 Automation Scripts

This directory contains Python scripts for managing Nix modules and templates automatically. These scripts help you create, validate, list, and organize your development environments efficiently.

---

## 📋 Available Scripts

| Script | Description | Command |
|--------|-------------|---------|
| `create_template.py` | Create a new project from a template with selected modules | `python create_template.py [options]` |
| `list_modules.py` | List all available modules with their metadata | `python list_modules.py [options]` |
| `validate_modules.py` | Validate module structure, syntax, and metadata | `python validate_modules.py [options]` |
| `new_module.py` | Create a new module skeleton with proper structure | `python new_module.py [options]` |

---

## 🎯 create_template.py

**Purpose:** Create a complete development environment project from a template with your selected modules.

### 📖 Usage

```bash
python create_template.py \
  --use-template <template_name> \
  --include-module <module_path> [--include-module <module_path> ...] \
  --output-dir <output_directory> \
  [--overwrite]
```

### ⚙️ Options

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--use-template`, `-t` | ✅ Yes | - | Name of the template to use (e.g., `default-template`, `dev-env-with-astronvim`) |
| `--include-module`, `-m` | ❌ No | - | Path to module(s) to include. Can be specified multiple times |
| `--output-dir`, `-o` | ✅ Yes | - | Output directory for the new project |
| `--overwrite`, `-f` | ❌ No | False | Overwrite existing files in output directory |

### 🎨 Examples

#### Example 1: Python Development Environment
```bash
python create_template.py \
  --use-template default-template \
  --include-module nix-modules/languages/python/python314.nix \
  --include-module nix-modules/utilities/dev-essentials.nix \
  --include-module nix-modules/shells/oh-my-zsh.nix \
  --output-dir my-python-app
```

#### Example 2: Node.js with AstroNvim
```bash
python create_template.py \
  --use-template dev-env-with-astronvim \
  --include-module nix-modules/languages/nodejs/pnpm.nix \
  --output-dir my-node-project
```

#### Example 3: Shell Scripting Environment
```bash
python create_template.py \
  --use-template shell-scripting-env \
  --output-dir my-scripts
```

#### Example 4: Custom Template with Multiple Modules
```bash
python create_template.py \
  --use-template default-template \
  --include-module nix-modules/languages/python/python314.nix \
  --include-module nix-modules/languages/nodejs/yarn.nix \
  --include-module nix-modules/utilities/cmake.nix \
  --include-module nix-modules/shells/oh-my-bash.nix \
  --output-dir my-multi-lang-project
```

### 📁 What Gets Created

When you run `create_template.py`, it creates:

```
my-project/
├── flake.nix              # Main flake file with your modules
├── flake.lock             # Lock file (auto-generated)
├── nix-modules/               # Copied modules
│   ├── python314.nix
│   ├── oh-my-zsh.nix
│   └── ...
└── README.md              # Existing project's README
```

### 💡 Tips

- Use **relative paths** for module paths: `nix-modules/languages/python/python314.nix`
- Check available templates with: `ls templates/`
- Check available modules with: `python list_modules.py`

---

## 📚 list_modules.py

**Purpose:** List all available modules with their metadata (name, description, category, tags, etc.).

### 📖 Usage

```bash
python list_modules.py [options]
```

### 🎨 Examples

#### List all modules
```bash
python list_modules.py
```

---

## 🔍 validate_modules.py

**Purpose:** Validate all modules for syntax errors, structure issues, and metadata completeness.

### 📖 Usage

```bash
python validate_modules.py
```

### 🎨 Examples

#### Validate all modules
```bash
python validate_modules.py
```


### ✅ What Gets Validated

1. **Syntax Validation**
   - Valid Nix syntax
   - Proper attribute structure
   - Correct package references

2. **Structure Validation**
   - Module exports `packages` or `shellHook`
   - Proper function parameters
   - Valid Nixpkgs references

3. **Metadata Validation** (if metadata block exists)
   - Required fields: `name`, `description`
   - Recommended fields: `version`, `author`, `category`, `tags`
   - Valid JSON format in metadata

4. **Best Practices**
   - Descriptive variable names
   - Proper indentation
   - Comment presence

---

## 🆕 new_module.py

**Purpose:** Create a new module skeleton with proper structure and metadata.

### 📖 Usage

```bash
python new_module.py [options]
```

### ⚙️ Options

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--name`, `-n` | ❌ No | - | Module name (used in filename and metadata) |
| `--category`, `-c` | ❌ No | - | Module category (languages, editors, shells, utilities) |
| `--description`, `-d` | ❌ No | - | Module description |
| `--author`, `-a` | ❌ No | - | Module author |
| `--tags`, `-t` | ❌ No | - | Comma-separated list of tags |
| `--packages`, `-p` | ❌ No | - | Comma-separated list of default packages |
| `--output`, `-o` | ❌ No | - | Output path (default: nix-modules/<category>/<name>.nix) |
| `--template`, `-T` | ❌ No | - | Use a specific template (basic, full, minimal) |
| `--help`, `-h` | ❌ No | - | Show help message |

### 🎨 Examples

#### Create a basic Python module
```bash
python new_module.py \
  --name python315 \
  --category languages \
  --description "Python 3.15 development environment" \
  --author "your-name" \
  --tags "python,pip,virtualenv" \
  --packages "python315,python315Packages.pip,python315Packages.virtualenv"
```

#### Create a module interactively
```bash
python new_module.py
# Follow the prompts to create your module
```

#### Create a module with custom path
```bash
python new_module.py \
  --name my-rust-module \
  --category languages \
  --output custom-modules/rust.nix
```

### 📁 Generated Module Structure

```nix
/* MODULE_METADATA_START
{
  "name": "module-name",
  "version": "1.0.0",
  "description": "Module description",
  "author": "your-name",
  "category": "category",
  "tags": ["tag1", "tag2"],
  "dependencies": [],
  "inputs": {
    "pkgs": "Nixpkgs package set (required)"
  },
  "outputs": {
    "packages": ["package1", "package2"],
    "shellHook": "Environment setup commands"
  },
  "usage": "import path/to/module.nix { inherit pkgs; }"
}
MODULE_METADATA_END
*/

{ pkgs, ... }:
{
  packages = with pkgs; [
    # Your packages here
    package1
    package2
  ];

  shellHook = ''
    # Your shell setup commands here
    echo "Module loaded: module-name"
  '';
}
```

---

## 💡 Scripts Workflow Examples

### Example 1: Complete Project Setup

```bash
# 1. Clone the repository
git clone https://github.com/kr4phy/my-nix-templates.git
cd my-nix-templates

# 2. List available modules
python scripts/list_modules.py

# 3. Create a new module (if needed)
python scripts/new_module.py --name custom-package --category utilities

# 4. Validate your new module
python scripts/validate_modules.py nix-modules/utilities/custom-package.nix

# 5. Create your project
python scripts/create_template.py \
  --use-template default-template \
  --include-module nix-modules/languages/python/python314.nix \
  --include-module nix-modules/utilities/custom-package.nix \
  --output-dir my-project

# 6. Enter development environment
cd my-project
nix develop
```

### Example 2: Module Development

```bash
# 1. Create a new module
python scripts/new_module.py --name golang --category languages

# 2. Edit the generated file
nano nix-modules/languages/golang.nix

# 3. Validate the module
python scripts/validate_modules.py --strict nix-modules/languages/golang.nix

# 4. Fix any issues
python scripts/validate_modules.py --fix nix-modules/languages/golang.nix

# 5. Test with a template
python scripts/create_template.py \
  --use-template default-template \
  --include-module nix-modules/languages/golang.nix \
  --output-dir test-golang

cd test-golang
nix develop
```

---

## 🛠️ Requirements

All scripts require:
- **Python 3.8 or higher**
- **Standard library modules** (no external dependencies)

The scripts are tested with:
- Python 3.8+
- Linux, macOS, Windows (WSL2)

---

## 🐛 Troubleshooting

### Scripts not found
**Issue:** `python: command not found` or `No module named scripts`

**Solution:**
- Make sure Python 3.8+ is installed
- Run from the repository root: `cd /path/to/my-nix-templates`
- Use explicit path: `python3 scripts/create_template.py`

### Module not found
**Issue:** `Module not found: nix-modules/languages/python/python314.nix`

**Solution:**
- Check the module path is correct
- Use relative paths from the repository root
- List available modules: `python scripts/list_modules.py`

### Permission denied
**Issue:** `Permission denied` when creating files

**Solution:**
- Make sure you have write permissions in the output directory
- Use `--overwrite` flag if the directory already exists

### Nix syntax errors
**Issue:** `error: syntax error` when running `nix develop`

**Solution:**
- Validate your modules: `python scripts/validate_modules.py`
- Check the error line number and fix the syntax
- Compare with existing working modules

---

## 📝 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-10-25 | Initial script documentation |

---

## 🤝 Contributing to Scripts

If you want to improve these scripts:

1. **Fork** the repository
2. **Create** a feature branch
3. **Test** your changes thoroughly
4. **Document** any new features or changes
5. **Submit** a Pull Request
