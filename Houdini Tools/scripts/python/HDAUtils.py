import os
import hou


def findLoadedHDAs():
    '''
    Returns a list of loaded HDAs in Houdini scene.
    HDAs installed by default with Houdini are skipped.
    '''
    loadedHDAs = []
    # Scan all node categories
    for category in hou.nodeTypeCategories().values():
        # Scan all node types
        for nodeType in category.nodeTypes().values():
            nodeDef = nodeType.definition()
            # If its a valid and unique HDA
            if (nodeDef is not None) and \
                    (nodeDef.libraryFilePath() not in loadedHDAs):
                # If not stored at "HFS" (Houdini Installation)
                if nodeDef.libraryFilePath().startswith(hou.getenv("LV")):
                    loadedHDAs.append(nodeDef)

    return loadedHDAs


def build_help():
    geo = hou.node("/obj/geo1")
    print(geo)
    i = 0
    for hda in findLoadedHDAs():
        if hda.nodeTypeCategory().name() == "Sop":
            if not "dev" in hda.nodeTypeName().lower():
                node = geo.createNode(hda.nodeTypeName())

                # node = hou.selectedNodes()[0]
                type_name = node.type().name()
                node_type = node.type().category().name()

                info = hou.hda.componentsFromFullNodeTypeName(type_name)

                namespace = f'{info[1]}--' if info[1] != '' else ''
                version = f'{info[3]}' if info[3] != '' else ''

                filename = namespace + info[2] + ".txt"

                path = hou.text.expandString("$LV") + "/help" + "/nodes/" + node_type

                combined = path + "/" + filename

                pretty = node.type().description()

                extra = f"= {pretty} =\n\n== Overview ==\n\nExplanation of the node's purpose and operation.\n\n@inputs\n\nLabel:\n\nWhat the input is for.\n\n@parameters"

                for parm in node.parms():
                    if not parm.isHidden():
                        if not parm.name().startswith("folder"):
                            # print("folder: ", parm.containingFolders()[-1])
                            # print(parm.description(), ", ", parm.name())
                            filler = parm.description()
                            ptype = parm.parmTemplate().type()
                            tname = ""
                            if ptype == hou.parmTemplateType.Int:
                                tname = "int"
                            elif ptype == hou.parmTemplateType.Float:
                                tname = "float"
                            elif ptype == hou.parmTemplateType.String:
                                tname = "string"
                            elif ptype == hou.parmTemplateType.Toggle:
                                tname = "toggle"
                            elif ptype == hou.parmTemplateType.Menu:
                                tname = "menu"
                            elif ptype == hou.parmTemplateType.Button:
                                tname = "button"
                            elif ptype == hou.parmTemplateType.Folder:
                                tname = "folder"
                            elif ptype == hou.parmTemplateType.Label:
                                tname = "label"
                            elif ptype == hou.parmTemplateType.Separator:
                                tname = "separator"
                            elif ptype == hou.parmTemplateType.Ramp:
                                tname = "ramp"
                            extra += "\n\n" + parm.description() + ":\n\t#" + parm.name() + ":\n\t" + tname + ": " + parm.description()

                if not os.path.exists(path):
                    os.makedirs(path)

                f = open(combined, "w")
                f.write(extra)
                f.close()

                node.destroy()
