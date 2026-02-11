# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
from PyQt5.QtWidgets import (
    QApplication, QDesktopWidget,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
    QLineEdit,
    QDialog,
    QTableWidget,
    QTableWidgetItem,
    QSpinBox,
    QFrame,
    QHeaderView,
    QHBoxLayout,
    QGroupBox, QAction, QMenuBar, QStatusBar, QMainWindow
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QSound
from smartpasslib import SmartPasswordManager, SmartPassword, SmartPasswordMaster

from core.config import Config
from core.sound_manager import SoundManager


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


class PasswordDisplayDialog(QDialog):
    def __init__(self, parent=None, description="", password="", sound_manager=None):
        super().__init__(parent)
        self.setWindowTitle(f'Password for "{description}"')
        self.setMinimumWidth(400)

        self.sound_manager = sound_manager

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)

        self.sound_manager.play_notify()

        header = QLabel(f'<h3>{description}</h3>')
        header.setWordWrap(True)
        header.setTextFormat(Qt.RichText)
        self.layout.addWidget(header)

        password_group = QGroupBox("Generated Password")
        password_layout = QVBoxLayout()

        self.password_display = QLineEdit()
        self.password_display.setText(password)
        self.password_display.setReadOnly(True)
        self.password_display.setStyleSheet("""
            QLineEdit {
                font-family: monospace;
                font-size: 14px;
                padding: 8px;
                background-color: #2a2a2a;
                border: 1px solid #444;
                border-radius: 4px;
            }
        """)
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
        note.setStyleSheet("color: #888;")
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
        self.copy_button.setStyleSheet("background-color: #2e7d32; color: white;")


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = Config()
        self.smart_pass_man = SmartPasswordManager()
        self.setWindowTitle(f'{self.config.description}')
        self.resize(900, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.click_sound = QSound("data/sounds/click.wav")

        self.about_sound = QSound("data/sounds/about.wav")

        self.notify_sound = QSound("data/sounds/notify.wav")

        self.error_sound = QSound("data/sounds/error.wav")

        self.sound_manager = SoundManager()

        self.sound_manager.register_sound('click', self.click_sound)
        self.sound_manager.register_sound('about', self.about_sound)
        self.sound_manager.register_sound('notify', self.notify_sound)
        self.sound_manager.register_sound('error', self.error_sound)

        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setSpacing(15)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        self.menu_bar = QMenuBar()
        self.main_layout.setMenuBar(self.menu_bar)

        self.setup_menu_bar()

        header_layout = QHBoxLayout()
        self.label_logo = QLabel(f"{self.config.title} <sup>{self.config.version}</sup>")
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.label_logo.setFont(font)
        self.label_logo.setStyleSheet("color: #2a82da;")
        header_layout.addWidget(self.label_logo)

        header_layout.addStretch()

        self.count_label = QLabel("0 passwords")
        self.count_label.setStyleSheet("color: #888;")
        header_layout.addWidget(self.count_label)

        self.main_layout.addLayout(header_layout)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(['Description', 'Length', 'Get', 'Edit', 'Delete'])
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.setStyleSheet("""
            QTableWidget {
                background-color: #2a2a2a;
                gridline-color: #444;
            }
            QHeaderView::section {
                background-color: #353535;
                padding: 8px;
                border: 1px solid #444;
                font-weight: bold;
            }
        """)

        self.table_widget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table_widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table_widget.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table_widget.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table_widget.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)

        self.main_layout.addWidget(self.table_widget)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.btn_new_password = QPushButton(self.config.btn_new_pass_title)
        self.btn_new_password.setMinimumHeight(40)
        self.btn_new_password.clicked.connect(self.sound_manager.play_click)
        self.btn_new_password.clicked.connect(self.add_password)
        self.btn_new_password.setStyleSheet("""
            QPushButton {
                background-color: #2a82da;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #1a72ca;
            }
        """)
        button_layout.addWidget(self.btn_new_password)

        button_layout.addStretch()

        self.btn_help = QPushButton('? ' + self.config.btn_help_title)
        self.btn_help.setMinimumHeight(40)
        self.btn_help.clicked.connect(self.sound_manager.play_click)
        self.btn_help.clicked.connect(self.show_help)
        button_layout.addWidget(self.btn_help)

        self.btn_about = QPushButton(self.config.btn_about_title)
        self.btn_about.setMinimumHeight(40)
        self.btn_about.clicked.connect(self.sound_manager.play_click)
        self.btn_about.clicked.connect(self.show_about)
        button_layout.addWidget(self.btn_about)

        self.btn_exit = QPushButton(self.config.btn_exit_title)
        self.btn_exit.setMinimumHeight(40)
        self.btn_exit.clicked.connect(self.close)
        self.btn_exit.setStyleSheet("""
            QPushButton {
                background-color: #ff7d7d;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #ca1a1a;
            }
        """)
        button_layout.addWidget(self.btn_exit)

        self.main_layout.addLayout(button_layout)

        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setStyleSheet("color: #444;")
        self.main_layout.addWidget(self.line)

        footer_layout = QVBoxLayout()
        footer_layout.setSpacing(5)

        self.setup_status_bar()

        copyright_text = 'Copyright © 2026, <a href="https://github.com/smartlegionlab" style="color: #2a82da; text-decoration: none;">Alexander Suvorov</a>. All rights reserved.'
        self.copyright_label = QLabel(copyright_text)
        self.copyright_label.setAlignment(Qt.AlignCenter)
        self.copyright_label.setStyleSheet("color: #888; font-size: 16px;")
        self.copyright_label.setOpenExternalLinks(True)
        footer_layout.addWidget(self.copyright_label)

        self.main_layout.addLayout(footer_layout)

        self._init()
        self.center_window()

    def setup_menu_bar(self):

        file_menu = self.menu_bar.addMenu('File')

        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        passwords_menu = self.menu_bar.addMenu('Passwords')

        create_pass_action = QAction('Create new password', self)
        create_pass_action.setShortcut('Ctrl+P')
        create_pass_action.triggered.connect(self.sound_manager.play_click)
        create_pass_action.triggered.connect(self.add_password)
        passwords_menu.addAction(create_pass_action)

        sounds_menu = self.menu_bar.addMenu('Sounds')

        sound_action = QAction('Enable Sounds', self)
        sound_action.setCheckable(True)
        sound_action.setChecked(False)
        sound_action.setShortcut('Ctrl+Shift+S')
        sound_action.triggered.connect(self.toggle_sounds)
        sounds_menu.addAction(sound_action)

        self.sound_manager.sound_enabled_changed.connect(
            sound_action.setChecked
        )

        help_menu = self.menu_bar.addMenu('Help')

        about_action = QAction('About', self)
        about_action.triggered.connect(self.sound_manager.play_click)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        help_action = QAction('Help', self)
        help_action.setShortcut('F1')
        help_action.triggered.connect(self.sound_manager.play_click)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)

    def center_window(self):
        frame = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(center_point)
        self.move(frame.topLeft())

    def _init(self):
        self.table_widget.setRowCount(0)
        self.update_password_count()
        for password in self.smart_pass_man.passwords.values():
            self.add_item(password)

    def show_help(self):
        self.sound_manager.play_notify()
        help_text = f"""
        <h3>Smart Password Manager Help {self.config.version}</h3>

        <p><b>How it works:</b></p>
        <ul>
        <li>Each password is generated from your secret phrase</li>
        <li>No passwords are stored - regenerate when needed</li>
        <li>Same secret phrase always generates the same password</li>
        </ul>

        <p><b>Basic Steps:</b></p>
        <ol>
        <li>Click <b>Add</b> to create a new password entry</li>
        <li>Enter password description (e.g., "GitHub")</li>
        <li>Enter and remember your secret phrase</li>
        <li>Select password length (recommended: 16-24 characters)</li>
        <li>Click <b>Get</b> to generate password</li>
        <li>Click <b>Edit</b> to change description or length</li>
        <li>Click <b>Delete</b> to remove entry (doesn't delete password)</li>
        </ol>

        <p><b>Important Notes:</b></p>
        <ul>
        <li>🔐 Never share your secret phrases</li>
        <li>📝 Back up your .cases.json file</li>
        <li>⚙️ Secret phrases are case-sensitive</li>
        <li>✏️ You can edit password descriptions anytime</li>
        <li>📏 Changing password length generates a different password!</li>
        <li>⚠️ First N characters remain same, new characters are added/removed</li>
        <li>🗑️ Deleting entry only removes metadata - password can be recreated</li>
        </ul>

        <hr>
        <p><b>Links:</b></p>
        <p>
        📂 <a href="https://github.com/smartlegionlab/smart-password-manager-desktop" style="color: #2a82da;">GitHub Repository</a><br>
        🐛 <a href="https://github.com/smartlegionlab/smart-password-manager-desktop/issues" style="color: #2a82da;">Report Issues</a>
        </p>
        """

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle('Smart Password Manager Help')
        msg_box.setTextFormat(Qt.RichText)
        msg_box.setText(help_text)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def show_about(self):
        self.sound_manager.play_about()
        QMessageBox.about(
            self,
            "About Smart Password Manager",
            f"""<h2>Smart Password Manager {self.config.version}</h2>
            <p>Cross-platform desktop manager for deterministic smart passwords.</p>
            <p><b>Features:</b></p>
            <ul>
            <li>Eliminates password storage completely</li>
            <li>Verify secret knowledge without exposure</li>
            <li>See all your password metadata at a glance</li>
            <li>Update descriptions and lengths anytime</li>
            <li>Hidden secret phrase entry with show/hide toggle</li>
            <li>Quick password copying for account setup</li>
            <li>No web dependencies or internet required</li>
            </ul>
            <p><b>Copyright © 2026, <a href="https://github.com/smartlegionlab/">Alexander Suvorov</a>. All rights reserved.</b></p>
            """
        )

    def update_password_count(self):
        count = len(self.smart_pass_man.passwords)
        self.count_label.setText(f"{count} password{'s' if count != 1 else ''}")

    def add_item(self, smart_password):
        row_position = self.table_widget.rowCount()
        self.table_widget.insertRow(row_position)

        desc_item = QTableWidgetItem(smart_password.description)
        desc_item.setToolTip(smart_password.description)
        self.table_widget.setItem(row_position, 0, desc_item)

        length_item = QTableWidgetItem(f"{smart_password.length} chars")
        length_item.setTextAlignment(Qt.AlignCenter)
        self.table_widget.setItem(row_position, 1, length_item)

        get_button = QPushButton("Get")
        get_button.setToolTip("Get Smart Password")
        get_button.setStyleSheet("""
            QPushButton {
                background-color: #2a82da;
                color: white;
                border-radius: 3px;
                padding: 5px 10px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #1a72ca;
            }
        """)
        get_button.clicked.connect(self.sound_manager.play_click)
        get_button.clicked.connect(lambda checked, pk=smart_password.public_key:
                                   self.get_password(pk))
        get_button.public_key = smart_password.public_key
        self.table_widget.setCellWidget(row_position, 2, get_button)

        edit_button = QPushButton("Edit")
        edit_button.setToolTip("Edit password description and length")
        edit_button.setStyleSheet("""
            QPushButton {
                background-color: #ff9800;
                color: white;
                border-radius: 3px;
                padding: 5px 10px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #e68900;
            }
        """)
        edit_button.clicked.connect(self.sound_manager.play_click)
        edit_button.clicked.connect(lambda checked, pk=smart_password.public_key:
                                    self.edit_password(pk))
        edit_button.public_key = smart_password.public_key
        self.table_widget.setCellWidget(row_position, 3, edit_button)

        delete_button = QPushButton("Delete")
        delete_button.setToolTip("Delete this password entry")
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: #da2a2a;
                color: white;
                border-radius: 3px;
                padding: 5px;
                min-width: 60px;
                max-width: 60px;
            }
            QPushButton:hover {
                background-color: #ca1a1a;
            }
        """)
        delete_button.clicked.connect(self.sound_manager.play_click)
        delete_button.clicked.connect(lambda checked, pk=smart_password.public_key:
                                      self.remove_password(pk))
        delete_button.public_key = smart_password.public_key
        self.table_widget.setCellWidget(row_position, 4, delete_button)

        self.update_password_count()

    def edit_password(self, public_key):
        self.sound_manager.play_notify()
        smart_password = self.smart_pass_man.get_smart_password(public_key)
        if not smart_password:
            QMessageBox.warning(self, 'Error', 'Password metadata not found.')
            return

        dialog = EditPasswordDialog(self, smart_password.description, smart_password.length, self.sound_manager)
        if dialog.exec_() == QDialog.Accepted:
            new_description, new_length = dialog.get_values()

            if not new_description:
                QMessageBox.warning(self, 'Missing Information', 'Please enter a password description.')
                return

            if new_description == smart_password.description and new_length == smart_password.length:
                QMessageBox.information(self, 'No Changes', 'No changes were made.')
                return

            if new_length != smart_password.length:
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle('⚠️ Password Length Change Warning')
                msg_box.setTextFormat(Qt.RichText)
                msg_box.setText(
                    f'Changing password length from {smart_password.length} to {new_length} characters:<br><br>'
                    f'• First {min(smart_password.length, new_length)} characters will remain the same<br>'
                    f'• You will get a {"longer" if new_length > smart_password.length else "shorter"} password<br>'
                    f'• Accounts using the old password may need to be updated<br><br>'
                    f'Are you sure you want to change the password length?'
                )
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                msg_box.setDefaultButton(QMessageBox.No)

                reply = msg_box.exec_()

                if reply == QMessageBox.No:
                    return

            try:
                success = self.smart_pass_man.update_smart_password(
                    public_key=public_key,
                    description=new_description,
                    length=new_length
                )

                if success:
                    row = self.find_row_by_public_key(public_key)
                    if row != -1:
                        desc_item = self.table_widget.item(row, 0)
                        if desc_item:
                            desc_item.setText(new_description)
                            desc_item.setToolTip(new_description)

                        length_item = self.table_widget.item(row, 1)
                        if length_item:
                            length_item.setText(f"{new_length} chars")

                    msg_box = QMessageBox(self)
                    msg_box.setWindowTitle('Updated')
                    msg_box.setTextFormat(Qt.RichText)

                    msg = f'✅ Successfully updated!'
                    if new_length != smart_password.length:
                        msg += f'<br><br>Password length changed from {smart_password.length} to {new_length} characters.'
                        msg += f'<br><br><i>Note: New password will have {"extended" if new_length > smart_password.length else "truncated"} characters.</i>'

                    msg_box.setText(msg)
                    msg_box.setIcon(QMessageBox.Information)
                    msg_box.setStandardButtons(QMessageBox.Ok)
                    msg_box.exec_()

            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to update:\n{str(e)}')

    def setup_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('Ready')

    def remove_password(self, public_key):
        self.sound_manager.play_notify()
        row = self.find_row_by_public_key(public_key)
        if row != -1:
            description = self.table_widget.item(row, 0).text()

            msg_box = QMessageBox(self)
            msg_box.setWindowTitle('Confirm Deletion')
            msg_box.setTextFormat(Qt.RichText)
            msg_box.setText(
                f'Delete password entry for:<br><b>{description}</b>?<br><br>'
                f'Note: This only deletes the metadata. You can recreate it '
                f'later using the same secret phrase.'
            )
            msg_box.setIcon(QMessageBox.Question)
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg_box.setDefaultButton(QMessageBox.No)

            reply = msg_box.exec_()

            if reply == QMessageBox.Yes:
                self.table_widget.removeRow(row)
                self.smart_pass_man.delete_smart_password(public_key)
                self.update_password_count()

                msg_box = QMessageBox(self)
                msg_box.setWindowTitle('Deleted')
                msg_box.setTextFormat(Qt.RichText)
                msg_box.setText(f'Password metadata for <b>{description}</b> has been deleted.')
                msg_box.setIcon(QMessageBox.Information)
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec_()

    def find_row_by_public_key(self, public_key):
        for row in range(self.table_widget.rowCount()):
            for col in [2, 3, 4]:
                widget = self.table_widget.cellWidget(row, col)
                if widget and hasattr(widget, 'public_key') and widget.public_key == public_key:
                    return row
        return -1

    def add_password(self):
        self.sound_manager.play_notify()
        dialog = PasswordInputDialog(self, self.sound_manager)
        if dialog.exec_() == QDialog.Accepted:
            description, secret, length = dialog.get_inputs()

            if not description or not secret:
                QMessageBox.warning(
                    self,
                    'Missing Information',
                    'Please provide both password description and secret phrase.'
                )
                return

            try:
                public_key = SmartPasswordMaster.generate_public_key(secret=secret)

                if public_key in self.smart_pass_man.passwords:
                    existing_password = self.smart_pass_man.passwords[public_key]
                    msg_box = QMessageBox(self)
                    msg_box.setWindowTitle('Duplicate Secret Phrase')
                    msg_box.setTextFormat(Qt.RichText)
                    msg_box.setText(
                        f'A password entry with this secret phrase already exists:<br><br>'
                        f'<b>"{existing_password.description}"</b><br>'
                        f'Length: {existing_password.length} characters<br><br>'
                        f'Each unique secret phrase generates a unique public key.<br>'
                        f'You cannot have multiple entries with the same secret.'
                    )
                    msg_box.setIcon(QMessageBox.Warning)
                    msg_box.setStandardButtons(QMessageBox.Ok)
                    msg_box.exec_()
                    return

                smart_password = SmartPassword(
                    public_key=public_key,
                    description=description,
                    length=length
                )

                password = SmartPasswordMaster.generate_smart_password(
                    secret=secret,
                    length=length
                )

                self.smart_pass_man.add_smart_password(smart_password)

                self.add_item(smart_password)

                display_dialog = PasswordDisplayDialog(self, description, password, self.sound_manager)
                display_dialog.exec_()

            except Exception as e:
                QMessageBox.critical(
                    self,
                    'Error',
                    f'Failed to create password:\n{str(e)}'
                )

    def get_password(self, public_key):
        self.sound_manager.play_notify()
        smart_password = self.smart_pass_man.get_smart_password(public_key)
        if not smart_password:
            QMessageBox.critical(
                self,
                'Error',
                'Password metadata not found. It may have been deleted.'
            )
            return

        description = smart_password.description
        dialog = SecretInputDialog(self, description, self.sound_manager)
        if dialog.exec_() == QDialog.Accepted:
            secret = dialog.get_secret()

            if not secret:
                QMessageBox.warning(
                    self,
                    'Missing Secret',
                    'Please enter your secret phrase.'
                )
                return

            try:
                is_valid = SmartPasswordMaster.check_public_key(
                    secret=secret,
                    public_key=public_key
                )

                if is_valid:
                    password = SmartPasswordMaster.generate_smart_password(
                        secret=secret,
                        length=smart_password.length
                    )

                    display_dialog = PasswordDisplayDialog(self, description, password, self.sound_manager)
                    display_dialog.exec_()

                else:
                    msg_box = QMessageBox(self)
                    msg_box.setWindowTitle('Invalid Secret')
                    msg_box.setTextFormat(Qt.RichText)
                    msg_box.setText(
                        'The secret phrase is incorrect. Please check:<br>'
                        '• Caps Lock<br>'
                        '• Keyboard layout<br>'
                        '• Spelling<br><br>'
                        f'Note: In {self.config.version}, secret phrases are case-sensitive.'
                    )
                    msg_box.setIcon(QMessageBox.Warning)
                    msg_box.setStandardButtons(QMessageBox.Ok)
                    msg_box.exec_()

            except Exception as e:
                QMessageBox.critical(
                    self,
                    'Error',
                    f'Failed to generate password:\n{str(e)}'
                )

    def toggle_sounds(self, enabled: bool):
        self.sound_manager.set_enabled(enabled)
        status = "enabled" if enabled else "disabled"
        self.status_bar.showMessage(f'Sounds {status}', 2000)

    def closeEvent(self, event):
        self.sound_manager.play_error()
        if len(self.smart_pass_man.passwords) > 0:
            reply = QMessageBox.question(
                self,
                'Exit',
                f'Are you sure you want to exit?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
