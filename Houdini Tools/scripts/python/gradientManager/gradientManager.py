import os
import sys
import hou
import json
import time

from PySide2 import QtCore, QtUiTools, QtWidgets, QtGui
# from PyQt5.QtCore import *
# from PyQt5.QtUiTools import *
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *


from gradientManager import gradientManager

class gradientManager(QtWidgets.QWidget):

    def __init__(self):
        super(gradientManager, self).__init__()

        self.folderpath =  hou.getenv("LV") + "/scripts/python/gradientManager"
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

        self.undoBtn = self.ui.findChild(QtWidgets.QPushButton, "undo")
        self.undoBtn.clicked.connect(self.undoRamp)

        self.graphGrid = self.ui.findChild(QtWidgets.QGridLayout, "graphGrid")

        self.createInterface() #run create interface

        mainLayout = QtWidgets.QVBoxLayout()

        self.gradGroup = QtWidgets.QButtonGroup()
        
        self.gradGroup.buttonClicked.connect(self.setGrad)

        self.loadRamps()

        mainLayout.addWidget(self.ui)
        self.setLayout(mainLayout)
        self.stringChanged()

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
        print(i)
        
        node = hou.selectedNodes()[0]
        ramp_parms = [p for p in node.parms() if p.parmTemplate().type() == hou.parmTemplateType.Ramp]

        p = ramp_parms[0]

        if os.path.isfile(f"{self.gradFolder}/ramp{i}.json"):

            with open(f"{self.gradFolder}/ramp{i}.json", "r") as openfile:
                json_object = json.load(openfile)

                basis_type = json_object["ramp_basis"]
                basis = None
                if basis_type == 0:
                    basis = hou.rampBasis.Linear
                elif basis_type == 1:
                    basis = hou.rampBasis.Constant
                elif basis_type == 2:
                    basis = hou.rampBasis.CatmullRom
                elif basis_type == 3:
                    basis = hou.rampBasis.MonotoneCubic
                elif basis_type == 4:
                    basis = hou.rampBasis.Bezier
                elif basis_type == 5:
                    basis = hou.rampBasis.BSpline
                elif basis_type == 6:
                    basis = hou.rampBasis.Hermite

                keys = json_object["ramp_keys"]

                new_keys = []
                for k in keys:
                    new_keys.append(k)

                values = json_object["ramp_values"]
                new_values = []

                for val in values:
                    test = tuple(val)
                    new_values.append(test)

                tvals = tuple(new_values)

                new_basis = (basis, ) * len(new_keys)

                new_ramp = hou.Ramp(new_basis, tuple(new_keys), tuple(new_values))
            
                p.set(new_ramp)

    def stringChanged(self):
        self.rampName =  self.rampNameBox.text()
        

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
            
            # print(values)

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

            plot_values = [v.lookup(i/50) for i in range(50)]
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
            with open(f"{self.gradFolder}/ramp{it}.json", "w") as outfile:
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
        for filename in os.listdir(self.gradFolder):
            f = os.path.join(self.gradFolder, filename)
            
            i += 1
            # checking if it is a file
            if os.path.isfile(f):

                with open(f"{f}", "r") as openfile:
                    json_object = json.load(openfile)

                name = json_object["name"]

                keys = json_object["ramp_keys"]

                new_keys = []
                for k in keys:
                    new_keys.append(float(k))

                values = json_object["ramp_values"] #.strip("()")

                new_values = []
                for val in values:
                    new_values.append(val)

                self.gradHolder = QtWidgets.QWidget()
                gradPolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
                self.gradHolder.setSizePolicy(gradPolicy)

                
                self.libItem = QtWidgets.QGridLayout()
                self.libItem.setContentsMargins(5, 5, 5, 5)
                self.itemThumb = QtWidgets.QPushButton()
                self.itemThumb.setMinimumSize(100,100)

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
                    kString.append(f'x{ki+1}:{float(ki)/(len(keys)-1)}, y{ki+1}:0')

                kString = ', '.join(kString)

                vString = []
                if json_object['isColor'] == False:
                    self.buttonLayout = QtWidgets.QGridLayout()
                    self.buttonLayout.setContentsMargins(0,0,0,0)
                    self.graph = GraphView(self.itemThumb, json_object['plot_values'])
                    self.graph.setRenderHint(QtGui.QPainter.Antialiasing)
                    self.graph.setMinimumSize(100,100)
                    self.graph.setWhatsThis(str(i))
                    self.buttonLayout.addWidget(self.graph)
                    self.itemThumb.setLayout(self.buttonLayout)
                    # self.graph.setStyleSheet("pointer-events: none;")
                else:
                    vi = -1
                    for val in values:
                        vi += 1
                        vString.append(f'stop: {float(vi)/(len(values)-1)} rgba({val[0]*255}, {val[1]*255}, {val[2]*255})')

                vString = ', '.join(vString)

                gradStyle = (f'QPushButton {{background-color: qlineargradient(spread:pad, x1:{keys[0]}, y1:0, x2:{keys[-1]}, y2:0, {str(vString)}); border: none; }}')
                self.itemThumb.setStyleSheet(gradStyle)
                self.itemThumb.setWhatsThis(str(i))

                # if json_object['isColor'] == False:
                #     # self.libItem.addWidget(self.graph)
                # else:
                self.libItem.addWidget(self.itemThumb, 0, 0, 1, 1)

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

                self.graphGrid.addWidget(self.gradHolder, i/4, i%4)

                tempi = i+1

        self.rampCount = tempi
        self.stringChanged()

    def undoRamp(self):
        
        count = self.graphGrid.count()
        
        QtCore.QCoreApplication.processEvents()
        index = len(os.listdir(self.gradFolder))
        if index == count:
            if index == 0:
                pass
            else:
                
                for i in range(count):

                    child = self.graphGrid.itemAt(0).widget()
                    self.graphGrid.removeWidget(child)
                    child.deleteLater()

                os.remove(f'{self.gradFolder}/ramp{index-1}.json')
                self.loadRamps()

        QtCore.QCoreApplication.processEvents()

    # def mouseReleaseEvent(self, event):
    #     print('mouse released')

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

        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(50,50,50)))
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