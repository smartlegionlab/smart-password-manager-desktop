# Copyright (©) 2025, Alexander Suvorov. All rights reserved.
import webbrowser

from PyQt5.QtWidgets import (
    QApplication,
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
    QGroupBox
)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt
from smartpasslib import SmartPasswordManager, SmartPassword, SmartPasswordMaster

from core.config import Config


class PasswordInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Create Smart Password')
        self.setMinimumWidth(400)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)

        description_group = QGroupBox("Service Information")
        description_layout = QVBoxLayout()
        self.description_label = QLabel('Service Description (e.g., "GitHub Account"):')
        description_layout.addWidget(self.description_label)
        self.description_input = QLineEdit(self)
        self.description_input.setPlaceholderText("Enter service name or description")
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
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        self.submit_button = QPushButton('Create Password', self)
        self.submit_button.setDefault(True)
        self.submit_button.clicked.connect(self.accept)
        self.submit_button.setStyleSheet("background-color: #2a82da; color: white;")
        button_layout.addWidget(self.submit_button)
        self.layout.addLayout(button_layout)

    def toggle_secret_visibility(self):
        if self.show_secret_checkbox.isChecked():
            self.secret_input.setEchoMode(QLineEdit.Normal)
            self.show_secret_checkbox.setText("👁 Hide")
        else:
            self.secret_input.setEchoMode(QLineEdit.Password)
            self.show_secret_checkbox.setText("👁 Show")

    def get_inputs(self):
        return self.description_input.text(), self.secret_input.text(), self.length_input.value()


class SecretInputDialog(QDialog):
    def __init__(self, parent=None, description=""):
        super().__init__(parent)
        self.setWindowTitle(f'Enter Secret Phrase for "{description}"')
        self.setMinimumWidth(350)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)

        instruction = QLabel(f'Enter the secret phrase for:\n<b>{description}</b>')
        instruction.setWordWrap(True)
        self.layout.addWidget(instruction)

        self.secret_input = QLineEdit(self)
        self.secret_input.setPlaceholderText("Enter your secret phrase")
        self.secret_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.secret_input)

        self.show_secret_checkbox = QPushButton("👁 Show")
        self.show_secret_checkbox.setCheckable(True)
        self.show_secret_checkbox.setMaximumWidth(100)
        self.show_secret_checkbox.clicked.connect(self.toggle_secret_visibility)
        self.layout.addWidget(self.show_secret_checkbox, alignment=Qt.AlignRight)

        button_layout = QHBoxLayout()
        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        self.submit_button = QPushButton('Generate Password', self)
        self.submit_button.setDefault(True)
        self.submit_button.clicked.connect(self.accept)
        self.submit_button.setStyleSheet("background-color: #2a82da; color: white;")
        button_layout.addWidget(self.submit_button)
        self.layout.addLayout(button_layout)

    def toggle_secret_visibility(self):
        if self.show_secret_checkbox.isChecked():
            self.secret_input.setEchoMode(QLineEdit.Normal)
            self.show_secret_checkbox.setText("👁 Hide")
        else:
            self.secret_input.setEchoMode(QLineEdit.Password)
            self.show_secret_checkbox.setText("👁 Show")

    def get_secret(self):
        return self.secret_input.text()


