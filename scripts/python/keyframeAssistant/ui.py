# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'keyframeAssistant.ui'
##
# Created by: Qt User Interface Compiler version 5.15.2
##
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(560, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setSpacing(8)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(-1, -1, -1, 0)
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(
            u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 556, 596))
        self.gridLayout_2 = QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 10)
        self.mainGrid = QGridLayout()
        self.mainGrid.setObjectName(u"mainGrid")
        self.allParms = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.allParms.setObjectName(u"allParms")
        self.allParms.setMaximumSize(QSize(100, 16777215))

        self.mainGrid.addWidget(self.allParms, 0, 1, 1, 1)

        self.parmName = QLabel(self.scrollAreaWidgetContents_2)
        self.parmName.setObjectName(u"parmName")
        self.parmName.setMaximumSize(QSize(100, 16777215))
        self.parmName.setAlignment(
            Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.mainGrid.addWidget(self.parmName, 0, 0, 1, 1)

        self.multiBlock = QGridLayout()
        self.multiBlock.setObjectName(u"multiBlock")
        self.pushButton = QPushButton(self.scrollAreaWidgetContents_2)
        self.pushButton.setObjectName(u"pushButton")

        self.multiBlock.addWidget(self.pushButton, 0, 0, 1, 1)

        self.mainGrid.addLayout(self.multiBlock, 0, 2, 1, 1)

        self.gridLayout_2.addLayout(self.mainGrid, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 1, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)

        self.gridLayout_5.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.gridLayout.addLayout(self.gridLayout_5, 4, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate(
            "MainWindow", u"MainWindow", None))
        self.allParms.setText(
            QCoreApplication.translate("MainWindow", u"All", None))
        self.parmName.setText(QCoreApplication.translate(
            "MainWindow", u"Parm Name", None))
        self.pushButton.setText(QCoreApplication.translate(
            "MainWindow", u"Parm Name", None))
    # retranslateUi
