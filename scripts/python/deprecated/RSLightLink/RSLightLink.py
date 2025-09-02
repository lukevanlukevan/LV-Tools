import os
import sys
import hou
import json

from hutil.PySide import QtCore, QtUiTools, QtWidgets, QtGui
from hutil.PySide.QtWidgets import (
    QGridLayout,
    QLineEdit,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QButtonGroup,
    QCheckBox,
)


from RSLightLink import RSLightLink

loader = QtUiTools.QUiLoader()


class RSLightLink(QtWidgets.QWidget):
    def __init__(self):
        super(RSLightLink, self).__init__()

        self.folderpath = os.path.abspath(os.path.dirname(__file__))

        ui_file_path = self.folderpath + "/RSLightLink.ui"

        self.ui = loader.load(ui_file_path)

        self.maingrid = self.ui.findChild(QGridLayout, "mainGrid")

        self.lightlink = self.ui.findChild(QLineEdit, "lightLink")
        self.lightlink.textChanged.connect(self.fillList)

        self.syncBtn = self.ui.findChild(QPushButton, "syncButton")
        self.syncBtn.clicked.connect(self.addLightLink)

        self.incBtn = self.ui.findChild(QPushButton, "inc")
        self.excBtn = self.ui.findChild(QPushButton, "exc")

        self.toggleGroup = QButtonGroup()
        self.toggleGroup.addButton(self.incBtn, 1)
        self.toggleGroup.addButton(self.excBtn, 0)
        self.toggleGroup.setExclusive(True)
        self.toggleGroup.idClicked.connect(self.toggle)

        self.nodepaths = []
        self.shadownodepaths = []
        self.node = None

        self.toggleState = 0

        mainLayout = QtWidgets.QVBoxLayout()

        # self.setStyleSheet('border: 1px solid')

        mainLayout.addWidget(self.ui)
        self.setLayout(mainLayout)

    def createInterface(self):
        pass

    def setLink(self):
        lightnames = [
            "rslight",
            "rslightsun",
            "rslightdome",
            "rslightportal",
            "rslighties",
        ]
        try:
            self.node = hou.selectedNodes()[0]
            if any(self.node.type().name() == x for x in lightnames):
                self.addLightLink()
            else:
                for widget in range(self.maingrid.count()):
                    d = self.maingrid.takeAt(0)
                    d.widget().deleteLater()
        except:
            pass

    def toggle(self, id):
        id = id
        self.toggleState = id
        for btn in self.toggleGroup.buttons():
            btn.setStyleSheet("color: #161616")
        self.toggleGroup.button(id).setStyleSheet("color: #e5e5e5")
        for widget in range(self.maingrid.count()):
            d = self.maingrid.takeAt(0)
            d.widget().deleteLater()
        self.fillList()

    def addLightLink(self):
        # try:

        gList = (
            self.node.parm("RSL_lightLinking").eval().replace("^", "").replace("*", "")
        )
        gList = gList.split(" ")
        self.nodepaths = [x for x in gList if x != ""]

        sList = (
            self.node.parm("RSL_shadowLinking").eval().replace("^", "").replace("*", "")
        )
        sList = sList.split(" ")
        self.shadownodepaths = [x for x in gList if x != ""]

        self.lightlink.setText(hou.selectedNodes()[0].path())
        self.node = hou.node(self.lightlink.text())

    def fillList(self):
        for widget in range(self.maingrid.count()):
            d = self.maingrid.takeAt(0)
            d.widget().deleteLater()

        geo = hou.node("/obj").children()

        i = 0
        for node in geo:
            if node.type().name() == "geo":
                if node.path() in self.nodepaths:
                    if node.path() in self.shadownodepaths:
                        item = ItemWidget(self, node, True, True)
                    else:
                        item = ItemWidget(self, node, True, False)
                else:
                    if node.path() in self.shadownodepaths:
                        item = ItemWidget(self, node, False, True)
                        print("in l and in s")
                    else:
                        item = ItemWidget(self, node, False, False)

                self.maingrid.addWidget(item, i, 0)
                i += 1


class ItemWidget(QtWidgets.QWidget):
    def __init__(self, parent, node, lightstate, shadowstate):
        super().__init__()

        self.main = parent

        self.setContentsMargins(0, 0, 0, 0)

        self.folderpath = os.path.abspath(os.path.dirname(__file__))
        self.itemWidget = loader.load(self.folderpath + "/item.ui")

        self.lightBtn = self.itemWidget.findChild(QPushButton, "light")
        self.shadowBtn = self.itemWidget.findChild(QPushButton, "shadow")
        self.lightBtn.toggled.connect(self.lightStateChanged)
        self.shadowBtn.toggled.connect(self.shadowStateChanged)

        if lightstate == True:
            pass
            # self.toggleLight(self.state)

        layout = self.itemWidget.findChild(QHBoxLayout)

        name = node.name()

        hicon = node.type().icon()
        qticon = hou.qt.Icon(hicon)

        self.path = node.path()

        if lightstate == True:
            self.lightBtn.setChecked(True)
        else:
            self.lightBtn.setIcon(QtGui.QIcon(self.main.folderpath + "/icon/on.png"))

        if shadowstate == True:
            self.shadowBtn.setChecked(True)
        else:
            self.shadowBtn.setIcon(QtGui.QIcon(self.main.folderpath + "/icon/on.png"))

        label = self.itemWidget.findChild(QLabel, "label")
        icon = self.itemWidget.findChild(QLabel, "icon")
        label.setText(name)
        icon.setPixmap(qticon.pixmap(16, 16))

        self.setLayout(layout)

    def lightStateChanged(self, checked):
        state = checked
        if state == True:
            if self.path in self.main.nodepaths:
                pass
            else:
                self.main.nodepaths.append(self.path)

            # self.lightBtn.setStyleSheet('color:hsl(0, 100%, 55%)')
            self.lightBtn.setText("Light Excluded")
            self.lightBtn.setIcon(QtGui.QIcon(self.main.folderpath + "/icon/off.png"))

        else:
            self.main.nodepaths.remove(self.path)
            # self.lightBtn.setStyleSheet('color:hsl(0,0,52%)')
            self.lightBtn.setText("Light Included")
            self.lightBtn.setIcon(QtGui.QIcon(self.main.folderpath + "/icon/on.png"))

        newpaths = []

        for path in self.main.nodepaths:
            newpaths.append("^" + path)
        newlinks = "* " + " ".join(newpaths)

        self.main.node.parm("RSL_lightLinking").set(newlinks)

    def shadowStateChanged(self, checked):
        state = checked
        if state == True:
            if self.path in self.main.shadownodepaths:
                pass
            else:
                self.main.shadownodepaths.append(self.path)

            # self.shadowBtn.setStyleSheet('color:hsl(0, 100%, 55%)')
            self.shadowBtn.setText("Shadow Excluded")
            self.shadowBtn.setIcon(QtGui.QIcon(self.main.folderpath + "/icon/off.png"))

        else:
            self.main.shadownodepaths.remove(self.path)
            # self.shadowBtn.setStyleSheet('color:hsl(0,0,52%)')
            self.shadowBtn.setText("Shadow Included")
            self.shadowBtn.setIcon(QtGui.QIcon(self.main.folderpath + "/icon/on.png"))

        newpaths = []

        for path in self.main.shadownodepaths:
            newpaths.append("^" + path)
        newlinks = "* " + " ".join(newpaths)

        self.main.node.parm("RSL_shadowLinking").set(newlinks)

