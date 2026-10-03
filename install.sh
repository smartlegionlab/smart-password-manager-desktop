#!/bin/bash
# Smart Password Manager Desktop — Installer
# Usage:
#   Local:  ./install.sh
#   Remote: curl -fsSL https://raw.githubusercontent.com/smartlegionlab/smart-password-manager-desktop/master/install.sh | bash

set -e

# --- Config ---
REPO_URL="https://github.com/smartlegionlab/smart-password-manager-desktop.git"
APP_NAME="Smart Password Manager"
APP_ID="smart-password-manager"
INSTALL_DIR="$HOME/.local/share/$APP_ID"
VENV_DIR="$INSTALL_DIR/venv"
APPS_DIR="$HOME/.local/share/applications"
MENU_ENTRY="$APPS_DIR/$APP_ID.desktop"
DESKTOP_FILE="$APP_ID.desktop"
USER_DATA_DIR="$HOME/.config/smart_password_manager"
USER_DATA_FILE="$USER_DATA_DIR/passwords.json"

# --- Colors ---
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

info()  { echo -e "${GREEN}==>${NC} $*"; }
warn()  { echo -e "${YELLOW}==>${NC} $*"; }
error() { echo -e "${RED}==>${NC} $*" >&2; }
step()  { echo -e "${BOLD}${BLUE}[*]${NC} $*"; }

banner() {
    echo ""
    echo -e "${BOLD}${GREEN}==============================================${NC}"
    echo -e "${BOLD}${GREEN}  Smart Password Manager Desktop — Installer${NC}"
    echo -e "${BOLD}${GREEN}==============================================${NC}"
    echo ""
}

# --- Header ---
banner

echo "This installer will:"
echo "  1. Download the application source code"
echo "  2. Install it to:  $INSTALL_DIR"
echo "  3. Create a Python virtual environment and install dependencies"
echo "  4. Register the app in your application menu"
echo "  5. Optionally create a shortcut on your Desktop"
echo ""
echo -e "Your data will be stored separately in:"
echo -e "  ${BOLD}$USER_DATA_FILE${NC}"
echo "  (that folder is created by the app on first run)"
echo ""
read -r -p "Continue? [Y/n]: " CONFIRM
case "$CONFIRM" in
    [nN]*) echo "Aborted."; exit 0 ;;
esac
echo ""

# --- Detect source mode ---
step "Detecting source..."
if [ -n "${BASH_SOURCE[0]:-}" ] && [ -f "${BASH_SOURCE[0]}" ]; then
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    if [ -f "$SCRIPT_DIR/app.py" ]; then
        SOURCE_DIR="$SCRIPT_DIR"
        info "Source: local folder — $SOURCE_DIR"
    fi
fi

if [ -z "${SOURCE_DIR:-}" ]; then
    if ! command -v git >/dev/null 2>&1; then
        error "git is required but not installed."
        error "Install it first: sudo apt install git"
        exit 1
    fi
    TMP_CLONE="$(mktemp -d)"
    info "Source: remote repository"
    info "From:   $REPO_URL"
    info "Into:   $TMP_CLONE"
    git clone --depth 1 "$REPO_URL" "$TMP_CLONE" >/dev/null 2>&1
    SOURCE_DIR="$TMP_CLONE"
fi

# --- Python check ---
step "Checking Python..."
if ! command -v python3 >/dev/null 2>&1; then
    error "python3 is required but not installed."
    error "Install it first: sudo apt install python3 python3-venv"
    exit 1
fi
PY_VER="$(python3 --version 2>&1)"
info "Found: $PY_VER"

# --- Install directory ---
step "Preparing install directory..."
if [ -d "$INSTALL_DIR" ]; then
    warn "Existing install found at $INSTALL_DIR — removing it first."
    rm -rf "$INSTALL_DIR"
fi
mkdir -p "$INSTALL_DIR"
info "Install directory: $INSTALL_DIR"

# --- Copy files ---
step "Copying application files..."
if command -v rsync >/dev/null 2>&1; then
    rsync -a --exclude='.git' --exclude='venv' --exclude='__pycache__' \
          "$SOURCE_DIR"/ "$INSTALL_DIR"/
