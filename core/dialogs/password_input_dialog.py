# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
from PyQt5.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QLineEdit,
    QDialog,
    QSpinBox,
    QHBoxLayout,
    QGroupBox
)
from PyQt5.QtCore import Qt

from core.models.styles.password_input_dialog_styles import PasswordInputDialogStyles


class PasswordInputDialog(QDialog):
    def __init__(self, parent=None, sound_manager=None):
        super().__init__(parent)
        self.setWindowTitle('Create Smart Password')
        self.setMinimumWidth(400)

        self.styles = PasswordInputDialogStyles()

        self.sound_manager = sound_manager

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)

        description_group = QGroupBox("Password Description")
        description_layout = QVBoxLayout()
        self.description_label = QLabel('Password Description (e.g., "GitHub Account"):')
        description_layout.addWidget(self.description_label)

        self.description_input = QLineEdit(self)
        self.description_input.setPlaceholderText("Enter password description (max 255 chars)")
        self.description_input.textChanged.connect(self.check_inputs)
        description_layout.addWidget(self.description_input)

        self.description_warning = QLabel("")
        self.description_warning.setStyleSheet("color: #ff9800; font-size: 11px;")
        description_layout.addWidget(self.description_warning)

        description_group.setLayout(description_layout)
        self.layout.addWidget(description_group)

        secret_group = QGroupBox("Secret Phrase")
        secret_layout = QVBoxLayout()
        self.secret_label = QLabel('Your Secret Phrase (minimum 12 characters):')
        secret_layout.addWidget(self.secret_label)

        self.secret_example_label = QLabel('Example: "MyCat🐱Hippo2026" or "P@ssw0rd!LongSecret"')
        self.secret_example_label.setStyleSheet(self.styles.secret_example_label_style)
        secret_layout.addWidget(self.secret_example_label)

        self.secret_input = QLineEdit(self)
        self.secret_input.setPlaceholderText("Enter your secret phrase (min. 12 characters)")
        self.secret_input.setEchoMode(QLineEdit.Password)
        self.secret_input.textChanged.connect(self.check_inputs)
        secret_layout.addWidget(self.secret_input)

        self.show_secret_checkbox = QPushButton("👁 Show")
        self.show_secret_checkbox.setCheckable(True)
        self.show_secret_checkbox.setMaximumWidth(100)
        self.show_secret_checkbox.clicked.connect(self.sound_manager.play_click)
        self.show_secret_checkbox.clicked.connect(self.toggle_secret_visibility)
        secret_layout.addWidget(self.show_secret_checkbox, alignment=Qt.AlignmentFlag.AlignCenter)

        self.secret_warning_label = QLabel("⚠️ Secret phrase must be at least 12 characters")
        self.secret_warning_label.setStyleSheet(self.styles.secret_warning_label_style)
        self.secret_warning_label.setVisible(False)
        secret_layout.addWidget(self.secret_warning_label)

        secret_group.setLayout(secret_layout)
        self.layout.addWidget(secret_group)

        settings_group = QGroupBox("Password Settings")
        settings_layout = QHBoxLayout()
        self.length_label = QLabel('Password Length (minimum 12):')
        settings_layout.addWidget(self.length_label)
        self.length_input = QSpinBox(self)
        self.length_input.setMinimum(12)
        self.length_input.setMaximum(100)
        self.length_input.setValue(16)
        self.length_input.setSuffix(" characters")
        settings_layout.addWidget(self.length_input)
        settings_layout.addStretch()
        settings_group.setLayout(settings_layout)
        self.layout.addWidget(settings_group)

        button_layout = QHBoxLayout()
        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.sound_manager.play_click)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        self.submit_button = QPushButton('Create Password', self)
        self.submit_button.setDefault(True)
        self.submit_button.clicked.connect(self.sound_manager.play_click)
        self.submit_button.clicked.connect(self.accept)
        self.submit_button.setStyleSheet(self.styles.submit_button_style)
        button_layout.addWidget(self.submit_button)
        self.layout.addLayout(button_layout)

        self.submit_button.setEnabled(False)
        self.description_input.textChanged.connect(self.check_inputs)

    def toggle_secret_visibility(self):
        if self.show_secret_checkbox.isChecked():
            self.secret_input.setEchoMode(QLineEdit.Normal)
            self.show_secret_checkbox.setText("🙈 Hide")
        else:
            self.secret_input.setEchoMode(QLineEdit.Password)
            self.show_secret_checkbox.setText("👁 Show")

    def validate_description(self, text):
        forbidden_chars = ['"', '\\']

        for char in forbidden_chars:
            if char in text:
                self.description_warning.setText(f"⚠️ Symbol '{char}' is not allowed in description")
                return False

        if len(text) > 255:
            self.description_warning.setText("⚠️ Description must be 255 characters or less")
            return False

        if not text.strip():
            self.description_warning.setText("⚠️ Description cannot be empty")
            return False

        self.description_warning.setText("")
        return True

    def check_inputs(self):
        description = self.description_input.text()
        secret = self.secret_input.text()

        description_valid = self.validate_description(description)

        secret_valid = len(secret) >= 12
        self.secret_warning_label.setVisible(not secret_valid and len(secret) > 0)

        self.submit_button.setEnabled(secret_valid and description_valid)

    def get_inputs(self):
        description = self.description_input.text().strip()
        secret = self.secret_input.text()
        length = self.length_input.value()

        if not description:
            return None, None, None

        if not self.validate_description(description):
            return None, None, None

        if len(secret) < 12:
            return None, None, None

        return description, secret, length
