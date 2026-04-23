

class MainWindowStyles:
    label_logo_style = "color: #2a82da;"
    count_label_style = "color: #888;"
    line_style = "color: #444;"
    copyright_label_style = "color: #888; font-size: 16px;"
    table_widget_style = """
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
        """
    btn_new_password_style = """
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
        """
    btn_exit_style = """
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
        """
    help_label_style = """
            QLabel {
                background-color: #2a2a2a;
                padding: 15px;
                border-radius: 5px;
            }
            a {
                color: #2a82da;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        """
    ok_button_style = """
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
        """
    get_button_style = """
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
        """
    edit_button_style = """
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
        """
    delete_button_style = """
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
        """

class DesktopEntryDialogStyles:
    title_label_style = "color: #2a82da; margin: 10px;"
    note_label_style = "color: #0d47a1; background-color: #e3f2fd; padding: 8px; border-radius: 5px;"
    create_btn_style = """
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
        """
    cancel_btn_style = """
            QPushButton {
                background-color: #666;
                color: white;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """

class  EditPasswordDialogStyles:
    length_warning_style = "color: #ff9800; font-style: italic;"
    note_style = "color: #888;"
    submit_button_style = "background-color: #ff9800; color: white;"


class ExportImportDialogStyles:
    instruction_style = "color: #aaa; padding: 5px;"
    file_path_label_style = "color: #888; font-style: italic;"
    warning_style = "color: #ff9800; background-color: #332200; padding: 8px; border-radius: 4px;"
    action_button_export_style = "background-color: #2a82da; color: white;"
    action_button_import_style = "background-color: #ff9800; color: white;"
    file_path_label_new_style = "color: #2a82da;"


class PasswordDisplayDialogStyles:
    password_display_style = """
            QLineEdit {
                font-family: monospace;
                font-size: 14px;
                padding: 8px;
                background-color: #2a2a2a;
                border: 1px solid #444;
                border-radius: 4px;
            }
        """
    note_style = "color: #888;"
    copy_button_style = "background-color: #2e7d32; color: white;"


class PasswordInputDialogStyles:
    secret_example_label_style = "color: #888; font-size: 11px; font-style: italic;"
    secret_warning_label_style = "color: #e74c3c; font-size: 11px;"
    submit_button_style = "background-color: #2a82da; color: white;"


class SecretInputDialogStyles:
    submit_button_style = "background-color: #2a82da; color: white;"
