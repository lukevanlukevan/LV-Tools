from PySide2 import QtWidgets, QtUiTools, QtCore, QtGui  # type: ignore
from PySide2.QtWidgets import QPushButton, QComboBox, QTableWidget, QTableWidgetItem  # type: ignore
import hou

import os
import json
from imp import reload  # type: ignore

import LVParmUtils
reload(LVParmUtils)

global direction
direction = 1

global loads


class lvnodeutils(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.folderpath = hou.getenv("LV") + "/scripts/python/lvnodeutils"
        ui_file_path = self.folderpath + "/lvnodeutils.ui"

        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file_path)

        # create initial

        global btnLayout
        global btnLayout2
        global hori

        hori = self.ui.findChild(QtWidgets.QPushButton, "hori")
        hori.setIcon(hou.qt.Icon('BUTTONS_flip_vertical'))
        hori.setText('Collapse')
        hori.clicked.connect(self.setDir)

        # btnLayout = QtWidgets.QVBoxLayout()
        btnLayout = self.ui.findChild(QtWidgets.QWidget, "vlayout").layout()
        # self.ui.findChild(QtWidgets.QGridLayout, "mainGrid").addLayout(btnLayout, 2, 0)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.ui)
        self.setLayout(layout)

        self.load_json()

        self.initBtns()

    def load_json(self):
        global loads
        file_path = self.folderpath + "/commands.json"
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                loads = json.load(f)
        else:
            with open(file_path, 'w') as f:
                loads = {}
                json.dump(loads, f)

    def initBtns(self):
        global btns

        btns = []

        # adding one million buttons
        addFloatParm = (QPushButton(hou.qt.Icon('DATATYPES_parameter'), "Add Float Parm"), "attribwrangle",  "Add Float Parm")
        addFloatParm[0].clicked.connect(lambda: LVParmUtils.addFloatParm(kwargs={"parms": (currentNode.parm("snippet"),)}))
        btns.append(addFloatParm)

        addChramp = (QPushButton(hou.qt.Icon('COP2_ramp'), "Add Float Ramp Parm"), "attribwrangle", "Add Float Ramp Parm")
        addChramp[0].clicked.connect(lambda: LVParmUtils.addChramp(kwargs={"parms": (currentNode.parm("snippet"),)}))
        btns.append(addChramp)

        cleanParms = (QPushButton(hou.qt.Icon('ENGINE_clean_temp'), "Remove unused parms"), "attribwrangle", "Remove unused parms")
        cleanParms[0].clicked.connect(lambda: LVParmUtils.cleanParms(kwargs={"parms": (currentNode.parm("snippet"),)}))
        btns.append(cleanParms)

        # for d in loads:
        #     label = d['label']
        #     icon = d['icon']
        #     command = d['command']
        #     new = d['node']

        #     btn = (QPushButton(hou.qt.Icon(icon), label), "attribwrangle", label)
        #     btn[0].clicked.connect(lambda: exec("lambda: LVParmUtils.addFloatParm(kwargs={'parms': (currentNode.parm('snippet'),)})"))
        #     btns.append(btn)

        for btn in btns:
            btnLayout.addWidget(btn[0])
            btn[0].hide()
            btn[0].setToolTip(btn[2])

        spacer = QtWidgets.QSpacerItem(0, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        btnLayout.addItem(spacer)

    def setDir(self):
        global direction
        d = direction
        direction = 0 if direction else 1
        if direction == 0:
            hori.setText('Expand')
            hori.setIcon(hou.qt.Icon('BUTTONS_flip_horizontal'))
        else:
            hori.setText('Collapse')
            hori.setIcon(hou.qt.Icon('BUTTONS_flip_horizontal'))
        for btn in btns:
            if direction == 1:
                btn[0].setText(btn[2])
                btn[0].setToolTip(btn[2])
            else:
                btn[0].setText('')
                btn[0].setToolTip(btn[2])
                btn[0].show()

            btn[0].setToolTip(btn[0].text())

    def getNode(self, node):
        self.buildUI(node)

    def buildUI(self, node):
        global currentNode

        currentNode = node
        selector = node.type().name()
        for btn in btns:
            condition = btn[1]
            widget = btn[0]
            if not selector == condition:
                widget.hide()
            else:
                widget.show()
