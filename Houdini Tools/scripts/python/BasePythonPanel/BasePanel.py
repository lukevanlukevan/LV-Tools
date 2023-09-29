import os
import sys
import hou
import json

from PySide2 import QtCore, QtUiTools, QtWidgets, QtGui
from PySide2.QtWidgets import QGridLayout


from texManager import texManager

class TexManager(QtWidgets.QWidget):

    def __init__(self):
        super(TexManager, self).__init__()

        self.folderpath =  os.path.dirname(os.path.realpath(__file__))

        ui_file_path = self.folderpath + "/BasePanel.ui"

        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file_path)

        mainLayout = QtWidgets.QVBoxLayout()

        mainLayout.addWidget(self.ui)
        self.setLayout(mainLayout)

    def createInterface(self):
        pass

        

    