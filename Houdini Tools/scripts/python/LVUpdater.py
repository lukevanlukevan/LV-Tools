# from git import Repo
import hou
import subprocess
import os
import shutil


def update():
    install_dir = hou.text.expandString("$LV")
    temp_dir = hou.text.expandString("$HOUDINI_TEMP_DIR") + "/LV-Tools"

    new_path = os.path.dirname(install_dir)
    print(new_path)
    hou.ui.showInFileBrowser(temp_dir)

    git_path = "https://github.com/lukevanlukevan/LV-Tools.git"

    # print("Downloading")
    shutil.rmtree(temp_dir, ignore_errors=True)
    os.mkdir(temp_dir)

    command_str = f"git clone '{git_path}' '{temp_dir}'"
    print(command_str)
    subprocess.call(["git", "clone", git_path, temp_dir])
    for f in os.listdir(temp_dir + "/Houdini Tools/"):
        print(f)
        shutil.move(temp_dir + "/Houdini Tools/" + f, install_dir + "/" + f)
    # shutil.move(temp_dir + "/Houdini Tools", new_path + "1")

    print("Downloaded")
