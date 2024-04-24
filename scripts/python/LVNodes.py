import math
import os
import hou


def light_arrange(*kwargs):
    obj = hou.node('/obj')

    centerPos = hou.Vector2(0, 0)

    nodes = hou.selectedNodes()

    for index, n in enumerate(nodes):
        if index == 0:
            nodePos = n.position()
            centerPos -= nodePos
        else:
            ss = ""
            fb = ""
            ud = ""

            node = n

            node.setGenericFlag(hou.nodeFlag.DisplayComment, True)

            posx = node.parm('tx').eval()
            posz = node.parm('tz').eval() * -1
            posy = node.parm('ty').eval()

            if node.type().name() == 'rslight':
                intensity = str(node.parm('RSL_intensityMultiplier').eval())
                exposure = str(node.parm('Light1_exposure').eval())
                spread = str(node.parm('RSL_spread').eval())

            pos = hou.Vector2(posx, posz)
            newPos = pos.normalized()
            newPos *= 3 + (pos.length()/12)

            if posx < 0:
                ss = "Left"
            elif posx == 0:
                ss = ""
            else:
                ss = "Right"

            if posz > 0:
                fb = "Back"
            elif posz == 0:
                fb = ""
            else:
                fb = "Front"

            if posy > 0:
                ud = "Top"
            elif posy == 0:
                ud = ""
            else:
                ud = "Bottom"

            node.setPosition(hou.Vector2(newPos[0]-centerPos[0], newPos[1]-centerPos[1]))

            node.setName(ud + fb + ss + "_" + node.type().name(), True)
            if node.type().name() == 'rslight':
                node.setComment('Intensity: ' + intensity + os.linesep +
                                'Exposure: ' + exposure + os.linesep +
                                'Spread: ' + spread)


def comment_cache_size(*kwargs):

    def convert_size(size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    try:
        if kwargs[0]["node"] is not None:
            node = kwargs[0]["node"]
        else:
            hou.ui.displayMessage("Unable to detect path. Please select a node and try again.")
            return

        path = ""
        ntype = node.type().name()

        if ntype == "vellumio::2.0":
            path = node.parm("file").eval()
        elif ntype == "filecache::2.0":
            path = node.parm("sopoutput").eval()
        elif ntype == "labs::filecache::2.0":
            path = node.parm("sopoutput").eval()

        base = path.split("/")[0:-1]

        build = "/".join(base) + "/"

        if not os.path.exists(build):
            hou.ui.displayMessage("Path does not exist. Have you cached yet?")
            return

        size = sum(os.path.getsize(os.path.join(build, f)) for f in os.listdir(build))

        node.setComment("Size on disk: " + convert_size(size))
        node.setGenericFlag(hou.nodeFlag.DisplayComment, True)
    except Exception as e:
        print(e)
        hou.ui.displayMessage("Unable to detect path. Please share error in console on Discord.")
