from datetime import date
from smartpasslib import __version__ as lib_version


class BaseConfig:
    def __init__(self):
        self.year = str(date.today().year)
        self.app_name = 'Smart Password Manager'
        self.app_long_name = "Smart Password Manager Desktop (Python)"
        self.author = 'Alexander Suvorov'
        self.version = '3.1.0'
        self.description = ("Cross-platform desktop manager for deterministic smart passwords. "
                       "Generate, manage, and retrieve passwords without storing them. "
                       "Your secret phrase is the only key you need.")
        self.app_type = "Linux/Desktop"
        self.lib_name = "smartpasslib"
        self.lib_version = lib_version
        self.lib_lang = "python"
        self.github_url = "https://github.com/smartlegionlab"
        self.project_url = f'https://github.com/smartlegionlab/smart-password-manager-desktop/'

    @property
    def copyright(self):
        return f'Copyright © {self.year}, {self.author}. All rights reserved.'

    @property
    def copyright_text(self):
        return (f'Copyright © {self.year}, <a href="{self.github_url}" style="color: #2a82da; '
                      f'text-decoration: none;">{self.author}</a>. All rights reserved.')
