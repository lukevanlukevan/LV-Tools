
def shader_switch_to_mat(kwargs):
    node = kwargs['node']

    parms = node.parms()
    for inputs in node.inputs():
        pass
    # for parm in parms:
    #     print(parm.name())
    #     if parm.name.startswith('shader'):
    #         parm.set(1)