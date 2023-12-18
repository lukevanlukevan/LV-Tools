import hou
import vexpressionmenu
import subprocess
import re
from LVUtils import lv_error


def moveWrangleParms(kwargs):
    node = kwargs["parms"][0].node()

    folder_name = "folder_generatedparms_snippet"
    ptg = node.parmTemplateGroup()

    # Find the folder to move
    folder = ptg.findFolder(folder_name)

    # Remove the folder from its current location
    ptg.remove(folder)

    # Add the folder to the new location
    new_folder = ptg.findFolder('folder1')
    if new_folder is None:
        new_folder = hou.FolderParmTemplate('folder1', 'folder1')
        ptg.append(new_folder)
    new_folder.addParmTemplate(folder)

    # Set the new parameter template group for the node
    node.setParmTemplateGroup(ptg)


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


def pivotFromSpare(kwargs):
    node = kwargs.get("node")
    try:
        if node.parm("spare_input0"):
            pass
        else:
            spare_input = hou.StringParmTemplate("spare_input0", "Spare Input 0", 1, default_value=([""]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.NodeReference, menu_items=(
                []), menu_labels=([]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal)
            spare_input.setHelp("Refer to this in expressions as -1, such as: npoints(-1)")
            spare_input.setTags({"cook_dependent": "1", "opfilter": "!!SOP!!", "oprelative": "."})
            node.addSpareParmTuple(spare_input)
        pt_sel = hou.IntParmTemplate("pt_sel", "Point Selection", 1, default_value=(0,))
        node.addSpareParmTuple(pt_sel)
    except:
        pass

    node.parm("px").setExpression('point(-1, ch("pt_sel"), "P", 0)', language=hou.exprLanguage.Hscript)
    node.parm("py").setExpression('point(-1, ch("pt_sel"), "P", 1)', language=hou.exprLanguage.Hscript)
    node.parm("pz").setExpression('point(-1, ch("pt_sel"), "P", 2)', language=hou.exprLanguage.Hscript)


def offsetByAttribute(kwargs):
    node = kwargs.get("node")
    parm = node.parm("frame")

    clicked, vals = hou.ui.readInput(
        "Offset attribute:",
        title="Offset By Attribute",
        default_choice=0, close_choice=1,
    )

    if clicked == 0:
        # try:
        spare_input = hou.StringParmTemplate("spare_input0", "Spare Input 0", 1, default_value=([""]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.NodeReference, menu_items=(
            []), menu_labels=([]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal)
        spare_input.setHelp("Refer to this in expressions as -1, such as: npoints(-1)")
        spare_input.setTags({"cook_dependent": "1", "opfilter": "!!SOP!!", "oprelative": "."})
        node.addSpareParmTuple(spare_input)

        offset = hou.IntParmTemplate("per_piece", "Offset Frames", 1, default_value=(0,))
        node.addSpareParmTuple(offset)

        parm.setExpression('$FF + (detail(-1, "iteration", 0) * ch("per_piece"))')

        recon = node.inputs()[0]

        split = node.createInputNode(0, 'split', f'split_by_{vals}')
        split.addSpareParmTuple(spare_input)
        loopStart = split.createInputNode(0, 'block_begin')
        loopStart.parm("method").set('input')

        loopStart.setInput(0, recon)

        meta = loopStart.parent().createNode('block_begin')
        meta.parm("method").set('metadata')
        meta.setPosition(loopStart.position() + hou.Vector2(4, 0))

        det = meta.path()

        split.parm('group').set(f'@{vals}==`detail(-1, "iteration", 0)`')
        split.parm('spare_input0').set(det)
        split.parm("grouptype").set("prims")
        # split.parm('negate').set(1)
        node.parm('spare_input0').set(det)

        loopEnd = node.createOutputNode('block_end')
        loopEnd.parm("useattrib").set(0)
        loopEnd.parm("itermethod").set('auto')
        loopEnd.parm("attrib").set(vals)
        loopEnd.parm("method").set('merge')
        # loopEnd.parm("blockpath").set(loopEnd.relativePathTo(loopStart))
        loopEnd.parm("blockpath").set(loopStart.path())
        loopEnd.parm("templatepath").set(loopStart.path())
        loopEnd.parm("class").set("primitive")
        loopEnd.parm("resetcookpass").pressButton()

        # loopStart.parm("blockpath").set(loopStart.relativePathTo(loopEnd))
        loopStart.parm("blockpath").set(loopEnd.path())
        meta.parm("blockpath").set(loopEnd.path())

        # except Exception as e:

        # lv_error("offsetByAttribute", e)


def regenParms(kwargs):
    node = kwargs["parms"][0].node()

    node.removeSpareParms()

    snippet = node.parm("snippet").eval()

    vexpressionmenu.createSpareParmsFromChCalls(node, 'snippet')
