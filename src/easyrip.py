import sys
import os
import subprocess as subproc

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QDialog, QGroupBox, QWidget, QGridLayout

import com_ui


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"Easyrip || Version {com_ui.UIProperties.get_version()}")
        self.setWindowIcon(com_ui.UIProperties.get_app_icon())
        self.setFixedSize(
            com_ui.UIProperties.get_app_width(),
            com_ui.UIProperties.get_app_height())

        self.setCentralWidget(EasyripUI())


class EasyripUI(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.easyrip_instance = Easyrip(self)
        main_layout = self.setup_ui()
        self.setLayout(main_layout)

    def setup_ui(self) -> QVBoxLayout:
        main_layout = QVBoxLayout()

        tip = QLabel(
            "Please enter your URL below and press rip when ready to download!")
        input_group = self.setup_input_wdgt()

        main_layout.addWidget(tip)
        main_layout.addWidget(input_group)

        return main_layout

    def setup_input_wdgt(self) -> QGroupBox:
        self.input_wdgt = QWidget()

        input_group = QGroupBox()
        input_layout = QGridLayout()

        self.url_entry = com_ui.CommonUI.line_edit(
            self, "", self.easyrip_instance.url_changed)
        button = com_ui.CommonUI.push_button(
            self, "Rip", self.easyrip_instance.rip_from_url)

        input_layout.addWidget(QLabel("URL: "), 0, 0)
        input_layout.addWidget(self.url_entry, 0, 1)
        input_layout.addWidget(button, 0, 2)
        input_group.setLayout(input_layout)

        return input_group

    def finished_rip(self) -> None:
        self.msg_box = com_ui.CommonUI.message_box(self)
        self.msg_box.exec_()


class Easyrip:
    def __init__(self, easyrip_ui) -> None:
        self.easyrip_ui = easyrip_ui
        self.username = os.path.expanduser('~').replace("\\", "/")
        self.url = ""
        self.output_location = f"{self.username}/Downloads/"

    def url_changed(self, text) -> None:
        self.url = text

    def rip_from_url(self) -> None:
        cwd = os.getcwd()
        os.chdir(self.output_location)
        subproc.run(["yt-dlp.exe", self.url])
        os.chdir(cwd)

        self.easyrip_ui.finished_rip()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
