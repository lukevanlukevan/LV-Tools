import os
import sys
import hou
import json

from hutil.PySide import QtCore, QtUiTools, QtWidgets, QtGui

from keyframeAssistant import keyframeAssistant


class keyframeAssistant(QtWidgets.QWidget):
    def __init__(self):
        super(keyframeAssistant, self).__init__()

        self.folderpath = hou.getenv("LV") + "/scripts/python/keyframeAssistant"

        ui_file_path = self.folderpath + "/keyframeAssistant.ui"

        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file_path)

        # find child here

        node = None

        self.mainGrid = self.ui.findChild(QtWidgets.QGridLayout, "mainGrid")

        self.refreshBtn = self.ui.findChild(QtWidgets.QPushButton, "refresh")
        self.refreshBtn.clicked.connect(self.parmsFromNode)
        self.clearBtn = self.ui.findChild(QtWidgets.QPushButton, "clear")
        self.clearBtn.clicked.connect(self.clearParms)

        self.currentLink = self.ui.findChild(QtWidgets.QLineEdit, "currentLink")

        self.keyAllBtn = self.ui.findChild(QtWidgets.QPushButton, "all")
        self.keyAllBtn.clicked.connect(self.keyAll)

        self.keyKeyedBtn = self.ui.findChild(QtWidgets.QPushButton, "pending")
        self.keyKeyedBtn.clicked.connect(self.keyPending)
        self.keyKeyedBtn.setStyleSheet("color: hsl(180, 50%, 50%)")

        self.keyKeyedBtn = self.ui.findChild(QtWidgets.QPushButton, "keyed")
        self.keyKeyedBtn.clicked.connect(self.keyKeyed)
        self.keyKeyedBtn.setStyleSheet("color: hsl(120, 50%, 50%)")

        self.parmBtnGroup = QtWidgets.QButtonGroup()
        self.parmBtnGroup.buttonClicked.connect(self.parmBtnClick)

        self.createInterface()
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.ui)
        self.setLayout(mainLayout)

    def keyAll(self):
        node = self.node

        parms = node.parms()

        testParms = ["Translate", "Rotate", "Scale"]

        for parm in parms:
            if parm.description() in testParms:
                myKey = hou.Keyframe()
                myKey.setFrame(hou.frame())
                myKey.setValue(parm.eval())
                parm.setKeyframe(myKey)

    def keyPending(self):
        node = self.node

        parms = node.parms()

        testParms = ["Translate", "Rotate", "Scale"]

        for parm in parms:
            if parm.description() in testParms:
                # print(parm)
                kfs = parm.keyframes()
                kBefore = parm.keyframesBefore(hou.frame())

                if len(kBefore) > 0:
                    bval = kBefore[-1].value()

                myKey = hou.Keyframe()
                myKey.setFrame(hou.frame())
                myKey.setValue(parm.eval())
                if len(kfs) > 0:
                    if len(kBefore) > 0:
                        if bval == parm.eval():
                            pass
                        else:
                            parm.setKeyframe(myKey)

                    # parm.setKeyframe(myKey)

    def keyKeyed(self):
        node = self.node

        parms = node.parms()

        testParms = ["Translate", "Rotate", "Scale"]

        for parm in parms:
            if parm.description() in testParms:
                kfs = parm.keyframes()

                myKey = hou.Keyframe()
                myKey.setFrame(hou.frame())
                myKey.setValue(parm.eval())
                if len(kfs) > 0:
                    parm.setKeyframe(myKey)

    def createInterface(self):
        pass

    def setPrefs(self):
        prefs = {
            # "difChecks": f"{self.difChecks.text()}",
            # "difCS": f"{self.spaceDropBox.currentText()}",
            # "rawChecks": f"{self.rawChecks.text()}",
            # "rawCS": f"{self.spaceDropBoxRaw.currentText()}"
        }
        # with open(f"{self.folderpath}/prefs.json", "w") as outfile:
        #     json.dump(prefs, outfile)

    def parmBtnClick(self, button):
        path = button.whatsThis()

        if path.startswith("onlyKey"):
            paths = path[7:]
            paths = paths[1:-1]
            paths = paths.replace("'", "")
            paths = paths.split(", ")
            for path in paths:
                parm = hou.parm(path)
                kfs = parm.keyframes()
                kBefore = parm.keyframesBefore(hou.frame())

                if len(kBefore) > 0:
                    bval = kBefore[-1].value()

                myKey = hou.Keyframe()
                myKey.setFrame(hou.frame())
                myKey.setValue(parm.eval())
                if len(kfs) > 0:
                    if len(kBefore) > 0:
                        if bval == parm.eval():
                            pass
                        else:
                            parm.setKeyframe(myKey)
                    # else:
                    parm.setKeyframe(myKey)

        else:
            if path.startswith("["):
                paths = path[1:-1]
                paths = paths.replace("'", "")
                paths = paths.split(", ")
                for path in paths:
                    parm = hou.parm(path)
                    myKey = hou.Keyframe()
                    myKey.setFrame(hou.frame())
                    myKey.setValue(parm.eval())
                    parm.setKeyframe(myKey)
            else:
                parm = hou.parm(path)
                myKey = hou.Keyframe()
                myKey.setFrame(hou.frame())
                myKey.setValue(parm.eval())
                parm.setKeyframe(myKey)

        # parm =  hou.parm(path)
        # myKey = hou.Keyframe()
        # myKey.setFrame(hou.frame())
        # myKey.setValue(parm.eval())

        # parm.setKeyframe(myKey)

    def clearParms(self):
        self.currentLink.setText("")
        count = self.mainGrid.count()

        for i in range(count):
            child = self.mainGrid.itemAt(0).widget()
            self.mainGrid.removeWidget(child)
            child.deleteLater()

    def parmsFromNode(self):
        self.clearParms()

        testParms = ["Translate", "Rotate", "Scale"]
        tParms = ["t", "r", "s"]

        if len(hou.selectedNodes()) == 0:
            self.currentLink.setText("")
        else:
            self.node = hou.selectedNodes()[0]
            self.currentLink.setText(self.node.path())
            parms = self.node.parms()
            pTuple = self.node.parmTuples()

            i = -1
            j = -1
            currentDesc = testParms[0]
            # print(parms)
            for tuple in pTuple:
                if tuple.description() in testParms:
                    i += 1

                    # parmLine = singleParm(self, self.mainGrid, i, tuple)

                    j = -1

            #         currentDesc = x.description()

        count = self.mainGrid.count()

    # def btnClicked(self, button):
    #     print(f'{button}')


