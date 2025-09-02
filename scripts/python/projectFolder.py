import os
import hou

def openDir():
    hou.ui.showInFileBrowser(hou.hipFile.path())