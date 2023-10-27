import hou
import vexpressionmenu
import subprocess


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


def regenParms(kwargs):
    node = kwargs["parms"][0].node()

    node.removeSpareParms()

    snippet = node.parm("snippet").eval()

    vexpressionmenu.createSpareParmsFromChCalls(node, 'snippet')
