# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
from PyQt5.QtWidgets import (
    QDesktopWidget,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
    QDialog,
    QTableWidget,
    QTableWidgetItem,
    QFrame,
    QHeaderView,
    QHBoxLayout,
    QAction, QMenuBar, QStatusBar, QMainWindow, QMenu
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QSound
from smartpasslib import SmartPasswordManager, SmartPassword, SmartPasswordMaster

from core.dialogs.edit_password_dialog import EditPasswordDialog
from core.dialogs.password_display_dialog import PasswordDisplayDialog
from core.dialogs.password_input_dialog import PasswordInputDialog
from core.dialogs.secret_input_dialog import SecretInputDialog
from core.utils.config import Config
from core.utils.sound_manager import SoundManager

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = Config()
        self.smart_pass_man = SmartPasswordManager()
        self.setWindowTitle(f'{self.config.app_name} {self.config.version}')
        self.resize(800, 600)

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
        self.label_logo = QLabel(f"{self.config.app_name}")
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

        self.setup_table_context_menu()

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

        copyright_text = self.config.copyright_text
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

        export_menu = file_menu.addMenu('Export')

        export_action = QAction('Export passwords...', self)
        export_action.setShortcut('Ctrl+E')
        export_action.triggered.connect(self.sound_manager.play_click)
        export_action.triggered.connect(self.export_passwords)
        export_menu.addAction(export_action)

        import_menu = file_menu.addMenu('Import')

        import_action = QAction('Import passwords...', self)
        import_action.setShortcut('Ctrl+I')
        import_action.triggered.connect(self.sound_manager.play_click)
        import_action.triggered.connect(self.import_passwords)
        import_menu.addAction(import_action)

        import_menu.addSeparator()

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
        about_action.setShortcut('Ctrl+Shift+A')
        about_action.triggered.connect(self.sound_manager.play_click)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        shortcuts_action = QAction('Keyboard shortcuts', self)
        shortcuts_action.setShortcut('Ctrl+/')
        shortcuts_action.triggered.connect(self.sound_manager.play_click)
        shortcuts_action.triggered.connect(self._show_keyboard_shortcuts)
        help_menu.addAction(shortcuts_action)

        help_action = QAction('Help', self)
        help_action.setShortcut('F1')
        help_action.triggered.connect(self.sound_manager.play_click)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)

    def setup_table_context_menu(self):
        self.table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_widget.customContextMenuRequested.connect(self.show_table_context_menu)

    def show_table_context_menu(self, position):
        item = self.table_widget.itemAt(position)
        if not item:
            return

        row = item.row()
        public_key = None

        for col in [2, 3, 4]:
            widget = self.table_widget.cellWidget(row, col)
            if widget and hasattr(widget, 'public_key'):
                public_key = widget.public_key
                break

        if not public_key:
            return

        context_menu = QMenu(self)

        get_action = context_menu.addAction("🔑 Get Password")
        get_action.triggered.connect(lambda checked, pk=public_key: self.get_password(pk))

        edit_action = context_menu.addAction("✏️ Edit Metadata")
        edit_action.triggered.connect(lambda checked, pk=public_key: self.edit_password(pk))

        context_menu.addSeparator()

        delete_action = context_menu.addAction("🗑️ Delete Entry")
        delete_action.triggered.connect(lambda checked, pk=public_key: self.remove_password(pk))

        context_menu.exec_(self.table_widget.viewport().mapToGlobal(position))

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
        self.show_status_message(f'Loaded {self.smart_pass_man.password_count} passwords', 3000)

    def show_help(self):
        self.sound_manager.play_notify()
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle('Smart Password Manager Help')
        msg_box.setTextFormat(Qt.RichText)
        msg_box.setText(self.config.help_text)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def show_about(self):
        self.sound_manager.play_about()
        QMessageBox.about(
            self,
            "About Smart Password Manager",
            self.config.about_text
        )

    def _show_keyboard_shortcuts(self):
        self.sound_manager.play_notify()

        QMessageBox.about(
            self,
            "Keyboard Shortcuts",
            f"""<h2>Keyboard Shortcuts</h2>

            <p><b>F1</b> - Show Help</p>
            <p><b>Ctrl + Q</b> - Exit Application</p>
            <p><b>Ctrl + P</b> - Create New Password</p>
            <p><b>Ctrl + Shift + S</b> - Toggle Sounds</p>
            <p><b>Ctrl + /</b> - Keyboard shortcuts</p>
            <p><b>Ctrl + Shift + A</b> - About</p>
            <p><b>Ctrl + I</b> - Import Passwords</p>
            <p><b>Ctrl + E</b> - Export Passwords</p>
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
                    self.show_status_message('Password metadata updated', 3000)

                    msg_box = QMessageBox(self)
                    msg_box.setWindowTitle('Updated')
                    msg_box.setTextFormat(Qt.RichText)

                    msg = f'✅ Successfully updated!'
                    if new_length != smart_password.length:
                        msg += (f'<br><br>Password length changed from {smart_password.length} '
                                f'to {new_length} characters.')
                        msg += (f'<br><br><i>Note: New password will have '
                                f'{"extended" if new_length > smart_password.length else "truncated"} characters.</i>')

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
                self.show_status_message(f'Password entry for "{description}" deleted', 3000)
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
                    self.show_status_message('Duplicate secret phrase detected', 3000)
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
                self.show_status_message(f'Password created for "{description}"', 3000)

                display_dialog = PasswordDisplayDialog(self, description, password, self.sound_manager)
                display_dialog.exec_()

            except Exception as e:
                self.show_status_message('Failed to create password', 3000)
                QMessageBox.critical(
                    self,
                    'Error',
                    f'Failed to create password:\n{str(e)}'
                )

    def get_password(self, public_key):
        self.sound_manager.play_notify()
        smart_password = self.smart_pass_man.get_smart_password(public_key)
        if not smart_password:
            self.show_status_message('Password metadata not found', 3000)
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
                self.show_status_message('Missing secret phrase', 3000)
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
                    self.show_status_message(f'Password retrieved for "{description}"', 3000)
                    display_dialog = PasswordDisplayDialog(self, description, password, self.sound_manager)
                    display_dialog.exec_()

                else:
                    self.show_status_message('Invalid secret phrase', 3000)
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
                self.show_status_message('Failed to generate password', 3000)
                QMessageBox.critical(
                    self,
                    'Error',
                    f'Failed to generate password:\n{str(e)}'
                )

    def toggle_sounds(self, enabled: bool):
        self.sound_manager.set_enabled(enabled)
        status = "enabled" if enabled else "disabled"
        self.show_status_message(f'Sounds {status}', 2000)

    def export_passwords(self):
        from core.dialogs.export_import_dialog import ExportImportDialog

        dialog = ExportImportDialog(
            self,
            mode="export",
            smart_pass_man=self.smart_pass_man,
            sound_manager=self.sound_manager
        )

        if dialog.exec_() == QDialog.Accepted:
            self.show_status_message('Passwords exported successfully', 3000)

    def import_passwords(self):
        from core.dialogs.export_import_dialog import ExportImportDialog

        dialog = ExportImportDialog(
            self,
            mode="import",
            smart_pass_man=self.smart_pass_man,
            sound_manager=self.sound_manager
        )

        if dialog.exec_() == QDialog.Accepted:
            self.refresh_table()
            self.update_password_count()
            self.show_status_message(f'Passwords imported successfully. '
                                     f'Total: {self.smart_pass_man.password_count}', 3000)

    def refresh_table(self):
        self.table_widget.setRowCount(0)

        for password in self.smart_pass_man.passwords.values():
            self.add_item(password)

    def show_status_message(self, message, duration=3000):
        self.status_bar.showMessage(message, duration)

    def update_status_on_action(self, action_name):
        messages = {
            'add': 'Password created successfully',
            'get': 'Password retrieved successfully',
            'edit': 'Password metadata updated',
            'delete': 'Password entry deleted',
            'export': 'Passwords exported successfully',
            'import': 'Passwords imported successfully',
            'copy': 'Password copied to clipboard',
            'sound_on': 'Sounds enabled',
            'sound_off': 'Sounds disabled',
            'ready': 'Ready',
            'duplicate': 'Duplicate secret phrase detected',
            'invalid_secret': 'Invalid secret phrase'
        }
        self.status_bar.showMessage(messages.get(action_name, 'Action completed'), 3000)

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
