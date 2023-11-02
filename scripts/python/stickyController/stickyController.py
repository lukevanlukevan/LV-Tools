import os
import sys
import hou
import json

from PySide2 import QtCore, QtUiTools, QtWidgets, QtGui
# from PyQt5.QtCore import *
# from PyQt5.QtUiTools import *
# from PyQt5.QtGui import *
from PySide2.QtWidgets import QGridLayout, QHBoxLayout

from stickyController import stickyController

class StickyController(QtWidgets.QWidget):

    def __init__(self):
        super(StickyController, self).__init__()

        self.folderpath =  hou.getenv("LV") + "/scripts/python/stickyController"

        ui_file_path = self.folderpath + "/BasePanel.ui"

        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file_path)
        self.basegrid = self.ui.findChild(QGridLayout, "baseGrid")

        mainLayout = QtWidgets.QVBoxLayout()

        self.initUI()

        mainLayout.addWidget(self.ui)
        self.setLayout(mainLayout)

    def initUI(self):
        self.c1 = hou.qt.ColorField()
        self.c2 = hou.qt.ColorField()
        self.hb1 = self.ui.findChild(QHBoxLayout, "hb1")
        self.hb2 = self.ui.findChild(QHBoxLayout, "hb2")
        self.hb1.addWidget(self.c1)
        self.hb2.addWidget(self.c2)
        

    # node = hou.pwd()
    # note = node.parm("note")
    # slider = node.parm("size").eval()
    # tc = node.parmTuple("tcolor").eval()
    # bgc = node.parmTuple("bgc").eval()
    # bg = node.parm("bg").eval()

    # sNote = hou.item(note.eval())

    # tcolor = hou.Color((tc))
    # bgcolor = hou.Color((bgc))


    # sNote.setTextSize(slider)
    # sNote.setTextColor(tcolor)
    # sNote.setColor(bgcolor)
    # sNote.setDrawBackground(bg)