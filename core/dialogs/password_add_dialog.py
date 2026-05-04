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


class AddPasswordDialog(QDialog):
    def __init__(self, parent=None, sound_manager=None):
        super().__init__(parent)
        self.setWindowTitle('Create Smart Password')
        self.setMinimumWidth(400)

        self.styles = PasswordInputDialogStyles()
        self.sound_manager = sound_manager
        self.max_length = 255

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)

        description_group = QGroupBox("Password Description")
        description_layout = QVBoxLayout()
        self.description_label = QLabel('Password Description (e.g., "GitHub Account"):')
        description_layout.addWidget(self.description_label)

        self.description_input = QLineEdit(self)
        self.description_input.setPlaceholderText(f"Enter password description (max {self.max_length} chars)")
        self.description_input.textChanged.connect(self.on_description_changed)
        description_layout.addWidget(self.description_input)

        self.counter_label = QLabel("")
        self.counter_label.setStyleSheet("font-size: 10px; padding: 2px;")
        self.counter_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        description_layout.addWidget(self.counter_label)

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
        self.update_counter()

    def on_description_changed(self):
        text = self.description_input.text()

        if len(text) > self.max_length:
            self.description_input.setText(text[:self.max_length])
            cursor_pos = self.description_input.cursorPosition()
            self.description_input.setCursorPosition(cursor_pos - 1 if cursor_pos > 0 else 0)
            return

        self.update_counter()
        self.check_inputs()

    def update_counter(self):
        current = len(self.description_input.text())
        remaining = self.max_length - current

        if remaining < 0:
            self.counter_label.setText(f"🔴 {current}/{self.max_length} EXCEEDED!")
            self.counter_label.setStyleSheet("color: #dc3545; font-size: 10px; font-weight: bold;")
        elif remaining <= 10:
            self.counter_label.setText(f"⚠️ {current}/{self.max_length} - {remaining} chars left")
            self.counter_label.setStyleSheet("color: #ff9800; font-size: 10px; font-weight: bold;")
        elif remaining <= 30:
            self.counter_label.setText(f"📝 {current}/{self.max_length} - {remaining} chars left")
            self.counter_label.setStyleSheet("color: #ffc107; font-size: 10px;")
        else:
            self.counter_label.setText(f"📝 {current}/{self.max_length}")
            self.counter_label.setStyleSheet("color: #6c757d; font-size: 10px;")

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

        if len(text) > self.max_length:
            self.description_warning.setText(f"⚠️ Description must be {self.max_length} characters or less")
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
