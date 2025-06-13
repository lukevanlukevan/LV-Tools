import hou


def setTimeline(kwargs):
    playbar = hou.playbar
    range = playbar.frameRange()
    playRange = playbar.playbackRange()

    endmod = playRange[1]/range[1]
    startmod = playRange[0]/range[0]


    fps = hou.fps()

    btn_idx, values = hou.ui.readMultiInput(
        "Set timeline", ("FPS", "Start Frame", "End Frame"),
        initial_contents=(str(fps), str(range[0]), str(range[1])),
        title="Timeline Settings",
        buttons=("OK", "Cancel"),
        default_choice=0, close_choice=1,
    )

    playbar.setFrameRange(float(values[1]), float(values[2]))
    playbar.setPlaybackRange(float(values[1]) * startmod, float(values[2]) * endmod)
    hou.setFps(float(values[0]))
