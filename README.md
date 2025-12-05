# Smart Password Manager Desktop <sup>v2.0.0</sup>

---

> **Smart password manager** implementing deterministic password generation - your passwords are never stored, only regenerated when needed.

---

[![GitHub top language](https://img.shields.io/github/languages/top/smartlegionlab/smart-password-manager-desktop)](https://github.com/smartlegionlab/smart-password-manager-desktop)
[![GitHub license](https://img.shields.io/github/license/smartlegionlab/smart-password-manager-desktop)](https://github.com/smartlegionlab/smart-password-manager-desktop/blob/master/LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/smartlegionlab/smart-password-manager-desktop)](https://github.com/smartlegionlab/smart-password-manager-desktop/)
[![GitHub stars](https://img.shields.io/github/stars/smartlegionlab/smart-password-manager-desktop?style=social)](https://github.com/smartlegionlab/smart-password-manager-desktop/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/smartlegionlab/smart-password-manager-desktop?style=social)](https://github.com/smartlegionlab/smart-password-manager-desktop/network/members)

## 🖥️ Desktop Manager for Deterministic Smart Passwords

Cross-platform desktop application for managing password metadata using deterministic smart password generation.

> **Powered by** [smartpasslib v2.0.0](https://github.com/smartlegionlab/smartpasslib) - The core library for deterministic password generation

### ⚠️ **BREAKING CHANGES in v2.0.0**

**WARNING:** This version introduces breaking changes:
- All passwords generated with v1.x are now **INVALID**
- You must create **NEW** passwords using your secret phrases
- Simplified API - only secret phrase required (no login parameter)

## 🚀 Quick Start

### Prerequisites
- **Python 3.7+** required - [Download Python](https://python.org)
- **Git** for cloning repository

### Installation & Run
```bash
# Clone the repository
git clone https://github.com/smartlegionlab/smart-password-manager-desktop.git
cd smart-password-manager-desktop

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Launch the application
python app.py
```

## 🎨 Interface Overview

![Main Interface](https://github.com/smartlegionlab/smart-password-manager-desktop/raw/master/data/images/smartpassman.png)

### Key Features:
- **Dark Theme** - Easy on the eyes during extended use
- **Password Table** - View all stored password metadata
- **Quick Actions** - Generate, retrieve, and delete passwords
- **Copy to Clipboard** - One-click password copying
- **Secret Visibility** - Show/hide secret phrases during input

## 🔧 How It Works

### Discovery Over Storage

**Traditional Password Managers:**
- Store encrypted passwords
- Require master password decryption
- Risk data breaches

**Smart Password Manager:**
- Stores only **verification metadata** (public keys)
- Passwords generated **on-demand** from secret phrases
- No password database to breach
- Deterministic generation ensures consistency

### Creating a Password:
1. Enter service description (e.g., "GitHub Account")
2. Provide your secret phrase (never leaves your computer)
3. Set password length (4-100 characters)
4. Password is generated and can be copied to clipboard

### Retrieving a Password:
1. Select service from table
2. Enter your secret phrase
3. Password is regenerated identically

## 🔄 Smart Password Ecosystem

This desktop manager is part of a comprehensive suite of applications built on deterministic password technology:

### 🛠️ Console Applications
- [**CLI Smart Password Generator**](https://github.com/smartlegionlab/clipassgen/) - Command-line password generator
- [**CLI Smart Password Manager**](https://github.com/smartlegionlab/clipassman/) - Console-based password manager

### 🌐 Web Applications
- [**Web Smart Password Manager**](https://github.com/smartlegionlab/smart-password-manager) - Web-based management interface

### 💡 Core Technology
- [**SmartPassLib v2.0.0**](https://github.com/smartlegionlab/smartpasslib) - Core password generation library

## 🛡️ Security Features

### What Makes It Secure:
- **No Password Storage** - Passwords exist only when generated
- **Local Processing** - All cryptographic operations on your device
- **Deterministic Generation** - Same secret → same password, every time
- **Verification Without Storage** - Public keys verify secret knowledge
- **Open Source** - Transparent codebase for security verification

### Data Privacy:
- All data stored locally in `~/.cases.json`
- No internet connectivity required
- No telemetry or data collection
- No cloud synchronization

## ⚙️ Technical Details

### Architecture:
- **Frontend**: PyQt5 for cross-platform GUI
- **Backend**: smartpasslib v2.0.0 for password generation
- **Storage**: JSON-based local file storage
- **Platform**: Native desktop application

### Cryptographic Foundation:
- SHA3-512 for key derivation
- Deterministic random seeding
- Public key verification system
- No reversible password storage

## 📋 Migration from v1.x

### Important Notes:
- **v2.0.0 is NOT backward compatible** with v1.x
- **All v1.x passwords are invalid** in v2.0.0
- **You must recreate all passwords** using your secret phrases

### Migration Steps:
1. **Backup** any critical passwords from v1.x
2. **Install** v2.0.0 fresh
3. **Delete** old `~/.cases.json` file
4. **Recreate** all passwords using your secret phrases
5. **Update** all service credentials

### Why the Breaking Changes?
- Simplified API (removed login parameter)
- Improved cryptographic algorithms
- Better security model
- Cleaner codebase

## 🤝 Supported Platforms

### Fully Tested:
- **Linux** - Ubuntu 20.04+, Fedora 32+, Debian 10+
- **Windows** - Windows 10, Windows 11

## 🐛 Troubleshooting

### Common Issues:

**"Module not found" errors:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Application won't start:**
```bash
# Check Python version
python --version  # Should be 3.7+
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

**Password generation fails:**
- Ensure secret phrase is entered correctly
- Check Caps Lock and keyboard layout
- Verify password length is between 4-100 characters

### Getting Help:
1. Check [GitHub Issues](https://github.com/smartlegionlab/smart-password-manager-desktop/issues)
2. Review the [smartpasslib documentation](https://github.com/smartlegionlab/smartpasslib)
3. Create a new issue with details of your problem

## 🚀 Development

### For Developers:
```bash
# Clone with submodules
git clone --recursive https://github.com/smartlegionlab/smart-password-manager-desktop.git

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Build executable (Windows)
pyinstaller --onefile --windowed --icon=icon.ico app.py
```

## 📜 License

**BSD 3-Clause License**

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

## 🔗 Links & Resources

- **GitHub Repository**: [smart-password-manager-desktop](https://github.com/smartlegionlab/smart-password-manager-desktop)
- **Core Library**: [smartpasslib](https://github.com/smartlegionlab/smartpasslib)
- **Issues & Support**: [GitHub Issues](https://github.com/smartlegionlab/smart-password-manager-desktop/issues)
- **Pointer-Based Security Paradigm**: [Paper](https://doi.org/10.5281/zenodo.17204738)
- **Local Data Regeneration Paradigm**: [Paper](https://doi.org/10.5281/zenodo.17264327)

---

**Note**: Always keep backup copies of your secret phrases. 
If you lose your secret phrase, you cannot regenerate your passwords.
