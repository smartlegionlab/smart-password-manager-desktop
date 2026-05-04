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

from core.models.styles.edit_password_dialog_styles import EditPasswordDialogStyles


class EditPasswordDialog(QDialog):
    def __init__(self, parent=None, current_description="", current_length=16, sound_manager=None):
        super().__init__(parent)
        self.current_length = current_length
        self.setWindowTitle('Edit Password Metadata')
        self.setMinimumWidth(400)
        self.styles = EditPasswordDialogStyles()
        self.sound_manager = sound_manager

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)

        instruction = QLabel('Edit password metadata:')
        self.layout.addWidget(instruction)

        description_group = QGroupBox("Password Description")
        description_layout = QVBoxLayout()
        self.description_input = QLineEdit(self)
        self.description_input.setText(current_description)
        self.description_input.setPlaceholderText("Enter new password description (max 255 chars)")
        self.description_input.textChanged.connect(self.check_inputs)
        description_layout.addWidget(self.description_input)

        self.description_warning = QLabel("")
        self.description_warning.setStyleSheet("color: #ff9800; font-size: 11px;")
        description_layout.addWidget(self.description_warning)

        description_group.setLayout(description_layout)
        self.layout.addWidget(description_group)

        length_group = QGroupBox("Password Length")
        length_layout = QHBoxLayout()
        self.length_label = QLabel('Length:')
        length_layout.addWidget(self.length_label)

        self.length_input = QSpinBox(self)
        self.length_input.setMinimum(12)
        self.length_input.setMaximum(100)
        self.length_input.setValue(current_length)
        self.length_input.setSuffix(" characters")
        self.length_input.valueChanged.connect(self.on_length_changed)
        length_layout.addWidget(self.length_input)

        self.length_warning = QLabel("")
        self.length_warning.setStyleSheet(self.styles.length_warning_style)
        length_layout.addWidget(self.length_warning)

        length_layout.addStretch()
        length_group.setLayout(length_layout)
        self.layout.addWidget(length_group)

        note = QLabel(
            "<i>Note: Changing the length will generate a different password "
            "(first characters remain the same).</i>"
        )
        note.setWordWrap(True)
        note.setStyleSheet(self.styles.note_style)
        self.layout.addWidget(note)

        button_layout = QHBoxLayout()
        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.sound_manager.play_click)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        self.submit_button = QPushButton('Update', self)
        self.submit_button.setDefault(True)
        self.submit_button.clicked.connect(self.sound_manager.play_click)
        self.submit_button.clicked.connect(self.accept)
        self.submit_button.setStyleSheet(self.styles.submit_button_style)
        button_layout.addWidget(self.submit_button)
        self.layout.addLayout(button_layout)

        self.submit_button.setEnabled(True)
        self.on_length_changed(current_length)

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
        is_valid = self.validate_description(description)
        self.submit_button.setEnabled(is_valid)

    def on_length_changed(self, new_length):
        if new_length != self.current_length:
            if new_length > self.current_length:
                self.length_warning.setText(f"⚠️ Password will be extended")
            else:
                self.length_warning.setText(f"⚠️ Password will be shortened")
        else:
            self.length_warning.setText("")

    def get_values(self):
        description = self.description_input.text().strip()

        if not self.validate_description(description):
            return None, None

        return description, self.length_input.value()
