import hou
import vexpressionmenu
import subprocess
import re


def addFloatParm(kwargs):
    node = kwargs["parms"][0].node()

    snippet = node.parm("snippet").eval()

    click, name = hou.ui.readInput("Variable name")

    clean = name.replace(" ", "_")

    if click == 0:
        if name == '':
            pass
        else:
            channel = f'float {clean} = chf("{clean}")' + ";"

            node.parm("snippet").set(channel + "\n\n" + snippet)

            vexpressionmenu.createSpareParmsFromChCalls(node, 'snippet')


def addChramp(kwargs):
    node = kwargs["parms"][0].node()

    snippet = node.parm("snippet").eval()

    click, name = hou.ui.readMultiInput(
        "Create ramp", ("Variable Name", "Ramp Name", "Sample Variable"),
        title="Create Ramp",
        buttons=("OK", "Cancel"),
        default_choice=0, close_choice=1,
    )
    clean = name[0].replace(" ", "_")
    clean2 = name[1].replace(" ", "_")
    clean3 = name[2].replace(" ", "_")

    if click == 0:
        if name == '':
            pass
        else:
            channel = f"float {clean} = chramp('{clean2}', {clean3})" + ";"

            node.parm("snippet").set(channel + "\n\n" + snippet)

            vexpressionmenu.createSpareParmsFromChCalls(node, 'snippet')


def cleanParms(kwargs):
    node = kwargs["parms"][0].node()

    snippet = node.parm("snippet").eval()

    parms = node.parms()

    pattern = r'(chf\(\"(.*?)\"\))'
    matches = re.findall(pattern, snippet)

    list1 = list()

    for m in matches:
        match = m[1]
        list1.append(match)

    np = parms[::-1]
    toremove = []
    for parm in parms:
        if len(parm.containingFolders()) == 0 and parm.parmTemplate().type().name() == "Float":
            if not parm.name() in list1:
                toremove.append(parm)

    for r in toremove:
        node.removeSpareParmTuple(r)


def regenParms(kwargs):
    node = kwargs["parms"][0].node()

    node.removeSpareParms()

    snippet = node.parm("snippet").eval()

    vexpressionmenu.createSpareParmsFromChCalls(node, 'snippet')
