# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
from core.models.styles.base_dialog_styles import BaseDialogStyle


class ExportImportDialogStyles(BaseDialogStyle):

    instruction_style = "color: #aaa; padding: 5px;"
    file_path_label_style = "color: #888; font-style: italic;"
    file_path_label_new_style = "color: #2a82da;"
    warning_style = "color: #ff9800; background-color: #332200; padding: 8px; border-radius: 4px;"
