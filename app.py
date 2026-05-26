# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont

from core.main_window import MainWindow
from core.styles.theme_manager import ThemeManager


def main():
    import sys

    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    ThemeManager.apply_global_palette(app)

    font = QFont("Segoe UI", 9)
    app.setFont(font)

    app.setStyleSheet(f"""
        QDialog {{
            background-color: {ThemeManager.COLORS['bg_dark']};
        }}
        QStatusBar {{
            color: {ThemeManager.COLORS['text_muted']};
        }}
        QMenuBar {{
            background-color: {ThemeManager.COLORS['bg_panel']};
            color: {ThemeManager.COLORS['text_normal']};
        }}
        QMenuBar::item:selected {{
            background-color: {ThemeManager.COLORS['primary']};
        }}
        QMenu {{
            background-color: {ThemeManager.COLORS['bg_light']};
            color: {ThemeManager.COLORS['text_normal']};
        }}
        QMenu::item:selected {{
            background-color: {ThemeManager.COLORS['primary']};
        }}
        QToolTip {{
            background-color: {ThemeManager.COLORS['bg_light']};
            color: {ThemeManager.COLORS['text_normal']};
            border: 1px solid {ThemeManager.COLORS['border']};
        }}

        QWidget:disabled {{
            color: {ThemeManager.COLORS['text_disabled']};
        }}

        QPushButton:disabled {{
            color: {ThemeManager.COLORS['text_disabled']};
        }}

        QLabel:disabled {{
            color: {ThemeManager.COLORS['text_disabled']};
        }}
    """)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()