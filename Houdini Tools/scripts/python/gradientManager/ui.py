# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gradientManager.Tempui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, -1)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, 0, -1, -1)
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setEnabled(True)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tab.sizePolicy().hasHeightForWidth())
        self.tab.setSizePolicy(sizePolicy1)
        self.gridLayout_4 = QGridLayout(self.tab)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(6, 6, 6, 6)
        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(-1, 0, -1, 0)
        self.parmRow = QHBoxLayout()
        self.parmRow.setObjectName(u"parmRow")
        self.parmRow.setContentsMargins(0, 0, -1, 0)
        self.parmHolder = QGridLayout()
        self.parmHolder.setObjectName(u"parmHolder")

        self.parmRow.addLayout(self.parmHolder)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.parmRow.addItem(self.horizontalSpacer)

        self.label = QLabel(self.tab)
        self.label.setObjectName(u"label")

        self.parmRow.addWidget(self.label)

        self.rampName = QLineEdit(self.tab)
        self.rampName.setObjectName(u"rampName")
        self.rampName.setMaximumSize(QSize(200, 16777215))
        self.rampName.setMaxLength(50)

        self.parmRow.addWidget(self.rampName)

        self.saveRamp = QPushButton(self.tab)
        self.saveRamp.setObjectName(u"saveRamp")
        self.saveRamp.setMinimumSize(QSize(150, 0))
        self.saveRamp.setMaximumSize(QSize(300, 16777215))
        self.saveRamp.setStyleSheet(u"")

        self.parmRow.addWidget(self.saveRamp)


        self.gridLayout_5.addLayout(self.parmRow, 0, 0, 1, 1)

        self.line = QFrame(self.tab)
        self.line.setObjectName(u"line")
        sizePolicy2 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy2)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout_5.addWidget(self.line, 1, 0, 1, 1)

        self.scrollArea = QScrollArea(self.tab)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 776, 250))
        self.gridLayout_3 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.graphGrid = QGridLayout()
        self.graphGrid.setObjectName(u"graphGrid")
        self.graphGrid.setContentsMargins(-1, 0, -1, -1)
        self.gradHolder = QWidget(self.scrollAreaWidgetContents)
        self.gradHolder.setObjectName(u"gradHolder")
        self.gridLayout_7 = QGridLayout(self.gradHolder)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.libItem = QGridLayout()
        self.libItem.setObjectName(u"libItem")
        self.itemThumb = QPushButton(self.gradHolder)
        self.itemThumb.setObjectName(u"itemThumb")

        self.libItem.addWidget(self.itemThumb, 0, 0, 1, 1)


        self.gridLayout_7.addLayout(self.libItem, 0, 0, 1, 1)

        self.labelHolder = QGridLayout()
        self.labelHolder.setObjectName(u"labelHolder")
        self.removeBtn = QPushButton(self.gradHolder)
        self.removeBtn.setObjectName(u"removeBtn")

        self.labelHolder.addWidget(self.removeBtn, 0, 3, 1, 1)

        self.hspacer1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.labelHolder.addItem(self.hspacer1, 0, 0, 1, 1)

        self.itemLabel = QLabel(self.gradHolder)
        self.itemLabel.setObjectName(u"itemLabel")
        self.itemLabel.setAlignment(Qt.AlignCenter)

        self.labelHolder.addWidget(self.itemLabel, 0, 1, 1, 1)

        self.hspacer2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.labelHolder.addItem(self.hspacer2, 0, 2, 1, 1)


        self.gridLayout_7.addLayout(self.labelHolder, 1, 0, 1, 1)


        self.graphGrid.addWidget(self.gradHolder, 0, 0, 1, 1)


        self.gridLayout_3.addLayout(self.graphGrid, 0, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_5.addWidget(self.scrollArea, 4, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_5.addItem(self.verticalSpacer, 5, 0, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_5, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab_2, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 2, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"PBR Builder", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Ramp Name:", None))
        self.rampName.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\"Ease In\"", None))
        self.saveRamp.setText(QCoreApplication.translate("MainWindow", u"Save Ramp", None))
        self.itemThumb.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.removeBtn.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.itemLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Library", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Preferences", None))
    # retranslateUi

