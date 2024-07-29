#!/bin/bash

echo "script started"

# PATH=$(pwd)

# Log file
LOG_FILE="$HOME/setup_log.txt"

# Anaconda version to install
ANACONDA_VERSION="2023.09-0"

# Packages to install
PACKAGES=(
    "build-essential"
    "libgl1-mesa-glx"
    "libegl1-mesa"
    "libxrandr2"
    "libxss1"
    "libxcursor1"
    "libxcomposite1"
    "libasound2"
    "libxi6"
    "libxtst6"
    "arduino"
    "freecad"
    "darktable"
    "rsync"
    "code"
    "opera-stable"
    "virt-manager"
    "git"
    "htop"
    "cantor"
    "labplot"
    "tree"
)

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

handle_error() {
    local error_message="$1"
    local is_critical="${2:-false}"

    log "Error: $error_message"

    if [ "$is_critical" = true ]; then
        log "Critical error. Exiting script."
        exit 1
    fi
}

install_packages() {
    log "Installing packages..."
    sudo apt-get update || handle_error "Failed to update package lists" false
    for package in "${PACKAGES[@]}"; do
        log "Installing $package..."
        sudo apt-get install -y "$package" || handle_error "Failed to install $package" false
    done

}

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

install_anaconda() {
    if command_exists conda; then
        log "Anaconda is already installed."
    else
        log "Installing Anaconda..."
        wget "https://repo.anaconda.com/archive/Anaconda3-${ANACONDA_VERSION}-Linux-x86_64.sh" -O anaconda.sh || handle_error "Failed to download Anaconda" false
        bash anaconda.sh -b -p "$HOME/anaconda3" || handle_error "Failed to install Anaconda" true
        rm anaconda.sh
        "$HOME/anaconda3/bin/conda" init || handle_error "Failed to initialize Conda" false
        log "Anaconda installation complete."

    fi
}

log "Starting setup for $DESKTOP_ENV environment..."
if command_exists conda; then
    log "Anaconda is already installed."
else
    install_anaconda
    exec bash "$(dirname "$0")/function_test.sh"
fi
install_packages



