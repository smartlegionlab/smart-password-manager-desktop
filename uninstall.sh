#!/bin/bash
# Smart Password Manager Desktop — Uninstaller
# Usage:
#   Local:  ./uninstall.sh
#   Remote: curl -fsSL https://raw.githubusercontent.com/smartlegionlab/smart-password-manager-desktop/master/uninstall.sh | bash

set -e

# --- Config ---
APP_NAME="Smart Password Manager"
APP_ID="smart-password-manager"
INSTALL_DIR="$HOME/.local/share/$APP_ID"
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
    echo -e "${BOLD}${RED}==============================================${NC}"
    echo -e "${BOLD}${RED}  Smart Password Manager Desktop — Uninstaller${NC}"
    echo -e "${BOLD}${RED}==============================================${NC}"
    echo ""
}

# --- Header ---
banner

echo "This uninstaller will remove:"
echo "  • Application files:   $INSTALL_DIR"
echo "  • Menu entry:          $MENU_ENTRY"
echo "  • Desktop shortcut:    ~/Desktop/$DESKTOP_FILE  (if exists)"
echo ""
echo -e "${BOLD}${GREEN}Your password metadata is NOT touched.${NC}"
echo "It stays safe in:"
echo "  $USER_DATA_FILE"
echo ""
echo "If you want to remove your data as well, do it manually after uninstall:"
echo "  rm -rf $USER_DATA_DIR"
echo ""
read -r -p "Continue with uninstall? [y/N]: " CONFIRM
case "$CONFIRM" in
    [yY]*) ;;
    *) echo "Aborted."; exit 0 ;;
esac
echo ""

# --- Application files ---
step "Removing application files..."
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    info "Removed: $INSTALL_DIR"
else
    warn "Not found (already removed?): $INSTALL_DIR"
fi

# --- Menu entry ---
step "Removing menu entry..."
if [ -f "$MENU_ENTRY" ]; then
    rm -f "$MENU_ENTRY"
    info "Removed: $MENU_ENTRY"
else
    warn "Not found (already removed?): $MENU_ENTRY"
fi

# --- Desktop shortcut ---
step "Removing Desktop shortcut..."
DESKTOP_DIR="$(xdg-user-dir DESKTOP 2>/dev/null || true)"
[ -z "$DESKTOP_DIR" ] && DESKTOP_DIR="$HOME/Desktop"
if [ -f "$DESKTOP_DIR/$DESKTOP_FILE" ]; then
    rm -f "$DESKTOP_DIR/$DESKTOP_FILE"
    info "Removed: $DESKTOP_DIR/$DESKTOP_FILE"
else
    warn "Not found (already removed?): $DESKTOP_DIR/$DESKTOP_FILE"
fi

# --- Update desktop database ---
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$APPS_DIR" >/dev/null 2>&1 || true
fi

# --- Summary ---
echo ""
echo -e "${BOLD}${GREEN}==============================================${NC}"
echo -e "${BOLD}${GREEN}  Uninstall complete${NC}"
echo -e "${BOLD}${GREEN}==============================================${NC}"
echo ""
echo -e "${BOLD}What was removed:${NC}"
echo "  Application files, menu entry, and Desktop shortcut."
echo ""
echo -e "${BOLD}What was kept:${NC}"
echo "  Your password metadata:"
echo "    $USER_DATA_FILE"
echo ""
echo "To delete your data as well, run:"
echo "  rm -rf $USER_DATA_DIR"
echo ""
echo -e "${YELLOW}Note:${NC} If the menu entry still appears, log out and back in."
echo ""