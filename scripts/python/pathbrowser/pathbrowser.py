import os
import sys
import hou
import json

from hutil.PySide import QtCore, QtUiTools, QtWidgets, QtGui
from hutil.PySide.QtWidgets import QGridLayout, QTreeView
from hutil.PySide.QtCore import Qt, QAbstractItemModel, QModelIndex


class PathTreeModel(QAbstractItemModel):
    def __init__(self, paths=None):
        super(PathTreeModel, self).__init__()
        self.root_item = TreeItem("")
        if paths:
            self.add_paths(paths)

    def add_paths(self, paths):
        for path in paths:
            current = self.root_item
            parts = path.strip("/").split("/")
            for part in parts:
                found = False
                for child in current.children:
                    if child.data == part:
                        current = child
                        found = True
                        break
                if not found:
                    new_item = TreeItem(part, current)
                    current.children.append(new_item)
                    current = new_item

    def index(self, row, column, parent=QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()

        child_item = parent_item.children[row]
        if child_item:
            return self.createIndex(row, column, child_item)
        return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        child_item = index.internalPointer()
        parent_item = child_item.parent

        if parent_item == self.root_item:
            return QModelIndex()

        return self.createIndex(parent_item.row(), 0, parent_item)

    def rowCount(self, parent=QModelIndex()):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()

        return len(parent_item.children)

    def columnCount(self, parent=QModelIndex()):
        return 1

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        if role != Qt.DisplayRole:
            return None

        item = index.internalPointer()
        return item.data


class TreeItem:
    def __init__(self, data, parent=None):
        self.data = data
        self.parent = parent
        self.children = []

    def row(self):
        if self.parent:
            return self.parent.children.index(self)
        return 0


class PathBrowser(QtWidgets.QWidget):
    def __init__(self, kwargs):
        super(PathBrowser, self).__init__()
        self.folderpath = os.path.dirname(os.path.realpath(__file__))
        self.selection_callbacks = []  # List to store callback functions
        self.setup_ui()

    def getPaths(self, node_path):
        node = hou.node(node_path)
        geo = node.geometry()
        paths = geo.primStringAttribValues("path")
        return paths

    def node_selected(self, node):
        self.node_path = node.path()
        self.paths = self.getPaths(self.node_path)
        self.set_paths(self.paths)

    def setup_ui(self):
        # Create main layout
        mainLayout = QtWidgets.QVBoxLayout()

        self.node_chooser = hou.qt.NodeChooserButton()
        self.node_chooser.nodeSelected.connect(self.node_selected)

        self.node_path = ""
        mainLayout.addWidget(self.node_chooser)

        self.currentBtn = QtWidgets.QPushButton("Current node")
        self.currentBtn.clicked.connect(
            lambda x: self.set_paths(hou.selectedItems()[0])
        )
        mainLayout.addWidget(self.currentBtn)

        # Create tree view
        self.tree_view = QTreeView()
        self.tree_model = PathTreeModel()
        self.tree_view.setModel(self.tree_model)

        # Connect selection changed signal
        self.tree_view.selectionModel().selectionChanged.connect(
            self._on_selection_changed
        )

        # Add tree view to layout
        mainLayout.addWidget(self.tree_view)
        self.setLayout(mainLayout)

    def add_selection_callback(self, callback):
        """
        Add a callback function that will be called when an item is selected
        Args:
            callback (callable): Function that takes a single parameter (selected_path)
        """
        self.selection_callbacks.append(callback)

    def _on_selection_changed(self, selected, deselected):
        """
        Internal handler for selection changes
        """
        indexes = selected.indexes()
        if not indexes:
            return

        # Get the selected item
        index = indexes[0]
        selected_item = index.internalPointer()

        # Build the full path by traversing up the tree
        path_parts = []
        current = selected_item
        while current and current != self.tree_model.root_item:
            path_parts.insert(0, current.data)
            current = current.parent

        selected_path = "/" + "/".join(path_parts)

        # Call all registered callbacks
        for callback in self.selection_callbacks:
            callback(selected_path)

    def set_paths(self, paths):
        """
        Update the tree view with new paths
        Args:
            paths (list): List of paths to display
        """
        self.tree_model = PathTreeModel(paths)
        self.tree_view.setModel(self.tree_model)
        # Connect selection changed signal to new model
        self.tree_view.selectionModel().selectionChanged.connect(
            self._on_selection_changed
        )
        self.tree_view.expandAll()  # Expand all items by default

    def createInterface(self):
        pass
