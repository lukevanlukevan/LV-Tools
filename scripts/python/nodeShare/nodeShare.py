import os
import shutil
import sys
import hou
import json
import requests
import zipfile

from PySide2 import QtCore, QtUiTools, QtWidgets, QtGui
from PySide2.QtWidgets import QGridLayout

class nodeShare(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(nodeShare, self).__init__(parent)

        drop_label = QtWidgets.QLabel("Selected nodes (drag and drop to add):")

        # Create a QFrame to show where to drop items
        self.drop_area = QtWidgets.QFrame()
        self.drop_area.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        self.drop_area.setLineWidth(1)
        self.drop_area.setMidLineWidth(0)
        # self.drop_area.setFixedSize(300, 200)  # Adjust size as needed

        # Set size policy to stretch horizontally and vertically
        self.drop_area.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        # Add text to the center of the QFrame
        self.drop_area_layout = QtWidgets.QVBoxLayout(self.drop_area)
        self.drop_area_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.drop_area_label = QtWidgets.QLabel("Drop items here")
        self.drop_area_layout.addWidget(self.drop_area_label)

        horiz_layout = QtWidgets.QHBoxLayout()
        horiz_layout.addWidget(self.drop_area)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(drop_label)
        layout.addLayout(horiz_layout)
        layout.setAlignment(QtCore.Qt.AlignTop)  # Align layout to the top

        # Make the QFrame take up the remaining space
        horiz_layout.setStretch(0, 1)

        self.setLayout(layout)
        self.setAcceptDrops(True)

    def clean_cpio_files(self):
        temp_dir = hou.getenv("HOUDINI_TEMP_DIR")
        if temp_dir:
            cpio_files = [f for f in os.listdir(temp_dir) if f.endswith('.cpio')]
            for file in cpio_files:
                os.remove(os.path.join(temp_dir, file))

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

    def handle_http_drop(self, dropped_text):
        self.cleanup_temp_dir()
        self.save_link(dropped_text)

    def handle_file_drop(self, dropped_text):
        self.cleanup_temp_dir()
        file_path = dropped_text[8:]
        self.unzip_file(file_path)
        self.paste_nodes()

    def handle_node_drop(self):
        self.clean_cpio_files()
        hou.copyNodesToClipboard(hou.selectedNodes())
        temp_dir = hou.getenv("HOUDINI_TEMP_DIR")
        if not temp_dir:
            temp_dir = os.getenv('TEMP')

        if temp_dir:
            cpio_files = [f for f in os.listdir(temp_dir) if f.endswith('.cpio')]

            if cpio_files:
                zip_file_path = os.path.join(temp_dir, "nodes.lvshare")
                with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                    for file in cpio_files:
                        zipf.write(os.path.join(temp_dir, file), file)
                hou.ui.showInFileBrowser(zip_file_path)

    def save_link(self, link):
        with hou.InterruptableOperation("Downloading data", open_interrupt_dialog=True):
            temp_dir = hou.getenv("HOUDINI_TEMP_DIR")
            filename = link.split("?")[0].split("/")[-1]
            if not temp_dir:
                temp_dir = os.getenv('TEMP')
            if temp_dir:
                file_path = os.path.join(temp_dir, filename)
                try:
                    response = requests.get(link)
                    response.raise_for_status()
                    with open(file_path, 'wb') as file:
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
        # zip_file_path = file_path[:-8] + ".zip"
        zip_file_path = file_path
        # os.rename(file_path, zip_file_path)

        if temp_dir:
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
                # os.remove(zip_file_path)
        else:
            print("No temporary directory found or file is not a ZIP.")

    def paste_nodes(self):
        network = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor).pwd()
        hou.pasteNodesFromClipboard(network)
