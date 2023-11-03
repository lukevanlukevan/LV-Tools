# from git import Repo
import hou
import subprocess
import os
import shutil


def update():
    path = hou.text.expandString("$LV")
    os.chdir(path)
    result = subprocess.run('git fetch --dry-run', shell=True, capture_output=True, text=True)

    if not result.stdout == "":
        if hou.ui.displayMessage("Update available. Download update?", buttons=("Yes", "No")) == 0:
            subprocess.run('git fetch')
            hou.ui.displayMessage("Updated. Please restart Houdini.", buttons=("Okay", "Close"))

    else:
        hou.ui.displayMessage("Up to date.", buttons=("Okay", "Close"))
