import hou
import vexpressionmenu


def addFloatParm(kwargs):
    node = kwargs["parms"][0].node()

    snippet = node.parm("snippet").eval()

    name = hou.ui.readInput("Variable name")[1]

    clean = name.replace(" ", "_")

    if name == '':
        pass
    else:
        channel = f'float {clean} = chf("{clean}");'

        node.parm("snippet").set(channel + "\n\n" + snippet)

        vexpressionmenu.createSpareParmsFromChCalls(node, 'snippet')
