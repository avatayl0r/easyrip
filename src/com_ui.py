from PyQt5.QtWidgets import QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap


class CommonUI:
    def push_button(self, text, conn) -> QPushButton:
        button = QPushButton(text)
        button.clicked.connect(conn)
        return button

    def line_edit(self, text, conn) -> QLineEdit:
        line_edit = QLineEdit()
        line_edit.setText(text)
        line_edit.textEdited.connect(conn)
        return line_edit

    def message_box(self) -> QMessageBox:
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText("Rip finished!")
        msg_box.setInformativeText(
            "Your download is completed!\n\nYou can now find your download in the downloads folder.")
        msg_box.setWindowTitle("Rip finished!")
        msg_box.setStandardButtons(QMessageBox.Ok)
        return msg_box


class UIProperties:
    def get_app_width() -> int:
        return 640

    def get_app_height() -> int:
        return 100

    def get_app_icon() -> QIcon:
        return QIcon(QPixmap(":/icons/easyrip_logo.png"))

    def get_version() -> str:
        return "1.0.0"
