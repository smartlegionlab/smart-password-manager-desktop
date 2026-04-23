# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
import json
from pathlib import Path
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QCheckBox,
    QGroupBox,
    QRadioButton,
    QButtonGroup
)

from core.models.configs.export_import_config import ExportImportDialogConfig
from core.models.styles import ExportImportDialogStyles


class ExportImportDialog(QDialog):
    def __init__(self, parent=None, mode="export", smart_pass_man=None, sound_manager=None):
        super().__init__(parent)
        self.mode = mode
        self.smart_pass_man = smart_pass_man
        self.styles = ExportImportDialogStyles()
        self.config = ExportImportDialogConfig()
        self.sound_manager = sound_manager
        self.selected_file = None

        title = "Export Passwords" if mode == "export" else "Import Passwords"
        self.setWindowTitle(title)
        self.setMinimumWidth(450)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(15)

        instruction = QLabel(self._get_instruction_text())
        instruction.setWordWrap(True)
        instruction.setStyleSheet(self.styles.instruction_style)
        self.layout.addWidget(instruction)

        if mode == "export":
            self._setup_export_options()

        file_group = QGroupBox("File")
        file_layout = QVBoxLayout()

        file_select_layout = QHBoxLayout()
        self.file_path_label = QLabel("No file selected")
        self.file_path_label.setStyleSheet(self.styles.file_path_label_style)
        self.file_path_label.setWordWrap(True)
        file_select_layout.addWidget(self.file_path_label)

        self.browse_button = QPushButton("Browse...")
        self.browse_button.clicked.connect(self.sound_manager.play_click)
        self.browse_button.clicked.connect(self.browse_file)
        file_select_layout.addWidget(self.browse_button)

        file_layout.addLayout(file_select_layout)
        file_group.setLayout(file_layout)
        self.layout.addWidget(file_group)

        if mode == "import":
            warning = QLabel(
                "⚠️ <b>Warning:</b> Importing will merge with existing passwords. "
                "If public keys conflict, existing entries will be preserved."
            )
            warning.setWordWrap(True)
            warning.setStyleSheet(self.styles.warning_style)
            self.layout.addWidget(warning)

        button_layout = QHBoxLayout()

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.sound_manager.play_click)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        self.action_button = QPushButton(self._get_action_text())
        self.action_button.setDefault(True)
        self.action_button.clicked.connect(self.sound_manager.play_click)
        self.action_button.clicked.connect(self.execute)
        self.action_button.setEnabled(False)

        if mode == "export":
            self.action_button.setStyleSheet(self.styles.action_button_export_style)
        else:
            self.action_button.setStyleSheet(self.styles.action_button_import_style)

        button_layout.addWidget(self.action_button)
        self.layout.addLayout(button_layout)

    def _get_instruction_text(self):
        if self.mode == "export":
            return self.config.export_text
        else:
            return self.config.import_text

    def _get_action_text(self):
        return "Export" if self.mode == "export" else "Import"

    def _setup_export_options(self):
        options_group = QGroupBox("Export Options")
        options_layout = QVBoxLayout()

        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Format:"))

        self.format_group = QButtonGroup(self)
        self.format_json = QRadioButton("JSON (readable)")
        self.format_json.setChecked(True)
        self.format_minified = QRadioButton("JSON (minified)")

        format_layout.addWidget(self.format_json)
        format_layout.addWidget(self.format_minified)
        format_layout.addStretch()
        options_layout.addLayout(format_layout)

        self.include_metadata = QCheckBox("Include export metadata (timestamp, version)")
        self.include_metadata.setChecked(True)
        options_layout.addWidget(self.include_metadata)

        options_group.setLayout(options_layout)
        self.layout.addWidget(options_group)

    def browse_file(self):
        self.sound_manager.play_click()

        if self.mode == "export":
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"passwords_export_{timestamp}.json"

            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Export Passwords",
                str(Path.home() / default_filename),
                "JSON Files (*.json);;All Files (*)"
            )
        else:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Import Passwords",
                str(Path.home()),
                "JSON Files (*.json);;All Files (*)"
            )

        if file_path:
            self.selected_file = file_path
            self.file_path_label.setText(file_path)
            self.file_path_label.setStyleSheet(self.styles.file_path_label_new_style)
            self.action_button.setEnabled(True)

    def execute(self):
        if not self.selected_file:
            return

        if self.mode == "export":
            self.export_passwords()
        else:
            self.import_passwords()

    def export_passwords(self):
        try:
            export_data = {}

            if self.include_metadata.isChecked():
                from datetime import datetime

                export_data["_metadata"] = {
                    "exported_at": datetime.now().isoformat(),
                    "app_name": self.config.app_long_name,
                    "app_version": self.config.version,
                    "app_type": self.config.app_type,
                    "lib_name": self.config.lib_name,
                    "lib_version": self.config.lib_version,
                    "lib_lang": self.config.lib_lang,
                    "count": self.smart_pass_man.password_count
                }

            for public_key, sp in self.smart_pass_man.passwords.items():
                export_data[public_key] = sp.to_dict()

            indent = 2 if self.format_json.isChecked() else None
            separators = (',', ':') if self.format_minified.isChecked() else None

            with open(self.selected_file, 'w') as f:
                json.dump(export_data, f, indent=indent, separators=separators)

            self.sound_manager.play_notify()
            QMessageBox.information(
                self,
                "Export Successful",
                f"Successfully exported {self.smart_pass_man.password_count} passwords to:\n{self.selected_file}"
            )
            self.accept()

        except Exception as e:
            self.sound_manager.play_error()
            QMessageBox.critical(
                self,
                "Export Failed",
                f"Failed to export passwords:\n{str(e)}"
            )

    def import_passwords(self):
        try:
            with open(self.selected_file, 'r') as f:
                import_data = json.load(f)

            if "_metadata" in import_data:
                _ = import_data.pop("_metadata")

            added = 0
            skipped = 0

            for public_key, data in import_data.items():
                if not isinstance(data, dict) or 'public_key' not in data:
                    skipped += 1
                    continue

                if public_key in self.smart_pass_man.passwords:
                    skipped += 1
                    continue

                from smartpasslib import SmartPassword
                try:
                    sp = SmartPassword.from_dict(data)
                    self.smart_pass_man.add_smart_password(sp)
                    added += 1
                except:
                    skipped += 1

            self.sound_manager.play_notify()

            msg = f"Import completed:\n• Added: {added} new passwords\n• Skipped: {skipped} entries"
            if added > 0:
                msg += "\n\nRefresh the main window to see new passwords."

            QMessageBox.information(self, "Import Successful", msg)
            self.accept()

        except json.JSONDecodeError:
            self.sound_manager.play_error()
            QMessageBox.critical(
                self,
                "Import Failed",
                "Invalid JSON file format."
            )
        except Exception as e:
            self.sound_manager.play_error()
            QMessageBox.critical(
                self,
                "Import Failed",
                f"Failed to import passwords:\n{str(e)}"
            )
