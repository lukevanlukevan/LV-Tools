import os
import sys
import hou
import json
import requests
import zipfile
from hutil.PySide import QtCore, QtUiTools, QtWidgets, QtGui
from hutil.PySide.QtWidgets import QGridLayout
import shutil
from husd import assetutils


class ThumbnailModel(QtCore.QAbstractListModel):
    def __init__(self, directory, parent=None):
        super(ThumbnailModel, self).__init__(parent)
        self.directory = directory
        self.asset_list = []
        self._load_assets()

    def _load_assets(self):
        self.asset_list = []
        asset_extensions = (
            ".hip",
            ".hipnc",
            ".hda",
            ".hdanc",
            ".zip",
        )  # Added '.zip' for saved node assets
        for file in os.listdir(self.directory):
            if file.lower().endswith(asset_extensions):
                base_name = os.path.splitext(file)[0]
                asset_name = base_name  # Use base name as asset name
                linked_file = os.path.join(self.directory, file)
                thumb_path = os.path.join(
                    self.directory, base_name + ".png"
                )  # Corresponding thumbnail
                pixmap = QtGui.QPixmap()
                if os.path.exists(thumb_path):
                    pixmap.load(thumb_path)
                    scaled_pixmap = pixmap.scaled(
                        128,
                        128,
                        QtCore.Qt.KeepAspectRatio,
                        QtCore.Qt.SmoothTransformation,
                    )
                else:
                    # Use a default thumbnail if not found (e.g., a placeholder image)
                    # For now, we'll use an empty pixmap; you can load a default image here
                    scaled_pixmap = pixmap.scaled(128, 128, QtCore.Qt.KeepAspectRatio)
                self.asset_list.append(
                    {
                        "name": asset_name,
                        "linked_file": linked_file,
                        "thumbnail": scaled_pixmap,
                    }
                )

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.asset_list)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        item = self.asset_list[index.row()]
        if role == QtCore.Qt.DisplayRole:
            return item["name"]
        elif role == QtCore.Qt.ToolTipRole:
            return item["linked_file"]
        elif role == QtCore.Qt.DecorationRole:
            return QtGui.QIcon(item["thumbnail"])
        return None

    # Optional: Method to refresh the model if assets change
    def refresh(self):
        self.beginResetModel()
        self._load_assets()
        self.endResetModel()


