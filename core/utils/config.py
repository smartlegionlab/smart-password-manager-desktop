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
    github_url = "https://github.com/smartlegionlab"
    url = f'{github_url}/smart-password-manager-desktop/'
    version = f"v{ver}"
    label_len_title = 'Password length'
    btn_new_pass_title = '+ Add'
    btn_edit_pass_title = 'Edit'
    btn_remove_pass_title = '- Delete'
    btn_get_password_title = 'Get Password'
    btn_help_title = 'Help'
    btn_about_title = 'About'
    btn_exit_title = 'Exit'
    copyright_text = (f'Copyright © {date_}, <a href="{github_url}" style="color: #2a82da; '
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
            <li>Enter and remember your secret phrase</li>
            <li>Select password length (recommended: 16-24 characters)</li>
            <li>Click <b>Get</b> to generate password</li>
            <li>Click <b>Edit</b> to change description or length</li>
            <li>Click <b>Delete</b> to remove entry (doesn't delete password)</li>
            </ol>

            <p><b>Important Notes:</b></p>
            <ul>
            <li>🔐 Never share your secret phrases</li>
            <li>📝 Back up your .cases.json file</li>
            <li>⚙️ Secret phrases are case-sensitive</li>
            <li>✏️ You can edit password descriptions anytime</li>
            <li>📏 Changing password length generates a different password!</li>
            <li>⚠️ First N characters remain same, new characters are added/removed</li>
            <li>🗑️ Deleting entry only removes metadata - password can be recreated</li>
            </ul>

            <hr>
            <p><b>Links:</b></p>
            <p>
            📂 <a href="{url}" style="color: #2a82da;">GitHub Repository</a><br>
            🐛 <a href="{url}/issues" style="color: #2a82da;">Report Issues</a>
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
            </ul>
            <p><b>Copyright © {date_}, <a href="{github_url}/">{author_}</a>. All rights reserved.</b></p>
            """
