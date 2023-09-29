import hou


def listenForLight():
    sel = hou.selectedNodes()

    types = ['rslightdome::2.0', 'rslight']

    def flagChanged(node, event_type, **kwargs):
        if any(node.type().name() == x for x in types):
            enabled = node.parm("light_enabled")

            e = enabled.eval()
            node.setGenericFlag(hou.nodeFlag.DisplayComment, True)

            c = hou.Color()

            if e == 1:
                enabled.set(0)
                node.setComment('Light Off')
                hsv = (0, 1, 1)
                c.setHSV(hsv)
                node.setColor(c)
            else:
                enabled.set(1)
                node.setComment('Light On')
                hsv = (0, 0, 1)
                c.setHSV(hsv)
                node.setColor(c)

    for node in sel:
        node.removeAllEventCallbacks()
        node.addEventCallback((hou.nodeEventType.FlagChanged, ), flagChanged)

