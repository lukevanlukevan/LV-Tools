import os
import sys
import hou
import json

from hutil.PySide import QtCore, QtUiTools, QtWidgets, QtGui
# from PyQt5.QtCore import *
# from PyQt5.QtUiTools import *
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *

from PBRBuilder import PBRBuilder

class PBRBuilder(QtWidgets.QWidget):

    def __init__(self):
        super(PBRBuilder, self).__init__()

        self.folderpath =  hou.getenv("LV") + "/scripts/python/PBRBuilder"

        ui_file_path = self.folderpath + "/PBRBuilder.ui"

        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file_path)

        self.grid = self.ui.findChild(QtWidgets.QGridLayout, "gridLayout_3")
        self.grid2 = self.ui.findChild(QtWidgets.QGridLayout, "gridLayout5")
        self.graphGrid = self.ui.findChild(QtWidgets.QGridLayout, "graphGrid")


        self.diffTex = self.ui.findChild(QtWidgets.QLineEdit, "path0")
        self.roughTex = self.ui.findChild(QtWidgets.QLineEdit, "path1")
        self.bumpTex = self.ui.findChild(QtWidgets.QLineEdit, "path2")
        self.extraTex = self.ui.findChild(QtWidgets.QLineEdit, "path3")


        self.diffSpace = self.ui.findChild(QtWidgets.QComboBox, "diffSpace")
        self.roughSpace = self.ui.findChild(QtWidgets.QComboBox, "roughSpace")
        self.bumpSpace = self.ui.findChild(QtWidgets.QComboBox, "bumpSpace")
        self.extraSpace = self.ui.findChild(QtWidgets.QComboBox, "extraSpace")

        self.matnetBtn = self.ui.findChild(QtWidgets.QRadioButton, "matStyle1")
        self.matBtn = self.ui.findChild(QtWidgets.QRadioButton, "matStyle2")

        self.buildMatBtn = self.ui.findChild(QtWidgets.QPushButton, "buildMat")

        self.matStyleGroup = QtWidgets.QButtonGroup()
        self.matStyleGroup.addButton(self.matnetBtn, 0)
        self.matStyleGroup.addButton(self.matBtn, 1)

        self.matStyleGroup.idClicked.connect(self.matStyleSet)

        self.matStyle = 0
        
        self.buildMatBtn.clicked.connect(self.buildMaterial)

        self.saveBtn = self.ui.findChild(QtWidgets.QPushButton, "save")
        self.saveBtn.clicked.connect(self.setPrefs)

        self.spaces = []
        self.spaces.append(self.diffSpace)
        self.spaces.append(self.roughSpace)
        self.spaces.append(self.bumpSpace)
        self.spaces.append(self.extraSpace)

        self.createInterface() #run create interface

        mainLayout = QtWidgets.QVBoxLayout()

        mainLayout.addWidget(self.ui)

        rowCount = self.grid.rowCount()

        self.btnGroup = QtWidgets.QButtonGroup()
        self.btnGroup.buttonClicked.connect(self.fileTriggered)
        self.currentTex = None
        self.texpath = None

        for i in range(rowCount):
            self.filepicker = hou.qt.FileChooserButton()
            self.filepicker.setFileChooserStartDirectory(hou.getenv("HIP"))
            self.filepicker.setFileChooserFilter(hou.fileType.Image)
            self.filepicker.setWhatsThis(str(i))
            self.btnGroup.addButton(self.filepicker)

            self.filepicker.fileSelected.connect(self.onFileSelected)
            self.grid.addWidget(self.filepicker, i, 2)

        self.grid.setColumnStretch(1, 1)

        for i in range(10):
            self.grad = QtWidgets.QWidget()
            gradStyle = (' QWidget {background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));}')
            self.grad.setStyleSheet(gradStyle)
            self.grad.setMinimumHeight(100)
            # self.grad.setMinimumSize(200,200)
            # self.grad.setMaximumSize(200,200)

            self.button = QtWidgets.QPushButton(f"Test {i}")

            self.graphGrid.addWidget(self.grad, i/4, i%4)

        self.fillComboBox(self.spaces)

        self.setLayout(mainLayout)

        self.loadPrefs()

    def fillPath(self, index):
        item = self.ui.findChild(QtWidgets.QLineEdit, f"path{index}")
        item.setText(self.texpath)

    def fileTriggered(self, button):
        self.currentTex = button.whatsThis()
        self.fillPath(self.currentTex)

    def onFileSelected(self, file_path):
        self.texpath = file_path

    def setPrefs(self):
        prefs = {
            "diffSpace": f"{self.diffSpace.currentText()}",
            "roughSpace": f"{self.roughSpace.currentText()}",
            "bumpSpace": f"{self.bumpSpace.currentText()})",
            "extraSpace": f"{self.extraSpace.currentText()}",
            "matStyle": f"{self.matStyle}"
        }
        with open(f"{self.folderpath}/prefs.json", "w") as outfile:
            json.dump(prefs, outfile)

    def loadPrefs(self):
        if os.path.isfile(f"{self.folderpath}/prefs.json"):

            #start setting from prefs
            with open(f"{self.folderpath}/prefs.json", "r") as openfile:
                json_object = json.load(openfile)

            self.diffSpace.setCurrentText(str(json_object["diffSpace"]))
            self.roughSpace.setCurrentText(str(json_object["roughSpace"]))
            self.bumpSpace.setCurrentText(str(json_object["bumpSpace"]))
            self.extraSpace.setCurrentText(str(json_object["extraSpace"]))
            if str(json_object["matStyle"]) == "1":
                self.matBtn.setChecked(True)
                self.matStyle = 1


    def createInterface(self):
        pass
        
    def fillComboBox(self, boxes):
        for box in boxes:
            myList = hou.hscript("Redshift_getOcioColorSpacesForSolaris")

            items = myList[0].split(",")
            items = list(dict.fromkeys(items))

            for item in items:
                box.addItem(item)
            
            box.removeItem(0)

    def matStyleSet(self, id):
        self.matStyle = id

    def buildMaterial(self):

        if self.matStyle == 0:
            pass
            # build matnet
        else:
            #build /mat
            mat = hou.node("/mat")
            builder = mat.createNode("redshift_vopnet")
            builder.moveToGoodPosition()
            bpath = builder.path()

            material = hou.node(f"{bpath}/StandardMaterial1")
            mPos = material.position()

            inputIndex = ['base_color', "refl_roughness", "bump_input", "overall_color"]
            for i in range(0, 4):
                tex = builder.createNode('redshift::TextureSampler')
                tex.setPosition(hou.Vector2(mPos.x()-6, mPos.y()-(2*i)))
                tex.setParms({"tex0": self.ui.findChild(QtWidgets.QLineEdit, f"path{i}").text(),})

                if i == 3:
                    bump = builder.createNode('redshift::BumpMap')
                    bump.setInput(0, tex)
                    bump.setPosition(hou.Vector2(mPos.x()-3, mPos.y()-(2*i)))
                    material.setNamedInput(inputIndex[i], bump, 0)
                else:
                    material.setNamedInput(inputIndex[i], tex, 0)

