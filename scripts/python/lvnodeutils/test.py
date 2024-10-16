# from hutil.Qt import QtWidgets, QtUiTools,
from PySide2 import QtWidgets, QtUiTools, QtCore, QtGui
from PySide2.QtWidgets import QPushButton, QComboBox, QTableWidget, QTableWidgetItem
import hou
import os
import json
from importlib import reload

import LVParmUtils
reload(LVParmUtils)


class lvnodeutils(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.folderpath = hou.getenv("LV") + "/scripts/python/lvnodeutils"
        ui_file_path = self.folderpath + "/lvnodeutils.ui"

        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file_path)

        # create initial

        global btnLayout

        btnLayout = self.ui.findChild(QtWidgets.QVBoxLayout, "btnLayout")
        btnLayout = self.ui.findChild(QtWidgets.QVBoxLayout, "btnLayout")

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.ui)
        self.setLayout(layout)

    def getNode(self, node):
        print(node)

    def buildUI(self):
        # create buttons

        btns = []

        addFloatParm = QPushButton("Add Float Parm")
        # addFloatParm.clicked.connect(LVParmUtils.addFloatParm(kwargs={"node": hou.selectedNodes()[0]}))
        btns.append(addFloatParm)

        for btn in btns:
            btnLayout.addWidget(btn)

        # end create buttons

        spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        btnLayout.addItem(spacer)
