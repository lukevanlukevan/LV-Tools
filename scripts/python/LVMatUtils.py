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
    parms = node.parms()
    mat_node = node.path() + "/the_matnet/lv_mat1"
    new = hou.copyNodesTo([hou.node(mat_node)], hou.node("/mat"))
    node.parm("shop_materialpath1").set(new[0].path())

    for c in mat_node.children():
        c.destroy()