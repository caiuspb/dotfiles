#!/usr/bin/env bash

set -euo pipefail

repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
fisher_script="$(mktemp)"

cleanup() {
    rm -f -- "$fisher_script"
}
trap cleanup EXIT

require_sudo() {
    if ! command -v sudo >/dev/null 2>&1; then
        printf 'Error: sudo is required to install system packages.\n' >&2
        exit 1
    fi
}

install_dependencies() {
    if command -v apt-get >/dev/null 2>&1; then
        require_sudo
        sudo apt-get update
        sudo apt-get install --yes git stow fish zoxide curl openssh-client
        curl -sS https://starship.rs/install.sh | sh -s -- --yes
    elif command -v pacman >/dev/null 2>&1; then
        require_sudo
        sudo pacman --sync --needed --noconfirm git stow fish starship zoxide curl openssh
    elif command -v dnf >/dev/null 2>&1; then
        require_sudo
        sudo dnf install --assumeyes git stow fish starship zoxide curl openssh-clients
    else
        printf 'Error: unsupported package manager. Install the prerequisites from README.md, then rerun this script.\n' >&2
        exit 1
    fi
}

install_dependencies

cd -- "$repo_dir"
stow --restow --target="$HOME" .

curl --fail --silent --show-error --location \
    https://raw.githubusercontent.com/jorgebucaran/fisher/main/functions/fisher.fish \
    --output "$fisher_script"
fish --no-config -c "source '$fisher_script'; fisher update"

printf '\nDotfiles installed successfully. To make Fish your login shell, run:\n'
printf '  chsh -s "$(command -v fish)"\n'
