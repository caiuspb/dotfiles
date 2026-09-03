# Dotfiles Setup Guide

This repository contains my personal configuration files, managed with GNU Stow and Git. It recreates the same shell environment across systems.

## Prerequisites

Install the following packages before applying the dotfiles:

- `git` to clone and update the repository
- `stow` to create symbolic links
- `fish` as the configured shell
- `starship` as the shell prompt
- `zoxide` for smart directory navigation
- `curl` to install Fisher
- an OpenSSH client because Fish starts `ssh-agent` when needed
- [OpenCode](https://opencode.ai) to use the included agents and skills

Fisher is installed after the configuration has been linked in step 5.

### Debian and Ubuntu

```bash
sudo apt update
sudo apt install git stow fish zoxide curl openssh-client
curl -sS https://starship.rs/install.sh | sh
```

### Arch Linux

```bash
sudo pacman -S git stow fish starship zoxide curl openssh
```

### Fedora

```bash
sudo dnf install git stow fish starship zoxide curl openssh-clients
```

Verify the installation:

```bash
git --version
stow --version
fish --version
starship --version
zoxide --version
```

## Installation

### 1. Clone the Repository

Clone the dotfiles into your home directory:

```bash
git clone git@github.com:caiuspb/dotfiles.git ~/dotfiles
cd ~/dotfiles
```

If SSH authentication for GitHub is not configured, use the HTTPS URL instead:

```bash
git clone https://github.com/caiuspb/dotfiles.git ~/dotfiles
cd ~/dotfiles
```

### 2. Apply the Configuration with Stow

From inside the repository, run:

```bash
stow .
```

This creates symbolic links from the repository into your home directory, for example under `~/.config`.

### 3. Handle Existing Files

If configuration files already exist, Stow refuses to overwrite them. Review and move them manually, or adopt them into this repository:

```bash
stow --adopt .
```

`--adopt` moves existing configuration files into the repository and replaces them with symbolic links. Review the resulting changes before committing them:

```bash
git diff
git add .
git commit -m "adopt existing config"
```

### 4. Set Fish as the Default Shell

Add Fish to the list of valid login shells if necessary, then make it the default:

```bash
command -v fish | sudo tee -a /etc/shells
chsh -s "$(command -v fish)"
```

Log out and back in, or restart the session, for this change to take effect.

### 5. Install Fisher and Fish Plugins

Start Fish and install Fisher:

```bash
fish
```

Then run:

```fish
curl -sL https://raw.githubusercontent.com/jorgebucaran/fisher/main/functions/fisher.fish | source
fisher update
```

`fisher update` reads `~/.config/fish/fish_plugins` and installs the listed plugins.

### 6. Restart Fish

Fish loads Starship from `~/.config/starship.toml` and initializes Zoxide automatically. Restart the shell after Stow and Fisher have run:

```fish
exec fish
```

You can now use Zoxide with:

```fish
z <directory>
zi
```

### 7. Configure OpenCode Secrets

Stow links the OpenCode configuration to `~/.config/opencode`. Agents are in
`agent/`, and reusable skills are in `skills/<name>/SKILL.md`.

Create a local secret file from the tracked template and fill in only the keys
you need:

```bash
cp ~/.config/opencode/.env.example ~/.config/opencode/.env
chmod 600 ~/.config/opencode/.env
```

`.env` files are intentionally ignored by Git and are not loaded by OpenCode
automatically. Export the required variables in the environment that starts
OpenCode. For example, in Fish:

```fish
set -gx ANTHROPIC_API_KEY your-api-key
opencode
```

The included `example-reviewer` agent is a read-only review subagent. Invoke
it with `@example-reviewer`. `example-skill` documents the required structure
for new skills; copy its directory and customize `SKILL.md`.

Quit and restart OpenCode after changing `opencode.json`, an agent, or a skill;
OpenCode reads these files only at startup.

## Verification

Check that the symbolic links were created correctly:

```bash
ls -l ~/.config/fish
ls -l ~/.config/starship.toml
ls -l ~/.config/opencode
```

They should point into `~/dotfiles`.

## Updating Dotfiles

Update the repository and reapply the links:

```bash
cd ~/dotfiles
git pull
stow .
```

## Notes

- Only configuration files are tracked; installed software is not.
- Make changes in `~/dotfiles`, not directly in `~/.config`.
- Fish plugins are managed with Fisher.
- Starship is configured in `~/.config/starship.toml`.
