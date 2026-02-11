# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
from PyQt5.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QLineEdit,
    QDialog,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt


class SecretInputDialog(QDialog):
    def __init__(self, parent=None, description="", sound_manager=None):
        super().__init__(parent)
        self.setWindowTitle(f'Enter Secret Phrase for "{description}"')
        self.setMinimumWidth(350)

        self.sound_manager = sound_manager

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)

        instruction = QLabel(f'Enter the secret phrase for:\n<b>{description}</b>')
        instruction.setWordWrap(True)
        instruction.setTextFormat(Qt.RichText)
        self.layout.addWidget(instruction)

        self.secret_input = QLineEdit(self)
        self.secret_input.setPlaceholderText("Enter your secret phrase")
        self.secret_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.secret_input)

        self.show_secret_checkbox = QPushButton("👁 Show")
        self.show_secret_checkbox.setCheckable(True)
        self.show_secret_checkbox.setMaximumWidth(100)
        self.show_secret_checkbox.clicked.connect(self.sound_manager.play_click)
        self.show_secret_checkbox.clicked.connect(self.toggle_secret_visibility)
        self.layout.addWidget(self.show_secret_checkbox, alignment=Qt.AlignRight)

        button_layout = QHBoxLayout()
        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.sound_manager.play_click)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        self.submit_button = QPushButton('Generate Password', self)
        self.submit_button.setDefault(True)
        self.submit_button.clicked.connect(self.sound_manager.play_click)
        self.submit_button.clicked.connect(self.accept)
        self.submit_button.setStyleSheet("background-color: #2a82da; color: white;")
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
