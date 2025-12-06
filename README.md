# Smart Password Manager Desktop <sup>v2.2.2</sup>

---

**Cross-platform desktop manager for deterministic smart passwords. Generate, manage, and retrieve passwords without storing them. Your secret phrase is the only key you need.**

---

[![GitHub top language](https://img.shields.io/github/languages/top/smartlegionlab/smart-password-manager-desktop)](https://github.com/smartlegionlab/smart-password-manager-desktop)
[![GitHub license](https://img.shields.io/github/license/smartlegionlab/smart-password-manager-desktop)](https://github.com/smartlegionlab/smart-password-manager-desktop/blob/master/LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/smartlegionlab/smart-password-manager-desktop)](https://github.com/smartlegionlab/smart-password-manager-desktop/)
[![GitHub stars](https://img.shields.io/github/stars/smartlegionlab/smart-password-manager-desktop?style=social)](https://github.com/smartlegionlab/smart-password-manager-desktop/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/smartlegionlab/smart-password-manager-desktop?style=social)](https://github.com/smartlegionlab/smart-password-manager-desktop/network/members)

---

## **🔐 Core Principles:**

- 🔐 **Zero-Password Storage**: No passwords are ever stored or transmitted
- 🔑 **Deterministic Regeneration**: Passwords are recreated identically from your secret phrase
- 📝 **Metadata Management**: Store only descriptions and verification keys
- 🖥️ **Local Processing**: All cryptographic operations happen on your device
- 🔄 **On-Demand Discovery**: Passwords exist only when you generate them

**What You Can Do:**
1. **Create Smart Passwords**: Generate deterministic passwords from secret phrases
2. **Store Metadata Securely**: Keep password descriptions and lengths without storing passwords
3. **Regenerate Passwords**: Recreate passwords anytime using your secret phrase
4. **Manage Services**: Organize passwords for different accounts and services
5. **Edit Metadata**: Update password descriptions and lengths
6. **Copy to Clipboard**: One-click password copying for easy use
7. **Verify Secrets**: Prove knowledge of secrets without exposing them
8. **Cross-Platform Management**: Windows and Linux support with consistent interface

**Key Features:**
- ✅ **No Password Database**: Eliminates password storage completely
- ✅ **Dark Theme Interface**: Easy on the eyes during extended use
- ✅ **Public Key Verification**: Verify secret knowledge without exposure
- ✅ **Table View**: See all your password metadata at a glance
- ✅ **Edit Functionality**: Update descriptions and lengths anytime
- ✅ **Secure Input**: Hidden secret phrase entry with show/hide toggle
- ✅ **Copy to Clipboard**: Quick password copying for account setup
- ✅ **Desktop Native**: No web dependencies or internet required

**Security Model:**
- **Proof of Knowledge**: Verify you know a secret without storing it
- **Deterministic Security**: Same secret + length = same password, always
- **Metadata Separation**: Non-sensitive data stored separately from verification
- **Local Processing**: No data leaves your computer
- **No Recovery Backdoors**: Lost secret = permanently lost access (by design)

---

## ⚠️ Critical Notice

**BEFORE USING THIS SOFTWARE, READ THE COMPLETE LEGAL DISCLAIMER BELOW**

[View Legal Disclaimer & Liability Waiver](#-legal-disclaimer)

*Usage of this software constitutes acceptance of all terms and conditions.*

---

## 📚 Research Paradigms & Publications

- **[Pointer-Based Security Paradigm](https://doi.org/10.5281/zenodo.17204738)** - Architectural Shift from Data Protection to Data Non-Existence
- **[Local Data Regeneration Paradigm](https://doi.org/10.5281/zenodo.17264327)** - Ontological Shift from Data Transmission to Synchronous State Discovery

---

## 🔬 Technical Foundation

Powered by **[smartpasslib v2.1.0+](https://github.com/smartlegionlab/smartpasslib)** - The core library for deterministic password generation.

**Key principle**: Instead of storing passwords, you store verification metadata. The actual password is regenerated on-demand from your secret phrase.

**What's NOT stored**:
- Your secret phrase
- The actual password
- Any reversible password data

**What IS stored** (in `~/.cases.json`):
- Public verification key (hash of secret)
- Service description
- Password length parameter

**Security model**: Proof of secret knowledge without secret storage or password transmission.

---

## 🆕 What's New in v2.2.2

### ⚠️ **BREAKING CHANGES WARNING**

**CRITICAL**: v2.2.2 is **NOT** backward compatible with v1.x. All passwords generated with v1.x are now **INVALID**. You must recreate all passwords using your secret phrases.

### Major Improvements:

**New Edit Functionality:**
- Added **Edit** button for each password entry
- Update password descriptions anytime
- Change password length with visual warnings
- First N characters remain consistent when changing lengths

**Enhanced User Interface:**
- 5-column table layout: Description, Length, Get, Edit, Delete
- Improved button layouts and visual hierarchy
- Added length change warnings with clear explanations
- Better tooltips and user guidance

**Window Management:**
- Added automatic window centering on startup
- Improved dialog positioning and sizing
- Better responsive layout for different screen sizes

**User Experience:**
- Clearer warning messages for length changes
- Improved help documentation with edit instructions
- Better error messages and user feedback
- Streamlined table operations

### Breaking Changes:

**Compatibility:**
- **NOT compatible** with v1.x password generation
- Requires **smartpasslib v2.1.0+**
- **All v1.x passwords must be recreated**

**Migration Required:**
```bash
# Backup old passwords if needed
# Delete old ~/.cases.json file
# Recreate all passwords with v2.2.2
# Update all account credentials
```

### New Features:

**Password Metadata Editing:**
```python
# Edit password description and length
# First characters remain consistent when changing length
# Visual warnings for length changes
```

**Improved UI:**
- Separate columns for Get/Edit/Delete actions
- Better visual distinction between action types
- Enhanced help text with edit instructions
- Clear warnings for irreversible operations

**Technical Updates:**
- Updated to smartpasslib v2.1.0 API
- Improved public key handling
- Better error handling and validation
- Enhanced dialog management

### Key Improvements:

1. **Edit Functionality** - Change descriptions and lengths without recreating
2. **Better Warnings** - Clear explanations for length changes
3. **Improved Layout** - 5-column table for better organization
4. **Enhanced UX** - Better feedback and user guidance
5. **Modern API** - Updated to latest smartpasslib version

---

## 📦 Installation & Quick Start

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
# Linux/macOS: source venv/bin/activate
# Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Launch application
python app.py
```

---

## 🚀 Quick Usage Guide

### Creating Your First Password
1. Click **Add** button
2. Enter service description (e.g., "GitHub Account")
3. Enter your secret phrase (never shared or stored)
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
1. Click **Delete** button (🗑️)
2. Confirm deletion
3. Only metadata removed - password can be recreated

---

## 🏗️ Core Components

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

---

## 💡 Advanced Usage

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

**Best Practices:**
1. **Unique per service** - Different secret for each account type
2. **Memorable but complex** - Phrases you can remember
3. **Case-sensitive** - v2.2.2 enforces exact case matching
4. **No digital storage** - Keep only in memory
5. **Backup plan** - Physical written backup in secure location

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

---

## 🔧 Ecosystem Integration

### Part of Smart Password Suite

**Core Technology:**
- **[smartpasslib](https://github.com/smartlegionlab/smartpasslib)** - Core password generation library

**Console Applications:**
- **[CLI Smart Password Generator](https://github.com/smartlegionlab/clipassgen/)** - Terminal-based generation
- **[CLI Smart Password Manager](https://github.com/smartlegionlab/clipassman/)** - Command-line management

**Web Interface:**
- **[Web Smart Password Manager](https://github.com/smartlegionlab/smart-password-manager)** - Browser-based access

### Data Compatibility
- Uses same `~/.cases.json` format as CLI tools
- Compatible metadata with smartpasslib ecosystem
- Consistent cryptographic operations across platforms

---

## 👨‍💻 For Developers

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run application in development mode
python app.py

# Code structure
smart-password-manager-desktop/
├── app.py              # Application entry point
├── core/               # Core application modules
│   ├── config.py      # Configuration settings
│   └── main.py        # Main window implementation
├── requirements.txt    # Dependencies
└── README.md          # This documentation
```

### Building Executables

**Windows:**
```bash
pyinstaller --onefile --windowed --icon=assets/icon.ico app.py
```

**Linux:**
```bash
pyinstaller --onefile app.py
```

### Testing
- Manual testing for UI interactions
- Cross-platform compatibility verification
- Secret phrase validation testing
- Clipboard operations verification

---

## 📜 License

**[BSD 3-Clause License](LICENSE)**

Copyright (c) 2025, Alexander Suvorov

```
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

---

## 🆘 Support

- **Desktop Manager Issues**: [GitHub Issues](https://github.com/smartlegionlab/smart-password-manager-desktop/issues)
- **Core Library Issues**: [smartpasslib Issues](https://github.com/smartlegionlab/smartpasslib/issues)
- **Documentation**: Inline help and this README

**Note**: Always test password generation with non-essential accounts first. Implementation security depends on proper usage.

---

## ⚠️ Security Warnings

**Version Incompatibility**: v2.2.2 passwords are incompatible with v1.x.
Never mix secret phrases across different versions.

### Secret Phrase Security

**Your secret phrase is the cryptographic master key**

1. **Permanent data loss**: Lost secret phrase = irreversible loss of all derived passwords
2. **No recovery mechanisms**: No password recovery, no secret reset, no administrative override
3. **Deterministic generation**: Identical input (secret + length) = identical output (password)
4. **Single point of failure**: Secret phrase is the sole authentication factor for all passwords
5. **Secure storage required**: Digital storage of secret phrases is prohibited

**Critical**: Test password regeneration with non-essential accounts before production use

---

## 📄 Legal Disclaimer

**COMPLETE AND ABSOLUTE RELEASE FROM ALL LIABILITY**

**SOFTWARE PROVIDED "AS IS" WITHOUT ANY WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT.**

The copyright holder, contributors, and any associated parties **EXPLICITLY DISCLAIM AND DENY ALL RESPONSIBILITY AND LIABILITY** for:

1. **ANY AND ALL DATA LOSS**: Complete or partial loss of passwords, accounts, credentials, cryptographic keys, or any data whatsoever
2. **ANY AND ALL SECURITY INCIDENTS**: Unauthorized access, data breaches, account compromises, theft, or exposure of sensitive information
3. **ANY AND ALL FINANCIAL LOSSES**: Direct, indirect, incidental, special, consequential, or punitive damages of any kind
4. **ANY AND ALL OPERATIONAL DISRUPTIONS**: Service interruptions, account lockouts, authentication failures, or denial of service
5. **ANY AND ALL IMPLEMENTATION ISSUES**: Bugs, errors, vulnerabilities, misconfigurations, or incorrect usage
6. **ANY AND ALL LEGAL OR REGULATORY CONSEQUENCES**: Violations of laws, regulations, compliance requirements, or terms of service
7. **ANY AND ALL PERSONAL OR BUSINESS DAMAGES**: Reputational harm, business interruption, loss of revenue, or any other damages
8. **ANY AND ALL THIRD-PARTY CLAIMS**: Claims made by any other parties affected by software usage

**USER ACCEPTS FULL AND UNCONDITIONAL RESPONSIBILITY**

By installing, accessing, or using this software in any manner, you irrevocably agree that:

- You assume **ALL** risks associated with software usage
- You bear **SOLE** responsibility for secret phrase management and security
- You accept **COMPLETE** responsibility for all testing and validation
- You are **EXCLUSIVELY** liable for compliance with all applicable laws
- You accept **TOTAL** responsibility for any and all consequences
- You **PERMANENTLY AND IRREVOCABLY** waive, release, and discharge all claims against the copyright holder, contributors, distributors, and any associated entities

**NO WARRANTY OF ANY KIND**

This software comes with **ABSOLUTELY NO GUARANTEES** regarding:
- Security effectiveness or cryptographic strength
- Reliability or availability
- Fitness for any particular purpose
- Accuracy or correctness
- Freedom from defects or vulnerabilities

**NOT A SECURITY PRODUCT OR SERVICE**

This is experimental software. It is not:
- Security consultation or advice
- A certified cryptographic product
- A guaranteed security solution
- Professional security software
- Endorsed by any security authority

**FINAL AND BINDING AGREEMENT**

Usage of this software constitutes your **FULL AND UNCONDITIONAL ACCEPTANCE** of this disclaimer. If you do not accept **ALL** terms and conditions, **DO NOT USE THE SOFTWARE.**

**BY PROCEEDING, YOU ACKNOWLEDGE THAT YOU HAVE READ THIS DISCLAIMER IN ITS ENTIRETY, UNDERSTAND ITS TERMS COMPLETELY, AND ACCEPT THEM WITHOUT RESERVATION OR EXCEPTION.**

---

**Version**: 2.2.2 | [**Author**](https://smartlegionlab.ru): [Alexander Suvorov](https://alexander-suvorov.ru)

---

**Note**: This is v2.2.2. If migrating from v1.x, all passwords must be regenerated with new secret phrases.

---

## Interface

![Main Interface 1](https://github.com/smartlegionlab/smart-password-manager-desktop/raw/master/data/images/smartpassman1.png)

![Main Interface 2](https://github.com/smartlegionlab/smart-password-manager-desktop/raw/master/data/images/smartpassman2.png)

![Main Interface 3](https://github.com/smartlegionlab/smart-password-manager-desktop/raw/master/data/images/smartpassman3.png)

![Main Interface 4](https://github.com/smartlegionlab/smart-password-manager-desktop/raw/master/data/images/smartpassman4.png)
