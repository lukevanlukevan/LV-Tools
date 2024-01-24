import os
import sys
import hou
import json

from PySide2 import QtCore, QtUiTools, QtWidgets, QtGui
from PySide2.QtWidgets import QGridLayout

from easeManager import easeManager


class easeManager(QtWidgets.QWidget):

    def __init__(self):
        super(easeManager, self).__init__()

        self.folderpath = os.path.dirname(os.path.realpath(__file__))

        ui_file_path = self.folderpath + "/easeManager.ui"

        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file_path)

        self.swatchGrid = self.ui.findChild(QtWidgets.QGridLayout, "swatchGrid")

        for i in range(0, 10):
            btn = QtWidgets.QPushButton(f"Button {i}")
            btn.clicked.connect(lambda: print(f"Clicked Button: {i}"))
            self.swatchGrid.addWidget(btn, i, 0)

        # Needed stuff

        mainLayout = QtWidgets.QVBoxLayout()

        mainLayout.addWidget(self.ui)
        self.setLayout(mainLayout)
