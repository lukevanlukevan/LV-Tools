from hutil.Qt import QtWidgets, QtUiTools
from PySide2.QtWidgets import QPushButton
import hou
from imp import reload
from LVUtils import colorControl


class LVButton(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.folderpath = hou.getenv("LV") + "/scripts/python/LVButton"
        ui_file_path = self.folderpath + "/LVButton.ui"

        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file_path)

        self.btn = self.ui.findChild(QPushButton, "btn")
        self.btn.clicked.connect(self.message_log)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.ui)
        self.setLayout(layout)

    def message_log(self):
        colorControl()
