import hou


# def getKeys():
#     """
#     Returns a list of keyframes for the selected nodes.
#     """
#     pane_tab = hou.ui.paneTabOfType(hou.paneTabType.ChannelEditor)
#     keyframes = pane_tab.graph().selectedKeyframes()

#     for parm in keyframes.keys():
#         for key in keyframes[parm]:
#             # print(key)
#             print(key.isSlopeAuto())
#             print(key.asCode())
#             # val = key.value()
#             # t = key.time()
#             # inAccel = key.inAccel()
#             # outAccel = key.accel()

#             # inSlope = key.inSlope()
#             # outSlope = key.slope()

#             # print(val, t, inAccel, outAccel, inSlope, outSlope)


def flip_y():
    """
    Returns a list of keyframes for the selected nodes.
    """
    pane_tab = hou.ui.paneTabOfType(hou.paneTabType.ChannelEditor)
    keyframes = pane_tab.graph().selectedKeyframes()

    for parm in keyframes.keys():

        vals = []
        for key in keyframes[parm]:
            vals.append(key.value())

        min_val = min(vals)
        max_val = max(vals)

        for key in keyframes[parm]:
            val = key.value()
            led = lerp(val, min_val, max_val, max_val, min_val)
            key.setValue(led)
            # key.setValue(lerp(val, min_val, max_val, max_val, min_val))
            # inAccel = key.inAccel()
            # outAccel = key.accel()

            # inSlope = key.inSlope()
            # outSlope = key.slope()
            parm.setKeyframe(key)


def flip_x():
    """
    Returns a list of keyframes for the selected nodes.
    """
    pane_tab = hou.ui.paneTabOfType(hou.paneTabType.ChannelEditor)
    keyframes = pane_tab.graph().selectedKeyframes()

    for parm in keyframes.keys():

        flipped = keyframes[parm][::-1]
        print(flipped)
        print(keyframes[parm])

        for key in keyframes[parm]:
            code = key.asCode(function_name="key")
            # key = code
            # print(code)
            # print(type(code))
        #     val = key.value()
        #     # key.setValue(lerp(val, min_val, max_val, max_val, min_val))
        #     # inAccel = key.inAccel()
        #     # outAccel = key.accel()

        #     # inSlope = key.inSlope()
        #     # outSlope = key.slope()
            # parm.setKeyframe(eval(str(key)))


def lerp(value, inmin, inmax, outmin, outmax):
    """
    Linearly interpolates a value from one range to another.
    """
    return (value - inmin) * (outmax - outmin) / (inmax - inmin) + outmin
