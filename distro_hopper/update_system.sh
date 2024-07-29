#!/bin/bash

# Update APT packages
sudo apt update && sudo apt upgrade -y

# Refresh snap packages
sudo snap refresh

# Check if Conda is installed and update
if command -v conda &> /dev/null; then
    echo "Updating Conda..."
    conda update conda --yes
    conda update --all --yes
fi

# Clean up
sudo apt autoremove -y
sudo apt autoclean

