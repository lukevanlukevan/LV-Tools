import hou


def setTimeline(kwargs):
    playbar = hou.playbar
    range = playbar.frameRange()
    playRange = playbar.playbackRange()
    fps = hou.fps()

    btn_idx, values = hou.ui.readMultiInput(
        "Set timeline", ("FPS", "Start Frame", "End Frame"),
        initial_contents=(str(fps), str(range[0]), str(range[1])),
        title="Timeline Settings",
        buttons=("OK", "Cancel"),
        default_choice=0, close_choice=1,
    )

    playbar.setFrameRange(float(values[1]), float(values[2]))
    hou.setFps(float(values[0]))
