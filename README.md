Dotfiles Setup Guide

This repository contains my personal configuration files (dotfiles), managed with GNU Stow and Git.

The goal is to quickly reproduce the same environment across multiple systems.

1. Clone the Repository

Clone the dotfiles into your home directory:

git clone git@github.com:caiuspb/dotfiles.git ~/dotfiles
cd ~/dotfiles
2. Set Fish as Default Shell

After installing fish, set it as your default shell:

chsh -s $(which fish)

Log out and back in (or restart your session) for the change to take effect.

3. Apply the Configuration with Stow

From inside the repository, run:

stow .

This will create symbolic links from the repository into your home directory (e.g. ~/.config/...).

4. Handling Existing Files

If configuration files already exist on the system, stow will refuse to overwrite them.

Adopt existing files (recommended)
stow --adopt .

This will:

move existing config files into the repository
replace them with symlinks

Afterward, commit the adopted files:

git add .
git commit -m "adopt existing config"
5. Install Fisher (Fish Plugin Manager)

Start a fish shell:

fish

Then install fisher:

curl -sL https://git.io/fisher | source
6. Install Fish Plugins

Install all plugins defined in your dotfiles:

fisher update

This reads ~/.config/fish/fish_plugins and installs everything automatically.

7. Install and Enable Starship

Ensure starship is installed on the system.

Fish is configured to load it via:

starship init fish | source

The configuration file is located at:

~/.config/starship.toml

After installation, restart your shell:

exec fish
8. Install and Enable Zoxide

Ensure zoxide is installed on the system.

Fish is configured to initialize it via:

zoxide init fish | source

After installation, restart your shell:

exec fish

You can then use:

z <directory>
zi
9. Verify Setup

Check that symlinks were created correctly:

ls -l ~/.config/fish
ls -l ~/.config/starship.toml

You should see links pointing to ~/dotfiles/....

10. Updating Dotfiles

To update your configuration on any system:

cd ~/dotfiles
git pull
stow .
11. Structure

Example layout:

dotfiles/
└── .config/
    ├── fish/
    │   ├── config.fish
    │   └── fish_plugins
    └── starship.toml
12. Notes
Only configuration files are tracked — no binaries or installed software.
All changes should be made inside ~/dotfiles, not directly in ~/.config.
Symlinks ensure all systems stay in sync.
Fish plugins are managed via fisher and restored using fisher update.
Starship is configured via starship.toml.
Zoxide provides smart directory navigation (z, zi).