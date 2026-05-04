# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
import os

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
    QAction,
    QMenuBar,
    QStatusBar,
    QMainWindow,
    QMenu,
    QScrollArea,
    QLineEdit,
    QGroupBox,
    QTextEdit
)
from PyQt5.QtGui import QFont, QIcon, QDesktopServices
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QSound
from smartpasslib import SmartPasswordManager, SmartPassword, SmartPasswordMaster

from core.dialogs.edit_password_dialog import EditPasswordDialog
from core.dialogs.password_add_dialog import AddPasswordDialog
from core.dialogs.password_display_dialog import PasswordDisplayDialog
from core.dialogs.password_get_dialog import GetPasswordDialog
from core.dialogs.qr_dialog import QRDialog
from core.models.configs.main_window_config import MainWindowConfig
from core.models.styles.main_window_styles import MainWindowStyles
from core.utils.sound_manager import SoundManager


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = MainWindowConfig()
        self.styles = MainWindowStyles()
        self.smart_pass_man = SmartPasswordManager()
        self.setWindowTitle(f'{self.config.app_name}')
        self.resize(800, 600)

        self.setup_application_icon()

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
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.menu_bar = QMenuBar()
        self.main_layout.setMenuBar(self.menu_bar)

        self.setup_menu_bar()

        self.header_panel = QWidget()
        self.header_panel.setStyleSheet("background-color: #19191e;")
        header_layout = QVBoxLayout(self.header_panel)
        header_layout.setContentsMargins(20, 15, 20, 15)

        title_label = QLabel("Smart Password Manager")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2a82da;")
        header_layout.addWidget(title_label)

        subtitle_label = QLabel("Deterministic smart password manager - same secret + same length = same password")
        subtitle_label.setStyleSheet("color: #a0a0a0; font-size: 9pt;")
        header_layout.addWidget(subtitle_label)

        self.main_layout.addWidget(self.header_panel)

        self.top_button_panel = QWidget()
        self.top_button_panel.setStyleSheet("background-color: #23232a;")
        top_button_layout = QHBoxLayout(self.top_button_panel)
        top_button_layout.setContentsMargins(20, 10, 20, 10)

        self.btn_add = QPushButton("+ Add")
        self.btn_add.setMinimumHeight(40)
        self.btn_add.setMinimumWidth(100)
        self.btn_add.clicked.connect(self.sound_manager.play_click)
        self.btn_add.clicked.connect(self.add_password)
        self.btn_add.setStyleSheet(self.styles.btn_add)
        top_button_layout.addWidget(self.btn_add)

        self.btn_import = QPushButton("Import")
        self.btn_import.setMinimumHeight(40)
        self.btn_import.setMinimumWidth(100)
        self.btn_import.clicked.connect(self.sound_manager.play_click)
        self.btn_import.clicked.connect(self.import_passwords)
        self.btn_import.setStyleSheet(self.styles.btn_import)
        top_button_layout.addWidget(self.btn_import)

        top_button_layout.addStretch()

        self.search_panel = QWidget()
        self.search_panel.setStyleSheet(self.styles.search_panel)
        search_layout = QHBoxLayout(self.search_panel)
        search_layout.setContentsMargins(20, 5, 20, 10)

        search_label = QLabel("🔍")
        search_label.setStyleSheet("color: #2a82da; font-size: 14pt;")
        search_layout.addWidget(search_label)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by description or public key...")
        self.search_input.setMinimumHeight(30)
        self.search_input.setStyleSheet(self.styles.search_input)
        self.search_input.textChanged.connect(self.apply_filter)
        search_layout.addWidget(self.search_input)

        self.btn_clear_search = QPushButton("Clear")
        self.btn_clear_search.setMinimumWidth(70)
        self.btn_clear_search.setMinimumHeight(30)
        self.btn_clear_search.clicked.connect(self.clear_search)
        self.btn_clear_search.setStyleSheet(self.styles.btn_clear_search)
        search_layout.addWidget(self.btn_clear_search)

        self.main_layout.addWidget(self.top_button_panel)
        self.main_layout.addWidget(self.search_panel)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(['Description', 'Length', 'Public Key (short)'])
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_widget.setSelectionMode(QTableWidget.SingleSelection)
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.setStyleSheet(self.styles.table_widget_style)

        self.table_widget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table_widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table_widget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

        self.table_widget.doubleClicked.connect(self.get_password_for_selected_row)

        self.main_layout.addWidget(self.table_widget)

        self.bottom_button_panel = QWidget()
        self.bottom_button_panel.setStyleSheet(self.styles.bottom_button_panel)
        bottom_button_layout = QHBoxLayout(self.bottom_button_panel)
        bottom_button_layout.setContentsMargins(20, 10, 20, 10)

        self.btn_get = QPushButton("Get")
        self.btn_get.setMinimumHeight(40)
        self.btn_get.setMinimumWidth(100)
        self.btn_get.clicked.connect(self.sound_manager.play_click)
        self.btn_get.clicked.connect(self.get_password_for_selected_row)
        self.btn_get.setStyleSheet(self.styles.btn_get)
        bottom_button_layout.addWidget(self.btn_get)

        self.btn_edit = QPushButton("Edit")
        self.btn_edit.setMinimumHeight(40)
        self.btn_edit.setMinimumWidth(100)
        self.btn_edit.clicked.connect(self.sound_manager.play_click)
        self.btn_edit.clicked.connect(self.edit_password_for_selected_row)
        self.btn_edit.setStyleSheet(self.styles.btn_edit)
        bottom_button_layout.addWidget(self.btn_edit)

        self.btn_delete = QPushButton("Delete")
        self.btn_delete.setMinimumHeight(40)
        self.btn_delete.setMinimumWidth(100)
        self.btn_delete.clicked.connect(self.sound_manager.play_click)
        self.btn_delete.clicked.connect(self.delete_selected_row)
        self.btn_delete.setStyleSheet(self.styles.btn_delete)
        bottom_button_layout.addWidget(self.btn_delete)

        self.btn_qr = QPushButton("QR")
        self.btn_qr.setMinimumHeight(40)
        self.btn_qr.setMinimumWidth(100)
        self.btn_qr.clicked.connect(self.sound_manager.play_click)
        self.btn_qr.clicked.connect(self.show_qr_for_selected)
        self.btn_qr.setStyleSheet(self.styles.btn_qr)
        bottom_button_layout.addWidget(self.btn_qr)

        self.btn_export = QPushButton("Export")
        self.btn_export.setMinimumHeight(40)
        self.btn_export.setMinimumWidth(100)
        self.btn_export.clicked.connect(self.sound_manager.play_click)
        self.btn_export.clicked.connect(self.export_passwords)
        self.btn_export.setStyleSheet(self.styles.btn_export)
        bottom_button_layout.addWidget(self.btn_export)

        bottom_button_layout.addStretch()

        self.btn_exit = QPushButton("Exit")
        self.btn_exit.setMinimumHeight(40)
        self.btn_exit.setMinimumWidth(100)
        self.btn_exit.clicked.connect(self.close)
        self.btn_exit.setStyleSheet(self.styles.btn_exit)
        bottom_button_layout.addWidget(self.btn_exit)

        self.main_layout.addWidget(self.bottom_button_panel)

        self.setup_status_bar()

        self.setup_table_context_menu()

        self.all_passwords = []
        self._init()
        self.center_window()

    def setup_application_icon(self):
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "icons", "icon.png")
        if not os.path.exists(icon_path):
            icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
        if os.path.exists(icon_path):
            icon = QIcon(icon_path)
            self.setWindowIcon(icon)

    def create_desktop_entry(self):
        from core.dialogs.desktop_entry_dialog import DesktopEntryDialog
        dialog = DesktopEntryDialog(self, self.sound_manager)
        dialog.exec_()

    def setup_menu_bar(self):
        file_menu = self.menu_bar.addMenu('File')

        export_action = QAction('Export passwords...', self)
        export_action.setShortcut('Ctrl+E')
        export_action.triggered.connect(self.sound_manager.play_click)
        export_action.triggered.connect(self.export_passwords)
        file_menu.addAction(export_action)

        import_action = QAction('Import passwords...', self)
        import_action.setShortcut('Ctrl+I')
        import_action.triggered.connect(self.sound_manager.play_click)
        import_action.triggered.connect(self.import_passwords)
        file_menu.addAction(import_action)

        file_menu.addSeparator()

        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        passwords_menu = self.menu_bar.addMenu('Passwords')

        create_pass_action = QAction('Create new password', self)
        create_pass_action.setShortcut('Ctrl+N')
        create_pass_action.triggered.connect(self.sound_manager.play_click)
        create_pass_action.triggered.connect(self.add_password)
        passwords_menu.addAction(create_pass_action)

        passwords_menu.addSeparator()

        get_action = QAction('Get Password', self)
        get_action.setShortcut('Ctrl+G')
        get_action.triggered.connect(self.sound_manager.play_click)
        get_action.triggered.connect(self.get_password_for_selected_row)
        passwords_menu.addAction(get_action)

        edit_action = QAction('Edit', self)
        edit_action.setShortcut('Ctrl+Shift+E')
        edit_action.triggered.connect(self.sound_manager.play_click)
        edit_action.triggered.connect(self.edit_password_for_selected_row)
        passwords_menu.addAction(edit_action)

        qr_action = QAction('Show QR Code', self)
        qr_action.setShortcut('Ctrl+R')
        qr_action.triggered.connect(self.sound_manager.play_click)
        qr_action.triggered.connect(self.show_qr_for_selected)
        passwords_menu.addAction(qr_action)

        passwords_menu.addSeparator()

        delete_action = QAction('Delete', self)
        delete_action.setShortcut('Del')
        delete_action.triggered.connect(self.sound_manager.play_click)
        delete_action.triggered.connect(self.delete_selected_row)
        passwords_menu.addAction(delete_action)

        refresh_action = QAction('Refresh', self)
        refresh_action.setShortcut('F5')
        refresh_action.triggered.connect(self.load_passwords)
        passwords_menu.addAction(refresh_action)

        sounds_menu = self.menu_bar.addMenu('Sounds')
        sound_action = QAction('Enable Sounds', self)
        sound_action.setCheckable(True)
        sound_action.setChecked(False)
        sound_action.setShortcut('Ctrl+Shift+S')
        sound_action.triggered.connect(self.toggle_sounds)
        sounds_menu.addAction(sound_action)
        self.sound_manager.sound_enabled_changed.connect(sound_action.setChecked)

        tools_menu = self.menu_bar.addMenu('Tools')
        create_shortcut_action = QAction('Create Desktop Shortcut', self)
        create_shortcut_action.setShortcut('Ctrl+Alt+S')
        create_shortcut_action.triggered.connect(self.create_desktop_entry)
        tools_menu.addAction(create_shortcut_action)

        help_menu = self.menu_bar.addMenu('Help')

        help_action = QAction('Help', self)
        help_action.setShortcut('F1')
        help_action.triggered.connect(self.sound_manager.play_click)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)

        shortcuts_action = QAction('Keyboard shortcuts', self)
        shortcuts_action.setShortcut('Ctrl+/')
        shortcuts_action.triggered.connect(self.sound_manager.play_click)
        shortcuts_action.triggered.connect(self._show_keyboard_shortcuts)
        help_menu.addAction(shortcuts_action)

        help_menu.addSeparator()

        disclaimer_action = QAction('Disclaimer', self)
        disclaimer_action.setShortcut('Ctrl+D')
        disclaimer_action.triggered.connect(self.show_disclaimer)
        help_menu.addAction(disclaimer_action)

        license_action = QAction('License', self)
        license_action.setShortcut('Ctrl+L')
        license_action.triggered.connect(self.show_license)
        help_menu.addAction(license_action)

        help_menu.addSeparator()

        about_action = QAction('About', self)
        about_action.setShortcut('Ctrl+A')
        about_action.triggered.connect(self.sound_manager.play_click)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def setup_table_context_menu(self):
        self.table_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table_widget.customContextMenuRequested.connect(self.show_table_context_menu)

    def show_table_context_menu(self, position):
        item = self.table_widget.itemAt(position)
        if not item:
            return

        row = item.row()
        if row < 0 or row >= len(self.all_passwords):
            return

        public_key = self.all_passwords[row].public_key

        context_menu = QMenu(self)

        get_action = context_menu.addAction("🔓 Get Password")
        get_action.triggered.connect(lambda checked, pk=public_key: self.get_password(pk))

        edit_action = context_menu.addAction("✎ Edit")
        edit_action.triggered.connect(lambda checked, pk=public_key: self.edit_password(pk))

        qr_action = context_menu.addAction("📱 Show QR Code")
        qr_action.triggered.connect(lambda checked, pk=public_key: self.show_qr(pk))

        context_menu.addSeparator()

        delete_action = context_menu.addAction("🗑 Delete")
        delete_action.triggered.connect(lambda checked, pk=public_key: self.remove_password(pk))

        context_menu.exec_(self.table_widget.viewport().mapToGlobal(position))

    def _get_public_key_for_row(self, row):
        if row < 0 or row >= len(self.all_passwords):
            return None
        return self.all_passwords[row].public_key

    def get_password_for_selected_row(self):
        current_row = self.table_widget.currentRow()
        if current_row < 0:
            self.show_status_message('No row selected', 2000)
            return
        public_key = self._get_public_key_for_row(current_row)
        if public_key:
            self.get_password(public_key)

    def edit_password_for_selected_row(self):
        current_row = self.table_widget.currentRow()
        if current_row < 0:
            self.show_status_message('No row selected', 2000)
            return
        public_key = self._get_public_key_for_row(current_row)
        if public_key:
            self.edit_password(public_key)

    def delete_selected_row(self):
        current_row = self.table_widget.currentRow()
        if current_row < 0:
            self.show_status_message('No row selected', 2000)
            return
        public_key = self._get_public_key_for_row(current_row)
        if public_key:
            self.remove_password(public_key)

    def show_qr_for_selected(self):
        current_row = self.table_widget.currentRow()
        if current_row < 0:
            self.show_status_message('No password selected. Please select a row first.', 2000)
            QMessageBox.information(self, 'No Selection', 'Please select a password row first.')
            return
        public_key = self._get_public_key_for_row(current_row)
        if public_key:
            self.show_qr(public_key)

    def center_window(self):
        frame = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(center_point)
        self.move(frame.topLeft())

    def load_passwords(self):
        self.all_passwords = []
        for password in self.smart_pass_man.passwords.values():
            self.all_passwords.append(password)
        self.apply_filter()

    def apply_filter(self):
        search_text = self.search_input.text().strip().lower()

        self.table_widget.setRowCount(0)

        filtered = self.all_passwords
        if search_text:
            filtered = [p for p in self.all_passwords
                        if search_text in p.description.lower()
                        or search_text in p.public_key.lower()]

        self.table_widget.setRowCount(len(filtered))

        for row, pwd in enumerate(filtered):
            desc_item = QTableWidgetItem(pwd.description)
            self.table_widget.setItem(row, 0, desc_item)

            length_item = QTableWidgetItem(f"{pwd.length} chars")
            length_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_widget.setItem(row, 1, length_item)

            short_key = pwd.public_key[:30] + "..." if len(pwd.public_key) > 30 else pwd.public_key
            key_item = QTableWidgetItem(short_key)
            self.table_widget.setItem(row, 2, key_item)

        count = len(filtered)
        total = len(self.all_passwords)
        if search_text:
            self.count_label.setText(f"{count} / {total} passwords")
        else:
            self.count_label.setText(f"{total} passwords")

        storage_label = self.status_bar.findChild(QLabel, "storage_label")
        if storage_label:
            storage_label.setText(f"Storage: {self.smart_pass_man.file_path}")

    def clear_search(self):
        self.search_input.clear()
        self.search_input.setFocus()

    def _init(self):
        self.load_passwords()

    def show_help(self):
        self.sound_manager.play_notify()
        dialog = QDialog(self)
        dialog.setWindowTitle('Smart Password Manager Help')
        dialog.setMinimumWidth(650)
        dialog.setMinimumHeight(500)
        layout = QVBoxLayout(dialog)

        title_label = QLabel(f"<h2 style='color: #2a82da;'>Smart Password Manager Help</h2>")
        title_label.setTextFormat(Qt.TextFormat.RichText)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        help_label = QLabel(self.config.help_text)
        help_label.setTextFormat(Qt.TextFormat.RichText)
        help_label.setWordWrap(True)
        help_label.setOpenExternalLinks(True)
        help_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        help_label.setStyleSheet(self.styles.help_label_style)
        content_layout.addWidget(help_label)
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        ok_button = QPushButton("Ok")
        ok_button.setMinimumWidth(100)
        ok_button.setMinimumHeight(35)
        ok_button.setStyleSheet(self.styles.ok_button_style)
        ok_button.clicked.connect(dialog.accept)
        button_layout.addWidget(ok_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        dialog.setModal(True)
        x = self.x() + (self.width() - dialog.width()) // 2
        y = self.y() + (self.height() - dialog.height()) // 2
        dialog.move(x, y)
        dialog.exec_()

    def show_about(self):
        self.sound_manager.play_about()

        dialog = QDialog(self)
        dialog.setWindowTitle("About Smart Password Manager")
        dialog.setMinimumWidth(700)
        dialog.setMinimumHeight(550)
        dialog.setModal(True)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(10)

        title_layout = QHBoxLayout()
        icon_label = QLabel("🔐")
        icon_label.setStyleSheet("font-size: 32px;")
        title_layout.addWidget(icon_label)

        title_label = QLabel(f"<h1 style='color: #2a82da; margin: 0;'>{self.config.app_name}</h1>")
        title_label.setTextFormat(Qt.TextFormat.RichText)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        layout.addLayout(title_layout)

        version_label = QLabel(f"<b>Version {self.config.version}</b>")
        version_label.setTextFormat(Qt.TextFormat.RichText)
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setMinimumHeight(300)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(15)

        desc_label = QLabel(
            "Cross-platform desktop manager for deterministic smart passwords.\n"
            "Generate, manage, and retrieve passwords without storing them.\n"
            "Your secret phrase is the only key you need."
        )
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setStyleSheet(self.styles.desc_label)
        content_layout.addWidget(desc_label)

        info_frame = QFrame()
        info_frame.setStyleSheet(self.styles.info_frame)
        info_layout = QVBoxLayout(info_frame)

        dec_label = QLabel("<b>🔗 DECENTRALIZED BY DESIGN</b>")
        dec_label.setStyleSheet(self.styles.dec_label)
        info_layout.addWidget(dec_label)

        dec_text = QLabel(
            "• No cloud, no database, no trust required\n"
            "• Your secrets never leave your device\n"
            "• There is no \"forgot password\" button — you are in complete control"
        )
        dec_text.setWordWrap(True)
        dec_text.setStyleSheet("color: #c0c0c0; padding-left: 15px;")
        info_layout.addWidget(dec_text)

        info_layout.addSpacing(10)

        sec_label = QLabel("<b>🛡️ SECURITY MODEL</b>")
        sec_label.setStyleSheet(self.styles.sec_label)
        info_layout.addWidget(sec_label)

        sec_text = QLabel(
            "• Proof of Knowledge: Public keys verify secrets without exposing them\n"
            "• Deterministic Security: Same secret + length = same password\n"
            "• Zero-Storage: No passwords or secrets are ever stored\n"
            "• Local Processing: Secrets never leave your device"
        )
        sec_text.setWordWrap(True)
        sec_text.setStyleSheet("color: #c0c0c0; padding-left: 15px;")
        info_layout.addWidget(sec_text)

        info_layout.addSpacing(10)

        tech_label = QLabel("<b>⚙️ TECHNICAL FOUNDATION</b>")
        tech_label.setStyleSheet("color: #2a82da;")
        info_layout.addWidget(tech_label)

        tech_text = QLabel(
            "Powered by smartpasslib — deterministic password generation library\n"
            "Key derivation: 30 iterations (private key) / 60 iterations (public key)\n"
            "Character set: a-z A-Z 0-9 ! @ # $ & * - _"
        )
        tech_text.setWordWrap(True)
        tech_text.setStyleSheet("color: #c0c0c0; padding-left: 15px;")
        info_layout.addWidget(tech_text)

        content_layout.addWidget(info_frame)

        links_frame = QFrame()
        links_frame.setStyleSheet(self.styles.links_frame)
        links_layout = QHBoxLayout(links_frame)

        github_btn = QPushButton("📂 GitHub")
        github_btn.setStyleSheet(self.styles.github_btn)
        github_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(self.config.project_url)))
        links_layout.addWidget(github_btn)

        issues_btn = QPushButton("🐛 Report Issue")
        issues_btn.setStyleSheet(self.styles.issues_btn)
        issues_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(f"{self.config.project_url}/issues")))
        links_layout.addWidget(issues_btn)

        license_btn = QPushButton("📄 License")
        license_btn.setStyleSheet(self.styles.license_btn)
        license_btn.clicked.connect(self.show_license)
        links_layout.addWidget(license_btn)

        disclaimer_btn = QPushButton("⚠️ Disclaimer")
        disclaimer_btn.setStyleSheet(self.styles.disclaimer_btn)
        disclaimer_btn.clicked.connect(self.show_disclaimer)
        links_layout.addWidget(disclaimer_btn)

        content_layout.addWidget(links_frame)

        copyright_label = QLabel(f"Copyright © {self.config.year}, {self.config.author}")
        copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        copyright_label.setStyleSheet(self.styles.copyright_label)
        content_layout.addWidget(copyright_label)

        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        close_btn = QPushButton("Close")
        close_btn.setMinimumWidth(100)
        close_btn.setMinimumHeight(35)
        close_btn.setStyleSheet(self.styles.close_btn)
        close_btn.clicked.connect(dialog.accept)
        button_layout.addWidget(close_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        x = self.x() + (self.width() - dialog.width()) // 2
        y = self.y() + (self.height() - dialog.height()) // 2
        dialog.move(x, y)

        dialog.exec_()

    def show_disclaimer(self):
        self.sound_manager.play_notify()
        dialog = QDialog(self)
        dialog.setWindowTitle("Disclaimer")
        dialog.setMinimumWidth(700)
        dialog.setMinimumHeight(500)
        dialog.setMaximumWidth(800)
        dialog.setMaximumHeight(600)

        layout = QVBoxLayout(dialog)

        title_label = QLabel("<h2 style='color: #2a82da;'>⚠️ LEGAL DISCLAIMER</h2>")
        title_label.setTextFormat(Qt.TextFormat.RichText)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        text_label = QLabel(self.config.disclaimer_text)
        text_label.setTextFormat(Qt.TextFormat.PlainText)
        text_label.setWordWrap(True)
        text_label.setStyleSheet(self.styles.text_label)
        content_layout.addWidget(text_label)

        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        ok_button = QPushButton("Agree")
        ok_button.setMinimumWidth(100)
        ok_button.setMinimumHeight(35)
        ok_button.setStyleSheet(self.styles.ok_button)
        ok_button.clicked.connect(dialog.accept)
        button_layout.addWidget(ok_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        dialog.setModal(True)
        x = self.x() + (self.width() - dialog.width()) // 2
        y = self.y() + (self.height() - dialog.height()) // 2
        dialog.move(x, y)
        dialog.exec_()

    def show_license(self):
        self.sound_manager.play_notify()
        dialog = QDialog(self)
        dialog.setWindowTitle("License - BSD 3-Clause")
        dialog.setMinimumWidth(700)
        dialog.setMinimumHeight(500)
        dialog.setMaximumWidth(800)
        dialog.setMaximumHeight(600)

        layout = QVBoxLayout(dialog)

        title_label = QLabel("<h2 style='color: #2a82da;'>📄 BSD 3-CLAUSE LICENSE</h2>")
        title_label.setTextFormat(Qt.TextFormat.RichText)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        text_label = QLabel(self.config.license_text)
        text_label.setTextFormat(Qt.TextFormat.PlainText)
        text_label.setWordWrap(True)
        text_label.setStyleSheet(self.styles.text_label_2)
        content_layout.addWidget(text_label)

        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        ok_button = QPushButton("Agree")
        ok_button.setMinimumWidth(100)
        ok_button.setMinimumHeight(35)
        ok_button.setStyleSheet(self.styles.ok_button_2)
        ok_button.clicked.connect(dialog.accept)
        button_layout.addWidget(ok_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        dialog.setModal(True)
        x = self.x() + (self.width() - dialog.width()) // 2
        y = self.y() + (self.height() - dialog.height()) // 2
        dialog.move(x, y)
        dialog.exec_()

    def _show_keyboard_shortcuts(self):
        self.sound_manager.play_notify()

        dialog = QDialog(self)
        dialog.setWindowTitle("Keyboard Shortcuts")
        dialog.setMinimumWidth(600)
        dialog.setMinimumHeight(450)
        dialog.setModal(True)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(10)

        title_label = QLabel("<h2 style='color: #2a82da;'>Keyboard Shortcuts</h2>")
        title_label.setTextFormat(Qt.TextFormat.RichText)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        shortcuts_label = QLabel(self.config.short_cuts_text)
        shortcuts_label.setTextFormat(Qt.TextFormat.PlainText)
        shortcuts_label.setWordWrap(True)
        shortcuts_label.setStyleSheet(self.styles.shortcuts_label)
        content_layout.addWidget(shortcuts_label)

        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        ok_button = QPushButton("OK")
        ok_button.setMinimumWidth(100)
        ok_button.setMinimumHeight(35)
        ok_button.setStyleSheet(self.styles.ok_button_3)
        ok_button.clicked.connect(dialog.accept)
        button_layout.addWidget(ok_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        x = self.x() + (self.width() - dialog.width()) // 2
        y = self.y() + (self.height() - dialog.height()) // 2
        dialog.move(x, y)

        dialog.exec_()

    def show_qr(self, public_key):
        self.sound_manager.play_notify()
        smart_password = self.smart_pass_man.get_smart_password(public_key)
        if not smart_password:
            self.show_status_message('Password metadata not found', 2000)
            QMessageBox.warning(self, 'Error', 'Password metadata not found.')
            return
        dialog = QRDialog(
            self,
            description=smart_password.description,
            public_key=smart_password.public_key,
            length=smart_password.length,
            sound_manager=self.sound_manager
        )
        dialog.exec_()

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
                reply = QMessageBox.question(
                    self, '⚠️ Password Length Change Warning',
                    f'Changing password length from {smart_password.length} to {new_length} characters.\n\n'
                    f'First {min(smart_password.length, new_length)} characters will remain the same.\n'
                    f'Are you sure?',
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                )
                if reply == QMessageBox.No:
                    return
            try:
                success = self.smart_pass_man.update_smart_password(
                    public_key=public_key,
                    description=new_description,
                    length=new_length
                )
                if success:
                    self.load_passwords()
                    self.show_status_message('Password metadata updated', 3000)
                    QMessageBox.information(self, 'Updated', '✅ Successfully updated!')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to update:\n{str(e)}')

    def setup_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.count_label = QLabel("0 passwords")
        self.count_label.setStyleSheet("color: #a0a0a0; padding: 0 10px;")
        self.status_bar.addPermanentWidget(self.count_label)

        storage_label = QLabel("")
        storage_label.setObjectName("storage_label")
        storage_label.setStyleSheet("color: #a0a0a0; padding: 0 10px;")
        self.status_bar.addPermanentWidget(storage_label)

        self.status_bar.showMessage('Ready')

    def find_row_by_public_key(self, public_key):
        for row in range(len(self.all_passwords)):
            if self.all_passwords[row].public_key == public_key:
                return row
        return -1

    def remove_password(self, public_key):
        self.sound_manager.play_notify()
        row = self.find_row_by_public_key(public_key)
        if row != -1:
            description = self.table_widget.item(row, 0).text()

            dialog = QDialog(self)
            dialog.setWindowTitle("Confirm Deletion")
            dialog.setMinimumWidth(450)
            dialog.setMaximumWidth(550)
            dialog.setModal(True)

            layout = QVBoxLayout(dialog)
            layout.setSpacing(15)

            title_label = QLabel("🗑️ Delete Password Entry")
            title_font = QFont()
            title_font.setPointSize(14)
            title_font.setBold(True)
            title_label.setFont(title_font)
            title_label.setStyleSheet("color: #dc3545;")
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(title_label)

            info_label = QLabel(
                "This will delete the password metadata. The actual password can still be "
                "recreated if you remember your secret phrase."
            )
            info_label.setWordWrap(True)
            info_label.setStyleSheet("color: #a0a0a0;")
            layout.addWidget(info_label)

            desc_group = QGroupBox("Password Description")
            desc_layout = QVBoxLayout()

            desc_text = QTextEdit()
            desc_text.setPlainText(description)
            desc_text.setReadOnly(True)
            desc_text.setMaximumHeight(80)
            desc_text.setMinimumHeight(60)
            desc_text.setStyleSheet(self.styles.desc_text)
            desc_layout.addWidget(desc_text)
            desc_group.setLayout(desc_layout)
            layout.addWidget(desc_group)

            question_label = QLabel("<b>Are you sure you want to delete this entry?</b>")
            question_label.setWordWrap(True)
            question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            question_label.setStyleSheet("color: #ffc107; padding: 10px;")
            layout.addWidget(question_label)

            button_layout = QHBoxLayout()
            button_layout.setSpacing(10)

            cancel_btn = QPushButton("Cancel")
            cancel_btn.setMinimumHeight(35)
            cancel_btn.setMinimumWidth(100)
            cancel_btn.setStyleSheet(self.styles.cancel_btn)
            cancel_btn.clicked.connect(dialog.reject)
            button_layout.addWidget(cancel_btn)

            delete_btn = QPushButton("🗑 Delete")
            delete_btn.setMinimumHeight(35)
            delete_btn.setMinimumWidth(100)
            delete_btn.setStyleSheet(self.styles.delete_btn)
            delete_btn.clicked.connect(dialog.accept)
            button_layout.addWidget(delete_btn)

            layout.addLayout(button_layout)

            x = self.x() + (self.width() - dialog.width()) // 2
            y = self.y() + (self.height() - dialog.height()) // 2
            dialog.move(x, y)

            if dialog.exec_() == QDialog.Accepted:
                self.smart_pass_man.delete_smart_password(public_key)
                self.load_passwords()
                self.show_status_message(f'Password entry for "{description}" deleted', 3000)

                QMessageBox.information(
                    self,
                    "Deleted",
                    f'✅ Password metadata for "{description}" has been deleted.',
                    QMessageBox.Ok
                )

    def add_password(self):
        self.sound_manager.play_notify()
        dialog = AddPasswordDialog(self, self.sound_manager)
        if dialog.exec_() == QDialog.Accepted:
            description, secret, length = dialog.get_inputs()
            if not description or not secret:
                QMessageBox.warning(self, 'Missing Information',
                                    'Please provide both password description and secret phrase.')
                return
            try:
                public_key = SmartPasswordMaster.generate_public_key(secret=secret)
                if public_key in self.smart_pass_man.passwords:
                    existing_password = self.smart_pass_man.passwords[public_key]
                    QMessageBox.warning(
                        self, 'Duplicate Secret Phrase',
                        f'A password entry with this secret phrase already exists:\n\n'
                        f'"{existing_password.description}"\n'
                        f'Length: {existing_password.length} characters\n\n'
                        f'You cannot have multiple entries with the same secret.'
                    )
                    return
                smart_password = SmartPassword(public_key=public_key, description=description, length=length)
                password = SmartPasswordMaster.generate_smart_password(secret=secret, length=length)
                self.smart_pass_man.add_smart_password(smart_password)
                self.load_passwords()
                self.show_status_message(f'Password created for "{description}"', 3000)
                display_dialog = PasswordDisplayDialog(self, description, password, self.sound_manager)
                display_dialog.exec_()
            except Exception as e:
                self.show_status_message('Failed to create password', 3000)
                QMessageBox.critical(self, 'Error', f'Failed to create password:\n{str(e)}')

    def get_password(self, public_key):
        self.sound_manager.play_notify()
        smart_password = self.smart_pass_man.get_smart_password(public_key)
        if not smart_password:
            self.show_status_message('Password metadata not found', 3000)
            QMessageBox.critical(self, 'Error', 'Password metadata not found.')
            return
        description = smart_password.description
        dialog = GetPasswordDialog(self, description, self.sound_manager)
        if dialog.exec_() == QDialog.Accepted:
            secret = dialog.get_secret()
            if not secret:
                self.show_status_message('Missing secret phrase', 3000)
                QMessageBox.warning(self, 'Missing Secret', 'Please enter your secret phrase.')
                return
            try:
                is_valid = SmartPasswordMaster.check_public_key(secret=secret, public_key=public_key)
                if is_valid:
                    password = SmartPasswordMaster.generate_smart_password(secret=secret, length=smart_password.length)
                    self.show_status_message(f'Password retrieved for "{description}"', 3000)
                    display_dialog = PasswordDisplayDialog(self, description, password, self.sound_manager)
                    display_dialog.exec_()
                else:
                    self.show_status_message('Invalid secret phrase', 3000)
                    QMessageBox.warning(self, 'Invalid Secret', 'The secret phrase is incorrect.')
            except Exception as e:
                self.show_status_message('Failed to generate password', 3000)
                QMessageBox.critical(self, 'Error', f'Failed to generate password:\n{str(e)}')

    def toggle_sounds(self, enabled: bool):
        self.sound_manager.set_enabled(enabled)
        status = "enabled" if enabled else "disabled"
        self.show_status_message(f'Sounds {status}', 2000)

    def export_passwords(self):
        from core.dialogs.export_import_dialog import ExportImportDialog
        dialog = ExportImportDialog(self, mode="export", smart_pass_man=self.smart_pass_man,
                                    sound_manager=self.sound_manager)
        if dialog.exec_() == QDialog.Accepted:
            self.show_status_message('Passwords exported successfully', 3000)

    def import_passwords(self):
        from core.dialogs.export_import_dialog import ExportImportDialog
        dialog = ExportImportDialog(self, mode="import", smart_pass_man=self.smart_pass_man,
                                    sound_manager=self.sound_manager)
        if dialog.exec_() == QDialog.Accepted:
            self.load_passwords()
            self.show_status_message(f'Passwords imported successfully. Total: {self.smart_pass_man.password_count}',
                                     3000)

    def show_status_message(self, message, duration=3000):
        self.status_bar.showMessage(message, duration)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            current_row = self.table_widget.currentRow()
            if current_row >= 0:
                self.get_password_for_selected_row()
            event.accept()
        else:
            super().keyPressEvent(event)

    def closeEvent(self, event):
        self.sound_manager.play_error()
        if len(self.smart_pass_man.passwords) > 0:
            reply = QMessageBox.question(self, 'Exit', 'Are you sure you want to exit?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
