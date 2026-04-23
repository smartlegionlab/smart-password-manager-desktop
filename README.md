# Smart Password Manager Desktop <sup>v3.1.0</sup>

---

**Cross-platform desktop manager for deterministic smart passwords. Generate, manage, and retrieve passwords without storing them. Your secret phrase is the only key you need.**

---

[![GitHub top language](https://img.shields.io/github/languages/top/smartlegionlab/smart-password-manager-desktop)](https://github.com/smartlegionlab/smart-password-manager-desktop)
[![GitHub license](https://img.shields.io/github/license/smartlegionlab/smart-password-manager-desktop)](https://github.com/smartlegionlab/smart-password-manager-desktop/blob/master/LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/smartlegionlab/smart-password-manager-desktop)](https://github.com/smartlegionlab/smart-password-manager-desktop/)
[![GitHub stars](https://img.shields.io/github/stars/smartlegionlab/smart-password-manager-desktop?style=social)](https://github.com/smartlegionlab/smart-password-manager-desktop/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/smartlegionlab/smart-password-manager-desktop?style=social)](https://github.com/smartlegionlab/smart-password-manager-desktop/network/members)
![Platform](https://img.shields.io/badge/platform-linux-lightgrey)

---

## ⚠️ Disclaimer

**By using this software, you agree to the full disclaimer terms.**

**Summary:** Software provided "AS IS" without warranty. You assume all risks.

**Full legal disclaimer:** See [DISCLAIMER.md](https://github.com/smartlegionlab/smart-password-manager-desktop/blob/master/DISCLAIMER.md)

---

## **Core Principles:**

- **Zero-Password Storage**: No passwords are ever stored or transmitted
- **Deterministic Regeneration**: Passwords are recreated identically from your secret phrase
- **Metadata Management**: Store only descriptions and verification keys
- **Local Processing**: All cryptographic operations happen on your device
- **On-Demand Discovery**: Passwords exist only when you generate them

**What You Can Do:**
1. **Create Smart Passwords**: Generate deterministic passwords from secret phrases
2. **Store Metadata Securely**: Keep password descriptions and lengths without storing passwords
3. **Regenerate Passwords**: Recreate passwords anytime using your secret phrase
4. **Manage Services**: Organize passwords for different accounts and services
5. **Edit Metadata**: Update password descriptions and lengths
6. **Copy to Clipboard**: One-click password copying for easy use
7. **Verify Secrets**: Prove knowledge of secrets without exposing them
8. **Export/Import**: Backup and restore your password metadata

**Key Features:**
- **No Password Database**: Eliminates password storage completely
- **Dark Theme Interface**: Easy on the eyes during extended use
- **Public Key Verification**: Verify secret knowledge without exposure
- **Table View**: See all your password metadata at a glance
- **Edit Functionality**: Update descriptions and lengths anytime
- **Secure Input**: Hidden secret phrase entry with show/hide toggle
- **Copy to Clipboard**: Quick password copying for account setup
- **Export/Import**: Backup and restore functionality
- **Desktop Native**: No web dependencies or internet required
- **Linux Desktop Integration**: Create application shortcuts in system menu (Linux only)

**Security Model:**
- **Proof of Knowledge**: Verify you know a secret without storing it
- **Deterministic Security**: Same secret + length = same password, always
- **Metadata Separation**: Non-sensitive data stored separately from verification
- **Local Processing**: No data leaves your computer
- **No Recovery Backdoors**: Lost secret = permanently lost access (by design)

---

## 🔄 Important: smartpasslib v3.x.x+ Breaking Change

> **⚠️ This release uses [smartpasslib](https://github.com/smartlegionlab/smartpasslib) v3.x.x+, which is NOT backward compatible with v2.x.x**

Passwords created with v2.x.x or earlier **cannot be regenerated** using v3.x.x+.

📖 **Full migration instructions** → see [MIGRATION.md](https://github.com/smartlegionlab/smart-password-manager-desktop/blob/master/MIGRATION.md)

---

## Technical Foundation

Powered by [**smartpasslib**](https://github.com/smartlegionlab/smartpasslib) — The core library for deterministic password generation.

**Key principle** (unchanged): Instead of storing passwords, you store verification metadata. The actual password is regenerated on-demand from your secret phrase.

**What's NOT stored** (unchanged):
- Your secret phrase
- The actual password
- Any reversible password data

**What IS stored** (in `~/.config/smart_password_manager/passwords.json`):
- Public verification key (hash of secret)
- Service description
- Password length parameter

**Export format**: Same JSON structure, but v3.x.x exports are **incompatible** with older versions. Always note which version created the export.

**Security model**: Proof of secret knowledge without secret storage or password transmission.

---

## File Locations

Starting from smartpasslib v2.2.0, configuration files are stored in:

| Platform | Configuration Path                                                |
|----------|:------------------------------------------------------------------|
| Linux    | `~/.config/smart_password_manager/passwords.json`                 |

**Automatic Migration**:
- Old `~/.cases.json` files are automatically migrated on first run
- Original file is backed up as `~/.cases.json.bak`
- Migration is one-time and non-destructive
- All your existing passwords are preserved

---

## Installation & Quick Start

### Prerequisites
- **Python 3.7+** required
- **Git** for cloning repository

### Quick Installation
```bash
# Clone repository
git clone https://github.com/smartlegionlab/smart-password-manager-desktop.git
cd smart-password-manager-desktop

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Launch application
python app.py
```

---

## Quick Usage Guide

### Creating Your First Password
1. Click **Add** button
2. Enter service description (e.g., "GitHub Account")
3. Enter your secret phrase (minimum 12 characters, never stored)
   - Good examples: `"MyCat🐱Hippo2026"` or `"P@ssw0rd!LongSecret"`
4. Set password length (16-24 recommended)
5. Click **Create Password** - password appears for copying

### Retrieving a Password
1. Find service in table
2. Click **Get** button
3. Enter your secret phrase
4. Password regenerates identically for copying

### Editing Password Metadata
1. Click **Edit** button next to password
2. Update description or change length
3. Receive warning if changing length
4. Confirm changes

### Deleting an Entry
1. Click **Delete** button
2. Confirm deletion
3. Only metadata removed - password can be recreated

### Exporting Passwords
1. Go to **File → Export → Export passwords...**
2. Choose export format (readable or minified JSON)
3. Select location (filename is auto-generated with timestamp: `passwords_export_YYYYMMDD_HHMMSS.json`)
4. You can rename the file if needed
5. Click **Export**

+ **Note**: Auto-generated timestamps prevent accidental file overwrites when exporting multiple times to the same folder.

### Importing Passwords
1. Go to **File → Import → Import passwords...**
2. Select previously exported JSON file
3. Review import summary
4. Click **OK** to refresh the view

---

## Core Components

### Main Interface Features

**Password Table:**
- **Description**: Service name or account identifier
- **Length**: Password character count
- **Get**: Regenerate password with secret phrase
- **Edit**: Modify description and length
- **Delete**: Remove entry (metadata only)

**Action Buttons:**
- **Add**: Create new password entry
- **Help**: Detailed usage instructions
- **Exit**: Close application with confirmation

**Security Features:**
- Secret phrase hidden by default
- Show/hide toggle for verification
- Copy to clipboard with visual feedback
- No internet connectivity required

---

### Desktop Integration (Linux)

**Creating Application Shortcuts:**

The application allows you to create desktop entries directly from the menu:

1. **Go to File → Create Desktop Entry**
2. **Choose locations:**
   - ✓ Application Menu (`~/.local/share/applications/`) - adds to system app menu
   - □ Desktop (`~/Desktop/`) - creates shortcut on desktop
3. **Click "Create Entry"**

**What happens:**
- Creates `.desktop` file(s) with proper configuration
- Sets executable permissions automatically
- Uses application icon if available

**After creation:**
- **Application Menu**: Log out and back in (or restart desktop) for entry to appear
- **Desktop shortcut**: May show "Unsecured Application Launcher" warning
  - Right-click on shortcut → "Allow Launching" or "Trust"
  - This is a one-time security confirmation

**Note:** This feature is only available on Linux systems with desktop environments that support `.desktop` files (GNOME, KDE, XFCE, etc.).

---

### Keyboard Shortcuts

| Shortcut       | Action              | Description                    |
|----------------|---------------------|--------------------------------|
| `F1`           | Help                | Show help                      |
| `Ctrl+Q`       | Exit                | Close the application          |
| `Ctrl+P`       | Create new password | Open "Create password" dialog  |
| `Ctrl+Shift+S` | Toggle sounds       | Enable/Disable app's sounds    |
| `Ctrl+/`       | Keyboard shortcuts  | Keyboard shortcuts             |
| `Ctrl+Shift+A` | About dialog        | About dialog                   |
| `Ctrl+E`       | Export passwords    | Export metadata to JSON file   |
| `Ctrl+I`       | Import passwords    | Import metadata from JSON file |
| `Ctrl+G`       | Get password        | Get selected password          |
| `Ctrl+Shift+E` | Edit password       | Edit selected password         |
| `Del`          | Delete password     | Delete selected password       |

---

### Context Menu

Right-click on any password row to access a context menu with all actions:

| Menu Item     | Action           | Description                   | Shortcuts      |
|---------------|------------------|-------------------------------|----------------|
| Get Password  | One-click access | Generate and display password | `Ctrl+G`       |
| Edit Metadata | Quick edit       | Modify description or length  | `Ctrl+Shift+E` |
| Delete Entry  | Direct deletion  | Remove password metadata      | `Del`          |

This provides an alternative to the table buttons for users who prefer context menus, while keeping the buttons for quick one-click access.

---

### Dialogs Overview

**Password Creation Dialog:**
- Service description input
- Secret phrase entry (hidden/shown)
- Password length selector (4-100 characters)
- Grouped sections for clear organization

**Secret Entry Dialog:**
- Service-specific prompts
- Hidden secret input
- Show/hide toggle
- Context-aware instructions

**Edit Metadata Dialog:**
- Description editing
- Length adjustment with warnings
- Visual feedback for changes
- Clear explanation of effects

**Password Display Dialog:**
- Generated password display
- Copy to clipboard button
- Service description header
- Security notes and reminders

**Export/Import Dialog:**
- File selection with browse button
- Format options (pretty/minified JSON)
- Metadata inclusion toggle
- Import warnings and statistics

---

## Advanced Usage

### Password Management Strategy

**For Multiple Accounts:**
```plaintext
Description Examples:
- GitHub Personal Account
- Work Email - Office 365
- Banking Portal - Chase
- Social Media - Twitter
- Cloud Storage - Dropbox

Length Strategy:
- Critical accounts: 20-24 characters
- Important accounts: 16-20 characters
- General accounts: 12-16 characters
```

### Secret Phrase Management

**Your secret phrase is the only key to all your passwords. Keep it safe, keep it secret.**

#### Minimum Requirements (enforced by the app):
- **At least 12 characters** — shorter secrets are not accepted
- **Case-sensitive** — "MySecret" and "mysecret" are different

#### Strong Secret Examples:
```
✅ "MyCat🐱Hippo2026"        — emoji + mixed case + numbers
✅ "P@ssw0rd!LongSecret"     — special chars + numbers + length
✅ "КотБегемот2026НаДиете"   — Cyrillic + numbers
✅ "Correct-Horse-Battery-42" — memorable phrase with separator
```

#### Weak Secret Examples (avoid):
```
❌ "password"                — dictionary word, too short
❌ "1234567890"              — only digits, too short
❌ "qwerty123"               — keyboard pattern
❌ "mysecret"                — common phrase, too short
```

#### Best Practices:
1. **Unique per service** - Different secret for each account type
2. **Memorable but complex** - Phrases you can remember
3. **Case-sensitive** - v3.x.x+ enforces exact case matching
4. **No digital storage** - Keep only in memory
5. **Backup plan** - Physical written backup in secure location
6. **Export regularly** - Backup metadata after adding new passwords

### Editing Strategy

**When to Edit:**
- Update service name after rebranding
- Change length for increased security
- Fix typos in descriptions
- Consolidate similar accounts

**Length Change Effects:**
- Increasing length: Password extended with new characters
- Decreasing length: Password truncated (first N characters kept)
- Consistency: First characters remain the same

### Backup Strategy

**Recommended workflow:**
1. Export metadata after adding new passwords
2. Store exports in secure, encrypted location
3. Keep exports across different machines for synchronization
4. Test import on a separate machine before relying on backups

---

## Cross-Platform Compatibility

Smart Password Manager Desktop (Python) produces **identical passwords** to:

| Platform         | Application                                                                             |
|------------------|-----------------------------------------------------------------------------------------|
| Python CLI       | [CLI PassMan](https://github.com/smartlegionlab/clipassman)                             |
| Python CLI Gen   | [CLI PassGen](https://github.com/smartlegionlab/clipassgen)                             |
| Desktop (C#)     | [Desktop Manager](https://github.com/smartlegionlab/SmartPasswordManagerCsharpDesktop)  |
| CLI C#           | [CLI Manager (C#)](https://github.com/smartlegionlab/SmartPasswordManagerCsharpCli)     |
| CLI Generator C# | [CLI Generator (C#)](https://github.com/smartlegionlab/SmartPasswordGeneratorCsharpCli) |
| Web              | [Web Manager](https://github.com/smartlegionlab/smart-password-manager-web)             |
| Android          | [Android Manager](https://github.com/smartlegionlab/smart-password-manager-android)     |

## Ecosystem

**Core Libraries:**
- **[smartpasslib](https://github.com/smartlegionlab/smartpasslib)** - Python
- **[smartpasslib-js](https://github.com/smartlegionlab/smartpasslib-js)** - JavaScript
- **[smartpasslib-kotlin](https://github.com/smartlegionlab/smartpasslib-kotlin)** - Kotlin
- **[smartpasslib-go](https://github.com/smartlegionlab/smartpasslib-go)** - Go
- **[smartpasslib-csharp](https://github.com/smartlegionlab/smartpasslib-csharp)** - C#

**CLI Applications:**
- **[CLI PassMan (Python)](https://github.com/smartlegionlab/clipassman)**
- **[CLI PassGen (Python)](https://github.com/smartlegionlab/clipassgen)**
- **[CLI Manager (C#)](https://github.com/smartlegionlab/SmartPasswordManagerCsharpCli)**
- **[CLI Generator (C#)](https://github.com/smartlegionlab/SmartPasswordGeneratorCsharpCli)**

**Desktop Applications:**
- **[Desktop Manager (Python)](https://github.com/smartlegionlab/smart-password-manager-desktop)** (this)
- **[Desktop Manager (C#)](https://github.com/smartlegionlab/SmartPasswordManagerCsharpDesktop)**

**Other:**
- **[Web Manager](https://github.com/smartlegionlab/smart-password-manager-web)**
- **[Android Manager](https://github.com/smartlegionlab/smart-password-manager-android)**

### Data Compatibility
- Uses same `~/.config/smart_password_manager/passwords.json` format as CLI tools
- Export files compatible across all ecosystem tools
- Consistent cryptographic operations across platforms

---

## Research Paradigms & Publications

- **[Pointer-Based Security Paradigm](https://doi.org/10.5281/zenodo.17204738)** - Architectural Shift from Data Protection to Data Non-Existence
- **[Local Data Regeneration Paradigm](https://doi.org/10.5281/zenodo.17264327)** - Ontological Shift from Data Transmission to Synchronous State Discovery

---

## Version History

| Version          | smartpasslib | Status                   | Migration Required      |
|------------------|--------------|--------------------------|-------------------------|
| v2.x.x and below | v2.x.x       | ❌ Deprecated/Unsupported | Must migrate to v3.x.x+ |
| v3.x.x+          | v3.x.x+      | ✅ Current                | N/A                     |

---

## License

**[BSD 3-Clause License](https://github.com/smartlegionlab/smart-password-manager-desktop/blob/master/LICENSE)**

Copyright (©) 2026, [Alexander Suvorov](https://github.com/smartlegionlab)

---

## Support

- **Desktop Manager Issues**: [GitHub Issues](https://github.com/smartlegionlab/smart-password-manager-desktop/issues)
- **Core Library Issues**: [smartpasslib Issues](https://github.com/smartlegionlab/smartpasslib/issues)
- **Documentation**: Inline help and this README

**Note**: Always test password generation with non-essential accounts first. Implementation security depends on proper usage.

---

## Security Warnings

### Secret Phrase Security

**Your secret phrase is the cryptographic master key**

1. **Permanent data loss**: Lost secret phrase = irreversible loss of all derived passwords
2. **No recovery mechanisms**: No password recovery, no secret reset, no administrative override
3. **Deterministic generation**: Identical input (secret + length) = identical output (password)
4. **Single point of failure**: Secret phrase is the sole authentication factor for all passwords
5. **Secure storage required**: Digital storage of secret phrases is prohibited

**Critical**: Test password regeneration with non-essential accounts before production use

### Secret Phrase Strength

**The security of your passwords depends entirely on your secret phrase.**

- **Minimum 12 characters** is enforced by the application
- Short secrets (under 12 chars) are **automatically rejected**
- Weak secrets like "password123" or "qwerty" will be rejected
- Use a mix of: uppercase, lowercase, numbers, symbols, emoji, or Cyrillic
- A 12-character secret with diverse character types provides **practical brute-force immunity**

**Remember:** The app cannot recover your secret phrase. If you lose it, all passwords are permanently lost.

### Export/Import Security Notes

- Export files contain ONLY metadata (public keys, descriptions, lengths)
- No passwords or secret phrases are ever exported
- Export files are plain JSON - store them securely
- Treat exported metadata as sensitive information

---

## Interface

![Main Interface 1](https://github.com/smartlegionlab/smart-password-manager-desktop/raw/master/data/images/smartpassman1.png)

![Main Interface 2](https://github.com/smartlegionlab/smart-password-manager-desktop/raw/master/data/images/smartpassman2.png)

![Main Interface 3](https://github.com/smartlegionlab/smart-password-manager-desktop/raw/master/data/images/smartpassman3.png)

![Main Interface 4](https://github.com/smartlegionlab/smart-password-manager-desktop/raw/master/data/images/smartpassman4.png)

