import os
import sys
import hou
import json
import re
# from PIL import Image

from PySide2 import QtCore, QtUiTools, QtWidgets, QtGui
from PySide2 import QtWidgets
# from PyQt5.QtCore import *
# from PyQt5.QtUiTools import *
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *

# TODO: LINK OTHER THUMBNAILS
# TODO: SORT OUT BUMP MAPPING
# TODO: ADD SLIDER FOR SIZE
# TODO: TRY ADD BATCHING
# TODO: FIX DOUBLE FOLDER NAMES


class HDRIManager(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        # ui stuff
        self.folderpath = hou.getenv("LV") + "/scripts/python/HDRIManager"
        ui_file_path = self.folderpath + "/HDRIManager.ui"

        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file_path)
        # end ui stuff

        self.refreshBtn = self.ui.findChild(QtWidgets.QPushButton, "refresh")
        self.refreshBtn.clicked.connect(self.startBrowser)

        self.favBtn = self.ui.findChild(QtWidgets.QPushButton, "favBtn")
        self.favBtn.setIcon(QtGui.QIcon(
            (QtGui.QPixmap(f"{os.path.dirname(__file__)}/icon/fav2.png"))))
        self.favBtn.clicked.connect(self.toggleFav)

        self.initLoad()
        # init load

        self.favs = []
        self.favmode = 0
        self.loadFavs()

        self.iconSize = 300

        self.prefGrid = self.ui.findChild(QtWidgets.QGridLayout, "prefGrid")
        self.savePrefBtn = self.ui.findChild(QtWidgets.QPushButton, "save")
        self.savePrefBtn.pressed.connect(self.setPrefs)
        self.gsgPathLine = QtWidgets.QLineEdit()
        self.prefGrid.addWidget(self.gsgPathLine, 0, 1)

        # self.mainList

        self.slider = self.ui.findChild(QtWidgets.QSlider, "sizeSlider")
        self.slider.valueChanged.connect(self.sliderChanged)

        # COMBO BOX
        self.folderSelector = self.ui.findChild(
            QtWidgets.QComboBox, "folderSelector")

        self.folders = []
        # self.folderNames = ['Car Paint', 'Everyday Material Collection', 'Metal Vol 1', 'Modern Surface Material Collection', 'Paper', 'Tech Products', 'Terrazzo', 'Wood Vol 1', 'Wood Vol 2']

        self.matpath = ''
        self.thumbroot = ''
        self.thumbPath = ""
        self.thumbPaths = []

        self.loadPrefs()

        if self.gsgpath == '':
            pass
        else:
            self.mainList = self.ui.findChild(QtWidgets.QListWidget, "mainList")
            self.mainList.setStyleSheet("border: 0px")
            self.mainList.viewport().setBackgroundRole(QtGui.QPalette.Window)
            self.mainList.setFlow(QtWidgets.QListWidget.LeftToRight)
            self.mainList.setWrapping(True)
            self.mainList.setMovement(QtWidgets.QListWidget.Static)
            self.mainList.setResizeMode(QtWidgets.QListWidget.Adjust)
            self.mainList.setHorizontalScrollMode(QtWidgets.QListWidget.ScrollPerPixel)
            self.mainList.setVerticalScrollMode(QtWidgets.QListWidget.ScrollPerPixel)
            self.mainList.setSpacing(4)

            self.mainList.setContextMenuPolicy(QtGui.Qt.CustomContextMenu)

            # self.mainList.setBatchSize(8)
            # self.mainList.setLayoutMode(QtWidgets.QListView.Batched)

            self.mainList.itemDoubleClicked.connect(self.setTex)
            self.mainList.itemClicked.connect(self.clicked)

            # TRIGGER CHANGE WHEN COMBO BOX CHANGED
            self.folderSelector.currentIndexChanged.connect(
                self.folderSelectorChanged)

            self.loadPrefs()

        # start obligatory stuff
        self.createInterface()  # run create interface. Not sure why this is necessary

        mainLayout = QtWidgets.QVBoxLayout()  # set actual widget main layout and apply
        mainLayout.addWidget(self.ui)
        self.setLayout(mainLayout)
        # end obligatory stuff

    def loadFavs(self):
        # pass
        try:
            with open(f"{os.path.dirname(__file__)}/favs.json", "r") as outfile:
                obj = json.load(outfile)

                self.favs = obj["favs"]
        except:
            self.favs = []

        # print(self.favs)

    def toggleFav(self, checked):
        if checked:
            self.favBtn.setIcon(QtGui.QIcon(
                (QtGui.QPixmap(f"{os.path.dirname(__file__)}/icon/fav1.png"))))
        else:
            self.favBtn.setIcon(QtGui.QIcon(
                (QtGui.QPixmap(f"{os.path.dirname(__file__)}/icon/fav2.png"))))

    def openMaterialFolder(self):
        # print(self.mainList.currentItem()
        # print(self.mainList.currentItem())

        # widget = self.mainList.itemWidget(item)
        # path = widget.path

        # path = item.widget().path
        # hou.ui.showInFileBrowser(path)
        pass

    def initLoad(self):
        with open(f"{os.path.dirname(__file__)}/prefs.json", "r") as outfile:
            obj = json.load(outfile)
            self.gsgpath = obj['gsglib']

    def showMenu(self, position):
        self.menu.exec_(self.mapToGlobal(position))

    def errorCatcher(self, errorMessage, severity):
        msg = errorMessage

        icon = self.ui.findChild(QtWidgets.QLabel, "errorIcon")
        if (severity == 0):
            error = QtGui.QPixmap(
                f"{os.path.dirname(__file__)}/icon/good.png").scaled(18, 18, QtCore.Qt.KeepAspectRatio)
        elif (severity == 1):
            error = QtGui.QPixmap(
                f"{os.path.dirname(__file__)}/icon/warning.png").scaled(18, 18, QtCore.Qt.KeepAspectRatio)
        elif (severity == 2):
            error = QtGui.QPixmap(
                f"{os.path.dirname(__file__)}/icon/error2.png").scaled(18, 18, QtCore.Qt.KeepAspectRatio)
        icon.setPixmap(error)
        box = self.ui.findChild(QtWidgets.QLabel, "errorBox")
        box.setText(msg)
        box.setContentsMargins(5, 0, 0, 0)
        box.setStyleSheet("font-size: 12pt")
        central = self.ui.findChild(
            QtWidgets.QWidget, "centralwidget").layout()
        grid = QtWidgets.QGridLayout()
        grid.addWidget(box, 0, 1)
        grid.addWidget(icon, 0, 0)
        central.addLayout(grid, 1, 0)

    def startBrowser(self):
        self.loadFavs()
        self.mainList.clear()
        self.folderSelector.clear()
        self.initLoad()
        try:
            self.matpath = os.path.join(self.gsgpath, "materials")
            self.thumbroot = os.path.join(self.gsgpath, "thumbs")

            # do folder and thumbnail directory linking
            self.folders = []
            self.thumbPaths = []
            try:
                for folder in os.listdir(self.matpath):
                    path = os.path.join(self.matpath, folder)
                    if os.path.isdir(path):
                        self.folders.append(path)
                        self.thumbPaths.append(
                            os.path.join(self.thumbroot, folder))

                for folder in self.folders:
                    fName = folder.split('\\')
                    fName = fName[-1]

                    # JUST USING BASE FOLDER NAME
                    self.folderSelector.addItem(fName)
                    # self.folderSelector.setItemText(i, self.folderNames[i])

                # disable proxy names
                # for i in range(self.folderSelector.count()):
                #     self.folderSelector.setItemText(i, self.folderNames[i])

                self.directory = self.folders[0]
                self.errorCatcher("Ready", 0)
            except:
                self.errorCatcher("Please check GSG path and refresh.", 2)
            ##

            self.fillList()
            self.errorCatcher("Ready", 0)
        except:
            self.errorCatcher(
                "Failed to start browser. Please check GSG path and refresh.", 1)

    def clicked(self, item):
        self.mainList.update()
        # print("clicked")

    def folderSelectorChanged(self, index):
        # self.folderSelector.setCurrentText(self.folderNames[index])
        try:
            self.directory = self.folders[index]
            self.thumbPath = self.thumbPaths[index]
            self.fillList()
        except:
            self.errorCatcher(
                "Failed to start browser. Please check GSG path and refresh.", 2)

    def sliderChanged(self, value):
        pass
        # items = self.mainList.items()
        # for item in items:
        #     widget = item.widget()
        #     print(widget)
        #     # item.setFixedSize()

    def setTex(self, item=None):
        if item is None:
            pass
        else:
            # print(item)
            widget = self.mainList.itemWidget(item)
            path = widget.folder
            print(path)
            matname = path.split('\\')[-1]
            print(matname)

            try:
                node = hou.selectedNodes()[0]

                gsg = node.createOutputNode("LV::GSG_Mat::1.0")
                gsg.parm('matname').set(matname)

                builder = hou.node(f'{gsg.path()}/matnet1/redshift_vopnet1')

                builder.moveToGoodPosition()
                bpath = builder.path()

                material = hou.node(f"{bpath}/StandardMaterial1")
                mPos = material.position()

                nodes = []

                i = -1
                for file in os.listdir(path):
                    i += 1
                    name = os.path.join(path, file)

                    # input = tex.parm("tex0").eval()
                    input = name.split('.')
                    input = input[0]
                    ext = input[1]
                    input = input.split("_")
                    input = input[-1]

                    if input == 'basecolor':
                        input = 'base_color'
                    elif input == 'metallic':
                        input = 'metalness'
                    elif input == 'anisotropyangle':
                        input = 'refl_aniso_rotation'
                    elif input == 'anisotropylevel' or input == 'anisotropy':
                        input = 'refl_aniso'
                    elif input == 'roughness':
                        input = 'refl_roughness'
                    elif input == 'normal':
                        input = 'bump_input'
                    elif input == 'edgetint':
                        input = 'refl_color'
                    elif input == 'scatteringweight':
                        input = 'ms_amount'
                    elif input == 'sheencolor':
                        input = 'sheen_color'
                    elif input == 'sheenopacity':
                        input = 'sheen_weight'
                    else:
                        input = 'notmap'

                    if input == 'notmap':
                        pass
                    else:

                        tex = builder.createNode('redshift::TextureSampler')
                        tex.parm("tex0").set(name)
                        nodes.append(tex)

                        tex.setPosition(hou.Vector2(mPos.x()-6, mPos.y()-(2*i)))

                        if input == 'base_color':
                            tex.parm('tex0_colorSpace').set('sRGB')
                        else:
                            tex.parm('tex0_colorSpace').set('Raw')

                        if input == 'bump_input':
                            bump = builder.createNode('redshift::BumpMap')
                            bump.setInput(0, tex)
                            bump.parm("inputType").set("1")
                            bump.moveToGoodPosition()
                            material.setNamedInput(input, bump, 0)
                        else:
                            try:
                                material.setNamedInput(input, tex, 0)
                                tex.moveToGoodPosition()
                            except:
                                print(f'{tex} was bad')

                    builder.layoutChildren(nodes)
            except:
                print('select node to create material under')

    def fillList(self):
        self.mainList.clear()
        directory = self.directory

        i = -1
        if self.gsgpath == '' or self.thumbPath == '':
            print('failed to find gsg path')
        else:
            for filename in os.listdir(directory):
                # print(filename)
                # we are in GSG material subfolder: Eg. Metal, or Paracord
                # and we are running over each file now
                folder = os.path.join(directory, filename)
                if os.path.isdir(folder):
                    i += 1
                    if i < 150:
                        f = filename
                        f = f.replace("_", " ")
                        folder = os.path.join(directory, folder)
                        # print(folder)
                        files = os.listdir(folder)
                        if "MSMC" in f:
                            pass
                        elif "Additional" in f:
                            pass
                        else:
                            # pass
                            self.addItem(folder, filename=f)

    def addItem(self, file, filename):
        item = QtWidgets.QListWidgetItem(file)
        item.setFlags(item.flags())
        item.setText("")
        self.mainList.addItem(item)
        isfav = 0
        if filename.replace(" ", "_") in self.favs:
            isfav = 1
        frame = ItemFrame(file, filename, self.thumbPath, item, isfav)

        item.setSizeHint(frame.sizeHint())
        self.mainList.setItemWidget(item, frame)

    def createInterface(self):
        pass
        # self.folderSelector.setCurrentIndex(0)

    def setPrefs(self):
        gsg = self.gsgPathLine.text().replace("/", "\\")
        if gsg == '':
            pass
        else:
            if gsg.endswith("\\"):
                pass
            else:
                gsg = gsg + "\\"

            prefs = {
                "currentIndex": f"{self.folderSelector.currentIndex()}",
                "gsglib": self.gsgPathLine.text()
            }
        with open(f"{os.path.dirname(__file__)}/prefs.json", "w") as outfile:
            json.dump(prefs, outfile)

    def loadPrefs(self):
        with open(f"{os.path.dirname(__file__)}/prefs.json", "r") as outfile:
            obj = json.load(outfile)
            index = obj['currentIndex']

            self.gsgPathLine.setText(obj['gsglib'])
            self.gsgpath = obj['gsglib']
            # self.folderSelectorChanged(0)