class PasswordDisplayDialog(QDialog):
    def __init__(self, parent=None, description="", password=""):
        super().__init__(parent)
        self.setWindowTitle(f'Password for "{description}"')
        self.setMinimumWidth(400)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)

        header = QLabel(f'<h3>{description}</h3>')
        header.setWordWrap(True)
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
        self.close_button.clicked.connect(self.accept)
        self.layout.addWidget(self.close_button)

    def copy_password(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.password_display.text())
        self.copy_button.setText("✅ Copied!")
        self.copy_button.setStyleSheet("background-color: #2e7d32; color: white;")


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = Config()
        self.smart_pass_man = SmartPasswordManager()
        self.setWindowTitle(f'{self.config.description}')
        self.resize(900, 700)

        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(15)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        header_layout = QHBoxLayout()
        self.label_logo = QLabel(f"{self.config.title} <sup>v2.0.0</sup>")
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
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(['Description', 'Length', 'Actions', ''])
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

        self.main_layout.addWidget(self.table_widget)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.btn_new_password = QPushButton('➕ ' + self.config.btn_new_pass_title)
        self.btn_new_password.setMinimumHeight(40)
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

        self.btn_help = QPushButton('❓ ' + self.config.btn_help_title)
        self.btn_help.setMinimumHeight(40)
        self.btn_help.clicked.connect(lambda: webbrowser.open(self.config.url))
        button_layout.addWidget(self.btn_help)

        self.btn_exit = QPushButton('🚪 ' + self.config.btn_exit_title)
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

        self.copyright_label = QLabel(self.config.copyright)
        self.copyright_label.setAlignment(Qt.AlignCenter)
        self.copyright_label.setStyleSheet("color: #888; font-size: 10px;")
        footer_layout.addWidget(self.copyright_label)

        self.main_layout.addLayout(footer_layout)

        self.setLayout(self.main_layout)
        self._init()

    def _init(self):
        self.table_widget.setRowCount(0)
        self.update_password_count()
        for password in self.smart_pass_man.passwords.values():
            self.add_item(password)

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

        get_button = QPushButton("🔑 Get Password")
        get_button.setStyleSheet("""
            QPushButton {
                background-color: #2a82da;
                color: white;
                border-radius: 3px;
                padding: 5px 10px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #1a72ca;
            }
        """)
        get_button.clicked.connect(lambda checked, pk=smart_password.public_key, desc=smart_password.description:
                                   self.get_password(pk, desc))
        self.table_widget.setCellWidget(row_position, 2, get_button)

        delete_button = QPushButton("🗑️")
        delete_button.setToolTip("Delete this password entry")
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: #da2a2a;
                color: white;
                border-radius: 3px;
                padding: 5px;
                min-width: 30px;
                max-width: 30px;
            }
            QPushButton:hover {
                background-color: #ca1a1a;
            }
        """)
        delete_button.clicked.connect(lambda checked, pk=smart_password.public_key:
                                      self.remove_password(pk))
        self.table_widget.setCellWidget(row_position, 3, delete_button)

        self.update_password_count()

    def remove_password(self, public_key):
        row = self.find_row_by_public_key(public_key)
        if row != -1:
            description = self.table_widget.item(row, 0).text()

            reply = QMessageBox.question(
                self,
                'Confirm Deletion',
                f'Delete password entry for:\n<b>{description}</b>?\n\n'
                f'Note: This only deletes the metadata. You can recreate it '
                f'later using the same secret phrase.',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                self.table_widget.removeRow(row)
                self.smart_pass_man.delete_smart_password(public_key)
                self.update_password_count()
                QMessageBox.information(
                    self,
                    'Deleted',
                    f'Password metadata for "{description}" has been deleted.'
                )

    def find_row_by_public_key(self, public_key):
        for row in range(self.table_widget.rowCount()):
            password_item = self.table_widget.item(row, 0)
            if password_item:
                for stored_password in self.smart_pass_man.passwords.values():
                    if stored_password.description == password_item.text() and stored_password.public_key == public_key:
                        return row
        return -1

    def add_password(self):
        dialog = PasswordInputDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            description, secret, length = dialog.get_inputs()

            if not description or not secret:
                QMessageBox.warning(
                    self,
                    'Missing Information',
                    'Please provide both service description and secret phrase.'
                )
                return

            try:
                public_key = SmartPasswordMaster.generate_public_key(secret=secret)

                if public_key in self.smart_pass_man.passwords:
                    existing_password = self.smart_pass_man.passwords[public_key]
                    QMessageBox.warning(
                        self,
                        'Duplicate Secret Phrase',
                        f'A password entry with this secret phrase already exists:\n\n'
                        f'"{existing_password.description}"\n'
                        f'Length: {existing_password.length} characters\n\n'
                        f'Each unique secret phrase generates a unique public key.\n'
                        f'You cannot have multiple entries with the same secret.'
                    )
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

                display_dialog = PasswordDisplayDialog(self, description, password)
                display_dialog.exec_()

            except Exception as e:
                QMessageBox.critical(
                    self,
                    'Error',
                    f'Failed to create password:\n{str(e)}'
                )

    def get_password(self, public_key, description):
        dialog = SecretInputDialog(self, description)
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
                smart_password = self.smart_pass_man.get_smart_password(public_key)
                if not smart_password:
                    QMessageBox.critical(
                        self,
                        'Error',
                        'Password metadata not found. It may have been deleted.'
                    )
                    return

                is_valid = SmartPasswordMaster.check_public_key(
                    secret=secret,
                    public_key=public_key
                )

                if is_valid:
                    password = SmartPasswordMaster.generate_smart_password(
                        secret=secret,
                        length=smart_password.length
                    )

                    display_dialog = PasswordDisplayDialog(self, description, password)
                    display_dialog.exec_()

                else:
                    QMessageBox.warning(
                        self,
                        'Invalid Secret',
                        'The secret phrase is incorrect. Please check:\n'
                        '• Caps Lock\n'
                        '• Keyboard layout\n'
                        '• Spelling\n\n'
                        'Note: In v2.0.0, secret phrases are case-sensitive.'
                    )

            except Exception as e:
                QMessageBox.critical(
                    self,
                    'Error',
                    f'Failed to generate password:\n{str(e)}'
                )

    def closeEvent(self, event):
        if len(self.smart_pass_man.passwords) > 0:
            reply = QMessageBox.question(
                self,
                'Exit',
                f'You have {len(self.smart_pass_man.passwords)} password(s) stored.\n'
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


def main():
    import sys

    app = QApplication(sys.argv)

    app.setStyle('Fusion')

    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(30, 30, 30))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(20, 20, 20))
    dark_palette.setColor(QPalette.AlternateBase, QColor(40, 40, 40))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(50, 50, 50))
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(50, 50, 50))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    dark_palette.setColor(QPalette.Disabled, QPalette.Text, QColor(100, 100, 100))
    dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(100, 100, 100))

    app.setPalette(dark_palette)

    warning_msg = """
    <h3>⚠️ IMPORTANT: SmartPassLib v2.0.0</h3>
    <p>This version has <b>BREAKING CHANGES</b>:</p>
    <ul>
    <li>All passwords generated with v1.x are now <b>INVALID</b></li>
    <li>You must create new passwords with your secret phrases</li>
    <li>Old password metadata cannot be migrated automatically</li>
    </ul>
    <hr>
    <ol>
    <li>Recover old passwords using the previous version.</li>
    <li>Generate new passwords using the new version.</li>
    <li>Replace old passwords with new ones.</li>
    </ol>
    """

    msg_box = QMessageBox()
    msg_box.setWindowTitle("Compatibility Warning")
    msg_box.setTextFormat(Qt.RichText)
    msg_box.setText(warning_msg)
    msg_box.setIcon(QMessageBox.Warning)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec_()

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
