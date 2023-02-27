#!/bin/bash

set -e

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
elif command -v zypper >/dev/null 2>&1; then
  PKG_MANAGER="zypper"
elif command -v apk >/dev/null 2>&1; then
  PKG_MANAGER="apk"
else
  echo "Error: No supported package manager found."
  exit 1
fi

case $PKG_MANAGER in
  "apt-get")
    sudo $PKG_MANAGER install python3 git -y
    ;;
  "dnf"|"yum"|"zypper")
    sudo $PKG_MANAGER install python3 git -y
    ;;
  "pacman")
    sudo pacman -Sy python git
    ;;
  "brew")
    brew install python git
    ;;
  "apk")
    sudo apk add python3 git
    ;;
esac

git clone https://codeberg.org/m3r/busfs-server.git

cd busfs-server

python3 -m venv venv

source venv/bin/activate

python3 -m pip install -r requirements.txt

echo "Setup complete!"
