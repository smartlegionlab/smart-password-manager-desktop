# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
from core.models.styles.base_dialog_styles import BaseDialogStyle


class PasswordInputDialogStyles(BaseDialogStyle):
    secret_example_label_style = "color: #888; font-size: 11px; font-style: italic;"
    secret_warning_label_style = "color: #e74c3c; font-size: 11px;"
