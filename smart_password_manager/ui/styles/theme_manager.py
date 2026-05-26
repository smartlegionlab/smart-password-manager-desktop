# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt


class ThemeManager:

    COLORS = {
        'primary': '#2a82da',
        'primary_hover': '#1a72ca',
        'primary_dark': '#0d47a1',

        'success': '#28a745',
        'success_hover': '#218838',
        'warning': '#ff9800',
        'warning_hover': '#e68900',
        'danger': '#dc3545',
        'danger_hover': '#c82333',
        'info': '#17a2b8',
        'info_hover': '#138496',
        'secondary': '#6c757d',
        'secondary_hover': '#5a6268',

        'bg_dark': '#1e1e1e',
        'bg_medium': '#2a2a2a',
        'bg_light': '#353535',
        'bg_input': '#2d2d34',
        'bg_panel': '#23232a',
        'bg_header': '#19191e',

        'text_normal': '#f0f0f0',
        'text_muted': '#888888',
        'text_disabled': '#a0a0a0',
        'text_dark': '#282828',

        'border': '#444444',
        'border_light': '#555555',

        'error': '#e74c3c',
        'error_bg': '#332200',
        'copy_success': '#2e7d32',
    }

    @classmethod
    def apply_global_palette(cls, app):
        palette = QPalette()

        palette.setColor(QPalette.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.Base, QColor(20, 20, 20))
        palette.setColor(QPalette.AlternateBase, QColor(40, 40, 40))

        palette.setColor(QPalette.ToolTipBase, QColor(50, 50, 50))
        palette.setColor(QPalette.ToolTipText, Qt.GlobalColor.white)

        palette.setColor(QPalette.Text, Qt.GlobalColor.white)
        palette.setColor(QPalette.Disabled, QPalette.Text, QColor(160, 160, 160))

        palette.setColor(QPalette.Button, QColor(50, 50, 50))
        palette.setColor(QPalette.ButtonText, Qt.GlobalColor.white)
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(160, 160, 160))

        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.GlobalColor.black)
        palette.setColor(QPalette.BrightText, Qt.GlobalColor.red)

        palette.setColor(QPalette.Link, QColor(42, 130, 218))

        app.setPalette(palette)

    @classmethod
    def get_button_style(cls, button_type='primary'):
        base_style = """
            QPushButton {
                font-weight: bold;
                border-radius: 5px;
                padding: 8px 16px;
                min-height: 20px;
            }
        """

        button_styles = {
            'primary': f"""
                QPushButton {{
                    background-color: {cls.COLORS['primary']};
                    color: white;
                }}
                QPushButton:hover {{
                    background-color: {cls.COLORS['primary_hover']};
                }}
                QPushButton:pressed {{
                    background-color: {cls.COLORS['primary']};
                }}
                QPushButton:disabled {{
                    background-color: {cls.COLORS['secondary']};
                    color: {cls.COLORS['text_disabled']};
                }}
            """,
            'success': f"""
                QPushButton {{
                    background-color: {cls.COLORS['success']};
                    color: white;
                }}
                QPushButton:hover {{ background-color: {cls.COLORS['success_hover']}; }}
                QPushButton:pressed {{ background-color: {cls.COLORS['success']}; }}
                QPushButton:disabled {{
                    background-color: {cls.COLORS['secondary']};
                    color: {cls.COLORS['text_disabled']};
                }}
            """,
            'warning': f"""
                QPushButton {{
                    background-color: {cls.COLORS['warning']};
                    color: white;
                }}
                QPushButton:hover {{ background-color: {cls.COLORS['warning_hover']}; }}
                QPushButton:pressed {{ background-color: {cls.COLORS['warning']}; }}
                QPushButton:disabled {{
                    background-color: {cls.COLORS['secondary']};
                    color: {cls.COLORS['text_disabled']};
                }}
            """,
            'danger': f"""
                QPushButton {{
                    background-color: {cls.COLORS['danger']};
                    color: white;
                }}
                QPushButton:hover {{ background-color: {cls.COLORS['danger_hover']}; }}
                QPushButton:pressed {{ background-color: {cls.COLORS['danger']}; }}
                QPushButton:disabled {{
                    background-color: {cls.COLORS['secondary']};
                    color: {cls.COLORS['text_disabled']};
                }}
            """,
            'info': f"""
                QPushButton {{
                    background-color: {cls.COLORS['info']};
                    color: white;
                }}
                QPushButton:hover {{ background-color: {cls.COLORS['info_hover']}; }}
                QPushButton:pressed {{ background-color: {cls.COLORS['info']}; }}
                QPushButton:disabled {{
                    background-color: {cls.COLORS['secondary']};
                    color: {cls.COLORS['text_disabled']};
                }}
            """,
            'secondary': f"""
                QPushButton {{
                    background-color: {cls.COLORS['secondary']};
                    color: white;
                }}
                QPushButton:hover {{ background-color: {cls.COLORS['secondary_hover']}; }}
                QPushButton:pressed {{ background-color: {cls.COLORS['secondary']}; }}
                QPushButton:disabled {{
                    background-color: {cls.COLORS['secondary']};
                    color: {cls.COLORS['text_disabled']};
                }}
            """,
        }

        style = button_styles.get(button_type, button_styles['primary'])
        return base_style + style

    @classmethod
    def get_input_style(cls):
        return f"""
            QLineEdit, QTextEdit {{
                background-color: {cls.COLORS['bg_input']};
                color: {cls.COLORS['text_normal']};
                border: 1px solid {cls.COLORS['border']};
                border-radius: 4px;
                padding: 5px;
            }}
            QLineEdit:focus, QTextEdit:focus {{
                border-color: {cls.COLORS['primary']};
            }}
            QLineEdit:disabled, QTextEdit:disabled {{
                background-color: {cls.COLORS['bg_light']};
                color: {cls.COLORS['text_disabled']};
            }}
            QLineEdit::placeholder, QTextEdit::placeholder {{
                color: {cls.COLORS['text_muted']};
            }}
        """

    @classmethod
    def get_groupbox_style(cls):
        return f"""
            QGroupBox {{
                font-weight: bold;
                border: 1px solid {cls.COLORS['border']};
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: {cls.COLORS['primary']};
            }}
            QGroupBox:disabled {{
                color: {cls.COLORS['text_disabled']};
            }}
        """

    @classmethod
    def get_table_style(cls):
        return f"""
            QTableWidget {{
                background-color: {cls.COLORS['bg_medium']};
                gridline-color: {cls.COLORS['border']};
            }}
            QHeaderView::section {{
                background-color: {cls.COLORS['bg_light']};
                padding: 8px;
                border: 1px solid {cls.COLORS['border']};
                font-weight: bold;
            }}
            QTableWidget::item:selected {{
                background-color: {cls.COLORS['primary']};
                color: black;
            }}
        """

    @classmethod
    def get_scroll_area_style(cls):
        return f"""
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
            QScrollBar:vertical {{
                background-color: {cls.COLORS['bg_light']};
                width: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {cls.COLORS['primary']};
                border-radius: 6px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {cls.COLORS['primary_hover']};
            }}
        """

    @classmethod
    def get_label_style(cls, label_type='normal'):
        styles = {
            'normal': f"color: {cls.COLORS['text_normal']};",
            'muted': f"color: {cls.COLORS['text_muted']};",
            'error': f"color: {cls.COLORS['error']};",
            'warning': f"color: {cls.COLORS['warning']};",
            'success': f"color: {cls.COLORS['success']};",
            'title': f"color: {cls.COLORS['primary']}; font-size: 14px; font-weight: bold;",
        }
        return styles.get(label_type, styles['normal'])
