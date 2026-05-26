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

from core.models.styles.edit_password_dialog_styles import EditPasswordDialogStyles
from core.styles.theme_manager import ThemeManager


class EditPasswordDialog(QDialog):
    def __init__(self, parent=None, current_description="", current_length=16, sound_manager=None):
        super().__init__(parent)
        self.current_length = current_length
        self.max_length = 255
        self.setWindowTitle('Edit Password Metadata')
        self.setMinimumWidth(400)
        self.styles = EditPasswordDialogStyles()
        self.sound_manager = sound_manager

        self.setStyleSheet(
            ThemeManager.get_input_style() +
            ThemeManager.get_groupbox_style()
        )

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)

        instruction = QLabel('Edit password metadata:')
        self.layout.addWidget(instruction)

        description_group = QGroupBox("Password Description")
        description_layout = QVBoxLayout()
        self.description_input = QLineEdit(self)
        self.description_input.setText(current_description)
        self.description_input.setPlaceholderText(f"Enter new password description (max {self.max_length} chars)")
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
        self.cancel_button.setStyleSheet(ThemeManager.get_button_style('secondary'))
        button_layout.addWidget(self.cancel_button)

        self.submit_button = QPushButton('Update', self)
        self.submit_button.setDefault(True)
        self.submit_button.clicked.connect(self.sound_manager.play_click)
        self.submit_button.clicked.connect(self.accept)
        self.submit_button.setStyleSheet(ThemeManager.get_button_style('warning'))
        button_layout.addWidget(self.submit_button)
        self.layout.addLayout(button_layout)

        self.update_counter()
        self.on_length_changed(current_length)

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
