# from hutil.Qt import QtWidgets, QtUiTools,
from PySide2 import QtWidgets, QtUiTools, QtCore, QtGui
from PySide2.QtWidgets import QPushButton, QComboBox, QTableWidget, QTableWidgetItem
import hou
import os
import json

from OD import shelftools


class LVProjectManager(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.folderpath = hou.getenv("LV") + "/scripts/python/LVProjectManager"
        ui_file_path = self.folderpath + "/LVProjectManager2.ui"
        self.prefpath = self.folderpath + "/prefs.json"

        self.notes = ""

        self.prefs = {"paths": [], "recent": -1}

        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file_path)

        self.extraPath = "02_Workflow/01-3D/Houdini/"

        self.jobs = self.ui.findChild(QtWidgets.QComboBox, "jobs")

        # runs once on startup when text is added
        self.jobs.activated.connect(self.selectFolder)

        self.table = self.ui.findChild(QtWidgets.QTableWidget, "table")
        self.table.cellDoubleClicked.connect(self.loadProject)

        self.folderBtn = self.ui.findChild(
            QtWidgets.QPushButton, "folders_btn")
        self.folderBtn.clicked.connect(self.pickFolder)

        self.prjRoot = self.ui.findChild(QtWidgets.QLineEdit, "prjRoot")
        self.prjRootPath = self.prjRoot.text()

        self.rootBtn = self.ui.findChild(QtWidgets.QPushButton, "rootBtn")
        self.rootBtn.clicked.connect(self.updateExtra)

        self.pathPrev = self.ui.findChild(QtWidgets.QLabel, "pathPrev")

        self.infoRow = self.ui.findChild(QtWidgets.QLineEdit, "infoRow")

        self.basePath = ""

        self.combinedPath = ""

        self.currentIndex = -1

        # init global vars
        self.addedPath = ""

        self.jobName = ""

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.ui)
        self.setLayout(layout)

        # row buttons

        self.explorerBtn = self.ui.findChild(
            QtWidgets.QPushButton, "explorerBtn")
        self.explorerBtn.clicked.connect(
            self.openDir)
        self.explorerBtn.setFont(QtGui.QFont("Source Sans Pro", 12))

        self.incBtn = self.ui.findChild(QPushButton, "incBtn")
        self.incBtn.clicked.connect(self.saveInc)
        self.incBtn.setFont(QtGui.QFont("Source Sans Pro", 12))

        self.initBtn = self.ui.findChild(QPushButton, "initBtn")
        self.initBtn.clicked.connect(self.initDir)
        self.initBtn.setFont(QtGui.QFont("Source Sans Pro", 12))

        self.flipBtn = self.ui.findChild(QPushButton, "flipBtn")
        self.flipBtn.clicked.connect(self.flipbook)
        self.flipBtn.setFont(QtGui.QFont("Source Sans Pro", 12))
        # Initial loads

        self.noteEdit = self.ui.findChild(QtWidgets.QTextEdit, "notes")
        self.noteEdit.textChanged.connect(self.saveNotes)
        self.noteEdit.setFont(QtGui.QFont("Source Sans Pro", 14))

        self.tabs = self.ui.findChild(QtWidgets.QTabWidget, "tabWidget")
        self.tabs.currentChanged.connect(self.loadNotes)

        self.notetab = self.ui.findChild(QtWidgets.QWidget, "Notes")
        # self.noteTab.tabBarClicked

        # UI Inits
        self.table.setColumnWidth(0, 950)

        self.header = self.table.horizontalHeader()
        self.header.setStretchLastSection(True)

        self.loadPrefs()
        self.loadFolders()
        self.loadNotes()
        self.setIndex()
        self.table.setHorizontalHeaderLabels(["Projects"])
        # hou.hscript("setenv -s %s=%s" %
        #             ("DB", f'/Users/lukevan/Partners in Crime Dropbox/Luke Van/STUDIO-PIC/'))

    def hipNameWithoutVersion(self):
        name = hou.hipFile.basename()
        fullname = name.split(".")[0]
        if fullname[-1].isdigit() and fullname[-2].isdigit():
            return fullname[:-3]
        else:
            return fullname

    def saveNotes(self):
        if self.tabs.currentIndex() == 2:
            self.notes = self.noteEdit.toPlainText()

            folder = hou.text.expandString(self.combinedPath) + "/notes/"

            if not os.path.isdir(folder):
                os.mkdir(folder)

            self.notepath = self.combinedPath + "/notes/" + self.hipNameWithoutVersion()

            with open(hou.text.expandString(self.notepath), 'w') as f:
                f.write(self.notes)

    def loadNotes(self):
        self.notepath = hou.getenv("HIP") + "/notes/" + self.hipNameWithoutVersion()

        if os.path.isfile(self.notepath):

            with open(self.notepath, "r") as openfile:
                self.notes = openfile.read()

            self.noteEdit.setText(self.notes)

    def flipbook(self):
        shelftools.createFlipAndHipCopy()

    def initDir(self):
        dirs = ['geo', 'abc', 'tex', 'render']
        p = hou.text.expandString(self.combinedPath)

        for d in dirs:
            c = os.path.join(p, d)
            if not os.path.exists(c):
                os.mkdir(c)

        hou.ui.displayConfirmation("Working directory created")

    def updateExtra(self):
        self.updatePrefs("rootPath", self.prjRoot.text())
        self.loadPrefs()

    def updatePrefs(self, item, val):
        if os.path.isfile(self.prefpath):

            with open(self.prefpath, "r") as openfile:
                self.prefs = json.load(openfile)

        self.prefs[item] = val

        with open(self.prefpath, "w") as outfile:
            json.dump(self.prefs, outfile, indent=4)

    def setIndex(self):

        self.jobs.setCurrentIndex(self.currentIndex)
        self.selectFolder()

    def setinfoRow(self):
        self.infoRow.setText("$JOB = " + self.processPath(self.basePath))

    def saveInc(self):
        name = hou.hipFile.basename()
        fullname = name.split(".")[0]
        if fullname[-1].isdigit() and fullname[-2].isdigit():
            hou.hipFile.saveAndIncrementFileName()
        self.loadFolders()

    def openDir(self):
        path = hou.expandString(
            self.combinedPath.replace("//", "/"))
        hou.ui.showInFileBrowser(path + "/")

    def savePrefs(self):

        self.prefs['paths'].append(self.addedPath)

        with open(self.prefpath, "w") as outfile:
            json.dump(self.prefs, outfile, indent=4)

    def saveRecent(self):

        self.prefs['recent'] = self.currentIndex

        with open(self.prefpath, "w") as outfile:
            json.dump(self.prefs, outfile, indent=4)

    def loadPrefs(self):
        if os.path.isfile(self.prefpath):

            with open(self.prefpath, "r") as openfile:
                self.prefs = json.load(openfile)

        # clear dropdown and add all the paths from json
        self.jobs.clear()
        self.jobs.addItem("Select a job")

        for path in self.prefs['paths']:
            self.jobs.addItem(path)

        self.currentIndex = self.prefs['recent']
        self.prjRoot.setText(self.prefs['rootPath'])
        self.pathPrev.setText("$JOB/" + self.prefs['rootPath'])
        self.extraPath = self.prefs['rootPath']

    def setCombinedPath(self, path):
        tocombine = path
        if self.extraPath.endswith("/"):
            extra = self.extraPath[:-1]
        else:
            extra = self.extraPath
        self.combinedPath = tocombine + extra
        self.loadFolders()

    def pathAdded(self):
        self.addedPath = self.basePath
        first = self.basePath
        if not self.basePath.endswith("/"):
            self.basePath = first + "/"

        self.savePrefs()
        self.loadPrefs()

    def pickFolder(self):
        self.basePath = self.processPath(
            hou.ui.selectFile(file_type=hou.fileType.Directory))

        self.pathAdded()
        self.loadFolders()
        # self.jobs.setCurrentIndex(self.jobs.count() - 1)

    def selectFolder(self):
        folder = self.jobs.currentText()
        self.basePath = self.processPath(folder)
        self.currentIndex = self.jobs.currentIndex()
        self.saveRecent()
        self.setCombinedPath(self.basePath)
        self.setEnvs()
        self.loadFolders()
        self.setinfoRow()
    # def setJob(self, path):
    #     self.setCombinedPath(path)

    def loadProject(self, i, j):
        cell = self.table.item(i, 0).text()
        path = os.path.join(self.combinedPath, cell)
        if hou.hipFile.name().endswith('untitled.hip'):
            hou.hipFile.load(path)
        elif hou.ui.displayMessage("Save current file and open?", buttons=("Yes", "No")) == 0:
            hou.hipFile.save()
            hou.hipFile.load(path)

        hou.hscript("autosave on")
        self.noteEdit.setText("")
        self.loadNotes()
        self.loadHDA()

    def getRecent(self):  # set the table from the dir
        base = hou.getenv("HOUDINI_USER_PREF_DIR")
        file = "file.history"

        load = os.path.join(base, file)

        data = open(load, "r")
        read = data.read().split("}")[0]
        read = read.split("{")[1]

        list = read.split("\n")

        return list

    def loadFolders(self):

        try:
            hou.getenv("JOB")
            search_path = self.basePath

            rows = self.table.rowCount()
            for i in range(rows):
                self.table.removeRow(0)

            prjs = os.listdir(hou.expandString(
                self.combinedPath).replace("//", "/"))

            prjs.sort()

            fpath = self.combinedPath.replace("//", "/") + "/"
            prjs.sort(key=lambda x: os.path.getmtime(hou.expandString(fpath + x)))

            # new = prjs.sort(key=lambda x: os.path.getmtime(x))

            # print(new)

            rowPosition = 1
            for job in prjs:
                if len(job) > 0:
                    if job.endswith(".hiplc"):
                        job = job.replace(
                            "C:/Users/PIC-TWO/Partners in Crime Dropbox/Luke Van/STUDIO-PIC/", "$DB/")
                        job = job.replace("P:/", "$DB/")
                        job = job.replace(
                            "/Users/lukevan/Partners in Crime Dropbox/STUDIO-PIC/", "$DB/")

                        self.table.insertRow(0)
                        # Insert at 0 index because we are inserting at the start

                        self.pathItem = QtWidgets.QTableWidgetItem(f"{job}")

                        self.pathItem.setFlags(
                            QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

                        self.table.setItem(
                            0, 0, self.pathItem)

                        rowPosition += 1

        except Exception as e:
            #     # if not type(e) == FileNotFoundError:
            # print(e)
            self.table.clear()
            self.table.insertRow(0)
            self.pathItem = QtWidgets.QTableWidgetItem("No .hip found")
            self.pathItem.setFlags(QtCore.Qt.ItemIsSelectable)
            self.table.setItem(
                0, 0, self.pathItem)

    def processPath(self, path):
        return hou.expandString(path).replace("C:/Users/PIC-TWO/Partners in Crime Dropbox/Luke Van/STUDIO-PIC/", "$DB/").replace("P:/", "$DB/").replace(
            "/Users/lukevan/Partners in Crime Dropbox/Luke Van/STUDIO-PIC/", "$DB/").replace("//", "/")

    def setEnvs(self):
        hou.hscript("setenv -s %s=%s" % ("JOB", f'{self.processPath(self.basePath)}'))
        hou.hscript("setenv -s %s=%s" % ("HIP", f'{self.processPath(self.combinedPath)}'))

    def loadHDA(self):
        try:
            file_path = hou.text.expandString("$HIP") + "/hda"

            print(file_path)
            files = os.listdir(file_path)
            for f in files:
                if not f == 'backup':
                    print(f)
                    hou.hda.installFile(file_path + "/" + f, oplibraries_file=None, change_oplibraries_file=True, force_use_assets=False)
        except:
            pass