class AssetLib(QtWidgets.QWidget):
    def __init__(self):
        super(AssetLib, self).__init__()
        self.folderpath = os.path.dirname(os.path.realpath(__file__))
        ui_file_path = self.folderpath + "/BasePanel.ui"
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file_path)
        mainLayout = QtWidgets.QVBoxLayout()
        self.libPath = hou.getenv(
            "lv_assetlib_path", os.path.join(self.folderpath + "\\db")
        )
        mainLayout.addWidget(self.ui)
        self.vertical = self.ui.findChild(QtWidgets.QVBoxLayout, "verticalLayout")
        self.setLayout(mainLayout)
        self.setAcceptDrops(True)  # Enable drag and drop on the widget
        self.drop_area_label = QtWidgets.QLabel("Drop items here")
        self.vertical.addWidget(self.drop_area_label)
        self.createInterface()

    def createInterface(self):
        self.model = ThumbnailModel(self.libPath, self)
        self.view = QtWidgets.QListView(self)
        self.view.setModel(self.model)
        self.view.setViewMode(QtWidgets.QListView.IconMode)
        self.view.setIconSize(QtCore.QSize(128, 128))
        self.view.setGridSize(QtCore.QSize(150, 150))
        self.view.setResizeMode(QtWidgets.QListView.Adjust)
        self.view.setMovement(QtWidgets.QListView.Static)  # Prevent dragging
        self.view.setWordWrap(True)
        self.view.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection
        )  # Allow multi-select if needed
        self.view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.view.customContextMenuRequested.connect(self.show_context_menu)
        self.view.doubleClicked.connect(self.load_asset)
        self.vertical.addWidget(self.view)
        # Optional: Add a refresh button or other controls
        refresh_button = QtWidgets.QPushButton("Refresh Assets")
        refresh_button.clicked.connect(self.model.refresh)
        self.vertical.addWidget(refresh_button)

    def load_asset(self, index):
        if not index.isValid():
            return
        item = self.model.asset_list[index.row()]
        linked = item["linked_file"]
        ext = os.path.splitext(linked)[1].lower()
        if ext == ".zip":
            self.cleanup_temp_dir()
            self.unzip_file(linked)
            self.paste_nodes()
        elif ext in (".hip", ".hipnc"):
            if hou.ui.displayConfirmation(
                f"Load HIP file {item['name']}? This will replace the current scene."
            ):
                hou.hipFile.load(linked)
        elif ext in (".hda", ".hdanc"):
            hou.hda.installFile(linked)
            hou.ui.displayMessage(f"HDA {item['name']} installed.")

    def show_context_menu(self, position):
        selected = self.view.selectedIndexes()
        if not selected:
            return
        menu = QtWidgets.QMenu(self)
        delete_action = menu.addAction("Delete")
        delete_action.triggered.connect(self.delete_selected)
        menu.exec_(self.view.viewport().mapToGlobal(position))

    def delete_selected(self):
        selected = self.view.selectedIndexes()
        if not selected:
            return
        if hou.ui.displayConfirmation(
            "Are you sure you want to delete the selected assets?"
        ):
            for idx in selected:
                item = self.model.asset_list[idx.row()]
                linked = item["linked_file"]
                thumb = os.path.join(self.libPath, item["name"] + ".png")
                try:
                    if os.path.exists(linked):
                        os.remove(linked)
                    if os.path.exists(thumb):
                        os.remove(thumb)
                except Exception as e:
                    print(f"Error deleting {linked}: {e}")
            self.model.refresh()

    def dragEnterEvent(self, event):
        text = event.mimeData().text()
        if text.startswith("http") or text.startswith("file"):
            self.drop_area_label.setText("Drop items here")
        else:
            self.drop_area_label.setText("Drop to paste")
        event.acceptProposedAction()

    def dropEvent(self, event):
        dropped_text = event.mimeData().text()
        if dropped_text.startswith("http"):
            self.handle_http_drop(dropped_text)
        elif dropped_text.startswith("file://"):
            self.handle_file_drop(dropped_text)
        else:
            self.handle_node_drop()
        self.drop_area_label.setText("Drop items here")
        event.acceptProposedAction()

    def clean_cpio_files(self):
        temp_dir = hou.getenv("HOUDINI_TEMP_DIR")
        if temp_dir:
            cpio_files = [f for f in os.listdir(temp_dir) if f.endswith(".cpio")]
            for file in cpio_files:
                os.remove(os.path.join(temp_dir, file))

    def handle_http_drop(self, dropped_text):
        self.cleanup_temp_dir()
        self.save_link(dropped_text)

    def handle_file_drop(self, dropped_text):
        self.cleanup_temp_dir()
        file_path = dropped_text[8:]
        self.unzip_file(file_path)
        self.paste_nodes()

    def handle_node_drop(self):
        selected = hou.selectedNodes()
        if not selected:
            return
        result = hou.ui.readInput("Enter asset name:", buttons=("OK", "Cancel"))
        button, asset_name = result
        if button != 0 or not asset_name:
            return
        self.clean_cpio_files()
        hou.copyNodesToClipboard(selected)
        temp_dir = hou.getenv("HOUDINI_TEMP_DIR")
        if not temp_dir:
            temp_dir = os.getenv("TEMP")
        if temp_dir:
            cpio_files = [f for f in os.listdir(temp_dir) if f.endswith(".cpio")]
            if cpio_files:
                zip_file_path = os.path.join(self.libPath, asset_name + ".zip")
                with zipfile.ZipFile(zip_file_path, "w") as zipf:
                    for file in cpio_files:
                        zipf.write(os.path.join(temp_dir, file), file)
                # Generate thumbnail
                viewer = hou.ui.paneTabOfType(hou.paneTabType.SceneViewer)
                thumb_path = os.path.join(self.libPath, asset_name + ".png")
                assetutils.saveThumbnailFromViewer(
                    sceneviewer=viewer, frame=1, res=(512, 512), output=thumb_path
                )
                self.model.refresh()

    def save_link(self, link):
        with hou.InterruptableOperation("Downloading data", open_interrupt_dialog=True):
            temp_dir = hou.getenv("HOUDINI_TEMP_DIR")
            filename = link.split("?")[0].split("/")[-1]
            if not temp_dir:
                temp_dir = os.getenv("TEMP")
            if temp_dir:
                file_path = os.path.join(temp_dir, filename)
                try:
                    response = requests.get(link)
                    response.raise_for_status()
                    with open(file_path, "wb") as file:
                        file.write(response.content)
                    if os.path.exists(file_path):
                        self.unzip_file(file_path)
                    self.paste_nodes()
                except requests.exceptions.RequestException as e:
                    print(f"Failed to download data: {e}")
            else:
                print("No temporary directory found.")

    def cleanup_temp_dir(self):
        temp_dir = hou.getenv("HOUDINI_TEMP_DIR")
        if temp_dir:
            lvshare_dir = os.path.join(temp_dir, "nodes.lvshare")
            zip_dir = os.path.join(temp_dir, "nodes.zip")
            if os.path.exists(zip_dir):
                os.remove(zip_dir)
            if os.path.exists(lvshare_dir):
                os.remove(lvshare_dir)

    def unzip_file(self, file_path):
        temp_dir = hou.getenv("HOUDINI_TEMP_DIR")
        file_path = file_path.replace("\\", "/")
        zip_file_path = file_path
        if temp_dir:
            with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
                zip_ref.extractall(temp_dir)
        else:
            print("No temporary directory found or file is not a ZIP.")

    def paste_nodes(self):
        network = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor).pwd()
        hou.pasteNodesFromClipboard(network)