class ItemFrame(QtWidgets.QWidget):
    def __init__(self, folder, filename, thumbpath, parent_item, isfav):
        super().__init__()
        self.path = folder.split('\\')
        self.path.pop(-1)
        self.path = "/".join(self.path)

        self.folder = os.path.join(self.path, filename.replace(' ', '_'))

        self.filename = filename
        self.parent_item = parent_item
        self.isfav = isfav

        self.main = HDRIManager()

        missing = os.path.join(os.path.dirname(__file__), "icon/missing.png")
        usethumb = missing
        missingThumb = False
        if self.filename.startswith("GSG MC"):
            thumbname = self.filename.replace(" ", "_")
            fname = thumbname
            thumbname = f'{thumbname}_preview.jpg'
            # self.path = os.path.join(self.path, fname)
            # print(thumbname)
            # p = self.path.replace("/","\\")
            usethumb = os.path.join(os.path.join(self.path, fname), thumbname)
            # print(usethumb)
        else:
            if "terrazzo" in thumbpath:
                thumbname = filename.replace(" ", "_")[4:]
                thumbname = thumbname.split("_")
                index = thumbname[-1].zfill(3)
                thumbname.pop(-1)
                thumbname = "".join(thumbname)+index+'_preview_380.jpg'

            elif "msmc" in thumbpath:
                thumbname = filename.replace(" ", "_")

                thumbname = thumbname.split("_")
                index = thumbname[-1].zfill(2)
                thumbname.pop(-1)
                thumbname = "".join(thumbname)+index+'_preview_380.jpg'
                # print(thumbname) # debug file name matches
            elif "paper" in thumbpath:
                thumbname = filename.replace(" ", "_")[4:]
                thumbname = thumbname.split("_")
                index = thumbname[-1].zfill(2)
                thumbname.pop(-1)
                thumbname = "".join(thumbname)+index+'_preview_380.jpg'
                # print(thumbname) # debug file name matches
            elif "metal" in thumbpath:
                thumbname = filename.replace(" ", "_")[14:]
                thumbname = thumbname.split("_")
                index = thumbname[-1].zfill(2)
                thumbname.pop(-1)
                thumbname = "".join(thumbname)+index+'_preview_380.jpg'
                print(thumbname)  # debug file name matches
            elif "carpaint" in thumbpath:
                thumbname = filename.replace(" ", "_")[14:]
                if thumbname.endswith("Camo"):
                    thumbname = thumbname + "01"
                thumbname = thumbname.split("_")
                index = thumbname[-1].zfill(2)
                thumbname.pop(-1)
                thumbname = "".join(thumbname)+index+'_preview_380.jpg'
                # print(thumbname) # debug file name matches
            else:
                thumbname = filename.replace(" ", "_")[14:]

                thumbname = thumbname.split("_")
                index = thumbname[-1].zfill(2)
                thumbname.pop(-1)
                thumbname = "".join(thumbname)+index+'_preview_380.jpg'
                # print(thumbname) # debug file name matches

            j = -1
            if missingThumb == False:
                for file in os.listdir(thumbpath):
                    cfile = os.path.join(thumbpath, file)
                    if os.path.isfile(cfile):
                        testname = file[15:]
                        # print(testname)
                        if thumbname == testname:
                            usethumb = os.path.join(thumbpath, file)
                            # print(usethumb)

        if filename.endswith("hdr"):
            pix = QtGui.QPixmap(missing)
        else:
            pix = QtGui.QPixmap(usethumb)
        self.image = QtWidgets.QLabel(pixmap=QtGui.QPixmap(
            pix).scaled(200, 200, QtCore.Qt.KeepAspectRatio))

        self.favPix = QtGui.QPixmap(
            f"{os.path.dirname(__file__)}/icon/fav1.png").scaled(16, 16, QtCore.Qt.KeepAspectRatio)
        self.nofavPix = QtGui.QPixmap(
            f"{os.path.dirname(__file__)}/icon/fav2.png").scaled(16, 16, QtCore.Qt.KeepAspectRatio)

        labelName = filename
        index = self.main.folderSelector.currentIndex()
        if index == 1:
            labelName = labelName[2:]
        elif index == 3:
            pass
        else:
            labelName = labelName[4:]

        self.menu = QtWidgets.QMenu(self)
        self.menu.addAction('Favorite', self.setFav)
        self.menu.addAction('Unfavorite', self.removeFav)
        self.menu.addAction('Open Material Folder', self.showMaterialFolder)

        self.imageLabel = QtWidgets.QLabel(
            labelName, alignment=QtCore.Qt.AlignCenter)
        self.imageLabel.setStyleSheet('font: 9pt;')
        self.imageLabel.setWordWrap(True)
        layout = QtWidgets.QGridLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(1)
        layout.addWidget(self.image, 0, 0)
        self.labelGrid = QtWidgets.QGridLayout()
        if self.isfav == 1:
            self.favicon = QtWidgets.QLabel(pixmap=self.favPix)
        else:
            self.favicon = QtWidgets.QLabel(pixmap=self.nofavPix)
        self.favicon.setContentsMargins(5, 5, 5, 5)
        self.labelGrid.addWidget(self.imageLabel, 0, 0)
        layout.addLayout(self.labelGrid, 1, 0)
        layout.addWidget(self.favicon, 0, 0, QtCore.Qt.AlignTop)

        self.setFixedSize(layout.sizeHint())

        self.setContextMenuPolicy(QtGui.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showMenu)

    def showMenu(self, position):
        self.menu.exec_(self.mapToGlobal(position))

    def showMaterialFolder(self):
        hou.ui.showInFileBrowser(self.folder)

    def setTex(self):
        print(self.main.mainList.currentItem())

    def setFav(self):

        self.main.favs.append(self.filename.replace(" ", "_"))
        print(self.main.favs)
        favs = {
            "favs": self.main.favs
        }

        with open(f"{os.path.dirname(__file__)}/favs.json", "w") as outfile:
            json.dump(favs, outfile)

        self.set_fav(1)

    def removeFav(self):
        print(f'CURRENT LIST: {self.main.favs}')
        self.main.favs.remove(self.filename.replace(" ", "_"))
        print(f'CURRENT LIST: {self.main.favs}')

        favs = {
            "favs": self.main.favs
        }

        with open(f"{os.path.dirname(__file__)}/favs.json", "w") as outfile:
            json.dump(favs, outfile)

        # self.main.loadFavs()
        self.set_fav(0)

    def set_fav(self, fav):
        item = self.parent_item
        self.isfav = fav
        if fav == 1:
            self.favicon.setPixmap(self.favPix)
        else:
            self.favicon.setPixmap(self.nofavPix)
