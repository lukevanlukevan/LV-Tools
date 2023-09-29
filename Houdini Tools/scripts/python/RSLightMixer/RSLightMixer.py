import os
import sys
import hou
import json

from PySide2 import QtCore, QtUiTools, QtWidgets, QtGui
from PySide2.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QSlider, QLabel, QPushButton, QHBoxLayout, QCheckBox
from PySide2.QtCore import Qt

from RSLightMixer import RSLightMixer

loader = QtUiTools.QUiLoader()

class RSLightMixer(QtWidgets.QWidget):

    def __init__(self):
        super(RSLightMixer, self).__init__()

        self.folderpath =  os.path.dirname(os.path.realpath(__file__))

        ui_file_path = self.folderpath + "/RSLightMixer.ui"
        
        self.ui = loader.load(ui_file_path)

        self.layout = QtWidgets.QVBoxLayout()
        self.main = self.ui.findChild(QGridLayout, "itemBox")

        self.fillList()

        self.layout.addWidget(self.ui)
        self.setLayout(self.layout)
        

        

    def fillList(self):
        geo = hou.node('/obj').children()

        i = 0
        for node in geo:
            # if node.type().name() == 'rsLight':
            item = LightItem(node)
            self.main.addWidget(item, i, 0)
            i += 1

class LightItem(QWidget):
    def __init__(self, node):
        super().__init__()

        parmDict = ['RSL_intensityMultiplier',
                    'Light1_exposure',
                    'RSL_spread']

        self.node = node

        self.folderpath = os.path.dirname(os.path.realpath(__file__))

        self.item = loader.load(self.folderpath + "/Item.ui")

        self.itemMain = self.item.findChild(QHBoxLayout)
        self.itemV = self.item.findChild(QVBoxLayout, "lightItem")

        self.enable = self.item.findChild(QCheckBox)
        if self.node.parm('light_enabled').eval() == 1:
            self.enable.setChecked(True)

        self.enable.setText(self.node.name())

        for parm in self.node.parms():
            if parm.name() in parmDict:

                holder = QHBoxLayout()
                label = QLabel(parm.description())
                label.setMinimumWidth(120)
                slider = QSlider(Qt.Horizontal)

                holder.addWidget(label)
                holder.addWidget(slider)

                self.itemV.addLayout(holder)



        #pass item into widget
        self.setLayout(self.itemMain)
        self.setFixedHeight(self.sizeHint().height())


        

    