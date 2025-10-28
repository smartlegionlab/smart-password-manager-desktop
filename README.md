# Smart Password Manager Desktop <sup>v1.1.2</sup>

---

> Note: This is a production-ready password manager. For academic research on the underlying security paradigm, see [The Pointer-Based Security Paradigm](https://doi.org/10.5281/zenodo.17204738).

---


[![GitHub top language](https://img.shields.io/github/languages/top/smartlegionlab/smart-password-manager-desktop)](https://github.com/smartlegionlab/smart-password-manager-desktop)
[![GitHub license](https://img.shields.io/github/license/smartlegionlab/smart-password-manager-desktop)](https://github.com/smartlegionlab/smart-password-manager-desktop/blob/master/LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/smartlegionlab/smart-password-manager-desktop)](https://github.com/smartlegionlab/smart-password-manager-desktop/)
[![GitHub stars](https://img.shields.io/github/stars/smartlegionlab/smart-password-manager-desktop?style=social)](https://github.com/smartlegionlab/smart-password-manager-desktop/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/smartlegionlab/smart-password-manager-desktop?style=social)](https://github.com/smartlegionlab/smart-password-manager-desktop/network/members)

## 🖥️ Desktop Password Manager for Smart Passwords

Smart Password Manager (Desktop Version)

> **Powered by** [smartpasslib](https://github.com/smartlegionlab/smartpasslib) - The core library for deterministic password generation

Your passwords don't need to be stored because they were never created - they already exist as mathematical certainties, waiting to be discovered through the correct combination of login and secret phrase.

## 🚀 Quick Start

### Prerequisites
- **Python 3.7+** required - [Download Python](https://python.org)

### Installation & Run
```bash
# Clone the repository
git clone https://github.com/smartlegionlab/smart-password-manager-desktop.git
cd smart-password-manager-desktop

# Create virtual environment
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


![Password Management](https://github.com/smartlegionlab/smart-password-manager-desktop/raw/master/data/images/smartpassman2.png)


![Settings Configuration](https://github.com/smartlegionlab/smart-password-manager-desktop/raw/master/data/images/smartpassman3.png)

## 🔄 Smart Password Ecosystem

This desktop manager is part of a comprehensive suite of applications built on smart password technology:

### 🛠️ Console Applications
- [**CLI PassGen**](https://github.com/smartlegionlab/clipassgen/) - Command-line password generator
- [**CLI PassMan**](https://github.com/smartlegionlab/clipassman/) - Console-based password manager

### 🌐 Web & Mobile Applications
- [**Web Password Manager**](https://github.com/smartlegionlab/smart-password-manager) - Web-based management interface

### 💡 Core Technology
- [**SmartPassLib**](https://github.com/smartlegionlab/smartpasslib) - Core password generation library

## 🛡️ Security Features

- **No Password Storage** - Credentials are generated on-demand
- **Local Processing** - All operations occur on your local machine
- **Open Source** - Transparent codebase for security verification

## 🤝 Supported Platforms

- **Linux** - Ubuntu, Fedora, Debian, and other major distributions
- **Windows** - 7, 8, 10, 11


## 📜 License

BSD 3-Clause License

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
