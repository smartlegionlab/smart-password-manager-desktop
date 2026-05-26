# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QTextEdit,
    QDialog,
    QHBoxLayout,
    QGroupBox
)
from PyQt5.QtCore import Qt

from core.models.styles.password_display_dialog_styles import PasswordDisplayDialogStyles


class PasswordDisplayDialog(QDialog):
    def __init__(self, parent=None, description="", password="", sound_manager=None):
        super().__init__(parent)
        self.setWindowTitle(f'Password for "{description}"')
        self.setMinimumWidth(450)
        self.setMaximumWidth(550)

        self.styles = PasswordDisplayDialogStyles()
        self.sound_manager = sound_manager

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)

        self.sound_manager.play_notify()

        header = QLabel(f'<h3>Password Generated</h3>')
        header.setWordWrap(True)
        header.setTextFormat(Qt.TextFormat.RichText)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(header)

        desc_group = QGroupBox("Description")
        desc_layout = QVBoxLayout()

        self.description_text = QTextEdit()
        self.description_text.setPlainText(description)
        self.description_text.setReadOnly(True)
        self.description_text.setMaximumHeight(60)
        self.description_text.setMinimumHeight(40)
        self.description_text.setStyleSheet("""
            QTextEdit {
                background-color: #2a2a2a;
                color: #f0f0f0;
                border: 1px solid #444;
                border-radius: 4px;
                font-family: monospace;
                font-size: 11px;
            }
        """)
        desc_layout.addWidget(self.description_text)
        desc_group.setLayout(desc_layout)
        self.layout.addWidget(desc_group)

        password_group = QGroupBox("Generated Password")
        password_layout = QVBoxLayout()

        self.password_display = QTextEdit()
        self.password_display.setPlainText(password)
        self.password_display.setReadOnly(True)
        self.password_display.setMaximumHeight(80)
        self.password_display.setMinimumHeight(60)
        self.password_display.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #4ec9b0;
                border: 1px solid #444;
                border-radius: 4px;
                font-family: monospace;
                font-size: 12px;
                font-weight: bold;
            }
        """)
        password_layout.addWidget(self.password_display)

        copy_layout = QHBoxLayout()
        copy_layout.addStretch()
        self.copy_button = QPushButton("📋 Copy to Clipboard")
        self.copy_button.clicked.connect(self.sound_manager.play_click)
        self.copy_button.clicked.connect(self.copy_password)
        self.copy_button.setMinimumWidth(150)
        copy_layout.addWidget(self.copy_button)
        password_layout.addLayout(copy_layout)

        password_group.setLayout(password_layout)
        self.layout.addWidget(password_group)

        note = QLabel(
            "<i>Note: This password is generated deterministically from your secret phrase. "
            "It's not stored anywhere - regenerate it when needed.</i>"
        )
        note.setWordWrap(True)
        note.setStyleSheet(self.styles.note_style)
        self.layout.addWidget(note)

        self.close_button = QPushButton('Close', self)
        self.close_button.setDefault(True)
        self.close_button.clicked.connect(self.sound_manager.play_click)
        self.close_button.clicked.connect(self.accept)
        self.close_button.setMinimumWidth(100)
        self.layout.addWidget(self.close_button, alignment=Qt.AlignmentFlag.AlignCenter)

    def copy_password(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.password_display.toPlainText())
        self.copy_button.setText("✅ Copied!")
        self.copy_button.setStyleSheet(self.styles.copy_button_style)

        main_window = self.parent()
        while main_window and not hasattr(main_window, 'show_status_message'):
            main_window = main_window.parent()
        if main_window:
            main_window.show_status_message('Password copied to clipboard', 2000)

        from threading import Timer
        Timer(1.5, lambda: self.copy_button.setText("📋 Copy to Clipboard")).start()
