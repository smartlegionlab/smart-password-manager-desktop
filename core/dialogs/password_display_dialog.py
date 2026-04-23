# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QLineEdit,
    QDialog,
    QHBoxLayout,
    QGroupBox
)
from PyQt5.QtCore import Qt

from core.models.styles import PasswordDisplayDialogStyles


class PasswordDisplayDialog(QDialog):
    def __init__(self, parent=None, description="", password="", sound_manager=None):
        super().__init__(parent)
        self.setWindowTitle(f'Password for "{description}"')
        self.setMinimumWidth(400)

        self.styles = PasswordDisplayDialogStyles()

        self.sound_manager = sound_manager

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)

        self.sound_manager.play_notify()

        header = QLabel(f'<h3>{description}</h3>')
        header.setWordWrap(True)
        header.setTextFormat(Qt.TextFormat.RichText)
        self.layout.addWidget(header)

        password_group = QGroupBox("Generated Password")
        password_layout = QVBoxLayout()

        self.password_display = QLineEdit()
        self.password_display.setText(password)
        self.password_display.setReadOnly(True)
        self.password_display.setStyleSheet(self.styles.password_display_style)
        password_layout.addWidget(self.password_display)

        copy_layout = QHBoxLayout()
        copy_layout.addStretch()
        self.copy_button = QPushButton("📋 Copy to Clipboard")
        self.copy_button.clicked.connect(self.sound_manager.play_click)
        self.copy_button.clicked.connect(self.copy_password)
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
        self.layout.addWidget(self.close_button)

    def copy_password(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.password_display.text())
        self.copy_button.setText("✅ Copied!")
        self.copy_button.setStyleSheet(self.styles.copy_button_style)

        main_window = self.parent()
        while main_window and not hasattr(main_window, 'show_status_message'):
            main_window = main_window.parent()
        if main_window:
            main_window.show_status_message('Password copied to clipboard', 2000)
