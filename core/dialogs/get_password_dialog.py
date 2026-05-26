# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
from PyQt5.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QLineEdit,
    QTextEdit,
    QDialog,
    QHBoxLayout,
    QGroupBox
)
from PyQt5.QtCore import Qt

from core.models.styles.secret_input_dialog_styles import SecretInputDialogStyles


class GetPasswordDialog(QDialog):
    def __init__(self, parent=None, description="", sound_manager=None):
        super().__init__(parent)
        self.setWindowTitle(f'Get Smart Password')
        self.setMinimumWidth(450)
        self.setMaximumWidth(550)

        self.styles = SecretInputDialogStyles()
        self.sound_manager = sound_manager
        self.description = description

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)

        header = QLabel(f'<h3>Enter Secret Phrase</h3>')
        header.setWordWrap(True)
        header.setTextFormat(Qt.TextFormat.RichText)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(header)

        desc_group = QGroupBox("Description")
        desc_layout = QVBoxLayout()

        self.description_text = QTextEdit()
        self.description_text.setPlainText(description)
        self.description_text.setReadOnly(True)
        self.description_text.setMaximumHeight(40)
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

        secret_group = QGroupBox("Secret Phrase")
        secret_layout = QVBoxLayout()

        self.secret_input = QLineEdit(self)
        self.secret_input.setPlaceholderText("Enter your secret phrase")
        self.secret_input.setEchoMode(QLineEdit.Password)
        secret_layout.addWidget(self.secret_input)

        self.show_secret_checkbox = QPushButton("👁 Show")
        self.show_secret_checkbox.setCheckable(True)
        self.show_secret_checkbox.setMaximumWidth(100)
        self.show_secret_checkbox.clicked.connect(self.sound_manager.play_click)
        self.show_secret_checkbox.clicked.connect(self.toggle_secret_visibility)
        secret_layout.addWidget(self.show_secret_checkbox, alignment=Qt.AlignmentFlag.AlignCenter)

        secret_group.setLayout(secret_layout)
        self.layout.addWidget(secret_group)

        note = QLabel(
            "<i>Your secret phrase is never stored. "
            "The same secret phrase always generates the same password.</i>"
        )
        note.setWordWrap(True)
        note.setStyleSheet("color: #6c757d; font-size: 10px;")
        self.layout.addWidget(note)

        button_layout = QHBoxLayout()

        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.sound_manager.play_click)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        self.submit_button = QPushButton('Generate Password', self)
        self.submit_button.setDefault(True)
        self.submit_button.clicked.connect(self.sound_manager.play_click)
        self.submit_button.clicked.connect(self.accept)
        self.submit_button.setStyleSheet(self.styles.submit_button_style)
        button_layout.addWidget(self.submit_button)

        self.layout.addLayout(button_layout)

    def toggle_secret_visibility(self):
        if self.show_secret_checkbox.isChecked():
            self.secret_input.setEchoMode(QLineEdit.Normal)
            self.show_secret_checkbox.setText("🙈 Hide")
        else:
            self.secret_input.setEchoMode(QLineEdit.Password)
            self.show_secret_checkbox.setText("👁 Show")

    def get_secret(self):
        return self.secret_input.text()

    def showEvent(self, event):
        self.secret_input.setFocus()
        super().showEvent(event)
