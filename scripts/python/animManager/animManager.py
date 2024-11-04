import os
import random
import sys
import hou
import json
from functools import partial

from PySide2 import QtCore, QtUiTools, QtWidgets, QtGui
from PySide2.QtWidgets import QGridLayout

class ColorSwatchButton(QtWidgets.QPushButton):
    rightClicked = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super(ColorSwatchButton, self).__init__(*args, **kwargs)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            self.rightClicked.emit()
        else:
            super(ColorSwatchButton, self).mousePressEvent(event)

class RightClickableButton(QtWidgets.QPushButton):
    rightClicked = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super(RightClickableButton, self).__init__(*args, **kwargs)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            self.rightClicked.emit()
        else:
            super(RightClickableButton, self).mousePressEvent(event)

class animManager(QtWidgets.QWidget):

    def __init__(self):
        super(animManager, self).__init__()

        self.folderpath = os.path.dirname(os.path.realpath(__file__))

        ui_file_path = self.folderpath + "/animManager.ui"

        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file_path)

        mainLayout = QtWidgets.QVBoxLayout()

        prev_key_btn = QtWidgets.QPushButton("Prev Key")
        prev_key_btn.setMinimumWidth(50)
        prev_key_btn.clicked.connect(self.prev_key)

        next_key_btn = QtWidgets.QPushButton("Next Key")
        next_key_btn.setMinimumWidth(50)
        next_key_btn.clicked.connect(self.next_key)

        diretion_btns = QtWidgets.QHBoxLayout()
        diretion_btns.addWidget(prev_key_btn)
        diretion_btns.addWidget(next_key_btn)

        mainLayout.addLayout(diretion_btns)

        # bookmark btns
        bookmark_btn = RightClickableButton("Bookmark this frame")
        bookmark_btn.setMinimumWidth(50)
        bookmark_btn.clicked.connect(self.init_bookmark)
        bookmark_btn.rightClicked.connect(self.handleMainButtonRightClick)
        bookmark_btn.setToolTip("Left click: Bookmark this frame\nRight click: Create with custom name")
        mainLayout.addWidget(bookmark_btn)

        # scroll area for the btns
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QtWidgets.QWidget()
        self.bookmarks = QtWidgets.QGridLayout(scroll_content)
        scroll_content.setLayout(self.bookmarks)
        scroll_area.setWidget(scroll_content)
        mainLayout.addWidget(scroll_area)

        self.setLayout(mainLayout)

        self.reload_bookmarks()

    def createInterface(self):
        pass

    def get_closest_key(self, parms, direction):
        curr_frame = hou.frame()
        closest_key = None

        all_keys = []

        if direction == "next":
            for parm in parms:
                after = parm.keyframesAfter(curr_frame)
                if after:
                    keys = [all_keys.append(key.frame()) for key in after if key.frame() > curr_frame]
            all_keys.sort()
        elif direction == "prev":
            for parm in parms:
                before = parm.keyframesBefore(curr_frame)
                if before:
                    keys = [all_keys.append(key.frame()) for key in before if key.frame() < curr_frame]
            all_keys.sort(reverse=True)

        closest_key = all_keys[0] if all_keys else None
        return closest_key if closest_key else curr_frame

    def get_graph(self):
        self.chan_edit = hou.ui.paneTabOfType(hou.paneTabType.ChannelEditor)
        self.list = self.chan_edit.channelList()
        self.parms = self.list.selected()

    def set_to_close(self, direction):
        self.get_graph()
        close = self.get_closest_key(self.parms, direction)
        hou.setFrame(close)
        pass

    def next_key(self):
        self.set_to_close("next")
        pass

    def prev_key(self):
        self.set_to_close("prev")
        pass

    def reload_bookmarks(self):
        while self.bookmarks.count():
            child = self.bookmarks.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for index, book in enumerate(hou.anim.bookmarks()):
            empty_btn = ColorSwatchButton()
            empty_btn.setFixedSize(20, 20)
            color = book.color().rgb()
            colorstring = 'QPushButton {background-color: rgb(' + str(color[0] * 255) + ',' + str(color[1] * 255) + ',' + str(color[2] * 255) + '); border: 1;}'
            empty_btn.setStyleSheet(colorstring)
            empty_btn.setFlat(True)
            empty_btn.setToolTip(f"Left click: Change color\nRight click: Rename")
            empty_btn.clicked.connect(partial(self.picker, index))
            empty_btn.rightClicked.connect(partial(self.handleRightClick, index))
            self.bookmarks.addWidget(empty_btn, index, 0)

            if book.name() == "":
                label_string = "Frame: " + str(int(book.startFrame()))
            else:
                label_string = book.name()

            bookmark_btn = RightClickableButton(label_string)
            bookmark_btn.setMinimumWidth(40)
            bookmark_btn.clicked.connect(partial(self.handleGridClick, index, delete=False))
            bookmark_btn.rightClicked.connect(partial(self.handleRightClick, index))
            bookmark_btn.setToolTip(f"Left click: Jump to frame\nRight click: Rename")
            self.bookmarks.addWidget(bookmark_btn, index, 1)

            delbtn = QtWidgets.QPushButton("❌")
            delbtn.setFixedSize(20, 20)
            delbtn.clicked.connect(partial(self.handleGridClick, index, delete=True))
            self.bookmarks.addWidget(delbtn, index, 2)

        spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.bookmarks.addItem(spacer, len(hou.anim.bookmarks()), 0, 1, 3)

    def handleRightClick(self, index):
        if index is not None:
            idx, name = hou.ui.readInput("Enter a name for the bookmark", buttons=("OK", "Cancel"))
            if idx == 0:
                hou.anim.bookmarks()[index].setName(name)
                self.reload_bookmarks()
        else:
            idx, name = hou.ui.readInput("Enter a name for the new bookmark", buttons=("OK", "Cancel"))
            if idx == 0:
                curr_frame = hou.frame()
                book = hou.anim.newBookmark(name, int(curr_frame), int(curr_frame))
                color = hou.Color((random.random(), random.random(), random.random()))
                book.setColor(color)
                self.reload_bookmarks()

    def picker(self, index):
        color = hou.ui.selectColor(initial_color=hou.anim.bookmarks()[index].color())
        self.set_color(index, color)

    def set_color(self, index, color):
        hou.anim.bookmarks()[index].setColor(color)
        self.reload_bookmarks()

    def handleGridClick(self, index, delete):
        bookmark = hou.anim.bookmarks()[index]
        if delete:
            self.remove_bookmark(bookmark)
        else:
            self.on_book_click(bookmark.startFrame())

    def remove_bookmark(self, bookmark):
        hou.anim.removeBookmarks([bookmark])
        self.reload_bookmarks()

    def on_book_click(self, index):
        self.jump_to_key(index)

    def jump_to_key(self, index):
        hou.setFrame(index)

    def init_bookmark(self, label=None):
        self.get_graph()
        curr_frame = hou.frame()
        label = label if label else str(curr_frame)
        book = hou.anim.newBookmark(label, int(curr_frame), int(curr_frame))
        color = hou.Color((random.random(), random.random(), random.random()))
        book.setColor(color)
        self.reload_bookmarks()

    def handleMainButtonRightClick(self):
        idx, label = hou.ui.readInput("Enter a name for the bookmark", buttons=("OK", "Cancel"), initial_contents=str(hou.frame()), title="Bookmark this frame")
        if idx == 0:
            if not label == "":
                self.init_bookmark(label)
            else :
                self.init_bookmark()