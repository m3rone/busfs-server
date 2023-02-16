#!/bin/bash

if [ "$EUID" -eq 0 ]
  then echo "Please do not run this script as root."
  exit
fi

if command -v apt-get >/dev/null 2>&1; then
  PKG_MANAGER="apt-get"
elif command -v dnf >/dev/null 2>&1; then
  PKG_MANAGER="dnf"
elif command -v yum >/dev/null 2>&1; then
  PKG_MANAGER="yum"
elif command -v pacman >/dev/null 2>&1; then
  PKG_MANAGER="pacman"
elif command -v brew >/dev/null 2>&1; then
  PKG_MANAGER="brew"
else
  echo "Error: No supported package manager found."
  exit 1
fi

if [ "$PKG_MANAGER" = "pacman" ]; then
  sudo pacman -Sy python git || exit
else
  sudo $PKG_MANAGER install python3 git -y || exit
fi

git clone https://codeberg.org/m3r/busfs-server.git || exit

cd busfs-server || exit

python3 -m venv venv || exit

source venv/bin/activate || exit

python3 -m pip install -r requirements.txt || exit

echo "Setup complete!"