else
    cp -r "$SOURCE_DIR"/. "$INSTALL_DIR"/
    rm -rf "$INSTALL_DIR/.git" "$INSTALL_DIR/venv"
fi
info "Files copied to: $INSTALL_DIR"

if [ -n "${TMP_CLONE:-}" ]; then
    rm -rf "$TMP_CLONE"
    info "Temporary clone removed: $TMP_CLONE"
fi

# --- Virtual environment ---
step "Creating virtual environment..."
info "Location: $VENV_DIR"
python3 -m venv "$VENV_DIR"

step "Installing dependencies..."
info "From: $INSTALL_DIR/requirements.txt"
info "Into: $VENV_DIR"
"$VENV_DIR/bin/pip" install --upgrade pip >/dev/null
"$VENV_DIR/bin/pip" install -r "$INSTALL_DIR/requirements.txt" >/dev/null
info "Dependencies installed."

# --- Icon ---
ICON_PATH="$INSTALL_DIR/data/icons/icon.png"
[ -f "$ICON_PATH" ] || ICON_PATH="system-run"

# --- Desktop entry content ---
DESKTOP_CONTENT="[Desktop Entry]
Version=1.0
Type=Application
Name=$APP_NAME
Comment=Secure deterministic Smart Password Manager
Exec=$VENV_DIR/bin/python $INSTALL_DIR/app.py
Icon=$ICON_PATH
Terminal=false
Categories=Utility;Security;
StartupNotify=true
Keywords=password;manager;security;deterministic;
"

# --- Install to Application Menu ---
step "Registering application in the menu..."
mkdir -p "$APPS_DIR"
echo "$DESKTOP_CONTENT" > "$MENU_ENTRY"
chmod +x "$MENU_ENTRY"
info "Menu entry created: $MENU_ENTRY"
info "  → Look for \"$APP_NAME\" in your application menu."

# --- Desktop shortcut (optional) ---
step "Desktop shortcut (optional)"
echo ""
warn "Notes about the Desktop shortcut:"
echo "  - On GNOME (default on Ubuntu), desktop icons may be hidden by default."
echo "  - The shortcut may show an 'Unsecured Application Launcher' warning."
echo "  - If it does: right-click → 'Allow Launching' (one-time action)."
echo ""
read -r -p "Create Desktop shortcut? [y/N]: " REPLY
echo ""
if [[ "$REPLY" =~ ^[Yy]$ ]]; then
    DESKTOP_DIR="$(xdg-user-dir DESKTOP 2>/dev/null || true)"
    [ -z "$DESKTOP_DIR" ] && DESKTOP_DIR="$HOME/Desktop"
    mkdir -p "$DESKTOP_DIR"
    echo "$DESKTOP_CONTENT" > "$DESKTOP_DIR/$DESKTOP_FILE"
    chmod +x "$DESKTOP_DIR/$DESKTOP_FILE"
    info "Desktop shortcut created: $DESKTOP_DIR/$DESKTOP_FILE"
else
    info "Skipped Desktop shortcut."
fi

# --- Update desktop database ---
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$APPS_DIR" >/dev/null 2>&1 || true
fi

# --- Summary ---
echo ""
echo -e "${BOLD}${GREEN}==============================================${NC}"
echo -e "${BOLD}${GREEN}  Installation complete${NC}"
echo -e "${BOLD}${GREEN}==============================================${NC}"
echo ""
echo -e "${BOLD}What was installed:${NC}"
echo "  Application:      $INSTALL_DIR"
echo "  Virtual env:      $VENV_DIR"
echo "  Menu entry:       $MENU_ENTRY"
echo "  Your data folder: $USER_DATA_DIR"
echo "                    (created by the app on first run, holds passwords.json)"
echo ""
echo -e "${BOLD}How to launch:${NC}"
echo "  • Application menu → \"$APP_NAME\""
echo "  • Desktop shortcut (if you created one)"
echo ""
echo -e "${BOLD}How to uninstall:${NC}"
echo "  curl -fsSL https://raw.githubusercontent.com/smartlegionlab/smart-password-manager-desktop/master/uninstall.sh | bash"
echo ""
echo -e "${YELLOW}Note:${NC} If the menu entry does not appear immediately, log out and back in."
echo -e "${YELLOW}Note:${NC} Your passwords metadata is NEVER touched by this installer."
echo ""