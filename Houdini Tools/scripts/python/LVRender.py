import hou
import subprocess


def post_render(node=hou.pwd()):
    start = node.parm("f1").eval()  # type: ignore
    parm = node.parm("RS_outputFileNamePrefix")
    wide = parm.unexpandedString()  # type: ignore
    wide = wide.replace("$OS", node.name())

    if "$F4" in wide:
        wide = wide.replace("$F4", "%04d")
    elif "$F3" in wide:
        wide = wide.replace("$F3", "%03d")
    elif "$F2" in wide:
        wide = wide.replace("$F2", "%02d")

    full = hou.expandString(wide)
    print("full: ", full)

    video = "".join(full.split(".")[:-1]) + ".mp4"

    video = video.replace("%04d", "")
    video = video.replace("%03d", "")
    video = video.replace("%02d", "")

    command = f'ffmpeg -framerate 25 -y -start_number {start} -i "{full}" -c:v libx264 -crf 23 -pix_fmt yuv420p "{video}"'

    subprocess.Popen(command)

    hou.ui.showInFileBrowser(video)


def pre_render(node=hou.pwd()):
    parm = node.parm("RS_outputFileNamePrefix")
    wide = parm.unexpandedString()  # type: ignore
    import hou

    detects = ['$F', '$F4', '$F3', '$F2']
    if any(x in wide for x in detects):
        pass
        # hou.ui.displayMessage('Render output contains frame number identifier.', severity=hou.severityType.Message)
    else:
        hou.ui.displayMessage('Render output missing frame number identifier.', severity=hou.severityType.Warning)
        pass
        # hou.hscript('rkill *')
