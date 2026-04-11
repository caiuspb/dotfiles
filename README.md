# Dotfiles Setup Guide

This repository contains my personal configuration files (dotfiles), managed with **GNU Stow** and **Git**.

The goal is to quickly reproduce the same environment across multiple systems.

---

## 1. Clone the Repository

Clone the dotfiles into your home directory:

```bash
git clone git@github.com:caiuspb/dotfiles.git ~/dotfiles
cd ~/dotfiles
```

---

## 2. Apply the Configuration with Stow

From inside the repository, run:

```bash
stow .
```

This will create symbolic links from the repository into your home directory (e.g. `~/.config/...`).

---

## 3. Handling Existing Files

If configuration files already exist on the system, `stow` will refuse to overwrite them.

### Option A (recommended): Backup existing files

```bash
mkdir -p ~/.config_backup

mv ~/.config/fish ~/.config_backup/ 2>/dev/null
mv ~/.config/starship.toml ~/.config_backup/ 2>/dev/null
```

Then run:

```bash
stow .
```

---

### Option B: Adopt existing files into the repo

```bash
stow --adopt .
```

This moves existing files into the repository and replaces them with symlinks.

---

## 4. Verify Setup

Check that symlinks were created correctly:

```bash
ls -l ~/.config/fish
ls -l ~/.config/starship.toml
```

You should see links pointing to `~/dotfiles/...`.

---

## 5. Post-Setup Notes

* Restart your shell:

  ```bash
  exec fish
  ```

* Ensure required tools are available (e.g. `fish`, `starship`, `zoxide`, etc.)

* If using `fish`, plugins can be installed with:

  ```fish
  fisher update
  ```

---

## 6. Updating Dotfiles

To update your configuration on any system:

```bash
cd ~/dotfiles
git pull
stow .
```

---

## 7. Structure

Example layout:

```text
dotfiles/
└── .config/
    ├── fish/
    │   ├── config.fish
    │   └── fish_plugins
    └── starship.toml
```

---

## 8. Notes

* Only configuration files are tracked — no binaries or installed software.
* All changes should be made inside `~/dotfiles`, not directly in `~/.config`.
* Symlinks ensure all systems stay in sync.

---
