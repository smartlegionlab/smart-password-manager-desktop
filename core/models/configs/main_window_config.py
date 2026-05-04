from core.models.configs.base_config import BaseConfig


class MainWindowConfig(BaseConfig):
    def __init__(self):
        super().__init__()

        self.help_text = f"""
<h3>Smart Password Manager Help {self.version}</h3>

<p><b>How it works:</b></p>
<ul>
<li>Each password is generated from your secret phrase</li>
<li>No passwords are stored - regenerate when needed</li>
<li>Same secret phrase always generates the same password</li>
</ul>

<p><b>Basic Steps:</b></p>
<ol>
<li>Click <b>Add</b> to create a new password entry</li>
<li>Enter password description (e.g., "GitHub")</li>
<li>Enter and remember your secret phrase (minimum 12 characters); Example: 
<b>"MyCat🐱Hippo2026"</b> or <b>"P@ssw0rd!LongSecret"</b></li>
<li>Select password length (recommended: 16-24 characters)</li>
<li>Click <b>Get</b> to generate password</li>
<li>Click <b>Edit</b> to change description or length</li>
<li>Click <b>Delete</b> to remove entry (doesn't delete password)</li>
</ol>

<p><b>QR Code Export:</b></p>
<ul>
<li>Click <b>QR</b> button next to any password to generate a QR code</li>
<li>Scan with <b>Smart Password Manager Android</b> app to import the password metadata</li>
<li>Keyboard shortcut: <b>Ctrl+R</b> for selected password</li>
<li>QR contains only metadata - no secrets</li>
<li>Right-click on any password row → <b>Show QR Code</b></li>
</ul>

<p><b>Desktop Integration:</b></p>
<ul>
<li><b>File → Create Desktop Entry</b> — Create application shortcut in your system menu (Linux only)</li>
<li>Choose between Application Menu (~/.local/share/applications/) and/or Desktop (~/Desktop/)</li>
<li>After creation, you may need to log out and back in for the entry to appear</li>
<li>Desktop shortcuts may show "Unsecured Application Launcher" — right-click → "Allow Launching" (one-time only)</li>
</ul>

<p><b>Important Notes:</b></p>
<ul>
<li>Never share your secret phrases</li>
<li>Back up your /home/user/.config/smart_password_manager/passwords.json file</li>
<li>Secret phrases are case-sensitive</li>
<li>You can edit password descriptions anytime</li>
<li>Changing password length generates a different password!</li>
<li>First N characters remain same, new characters are added/removed</li>
<li>Deleting entry only removes metadata - password can be recreated</li>
</ul>

<hr>
<p><b>Links:</b></p>
<p>
📂 <a href="{self.project_url}" style="color: #2a82da;">GitHub Repository</a><br>
📂 <a href="{self.project_url}/blob/master/DISCLAIMER.md" style="color: #2a82da;">DISCLAIMER</a><br>
🐛 <a href="{self.project_url}/issues" style="color: #2a82da;">Report Issues</a>
</p>
"""

        self.about_text = f"""
═════════════════════════════════════════════════════════════════════════
  {self.app_name} {self.version}
═════════════════════════════════════════════════════════════════════════

Cross-platform desktop manager for deterministic smart passwords.
Generate, manage, and retrieve passwords without storing them.
Your secret phrase is the only key you need.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DECENTRALIZED BY DESIGN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• No cloud, no database, no trust required
• Your secrets never leave your device
• There is no "forgot password" button — you are in complete control
• Metadata can be synced via any channel

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  SECURITY MODEL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Proof of Knowledge: Public keys verify secrets without exposing them
• Deterministic Security: Same secret + length = same password
• Zero-Storage: No passwords or secrets are ever stored
• Local Processing: Secrets never leave your device

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  KEY FEATURES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Smart Password Generation from secret phrase
• Public/Private Key System (30/60 iterations)
• Export/Import: Backup and restore metadata
• QR Code Export: Transfer to Android app
• Copy to Clipboard: One-click password copying
• Hide/Show: Secure secret phrase entry

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  SECURITY REQUIREMENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Secret phrase: Minimum 12 characters
• Case-sensitive
• Use mixed case, numbers, symbols, emoji, or Cyrillic
• NEVER use your password description as secret phrase

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  STORAGE LOCATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🐧 Linux: ~/.config/smart_password_manager/passwords.json

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  TECHNICAL FOUNDATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Powered by smartpasslib — deterministic password generation library
Key derivation: 30 iterations (private key) / 60 iterations (public key)
Character set: a-z A-Z 0-9 ! @ # $ & * - _

═════════════════════════════════════════════════════════════════════════
  Copyright © {self.year}, <a href="{self.github_url}/">{self.author}</a>. 
  All rights reserved. Licensed under BSD 3-Clause License
═════════════════════════════════════════════════════════════════════════
"""

        self.short_cuts_text = """
    ═════════════════════════════════════════════════════════════════════════
      KEYBOARD SHORTCUTS
    ═════════════════════════════════════════════════════════════════════════

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      GLOBAL SHORTCUTS
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

      F1               →  Show Help
      Ctrl + Q         →  Exit Application
      Ctrl + N         →  Create New Password
      Ctrl + Shift + S →  Toggle Sounds
      Ctrl + /         →  Keyboard shortcuts
      Ctrl + A         →  About
      Ctrl + I         →  Import Passwords
      Ctrl + E         →  Export Passwords
      Ctrl + R         →  Show QR Code for selected password
      Ctrl + G         →  Get Password
      Ctrl + Shift + E →  Edit Password
      Del              →  Delete Password
      F5               →  Refresh list
      Enter            →  Get password (when item selected)

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      OTHER SHORTCUTS
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

      Ctrl + D         →  Show Disclaimer
      Ctrl + L         →  Show License
      Ctrl + Alt + S   →  Create Desktop Shortcut
        """

        self.disclaimer_text = """
LEGAL DISCLAIMER

COMPLETE AND ABSOLUTE RELEASE FROM ALL LIABILITY

SOFTWARE PROVIDED "AS IS" WITHOUT ANY WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT.

The copyright holder, contributors, and any associated parties EXPLICITLY DISCLAIM AND DENY ALL RESPONSIBILITY AND LIABILITY for:

1. ANY AND ALL DATA LOSS: Complete or partial loss of any data, files, configuration, or information whatsoever
2. ANY AND ALL SECURITY INCIDENTS: Unauthorized access, breaches, compromises, theft, or exposure of any sensitive information
3. ANY AND ALL FINANCIAL LOSSES: Direct, indirect, incidental, special, consequential, or punitive damages of any kind
4. ANY AND ALL OPERATIONAL DISRUPTIONS: Service interruptions, system failures, authentication issues, or denial of service
5. ANY AND ALL IMPLEMENTATION ISSUES: Bugs, errors, vulnerabilities, misconfigurations, incorrect usage, or compatibility problems
6. ANY AND ALL LEGAL OR REGULATORY CONSEQUENCES: Violations of laws, regulations, compliance requirements, or third-party terms of service
7. ANY AND ALL PERSONAL OR BUSINESS DAMAGES: Reputational harm, business interruption, loss of revenue, lost profits, or any other damages
8. ANY AND ALL THIRD-PARTY CLAIMS: Claims made by any other parties affected by software usage
9. ANY AND ALL SYSTEM DAMAGES: Hardware damage, software corruption, operating system instability, or data corruption

USER ACCEPTS FULL AND UNCONDITIONAL RESPONSIBILITY

By installing, accessing, cloning, forking, or using this software in any manner, you irrevocably agree that:

- You assume ALL risks associated with software usage
- You bear SOLE responsibility for your data, credentials, and system security
- You accept COMPLETE responsibility for all testing and validation before production use
- You are EXCLUSIVELY liable for compliance with all applicable laws and regulations
- You accept TOTAL responsibility for any and all consequences of usage
- You PERMANENTLY AND IRREVOCABLY waive, release, and discharge all claims against the copyright holder, contributors, distributors, and any associated entities

NO WARRANTY OF ANY KIND

This software comes with ABSOLUTELY NO GUARANTEES regarding:
- Security effectiveness or cryptographic strength
- Reliability, availability, or uptime
- Fitness for any particular purpose or use case
- Accuracy, correctness, or completeness
- Freedom from defects, vulnerabilities, or backdoors
- Compatibility with any specific hardware, software, or environment

NOT A PROFESSIONAL OR CERTIFIED SOLUTION

This software is provided for educational and experimental purposes. It is not:
- Professional advice or consultation of any kind
- A certified, audited, or validated product
- A guaranteed security solution
- Enterprise-grade or production-ready software
- Endorsed by any authority, organization, or standards body

FINAL AND BINDING AGREEMENT

Usage of this software constitutes your FULL AND UNCONDITIONAL ACCEPTANCE of this disclaimer. If you do not accept ALL terms and conditions, DO NOT USE, CLONE, FORK, OR DOWNLOAD THIS SOFTWARE.

BY PROCEEDING, YOU ACKNOWLEDGE THAT YOU HAVE READ THIS DISCLAIMER IN ITS ENTIRETY, UNDERSTAND ITS TERMS COMPLETELY, AND ACCEPT THEM WITHOUT RESERVATION OR EXCEPTION.
"""

        self.license_text = """
BSD 3-Clause License

Copyright (©) 2026, Alexander Suvorov

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

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
"""
