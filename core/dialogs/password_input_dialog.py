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


class PasswordInputDialog(QDialog):
    def __init__(self, parent=None, sound_manager=None):
        super().__init__(parent)
        self.setWindowTitle('Create Smart Password')
        self.setMinimumWidth(400)

        self.sound_manager = sound_manager

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)

        description_group = QGroupBox("Password Description")
        description_layout = QVBoxLayout()
        self.description_label = QLabel('Password Description (e.g., "GitHub Account"):')
        description_layout.addWidget(self.description_label)
        self.description_input = QLineEdit(self)
        self.description_input.setPlaceholderText("Enter password description")
        description_layout.addWidget(self.description_input)
        description_group.setLayout(description_layout)
        self.layout.addWidget(description_group)

        secret_group = QGroupBox("Secret Phrase")
        secret_layout = QVBoxLayout()
        self.secret_label = QLabel('Your Secret Phrase:')
        secret_layout.addWidget(self.secret_label)
        self.secret_input = QLineEdit(self)
        self.secret_input.setPlaceholderText("Enter your secret phrase")
        self.secret_input.setEchoMode(QLineEdit.Password)
        secret_layout.addWidget(self.secret_input)

        self.show_secret_checkbox = QPushButton("👁 Show")
        self.show_secret_checkbox.setCheckable(True)
        self.show_secret_checkbox.setMaximumWidth(100)
        self.show_secret_checkbox.clicked.connect(self.sound_manager.play_click)
        self.show_secret_checkbox.clicked.connect(self.toggle_secret_visibility)
        secret_layout.addWidget(self.show_secret_checkbox, alignment=Qt.AlignRight)
        secret_group.setLayout(secret_layout)
        self.layout.addWidget(secret_group)

        settings_group = QGroupBox("Password Settings")
        settings_layout = QHBoxLayout()
        self.length_label = QLabel('Password Length:')
        settings_layout.addWidget(self.length_label)
        self.length_input = QSpinBox(self)
        self.length_input.setMinimum(4)
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

    def get_inputs(self):
        return self.description_input.text(), self.secret_input.text(), self.length_input.value()
