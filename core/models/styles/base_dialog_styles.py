# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
from core.styles.theme_manager import ThemeManager


class BaseDialogStyle:

    @staticmethod
    def get_button_style(button_type='primary'):
        return ThemeManager.get_button_style(button_type)

    @staticmethod
    def get_input_style():
        return ThemeManager.get_input_style()

    @staticmethod
    def get_groupbox_style():
        return ThemeManager.get_groupbox_style()

    @staticmethod
    def get_label_style(label_type='normal'):
        return ThemeManager.get_label_style(label_type)
