import hou
from husd import assetutils


def lv_error(f, message):
    print("------------------------")
    print(f"Error running: {f}")
    # print("Logging error")
    print(message)
    print("------------------------")


def scenefile_preview():
    frame = hou.frame()
    options = f"-f {int(frame)} {int(frame)}"
    output_files = (
        hou.text.expandString("$HIP")
        + "/"
        + hou.text.expandString("$HIPNAME").split(".")[0]
        + ".jpg"
    )

    name = hou.hscript("viewls -n")[0].strip()

    command = f"viewwrite {options} {name}.persp1 {output_files}"
    print(command)
    hou.hscript(command)

    print("------------------------")
    print(f"Rendering scene file preview: {output_files}")
    print("------------------------")

    # sceneViewer = hou.ui.paneTabOfType(hou.paneTabType.SceneViewer)
    # viewport = sceneViewer.curViewport()
    # def_cam = viewport.camera()
    # if not def_cam:
    #     cam = hou.node("/obj").createNode("cam", "preview_cam")
    #     viewport.saveViewToCamera(cam)
    # else:
    #     cam = def_cam
    # viewport.setCamera(cam)
    # viewport.frameAll()

    # rop = hou.node("/out")
    # ogl = rop.createNode("opengl")
    # ogl.parm("camera").set(cam.path())
    # ogl.parm("trange").set(1)
    # ogl.parm("f1").set(hou.frame())
    # ogl.parm("f2").set(hou.frame())
    # ogl.parm("picture").set(output_files)
    # # ogl.parm("vm_outputpicture").set(output_files)
    # ogl.parm("execute").pressButton()

    # ogl.destroy()

    # viewer = hou.ui.paneTabOfType(hou.paneTabType.SceneViewer)
    # assetutils.saveThumbnailFromViewer(
    #     sceneviewer = viewer,
    #     frame=hou.frame(),
    #     res=(1080,1080),
    #     output=hou.getenv("HIPFILE").split(".")[0] + ".jpg"
    # )


def createRSMaterial(kwargs):
    path = kwargs["pane"].pwd()
    pane = kwargs["pane"]
    rs_mat = path.createNode("redshift_vopnet")

    rs_mat.setPosition(pane.cursorPosition())


def createNamedGeo(kwargs):
    input = hou.ui.readInput("Container name:")[1].replace(" ", "_")

    if input == "":
        geo_name = "geo1"
    else:
        geo_name = input

    path = kwargs["pane"].pwd()

    new_geo = path.createNode("geo", geo_name)

    net_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)

    new_geo.setPosition(net_editor.cursorPosition())


def createChildNull(kwargs):
    sel = hou.selectedItems()
    idx, input = hou.ui.readInput("Container name:", initial_contents="OUT ")

    if idx == 0:
        for node in sel:
            null = node.createOutputNode("null", input.strip().replace(" ", "_"))
            null.setDisplayFlag(False)
            null.setRenderFlag(False)


def makeSpace(kwargs):
    try:
        hou.selectedItems()[0]
    except:
        xpos = []
        ypos = []

        mult = 2

        nodes = hou.selectedItems()

        for node in nodes:
            xpos.append(node.position().x())
            ypos.append(node.position().y())

        x_av = sum(xpos) / len(xpos)
        y_av = sum(ypos) / len(ypos)

        for node in nodes:
            x_off = node.position().x() - x_av
            new_x = x_av + (x_off * mult)

            y_off = node.position().y() - y_av
            new_y = y_av + (y_off * mult)

            if kwargs["ctrlclick"]:
                node.setPosition(hou.Vector2(new_x, node.position().y()))
            else:
                node.setPosition(hou.Vector2(node.position().x(), new_y))


def colorControl():
    try:
        nodes = hou.selectedItems()

        sCol = hou.selectedItems()[0].color()

        color = sCol

        def handleColorChange(color, alpha):
            color = color

            nodes = hou.selectedItems()

            for index, n in enumerate(nodes):
                node = n
                if color:
                    n.setColor(color)
                else:
                    pass

        hou.ui.openColorEditor(
            handleColorChange, include_alpha=False, initial_color=sCol
        )
    except IndexError:
        print("No node selected")


def openControls():
    nodes = hou.selectedNodes()

    if len(nodes) > 0:
        node = nodes[0]

        hou.ui.openParameterInterfaceDialog(node)


def save_incremental():
    hou.hipFile.saveAndIncrementFileName()


def build_wedge():
    sel = hou.selectedItems()

    for node in sel:
        parms = node.parms()

        sel_parms = [parm.name() for parm in parms]

        hou.ui.selectParm(
            message=f"Select parm from {node.name()}",
            title=f"Wedge {node.name()}",
            initial_parms=list(node.parms()),
        )
        # hou.ui.selectFromList(parms, message=f"Select parm from {node.name()}", title=f"Wedge {node.name()}")


def inline_lvmat(**kwargs):
    nodes = hou.selectedItems()

    for node in nodes:
        node.createOutputNode("lv_mat")


def view_closest():
    net = hou.ui.paneTabUnderCursor()
    if not net.type() == hou.paneTabType.NetworkEditor:
        return
    else:
        netpos = net.cursorPosition()
        b = net.visibleBounds()
        min = b.min()
        max = b.max()
        tl = hou.Vector2(min.x(), max.y())
        br = hou.Vector2(max.x(), min.y())

        visnodes = net.networkItemsInBox(
            net.posToScreen(tl), net.posToScreen(br), for_select=True
        )
        sorted_visnodes = sorted(
            [node[0] for node in visnodes if node[1] == "node"],
            key=lambda x: (netpos - x.position()).length(),
        )

        sorted_visnodes[0].setGenericFlag(hou.nodeFlag.Display, True)
        sorted_visnodes[0].setGenericFlag(hou.nodeFlag.Render, True)


def snippet_to_text(kwargs=None):
    node = hou.selectedNodes()[0]
    print(kwargs)
    yes_names = ["snippet", "python", "code", "script"]

    fpath = hou.text.expandString("$LV/codeswap/swap.txt")

    found = None
    for parm in node.parms():
        if parm.name() in yes_names:
            found = parm.name()

    if kwargs["ctrlclick"] or kwargs["cmdclick"]:
        f = open(fpath, "r")
        node.parm(found).set(f.read())
        f.close()
    else:
        if found:
            content = node.parm(found).eval()
            f = open(fpath, "w")
            f.write(content)
            f.close()
