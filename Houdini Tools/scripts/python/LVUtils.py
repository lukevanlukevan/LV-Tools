import hou


def createNamedGeo(kwargs):

    input = hou.ui.readInput("Container name:")[1].replace(" ", "_")

    if input == "":
        geo_name = "geo1"
    else:
        geo_name = input

    path = kwargs['pane'].pwd()

    new_geo = path.createNode("geo", geo_name)

    net_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)

    new_geo.setPosition(net_editor.cursorPosition())


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

        x_av = sum(xpos)/len(xpos)
        y_av = sum(ypos)/len(ypos)

        for node in nodes:
            x_off = node.position().x()-x_av
            new_x = x_av + (x_off*mult)

            y_off = node.position().y()-y_av
            new_y = y_av + (y_off*mult)

            if kwargs['ctrlclick']:
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
                if (color):
                    n.setColor(color)
                else:
                    pass

        hou.ui.openColorEditor(
            handleColorChange,
            include_alpha=False,
            initial_color=sCol)
    except IndexError:
        print('No node selected')


def openControls():
    node = hou.selectedNodes()[0]

    hou.ui.openParameterInterfaceDialog(node)
