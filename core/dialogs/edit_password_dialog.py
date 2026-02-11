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


class EditPasswordDialog(QDialog):
    def __init__(self, parent=None, current_description="", current_length=16, sound_manager=None):
        super().__init__(parent)
        self.current_length = current_length
        self.setWindowTitle('Edit Password Metadata')
        self.setMinimumWidth(400)

        self.sound_manager = sound_manager

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)

        instruction = QLabel('Edit password metadata:')
        self.layout.addWidget(instruction)

        description_group = QGroupBox("Password Description")
        description_layout = QVBoxLayout()
        self.description_input = QLineEdit(self)
        self.description_input.setText(current_description)
        self.description_input.setPlaceholderText("Enter new password description")
        description_layout.addWidget(self.description_input)
        description_group.setLayout(description_layout)
        self.layout.addWidget(description_group)

        length_group = QGroupBox("Password Length")
        length_layout = QHBoxLayout()
        self.length_label = QLabel('Length:')
        length_layout.addWidget(self.length_label)

        self.length_input = QSpinBox(self)
        self.length_input.setMinimum(4)
        self.length_input.setMaximum(100)
        self.length_input.setValue(current_length)
        self.length_input.setSuffix(" characters")
        self.length_input.valueChanged.connect(self.on_length_changed)
        length_layout.addWidget(self.length_input)

        self.length_warning = QLabel("")
        self.length_warning.setStyleSheet("color: #ff9800; font-style: italic;")
        length_layout.addWidget(self.length_warning)

        length_layout.addStretch()
        length_group.setLayout(length_layout)
        self.layout.addWidget(length_group)

        note = QLabel(
            "<i>Note: Changing the length will generate a different password "
            "(first characters remain the same).</i>"
        )
        note.setWordWrap(True)
        note.setStyleSheet("color: #888;")
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
        self.submit_button.setStyleSheet("background-color: #ff9800; color: white;")
        button_layout.addWidget(self.submit_button)
        self.layout.addLayout(button_layout)

        self.on_length_changed(current_length)

    def on_length_changed(self, new_length):
        if new_length != self.current_length:
            if new_length > self.current_length:
                self.length_warning.setText(f"⚠️ Password will be extended")
            else:
                self.length_warning.setText(f"⚠️ Password will be shortened")
        else:
            self.length_warning.setText("")

    def get_values(self):
        return self.description_input.text().strip(), self.length_input.value()
