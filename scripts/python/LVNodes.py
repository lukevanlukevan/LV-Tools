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


def comment_cache_size(kwargs=hou.pwd()):

    def convert_size(size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    try:
        # if kwargs["node"] is not None:
        #     node = kwargs["node"]
        # else:
        basenode = kwargs
        parm = basenode.parent()
        node = parm

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


def transfer_transform(kwargs=hou.pwd()):
    # node = kwargs

    nodes = hou.selectedNodes()
    n1 = nodes[0]
    n2 = nodes[1]

    n2.parm('tx').set(n1.parm('tx').eval())
    n2.parm('ty').set(n1.parm('ty').eval())
    n2.parm('tz').set(n1.parm('tz').eval())
    n2.parm('rx').set(n1.parm('rx').eval())
    n2.parm('ry').set(n1.parm('ry').eval())
    n2.parm('rz').set(n1.parm('rz').eval())
    n2.parm('sx').set(n1.parm('sx').eval())
    n2.parm('sy').set(n1.parm('sy').eval())
    n2.parm('sz').set(n1.parm('sz').eval())

    n1.parm('tx').set(0)
    n1.parm('ty').set(0)
    n1.parm('tz').set(0)
    n1.parm('rx').set(0)
    n1.parm('ry').set(0)
    n1.parm('rz').set(0)
    n1.parm('sx').set(1)
    n1.parm('sy').set(1)
    n1.parm('sz').set(1)

    n1.setInput(0, n2)


def createRSFocusTarget(kwargs):
    # print(kwargs)
    cam = hou.selectedNodes()[0]
    pos = cam.position()
    if cam.type().name() != "cam":
        hou.ui.displayMessage("Please select a camera node.")
        return
    else:
        ft = hou.node("/obj").createNode("null", "FT")
        cam.parm("RS_campro_dofUseHoudiniCamera").set(0)
        cam.parm("RS_campro_dofObject").set(ft.path())


def resetPsr(kwargs):
    nodes = hou.selectedNodes()
    for n in nodes:
        n.parm("tx").set(0)
        n.parm("ty").set(0)
        n.parm("tz").set(0)
        n.parm("rx").set(0)
        n.parm("ry").set(0)
        n.parm("rz").set(0)
