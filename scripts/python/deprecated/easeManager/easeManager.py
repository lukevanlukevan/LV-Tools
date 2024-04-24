from gradientManager import gradientManager
from PySide2.QtCore import Qt
from PySide2.QtGui import QCursor
from PySide2.QtWidgets import QMenu, QApplication
import glob
import random
import time
import os
import sys
import hou
import json

from PySide2 import QtCore, QtUiTools, QtWidgets, QtGui
from PySide2.QtWidgets import QGridLayout

# TODO Float eases are flipped on Y axis


from easeManager import easeManager


def is_shift_pressed():
    modifiers = QApplication.keyboardModifiers()
    return modifiers == Qt.ShiftModifier


def is_ctrl_pressed():
    modifiers = QApplication.keyboardModifiers()
    return modifiers == Qt.ControlModifier


def remap(old_val, old_min, old_max, new_min, new_max):
    return (new_max - new_min)*(old_val - old_min) / (old_max - old_min) + new_min


class easeManager(QtWidgets.QWidget):
    def __init__(self):
        super(easeManager, self).__init__()

        self.folderpath = hou.getenv("LV") + "/scripts/python/easeManager"
        self.gradFolder = self.folderpath + "/ease"

        ui_file_path = self.folderpath + "/easeManager.ui"

        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file_path)

        self.easeCount = 0
        self.easeSize = 100

        self.easeNameBox = self.ui.findChild(QtWidgets.QLineEdit, "easeName")
        self.easeName = ""
        self.easeNameBox.editingFinished.connect(self.stringChanged)

        self.saveEaseBtn = self.ui.findChild(QtWidgets.QPushButton, "saveEase")
        self.saveEaseBtn.clicked.connect(self.saveEase)

        self.parmRow = self.ui.findChild(QtWidgets.QHBoxLayout, "parmRow")

        self.controlGroup = QtWidgets.QButtonGroup()
        self.toggleState = 'All'
        self.controlGroup.buttonClicked.connect(self.setToggle)

        self.graphGrid = self.ui.findChild(QtWidgets.QGridLayout, "graphGrid")

        self.zoomIn = self.ui.findChild(QtWidgets.QPushButton, "zoomIn")
        self.zoomIn.setStyleSheet("border: none; background-color: hsl(200, 50%, 100); border-radius: 5px; color: hsl(0, 0%, 100%); font-size: 14px;")
        self.zoomOut = self.ui.findChild(QtWidgets.QPushButton, "zoomOut")
        self.zoomOut.setStyleSheet("border: none; border-color: white; background-color: hsl(200, 50%, 100); border-radius: 5px; color: hsl(0, 0%, 100%); font-size: 14px;")

        self.zoomBtns = QtWidgets.QButtonGroup()
        self.zoomBtns.addButton(self.zoomIn, 1)
        self.zoomBtns.addButton(self.zoomOut, 0)
        self.zoomBtns.idPressed.connect(self.resizeGraphs)

        self.createInterface()  # run create interface

        mainLayout = QtWidgets.QVBoxLayout()

        self.gradGroup = QtWidgets.QButtonGroup()

        self.gradGroup.buttonClicked.connect(self.setGrad)

        self.loadEases()

        mainLayout.addWidget(self.ui)
        self.setLayout(mainLayout)
        self.stringChanged()

    def resizeGraphs(self, val):
        if val == 1:
            self.easeSize += 10
        else:
            self.easeSize -= 10

        self.easeSize = max(20, self.easeSize)
        self.easeSize = min(100, self.easeSize)

        self.loadEases()

    def setToggle(self, button):
        i = button.whatsThis()
        self.toggleState = i
        self.loadEases()

    def savePrefs(self):
        prefs = {
            "difChecks": f"{self.difChecks.text()}"
        }
        with open(f"{self.folderpath}/eases.json", "w") as outfile:
            json.dump(prefs, outfile)

    def createInterface(self):
        pass

    def gradActivate(self):
        pass

    def setGrad(self, button):

        if len(hou.ui.paneTabOfType(hou.paneTabType.ChannelEditor).graph().selectedKeyframes()) == 0:
            print("Please select keyframes.")
        else:
            i = button.whatsThis()

            name = ""
            times = []
            frames = []
            values = []
            accels = []
            slopes = []

            if os.path.isfile(f"{self.gradFolder}/ease{str(i).zfill(3)}.json"):

                with open(f"{self.gradFolder}/ease{str(i).zfill(3)}.json", "r") as openfile:
                    json_object = json.load(openfile)

                    name = json_object["name"]
                    times = json_object["times"]
                    frames = json_object["frames"]
                    values = json_object["values"]
                    accels = json_object["accels"]
                    slopes = json_object["slopes"]

            pane_tab = hou.ui.paneTabOfType(hou.paneTabType.ChannelEditor)
            keyframes = pane_tab.graph().selectedKeyframes()  # type: ignore

            div = 0

            for parm in keyframes.keys():
                for key in keyframes[parm]:
                    # print(key)
                    pass
                keys = keyframes[parm]

                key1 = keys[0]
                key2 = keys[1]

                in_time = key1.time()
                out_time = key2.time()

                div = (out_time-in_time) - (in_time-in_time)

            for parm in keyframes.keys():
                for o, key in enumerate(keyframes[parm]):
                    new_key = hou.Keyframe()
                    new_key.interpretAccelAsRatio(True)

                    key.setValue(values[o])
                    if o == 1:
                        key.setInSlope(slopes[o]/div)
                        key.setInAccel(accels[o]*div)
                    else:
                        key.setSlope(slopes[o]/div)
                        key.setAccel(accels[o]*div)

                    parm.setKeyframe(key)

                    # something going wrong with the acelleration ratios when working with large scales. Need to figure that out

    def stringChanged(self):
        self.easeName = self.easeNameBox.text()

    def renameEases(self):
        files = os.listdir(self.gradFolder)
        files.sort()
        i = 0
        for filename in files:
            f = os.path.join(self.gradFolder, filename)
            # checking if it is a file
            if os.path.isfile(f):
                os.rename(f, f'{self.gradFolder}/ease{str(i).zfill(3)}.json')
                i += 1

    def saveEase(self):

        self.stringChanged()
        self.easeCount += 1

        if len(hou.ui.paneTabOfType(hou.paneTabType.ChannelEditor).graph().selectedKeyframes()) == 0:
            print("Please select keyframes.")
        else:
            # node = hou.selectedNodes()[0]

            # get graph

            pane_tab = hou.ui.paneTabOfType(hou.paneTabType.ChannelEditor)
            keyframes = pane_tab.graph().selectedKeyframes()  # type: ignore

            pair_data = {}

            for parm in keyframes.keys():
                for key in keyframes[parm]:
                    # print(key)
                    pass
                keys = keyframes[parm]

                key1 = keys[0]
                key2 = keys[1]

                in_time = key1.time()
                out_time = key2.time()

                in_frame = key1.frame()
                out_frame = key2.frame()

                in_value = key1.value()
                out_value = key2.value()

                in_accel = key1.accel()
                out_accel = key2.inAccel()

                in_slope = key1.slope()
                out_slope = key2.slope()

                div = (out_time-in_time) - (in_time-in_time)

                if out_value > in_value:
                    val_div = out_value - in_value
                else:
                    val_div = in_value - out_value

                norm_in_accel = in_accel / div
                norm_out_accel = out_accel / div

                t_ratio = (out_time-in_time) - (in_time-in_time)

                print(t_ratio)

                def get_samples(count, parm):
                    samples = []
                    for i in range(count):
                        t = remap(i, 0, count-1, in_time, out_time)
                        sample = remap(parm.evalAtTime(t), in_value, out_value, 1, 0)
                        samples.append(sample)

                    return samples

                samples = get_samples(100, parm)

                pair_data = {
                    "name": self.easeName,
                    "times": [in_time, out_time],
                    "frames": [in_frame, out_frame],
                    "values": [in_value, out_value],
                    "accels": [in_accel/t_ratio, out_accel/t_ratio],
                    "slopes": [in_slope, out_slope],
                    "plot_values": samples
                }

            prefs = pair_data
            dirfiles = os.listdir(self.gradFolder)
            it = len(dirfiles)
            with open(f"{self.gradFolder}/ease{str(it).zfill(3)}.json", "w") as outfile:
                json.dump(prefs, outfile)

            self.loadEases()
            self.easeNameBox.setText("")
            self.easeNameBox.setPlaceholderText(f'"Ease {it}"')
            self.stringChanged()

    def loadEases(self):

        self.renameEases()

        count = self.graphGrid.count()
        for i in range(count):

            child = self.graphGrid.itemAt(0).widget()
            self.graphGrid.removeWidget(child)
            child.deleteLater()

        i = -1
        grid = self.ui.findChild(QtWidgets.QGridLayout, "graphGrid")

        self.tab = self.ui.findChild(QtWidgets.QWidget, "tab")

        tempi = 0
        placement = -1
        if not os.path.exists(self.gradFolder):
            os.makedirs(self.gradFolder)

        # files = os.listdir(self.gradFolder)
        files = list(filter(os.path.isfile, glob.glob(self.gradFolder + "/*.json")))
        files.sort(key=lambda x: os.path.getmtime(x))
        for filename in files:
            f = os.path.join(self.gradFolder, filename)
            # checking if it is a file
            i += 1

            if os.path.isfile(f) and f.endswith(".json"):

                with open(f"{f}", "r") as openfile:
                    json_object = json.load(openfile)

                name = json_object["name"]
                times = json_object["times"]
                values = json_object["values"]
                accels = json_object["accels"]
                slopes = json_object["slopes"]
                plot_values = json_object["plot_values"]

                placement += 1
                new_keys = []
                # for k in keys:
                #     new_keys.append(float(k))

                # new_values = []
                # for val in values:
                #     new_values.append(val)

                self.gradHolder = QtWidgets.QWidget()
                gradPolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
                self.gradHolder.setSizePolicy(gradPolicy)

                self.libItem = QtWidgets.QGridLayout()
                self.libItem.setContentsMargins(5, 5, 5, 5)
                self.itemThumb = QtWidgets.QPushButton()
                self.itemThumb.setMinimumSize(100, self.easeSize)

                gradStyle = ('''QWidget:hover:!pressed {
                                background-color: rgba(255, 255, 255, 100);
                            }

                            ''')
                self.gradHolder.setStyleSheet(gradStyle)
                inColor = values[0]
                outColor = values[-1]

                kString = []
                ki = -1
                keys = values
                for k in values:
                    ki += 1
                    kString.append(f'x{ki+1}: {float(ki)/(len(keys)-1)}, y{ki+1}: 0')

                kString = ', '.join(kString)

                vString = []
                if False == False:
                    self.buttonLayout = QtWidgets.QGridLayout()
                    self.buttonLayout.setContentsMargins(0, 0, 0, 0)
                    self.graph = GraphView(self.itemThumb, json_object['plot_values'], self.easeSize)
                    self.graph.setRenderHint(QtGui.QPainter.Antialiasing)
                    self.graph.setMinimumSize(100, self.easeSize)
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
                    self.itemLabel.setText(f"Ease {i+1}")
                else:
                    self.itemLabel.setText(name)

                self.itemLabel.setEnabled(False)
                self.itemLabel.setStyleSheet('color: rgb(200, 200, 200);')

                self.itemLabel.setAlignment(QtCore.Qt.AlignHCenter)

                self.libItem.addWidget(self.itemLabel, 1, 0, 1, 1)

                self.gradGroup.addButton(self.itemThumb, i)

                self.gradHolder.setLayout(self.libItem)

                self.graphGrid.addWidget(self.gradHolder, placement/4, placement % 4)

                tempi = i+1

        self.easeCount = tempi
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
        action1 = contextMenu.addAction("Rename Ease")
        action2 = contextMenu.addAction("Delete Ease")

        action = contextMenu.exec_(position)
        if action == action1:
            self.renameEase(sel)
        if action == action2:
            self.deleteEase(sel)

        # handle other actions...

    def renameEase(self, i):
        clicked, val = hou.ui.readInput("Rename Ease", buttons=('Rename', 'Cancel'), initial_contents='')
        # Load the JSON file
        with open(f'{self.gradFolder}/ease{str(i).zfill(3)}.json', 'r') as f:
            data = json.load(f)

        # Change the name property
        data['name'] = val

        # Save the updated JSON file
        with open(f'{self.gradFolder}/ease{str(i).zfill(3)}.json', 'w') as f:
            json.dump(data, f)

        self.loadEases()

    def deleteEase(self, i):

        QtCore.QCoreApplication.processEvents()

        child = self.graphGrid.itemAt(int(i)).widget()
        self.graphGrid.removeWidget(child)
        child.deleteLater()

        os.remove(f'{self.gradFolder}/ease{str(i).zfill(3)}.json')
        # self.loadEases()

        QtCore.QCoreApplication.processEvents()
        self.loadEases()

        self.renameEases()

        # def rename_json_files(folder_path):
        # Get all JSON files in the folder
        # json_files = [file for file in os.listdir(folder_path) if file.endswith('.json')]

        # Sort the files in ascending order
        # json_files.sort()

        # Rename the files with numbered order
        # for i, file in enumerate(json_files):
        #     new_name = f'ease{str(i).zfill(3)}.json'
        #     os.rename(os.path.join(folder_path, file), os.path.join(folder_path, new_name))

        # Usage example
        # rename_json_files(self.gradFolder)


class GraphView(QtWidgets.QGraphicsView):
    def __init__(self, parent, y_values, easeSize):
        super().__init__()

        self.parent = parent

        self.y_values = y_values

        self.setEnabled(False)
        self.scene = QtWidgets.QGraphicsScene(parent)
        self.setScene(self.scene)

        self.height = easeSize*0.98

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
            # line = QtWidgets.QGraphicsLineItem(x1, 1-y1*self.height, x2, 1-y2*self.height)
            line = QtWidgets.QGraphicsLineItem(x1, remap(y1, 0, 1, -self.height/2, self.height/2), x2, remap(y2, 0, 1, -self.height/2, self.height/2))
            line.setPen(self.pen)
            self.scene.addItem(line)
