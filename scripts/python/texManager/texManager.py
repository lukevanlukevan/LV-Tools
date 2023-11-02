import os
import sys
import hou
import json

from hutil.Qt import QtCore, QtUiTools, QtWidgets, QtGui
# from PyQt5.QtCore import *
# from PyQt5.QtUiTools import *
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *

from texManager import texManager

class TexManager(QtWidgets.QWidget):

    def __init__(self):
        super(TexManager, self).__init__()

        self.nodes = hou.vopNodeTypeCategory().nodeType("redshift::TextureSampler").instances() 

        self.folderpath =  hou.getenv("LV") + "/scripts/python/texManager"

        ui_file_path = self.folderpath + "/texManager.ui"

        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file_path)

        self.setspacebtn = self.ui.findChild(QtWidgets.QPushButton, "setSpace")
        self.spaceDropBox = self.ui.findChild(QtWidgets.QComboBox, "spaceDrop")  
        self.spaceDropBoxRaw = self.ui.findChild(QtWidgets.QComboBox, "spaceDropRaw")
        self.difChecks = self.ui.findChild(QtWidgets.QLineEdit, "difChecks")
        self.rawChecks = self.ui.findChild(QtWidgets.QLineEdit, "rawChecks")
        self.saveBtn = self.ui.findChild(QtWidgets.QPushButton, "save")
        self.nodeTable = self.ui.findChild(QtWidgets.QTableWidget, "nodeTable")
        self.reloadBtn = self.ui.findChild(QtWidgets.QPushButton, "reload")


        #create connections

        self.setspacebtn.clicked.connect(self.setSpace)
        self.spaceDropBox.currentTextChanged.connect(self.updateNodes)
        self.spaceDropBoxRaw.currentTextChanged.connect(self.updateNodes)
        self.difChecks.editingFinished.connect(self.updateNodes)
        self.rawChecks.editingFinished.connect(self.updateNodes)
        self.saveBtn.clicked.connect(self.setPrefs)
        self.nodeTable.cellDoubleClicked.connect(self.selectedCell)
        self.reloadBtn.clicked.connect(self.updateNodes)

        #declare "global variables as self.var"
        self.createInterface()

        mainLayout = QtWidgets.QVBoxLayout()

        mainLayout.addWidget(self.ui)
        self.setLayout(mainLayout)

    def updateNodes(self):
        self.nodes = hou.vopNodeTypeCategory().nodeType("redshift::TextureSampler").instances()
        rows = self.nodeTable.rowCount()
        for i in range(rows):
            self.nodeTable.removeRow(0)
        self.setTable()
        
    def selectedCell(self, row, col):
        pane_tab = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)

        item = self.nodeTable.item(row, 5).text()
        sel = hou.item(item)

        pane_tab.setCurrentNode(sel, True)
        
        sel.setSelected("on", True)
    
    def spaceCheck(self, node):

        colorParms = self.difChecks.text()
        colorStrip = colorParms.strip()
        rawParms = self.rawChecks.text()
        rawStrip = rawParms.strip()
        dif = colorStrip.split(", ")
        raw = rawStrip.split(", ")
        parm = node.parm("tex0").eval()
        if parm == "":
            node.setParms({"tex0_colorSpace": "Auto",})       
        else:
            if any(trigger in parm for trigger in dif):
                return "dif"
            elif any(trigger in parm for trigger in raw):
                return "raw"
            else:
                pass

    def setSpace(self):

        for node in self.nodes:
            space = self.spaceCheck(node)
            if space == "dif":
                node.setParms({"tex0_colorSpace": self.spaceDropBox.currentText(),})
            elif space == "raw":
                node.setParms({"tex0_colorSpace": self.spaceDropBoxRaw.currentText(),})

        self.updateNodes()

    def setPrefs(self):
        prefs = {
            "difChecks": f"{self.difChecks.text()}",
            "difCS": f"{self.spaceDropBox.currentText()}",
            "rawChecks": f"{self.rawChecks.text()}",
            "rawCS": f"{self.spaceDropBoxRaw.currentText()}"
        }
        with open(f"{self.folderpath}/prefs.json", "w") as outfile:
            json.dump(prefs, outfile)

    def createInterface(self):
        myList = hou.hscript("Redshift_getOcioColorSpacesForSolaris")

        items = myList[0].split(",")
        items = list(dict.fromkeys(items))
        for item in items:
            self.spaceDropBox.addItem(item)
            self.spaceDropBoxRaw.addItem(item)
        
        self.spaceDropBox.removeItem(0)
        self.spaceDropBoxRaw.removeItem(0)
        #end base setup
        
        if os.path.isfile(f"{self.folderpath}/prefs.json"):

            #start setting from prefs
            with open(f"{self.folderpath}/prefs.json", "r") as openfile:
                json_object = json.load(openfile)
            
            self.difChecks.setText(str(json_object["difChecks"]))
            self.rawChecks.setText(str(json_object["rawChecks"]))

            self.spaceDropBox.setCurrentText(str(json_object["difCS"]))
            self.spaceDropBoxRaw.setCurrentText(str(json_object["rawCS"]))

        #add rows
        # self.setTable()
        

    def setTable(self):

        rowPosition = self.nodeTable.rowCount()
        for node in self.nodes:
            self.nodeTable.insertRow(rowPosition)
            self.nodeTable.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(f"{node.name()}"))
            fullName = node.parm('tex0').eval()
            texName = fullName.split('/')[-1]
            self.nodeTable.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(f"{texName}"))
            
            cs = node.parm('tex0_colorSpace').eval()
            if cs == "":
                self.nodeTable.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem("Auto"))
            else:
                self.nodeTable.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(cs))

            space = self.spaceCheck(node)
            if space == "dif":
                self.nodeTable.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(f"{self.spaceDropBox.currentText()}"))
            elif space == "raw":
                self.nodeTable.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(f"{self.spaceDropBoxRaw.currentText()}"))
            else:
                self.nodeTable.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(f"Auto"))
            if self.nodeTable.item(rowPosition, 2).text() == self.nodeTable.item(rowPosition, 3).text():
                pass
            else:
                font = QtGui.QFont()
                font.setBold(True)
                self.nodeTable.item(rowPosition, 3).setFont(font)
                
            self.nodeTable.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(f"{fullName}"))

            self.nodeTable.setItem(rowPosition, 5, QtWidgets.QTableWidgetItem(node.path()))

            rowPosition += 1
        
        # self.nodeTable.setColumnHidden(3,True)
        self.nodeTable.setColumnHidden(5,True)
        header = self.nodeTable.horizontalHeader() 
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
