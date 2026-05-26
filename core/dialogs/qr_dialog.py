# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
import json
import qrcode
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QApplication,
    QTextEdit
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage

from core.styles.theme_manager import ThemeManager


class QRDialog(QDialog):
    def __init__(self, parent=None, description="", public_key="", length=16, sound_manager=None):
        super().__init__(parent)
        self.setWindowTitle("QR Code Export")
        self.setMinimumWidth(500)
        self.setMaximumWidth(550)
        self.setModal(True)
        self.sound_manager = sound_manager

        self.description = description
        self.public_key = public_key
        self.length = length

        self.qr_data = {
            "l": length,
            "k": public_key
        }

        self.setStyleSheet(ThemeManager.get_input_style())

        self.setup_ui()
        self.center_dialog()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title_label = QLabel("QR Code for Smart Password")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(f"color: {ThemeManager.COLORS['primary']};")
        layout.addWidget(title_label)

        desc_label = QLabel("<b>Description:</b>")
        desc_label.setWordWrap(True)
        desc_label.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(desc_label)

        self.desc_text = QTextEdit()
        self.desc_text.setPlainText(self.description)
        self.desc_text.setReadOnly(True)
        self.desc_text.setMaximumHeight(40)
        self.desc_text.setMinimumHeight(20)
        self.desc_text.setStyleSheet(f"""
            QTextEdit {{
                background-color: {ThemeManager.COLORS['bg_medium']};
                color: {ThemeManager.COLORS['text_normal']};
                border: 1px solid {ThemeManager.COLORS['border']};
                border-radius: 4px;
                font-family: monospace;
                font-size: 11px;
            }}
        """)
        layout.addWidget(self.desc_text)

        length_label = QLabel(f"<b>Length:</b> {self.length} characters")
        length_label.setWordWrap(True)
        length_label.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(length_label)

        self.qr_label = QLabel()
        self.qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.qr_label.setStyleSheet("background: white; padding: 15px; border-radius: 8px;")
        self.generate_qr()
        layout.addWidget(self.qr_label)

        key_label = QLabel("<b>Public Key:</b>")
        key_label.setWordWrap(True)
        key_label.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(key_label)

        self.key_text = QTextEdit()
        self.key_text.setPlainText(self.public_key)
        self.key_text.setReadOnly(True)
        self.key_text.setMaximumHeight(40)
        self.key_text.setMinimumHeight(20)
        self.key_text.setStyleSheet(f"""
            QTextEdit {{
                background-color: {ThemeManager.COLORS['bg_medium']};
                color: {ThemeManager.COLORS['text_normal']};
                border: 1px solid {ThemeManager.COLORS['border']};
                border-radius: 4px;
                font-family: monospace;
                font-size: 10px;
            }}
        """)
        layout.addWidget(self.key_text)

        note_label = QLabel(
            '📲 Scan with <a href="https://github.com/smartlegionlab/smart-password-manager-android/releases" '
            f'style="color: {ThemeManager.COLORS["primary"]}; text-decoration: none;">Smart Password Manager Android</a>'
        )
        note_label.setOpenExternalLinks(True)
        note_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(note_label)

        button_layout = QHBoxLayout()

        self.copy_btn = QPushButton("📋 Copy JSON")
        self.copy_btn.clicked.connect(self.copy_json)
        self.copy_btn.setStyleSheet(ThemeManager.get_button_style('info'))
        button_layout.addWidget(self.copy_btn)

        copy_desc_btn = QPushButton("📝 Copy Description")
        copy_desc_btn.clicked.connect(self.copy_description)
        copy_desc_btn.setStyleSheet(ThemeManager.get_button_style('secondary'))
        button_layout.addWidget(copy_desc_btn)

        copy_key_btn = QPushButton("🔑 Copy Key")
        copy_key_btn.clicked.connect(self.copy_public_key)
        copy_key_btn.setStyleSheet(ThemeManager.get_button_style('secondary'))
        button_layout.addWidget(copy_key_btn)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        close_btn.setStyleSheet(ThemeManager.get_button_style('primary'))
        button_layout.addWidget(close_btn)

        layout.addLayout(button_layout)

    def generate_qr(self):
        try:
            qr_text = json.dumps(self.qr_data, separators=(',', ':'))

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=8,
                border=2,
            )
            qr.add_data(qr_text)
            qr.make(fit=True)

            qr_image = qr.make_image(fill_color="black", back_color="white")

            qr_image = qr_image.convert("RGB")
            width, height = qr_image.size
            bytes_per_line = 3 * width
            data = qr_image.tobytes()

            qimage = QImage(data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimage)

            pixmap = pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio,
                                   Qt.TransformationMode.SmoothTransformation)
            self.qr_label.setPixmap(pixmap)

        except Exception as e:
            self.qr_label.setText(f"Failed to generate QR code:\n{str(e)}")
            self.qr_label.setStyleSheet("color: red;")

    def copy_json(self):
        if self.sound_manager:
            self.sound_manager.play_click()

        clipboard = QApplication.clipboard()
        clipboard.setText(json.dumps(self.qr_data, separators=(',', ':')))

        original_text = self.copy_btn.text()
        self.copy_btn.setText("✅ Copied!")

        from threading import Timer
        Timer(1.5, lambda: self.copy_btn.setText(original_text)).start()

        if self.parent() and hasattr(self.parent(), 'show_status_message'):
            self.parent().show_status_message("QR data copied to clipboard", 2000)

    def copy_description(self):
        if self.sound_manager:
            self.sound_manager.play_click()

        clipboard = QApplication.clipboard()
        clipboard.setText(self.description)

        if self.parent() and hasattr(self.parent(), 'show_status_message'):
            self.parent().show_status_message("Description copied to clipboard", 2000)

    def copy_public_key(self):
        if self.sound_manager:
            self.sound_manager.play_click()

        clipboard = QApplication.clipboard()
        clipboard.setText(self.public_key)

        if self.parent() and hasattr(self.parent(), 'show_status_message'):
            self.parent().show_status_message("Public key copied to clipboard", 2000)

    def center_dialog(self):
        if self.parent():
            x = self.parent().x() + (self.parent().width() - self.width()) // 2
            y = self.parent().y() + (self.parent().height() - self.height()) // 2
            self.move(x, y)
