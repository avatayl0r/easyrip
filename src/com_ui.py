from PyQt5.QtWidgets import QLineEdit, QPushButton, QMessageBox, QMenuBar
from PyQt5.QtGui import QIcon, QPixmap

import easyrip_config as config

class CommonUI:
    def push_button(self, text, conn) -> QPushButton:
        button = QPushButton(text)
        button.clicked.connect(conn)
        return button

    def line_edit(self, text, placeholder, conn) -> QLineEdit:
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder)
        line_edit.setText(text)
        line_edit.textEdited.connect(conn)
        return line_edit

    def message_box(self, title, text, info_text) -> QMessageBox:
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(text)
        msg_box.setInformativeText(
            info_text)
        msg_box.setStandardButtons(QMessageBox.Ok)
        return msg_box

    def warning_box(self, title, text, info_text) -> QMessageBox:
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText(text)
        msg_box.setInformativeText(
            info_text)
        msg_box.setStandardButtons(QMessageBox.Ok)
        return msg_box


class UIProperties:
    def get_app_width() -> int:
        return config.APP_WIDTH

    def get_app_height() -> int:
        return config.APP_HEIGHT

    def get_app_icon() -> QIcon:
        return QIcon(QPixmap(config.APP_ICON))

    def get_version() -> str:
        return config.APP_VERSION

    def get_developer_name() -> str:
        return config.DEVELOPER_NAME
