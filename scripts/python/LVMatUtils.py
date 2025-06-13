import hou

def shader_switch_to_mat(kwargs):
    node = kwargs['node']

    parms = node.parms()
    for inputs in node.inputs():
        pass
    # for parm in parms:
    #     print(parm.name())
    #     if parm.name.startswith('shader'):
    #         parm.set(1)

def move_to_mat(kwargs):
    node = kwargs['node']
    mat_node = hou.node(node.path() + "/the_matnet/lv_mat1")
    new = hou.copyNodesTo([mat_node], hou.node("/mat"))
    node.parm("shop_materialpath1").set(new[0].path())

    for c in mat_node.children():
        c.destroy()

    # set parm refs
    new[0].setName(node.name())
    new[0].moveToGoodPosition()
    newmat = hou.node(new[0].path() + "/StandardMaterial1")
    newmat.parm("base_colorr").deleteAllKeyframes()
    newmat.parm("base_colorg").deleteAllKeyframes()
    newmat.parm("base_colorb").deleteAllKeyframes()
    newmat.parm("refl_weight").deleteAllKeyframes()
    newmat.parm("refl_roughness").deleteAllKeyframes()
    newmat.parm("base_colorr").set(node.parm("base_colorr").eval())
    newmat.parm("base_colorg").set(node.parm("base_colorg").eval())
    newmat.parm("base_colorb").set(node.parm("base_colorb").eval())
    newmat.parm("refl_weight").set(node.parm("refl_weight").eval())
    newmat.parm("refl_roughness").set(node.parm("refl_roughness").eval())

    oldinput = node.inputs()[0]

    material = node.createInputNode(0, "material")
    material.parm("shop_materialpath1").set(new[0].path())
    material.setInput(0, oldinput)
    node.destroy()
    material.moveToGoodPosition()
