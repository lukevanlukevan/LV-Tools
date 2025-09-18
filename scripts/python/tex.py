import hou


def createAbs():
    nodes = hou.selectedNodes()
    path = nodes[0].path()
    path_list = path.split("/")
    del path_list[-1]
    rebuild = "/".join(path_list)
    rebuild_item = hou.item(rebuild)

    abs = rebuild_item.createNode("RSMathAbs")
    baseP = nodes[0].position()
    abs.setPosition(hou.Vector2(baseP[0] - 5, baseP[1]))
    abs.setName("Scale_Controller", unique_name=True)
    for node in nodes:
        if node.type().name() == "redshift::TextureSampler":
            node.setInput(0, abs)

