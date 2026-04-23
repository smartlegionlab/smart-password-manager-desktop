# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
from datetime import date
from core import __version__ as ver
from core import __author__ as author_


class Config:
    date_ = str(date.today().year)
    author = author_
    app_name = 'Smart Password Manager'
    description = f'{app_name}'
    copyright = f'Copyright © {date_}, {author}. All rights reserved.'
    author_url = "https://github.com/smartlegionlab"
    github_url = f'{author_url}/smart-password-manager-desktop/'
    version = f"v{ver}"
    copyright_text = (f'Copyright © {date_}, <a href="{author_url}" style="color: #2a82da; '
                      f'text-decoration: none;">{author}</a>. All rights reserved.')
    help_text = f"""
        <h3>Smart Password Manager Help {version}</h3>

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
        <li>Enter and remember your secret phrase (minimum 12 characters); Example: <b>"MyCat🐱Hippo2026"</b> or <b>"P@ssw0rd!LongSecret"</b></li>
        <li>Select password length (recommended: 16-24 characters)</li>
        <li>Click <b>Get</b> to generate password</li>
        <li>Click <b>Edit</b> to change description or length</li>
        <li>Click <b>Delete</b> to remove entry (doesn't delete password)</li>
        </ol>

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
        📂 <a href="{github_url}" style="color: #2a82da;">GitHub Repository</a><br>
        📂 <a href="{github_url}/blob/master/DISCLAIMER.md" style="color: #2a82da;">DISCLAIMER</a><br>
        🐛 <a href="{github_url}/issues" style="color: #2a82da;">Report Issues</a>
        </p>
        """

    about_text = f"""<h2>{app_name} {ver}</h2>
        <p>Cross-platform desktop manager for deterministic smart passwords.</p>
        <p><b>Features:</b></p>
        <ul>
        <li>Eliminates password storage completely</li>
        <li>Verify secret knowledge without exposure</li>
        <li>See all your password metadata at a glance</li>
        <li>Update descriptions and lengths anytime</li>
        <li>Hidden secret phrase entry with show/hide toggle</li>
        <li>Quick password copying for account setup</li>
        <li>No web dependencies or internet required</li>
        <li>Linux desktop entry creation (Application Menu / Desktop shortcuts)</li>
        </ul>
        <p><b>Copyright © {date_}, <a href="{author_url}/">{author_}</a>. All rights reserved.</b></p>
        """
    short_cuts_text = f"""<h2 style="color: #2a82da">Global Keyboard Shortcuts</h2>

        <p><b style="color: #2a82da">F1</b> - Show Help</p>
        <p><b style="color: #2a82da">Ctrl + Q</b> - Exit Application</p>
        <p><b style="color: #2a82da">Ctrl + P</b> - Create New Password</p>
        <p><b style="color: #2a82da">Ctrl + Shift + S</b> - Toggle Sounds</p>
        <p><b style="color: #2a82da">Ctrl + /</b> - Keyboard shortcuts</p>
        <p><b style="color: #2a82da">Ctrl + Shift + A</b> - About</p>
        <p><b style="color: #2a82da">Ctrl + I</b> - Import Passwords</p>
        <p><b style="color: #2a82da">Ctrl + E</b> - Export Passwords</p>

        <hr>

        <h2 style="color: #2a82da">Password's Keyboard Shortcuts</h2>

        <p><b style="color: #2a82da">Ctrl + G</b> - Get Password</p>
        <p><b style="color: #2a82da">Ctrl + Shift + E</b> - Edit Password</p>
        <p><b style="color: #2a82da">Del</b> - Delete Password</p>
        """