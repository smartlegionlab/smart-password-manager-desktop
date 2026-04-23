

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
