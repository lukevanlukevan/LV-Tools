import os
import sys
import hou
import json
import time

from PySide2 import QtCore, QtUiTools, QtWidgets, QtGui
from PySide2.QtWidgets import QMenu, QApplication
from PySide2.QtGui import QCursor
# from PyQt5.QtCore import *
# from PyQt5.QtUiTools import *
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *


from gradientManager import gradientManager


class gradientManager(QtWidgets.QWidget):

    def __init__(self):
        super(gradientManager, self).__init__()

        self.folderpath = hou.getenv("LV") + "/scripts/python/gradientManager"
        self.gradFolder = self.folderpath + "/ramps"

        ui_file_path = self.folderpath + "/gradientManager.ui"

        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file_path)

        # self.rMenu = hou.qt.Menu()

        self.rampCount = 0

        self.rampNameBox = self.ui.findChild(QtWidgets.QLineEdit, "rampName")
        self.rampName = ""
        self.rampNameBox.editingFinished.connect(self.stringChanged)

        self.saveRampBtn = self.ui.findChild(QtWidgets.QPushButton, "saveRamp")
        self.saveRampBtn.clicked.connect(self.saveRamp)

        self.parmRow = self.ui.findChild(QtWidgets.QHBoxLayout, "parmRow")

        self.controlGroup = QtWidgets.QButtonGroup()
        self.toggleState = 'All'
        self.controlGroup.buttonClicked.connect(self.setToggle)

        self.all = QtWidgets.QPushButton("All")
        self.all.setCheckable(True)
        self.all.setWhatsThis("All")
        self.all.setChecked(True)
        self.float = QtWidgets.QPushButton("Float")
        self.float.setCheckable(True)
        self.float.setWhatsThis("False")
        self.color = QtWidgets.QPushButton("Color")
        self.color.setCheckable(True)
        self.color.setWhatsThis("True")

        self.controlGroup.addButton(self.color, 0)
        self.controlGroup.addButton(self.float, 1)
        self.controlGroup.addButton(self.all, 2)

        self.radio = self.ui.findChild(QtWidgets.QHBoxLayout, "toggleRow")
        self.radio.addWidget(self.all)
        self.radio.addWidget(self.float)
        self.radio.addWidget(self.color)

        # self.undoBtn = self.ui.findChild(QtWidgets.QPushButton, "undo")

        self.graphGrid = self.ui.findChild(QtWidgets.QGridLayout, "graphGrid")

        self.createInterface()  # run create interface

        mainLayout = QtWidgets.QVBoxLayout()

        self.gradGroup = QtWidgets.QButtonGroup()

        self.gradGroup.buttonClicked.connect(self.setGrad)

        self.loadRamps()

        mainLayout.addWidget(self.ui)
        self.setLayout(mainLayout)
        self.stringChanged()

    def setToggle(self, button):
        i = button.whatsThis()
        self.toggleState = i
        self.loadRamps()

    def savePrefs(self):
        prefs = {
            "difChecks": f"{self.difChecks.text()}"
        }
        with open(f"{self.folderpath}/ramps.json", "w") as outfile:
            json.dump(prefs, outfile)

    def createInterface(self):
        pass

    def gradActivate(self):
        pass

    def setGrad(self, button):
        i = button.whatsThis()

        node = hou.selectedNodes()[0]
        ramp_parms = [p for p in node.parms() if p.parmTemplate().type() == hou.parmTemplateType.Ramp]

        p = ramp_parms[0]

        if os.path.isfile(f"{self.gradFolder}/ramp{str(i).zfill(3)}.json"):

            with open(f"{self.gradFolder}/ramp{str(i).zfill(3)}.json", "r") as openfile:
                json_object = json.load(openfile)

                basis_type = json_object["ramp_basis"]
                basis = None
                types = [hou.rampBasis.Linear, hou.rampBasis.Constant, hou.rampBasis.CatmullRom, hou.rampBasis.MonotoneCubic, hou.rampBasis.Bezier, hou.rampBasis.BSpline, hou.rampBasis.Hermite]
                basis = types[basis_type]

                keys = json_object["ramp_keys"]

                new_keys = []
                for k in keys:
                    new_keys.append(k)

                values = json_object["ramp_values"]
                new_values = []

                for val in values:
                    if json_object['isColor'] == False:
                        new_values.append(val)
                    else:
                        test = tuple(val)
                        new_values.append(test)

                tvals = tuple(new_values)

                new_basis = (basis, ) * len(new_keys)

                new_ramp = hou.Ramp(new_basis, tuple(new_keys), tuple(new_values))

                if str(p.eval().isColor()) + " " + str(json_object['isColor']):
                    p.set(new_ramp)
                else:
                    pass

    def stringChanged(self):
        self.rampName = self.rampNameBox.text()

    def renameRamps(self):
        files = os.listdir(self.gradFolder)
        files.sort()
        i = 0
        for filename in files:
            f = os.path.join(self.gradFolder, filename)
            # checking if it is a file
            if os.path.isfile(f):
                os.rename(f, f'{self.gradFolder}/ramp{str(i).zfill(3)}.json')
                i += 1

    def saveRamp(self):

        self.stringChanged()
        self.rampCount += 1

        if len(hou.selectedNodes()) == 0:
            print("Please select a node")
        else:
            node = hou.selectedNodes()[0]
            ramp_parms = [p for p in node.parms() if p.parmTemplate().type() == hou.parmTemplateType.Ramp]

            p = ramp_parms[0]
            v = p.eval()
            keys = v.keys()
            ramp_basis = v.basis()[0]
            new_keys = []
            num_keys = len(v.basis())
            values = v.values()

            basis_type = 0
            if ramp_basis == hou.rampBasis.Linear:
                basis_type = 0
            elif ramp_basis == hou.rampBasis.Constant:
                basis_type = 1
            elif ramp_basis == hou.rampBasis.CatmullRom:
                basis_type = 2
            elif ramp_basis == hou.rampBasis.MonotoneCubic:
                basis_type = 3
            elif ramp_basis == hou.rampBasis.Bezier:
                basis_type = 4
            elif ramp_basis == hou.rampBasis.BSpline:
                basis_type = 5
            elif ramp_basis == hou.rampBasis.Hermite:
                basis_type = 6

            d = 100
            plot_values = [v.lookup(i/d) for i in range(d)]
            ramp = {
                "name": self.rampName,
                "isColor": v.isColor(),
                "ramp_basis": basis_type,
                "ramp_keys": keys,
                "ramp_values": values,
                "plot_values": plot_values
            }

            prefs = ramp
            dirfiles = os.listdir(self.gradFolder)
            it = len(dirfiles)
            with open(f"{self.gradFolder}/ramp{str(it).zfill(3)}.json", "w") as outfile:
                json.dump(prefs, outfile)

            self.loadRamps()
            self.rampNameBox.setText("")
            self.rampNameBox.setPlaceholderText(f'"Ramp {it}"')
            self.stringChanged()

    def loadRamps(self):

        count = self.graphGrid.count()
        for i in range(count):

            child = self.graphGrid.itemAt(0).widget()
            self.graphGrid.removeWidget(child)
            child.deleteLater()

        i = -1
        grid = self.ui.findChild(QtWidgets.QGridLayout, "graphGrid")

        self.tab = self.ui.findChild(QtWidgets.QWidget, "tab")

        tempi = 0
        files = os.listdir(self.gradFolder)
        files.sort()
        for filename in files:
            f = os.path.join(self.gradFolder, filename)
            # checking if it is a file
            if os.path.isfile(f):

                with open(f"{f}", "r") as openfile:
                    json_object = json.load(openfile)

                name = json_object["name"]

                keys = json_object["ramp_keys"]
                color = str(json_object["isColor"])

                if self.toggleState == color or self.toggleState == 'All':
                    i += 1

                    new_keys = []
                    for k in keys:
                        new_keys.append(float(k))

                    values = json_object["ramp_values"]  # .strip("()")

                    new_values = []
                    for val in values:
                        new_values.append(val)

                    self.gradHolder = QtWidgets.QWidget()
                    gradPolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
                    self.gradHolder.setSizePolicy(gradPolicy)

                    self.libItem = QtWidgets.QGridLayout()
                    self.libItem.setContentsMargins(5, 5, 5, 5)
                    self.itemThumb = QtWidgets.QPushButton()
                    self.itemThumb.setMinimumSize(100, 100)

                    gradStyle = ('''QWidget:hover:!pressed {
                                    background-color: rgba(255, 255, 255, 100);
                                }

                                ''')
                    self.gradHolder.setStyleSheet(gradStyle)
                    inColor = values[0]
                    outColor = values[-1]

                    kString = []
                    ki = -1
                    for k in keys:
                        ki += 1
                        kString.append(f'x{ki+1}: {float(ki)/(len(keys)-1)}, y{ki+1}: 0')

                    kString = ', '.join(kString)

                    vString = []
                    if json_object['isColor'] == False:
                        self.buttonLayout = QtWidgets.QGridLayout()
                        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
                        self.graph = GraphView(self.itemThumb, json_object['plot_values'])
                        self.graph.setRenderHint(QtGui.QPainter.Antialiasing)
                        self.graph.setMinimumSize(100, 100)
                        self.graph.setWhatsThis(str(i))
                        self.buttonLayout.addWidget(self.graph)
                        self.itemThumb.setLayout(self.buttonLayout)
                    else:
                        vi = -1
                        for val in values:
                            vi += 1
                            vString.append(f'stop: {float(vi)/(len(values)-1)} rgba({val[0]*255}, {val[1]*255}, {val[2]*255})')

                    vString = ', '.join(vString)

                    gradStyle = (f'QPushButton {{border: none; background-color: qlineargradient(spread: pad, x1: {keys[0]}, y1: 0, x2: {keys[-1]}, y2: 0, {str(vString)})}}')
                    self.itemThumb.setStyleSheet(gradStyle)
                    self.itemThumb.setWhatsThis(str(i))

                    self.libItem.addWidget(self.itemThumb, 0, 0, 1, 1)
                    self.gradHolder.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
                    self.gradHolder.customContextMenuRequested.connect(lambda: self.showContextMenu(self.gradHolder, QtGui.QCursor.pos(), i))
                    self.gradHolder.setWhatsThis(str(i))

                    self.itemLabel = QtWidgets.QLabel()
                    if name == "":
                        self.itemLabel.setText(f"Ramp {i+1}")
                    else:
                        self.itemLabel.setText(name)

                    self.itemLabel.setEnabled(False)
                    self.itemLabel.setStyleSheet('color: rgb(200, 200, 200);')

                    self.itemLabel.setAlignment(QtCore.Qt.AlignHCenter)

                    self.libItem.addWidget(self.itemLabel, 1, 0, 1, 1)

                    self.gradGroup.addButton(self.itemThumb, i)

                    self.gradHolder.setLayout(self.libItem)

                    self.graphGrid.addWidget(self.gradHolder, i/4, i % 4)

                    tempi = i+1

        self.rampCount = tempi
        self.stringChanged()

    def showContextMenu(self, widget, position, i):
        local_pos = position

        sel = -1

        # Iterate over all items in the layout
        for i in range(self.graphGrid.count()):
            # Get the widget of the current item
            widget = self.graphGrid.itemAt(i).widget()

            if widget.underMouse():
                sel = widget.whatsThis()

        contextMenu = QMenu()
        contextMenu.setStyleSheet('margin: 2px;')
        action1 = contextMenu.addAction("Rename Ramp")
        action2 = contextMenu.addAction("Delete Ramp")

        action = contextMenu.exec_(position)
        if action == action1:
            self.renameRamp(sel)
        if action == action2:
            self.deleteRamp(sel)

        # handle other actions...

    def renameRamp(self, i):
        clicked, val = hou.ui.readInput("Rename Ramp", buttons=('Rename', 'Cancel'), initial_contents='')
        # Load the JSON file
        with open(f'{self.gradFolder}/ramp{str(i).zfill(3)}.json', 'r') as f:
            data = json.load(f)

        # Change the name property
        data['name'] = val

        # Save the updated JSON file
        with open(f'{self.gradFolder}/ramp{str(i).zfill(3)}.json', 'w') as f:
            json.dump(data, f)

        self.loadRamps()

    def deleteRamp(self, i):

        QtCore.QCoreApplication.processEvents()

        child = self.graphGrid.itemAt(int(i)).widget()
        self.graphGrid.removeWidget(child)
        child.deleteLater()

        os.remove(f'{self.gradFolder}/ramp{str(i).zfill(3)}.json')
        # self.loadRamps()

        QtCore.QCoreApplication.processEvents()
        self.loadRamps()

        self.renameRamps()


class GraphView(QtWidgets.QGraphicsView):
    def __init__(self, parent, y_values):
        super().__init__()

        self.parent = parent

        self.y_values = y_values

        # set up the scene
        # self.Qview = QtWidgets.QGraphicsViewe
        self.setEnabled(False)
        self.scene = QtWidgets.QGraphicsScene(parent)
        self.setScene(self.scene)
        # self.height = self.height()
        self.height = 100*0.98

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.setStyleSheet("border: None;")

        # set up the pen for drawing the lines

        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50)))
        self.pen = QtGui.QPen(QtCore.Qt.white)
        self.pen.setWidth(2)

    def resizeEvent(self, event):
        # resize the scene to match the view

        # clear any existing items from the scene
        self.scene.clear()

        # calculate the x spacing
        num_points = len(self.y_values)
        x_spacing = self.width() / (num_points - 1)

        # draw the lines between the points
        for i in range(num_points - 1):
            x1 = i * x_spacing
            y1 = self.y_values[i]
            x2 = (i + 1) * x_spacing
            y2 = self.y_values[i + 1]
            line = QtWidgets.QGraphicsLineItem(x1, 1-y1*self.height, x2, 1-y2*self.height)
            line.setPen(self.pen)
            self.scene.addItem(line)
