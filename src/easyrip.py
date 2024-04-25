import sys
import os
import subprocess as subproc

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import (
    QLabel, QVBoxLayout, QDialog, QGroupBox, QWidget, QGridLayout, QMenuBar,
    QFileDialog)

import com_ui
import easyrip_config as config


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"Easyrip || Version {com_ui.UIProperties.get_version()}")
        self.setWindowIcon(com_ui.UIProperties.get_app_icon())
        self.setFixedSize(
            com_ui.UIProperties.get_app_width(),
            com_ui.UIProperties.get_app_height())

        with open(config.APP_STYLE, "r", encoding="UTF-8") as stylesheet:
            self.setStyleSheet(stylesheet.read())
        self.easyrip_ui = EasyripUI()
        self.setMenuBar(self.menu_bar())
        self.setCentralWidget(self.easyrip_ui)

    def menu_bar(self) -> QMenuBar:
        menubar = QMenuBar(self)

        file_menu = menubar.addMenu("File")

        output_action = file_menu.addAction("Output Location")
        output_action.triggered.connect(self.set_output_location)

        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.exit_app)

        help_menu = menubar.addMenu("Help")

        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.about_info)

        return menubar

    def set_output_location(self):
        filepath = QFileDialog.getExistingDirectory(
            self, "Select Directory")

        if not filepath:
            return False

        self.easyrip_ui.easyrip_instance.output_location = filepath
        self.easyrip_ui.current_output.setText(
            f"Output Location: '{filepath}'")

    def about_info(self):
        msg_box = com_ui.CommonUI.message_box(
            self,
            title = "About Easyrip",
            text = "Easyrip is a simple video downloader for YouTube, Instagram, etc.",
            info_text = f"""Version: v{com_ui.UIProperties.get_version()}
            \nDeveloped by: {com_ui.UIProperties.get_developer_name()}""")
        msg_box.exec_()

    def exit_app(self):
        self.close()


class EasyripUI(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.easyrip_instance = Easyrip(self)
        main_layout = self.setup_ui()
        self.setLayout(main_layout)

    def setup_ui(self) -> QVBoxLayout:
        main_layout = QVBoxLayout()

        self.current_output = QLabel(f"Output Location: '{self.easyrip_instance.output_location}'")
        tip = QLabel(
            "Please enter your URL below and press rip when ready to download!")
        input_group = self.setup_input_wdgt()

        text_group = QGroupBox()
        text_layout = QVBoxLayout()

        text_layout.addWidget(self.current_output)
        text_layout.addWidget(tip)

        text_group.setLayout(text_layout)

        main_layout.addWidget(text_group)
        main_layout.addWidget(input_group)

        return main_layout

    def setup_input_wdgt(self) -> QGroupBox:
        self.input_wdgt = QWidget()

        input_group = QGroupBox()
        input_layout = QGridLayout()

        self.url_entry = com_ui.CommonUI.line_edit(
            self,
            text="",
            placeholder="Enter URL here...",
            conn=self.easyrip_instance.url_changed)

        button = com_ui.CommonUI.push_button(
            self, "Rip", self.rip_from_url)

        input_layout.addWidget(QLabel("URL: "), 0, 0)
        input_layout.addWidget(self.url_entry, 0, 1)
        input_layout.addWidget(button, 0, 2)
        input_group.setLayout(input_layout)

        return input_group

    def rip_from_url(self) -> None:
        if not self.easyrip_instance.check_url():
            msg_box = com_ui.CommonUI.warning_box(
                self,
                title = "Empty URL!",
                text = "URL is empty!",
                info_text = "Please enter a URL to rip from!")
            msg_box.exec_()
            return False

        result = self.easyrip_instance.rip_from_url()
        if result:
            self.finished_rip()

    def finished_rip(self) -> None:
        msg_box = com_ui.CommonUI.message_box(
            self,
            title = "Finished Rip!",
            text = "Finished Rip!",
            info_text = f"""Please see '{self.easyrip_instance.output_location}' for the downloaded file!""")
        msg_box.exec_()
        self.url_entry.setText("")
        self.easyrip_instance.url_changed("")


class Easyrip:
    def __init__(self, easyrip_ui) -> None:
        self.easyrip_ui = easyrip_ui
        self.username = os.path.expanduser('~').replace("\\", "/")
        self.url = ""
        self.output_location = f"{self.username}/Downloads/"

    def url_changed(self, text) -> str:
        self.url = text
        return text

    def check_url(self) -> bool:
        if self.url == "":
            return False
        return True

    def rip_from_url(self) -> bool:
        cwd = os.getcwd()
        os.chdir(self.output_location)
        subproc.run(["yt-dlp.exe", self.url])
        os.chdir(cwd)
        return True


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
