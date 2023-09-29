import os
import sys
import hou
import json

from hutil.Qt import QtCore, QtUiTools, QtWidgets, QtGui
# from PyQt5.QtCore import *
# from PyQt5.QtUiTools import *
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *

from graph import graph

class graph(QtWidgets.QWidget):

    def __init__(self):
        super(graph, self).__init__()

        self.folderpath =  hou.getenv("LV") + "/scripts/python/graph"

        ui_file_path = self.folderpath + "/graph.ui"

        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file_path)


        self.mainGrid = self.ui.findChild(QtWidgets.QGridLayout, "mainGrid")

        self.y_values = [10, 30, 20, 50, 40, 30, 20, 10]
        self.graph  = GraphView(self.y_values)

        self.mainGrid.addWidget(self.graph, 0, 0)

        self.createInterface() #run create interface

        mainLayout = QtWidgets.QVBoxLayout()

        mainLayout.addWidget(self.ui)
        self.setLayout(mainLayout)

    def createInterface(self):
        pass

class GraphView(QtWidgets.QGraphicsView):
    def __init__(self, y_values):
        super().__init__()

        self.y_values = y_values

        # set up the scene
        self.scene = QtWidgets.QGraphicsScene(self)
        self.setScene(self.scene)

        self.setFixedSize(100, 100)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.setStyleSheet("border: None;")


        # set up the pen for drawing the lines
        self.pen = QtGui.QPen(QtCore.Qt.white)
        self.pen.setWidth(1)

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
            line = QtWidgets.QGraphicsLineItem(x1, y1, x2, y2)
            line.setPen(self.pen)
            self.scene.addItem(line)