class singleParm(QtWidgets.QWidget):
    def __init__(self, parent, mainGrid, wIndex, tuple):
        super(singleParm, self).__init__()

        i = wIndex
        self.index = i

        thisframe = hou.frame()

        axisIndex = i % 3
        axis = ["X", "Y", "Z"]

        self.name = f"{tuple.description()}:"

        self.holder = QtWidgets.QWidget()
        self.holder.setContentsMargins(0, 0, 0, 0)
        self.holder.setSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )

        widgetGrid = QtWidgets.QGridLayout(self.holder)
        widgetGrid.setMargin(0)

        self.parmName = QtWidgets.QLabel(self.name)
        self.parmName.setObjectName("parmName")
        self.parmName.setMaximumSize(QtCore.QSize(100, 16777215))
        self.parmName.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )

        self.allParm = QtWidgets.QPushButton(f"All Parms")
        self.allParm.setMaximumSize(QtCore.QSize(100, 16777215))
        paths = [parm.path() for parm in tuple]
        self.allParm.setWhatsThis(str(paths))
        parent.parmBtnGroup.addButton(self.allParm)

        self.onlyKey = QtWidgets.QPushButton("Only Keyed")
        self.onlyKey.setMaximumSize(QtCore.QSize(100, 16777215))
        self.onlyKey.setWhatsThis("onlyKey" + str(paths))
        parent.parmBtnGroup.addButton(self.onlyKey)

        self.multigrid = QtWidgets.QGridLayout()
        j = -1
        for parm in tuple:
            j += 1
            axisIndex = j % 3
            axis = ["X", "Y", "Z"]
            self.parmBtn = QtWidgets.QPushButton(f"{axis[axisIndex]}")
            # print(parm.path())
            self.parmBtn.setWhatsThis(str(parm.path()))
            parent.parmBtnGroup.addButton(self.parmBtn)

            # myKey = hou.Keyframe()
            # myKey.setFrame(thisframe)
            # myKey.setValue(parm.eval())
            self.multigrid.addWidget(self.parmBtn, 0, j)

        # add widgets to grid

        widgetGrid.addWidget(self.parmName, i, 0)

        widgetGrid.addWidget(self.allParm, i, 1)

        widgetGrid.addWidget(self.onlyKey, i, 2)

        widgetGrid.addLayout(self.multigrid, i, 3)

        mainGrid.addWidget(self.holder, i, 0)

        # self.allParms.setObjectName(u"allParms")

        # layout.addWidget(self.allParms, 0+i, 1, 1, 1)

        # if axisIndex == 0:
        #     self.parmName.setStyleSheet("color: red")
        # elif axisIndex == 1:
        #     self.parmName.setStyleSheet("color: green")
        # elif axisIndex == 2:
        #     self.parmName.setStyleSheet("color: blue")

        # layout.addWidget(self.parmName, 0+i, 0, 1, 1) # we need to remove this

        # self.multiBlock = QtWidgets.QGridLayout()
        # self.multiBlock.setObjectName(u"multiBlock")
        # self.parmButton = QtWidgets.QPushButton()
        # self.parmButton.setObjectName(u"pushButton")

        # self.holder.setLayout(layout)

        # self.holder.addWidget(self.parmButton, i, 0, 1, 1)

        # self.mainGrid.addLayout(self.multiBlock, i, 2, 1, 1)
