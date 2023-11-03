import hou
from hou import nodeEventType


def listenForLight(nodes):
    sel = nodes

    types = ['rslightdome::2.0', 'rslight', 'rslightsun']

    def flagChanged(node, event_type, **kwargs):
        flag = node.isDisplayFlagSet()

        # node.setGenericFlag(hou.nodeFlag.DisplayComment, True)

        c = hou.Color()

        if not flag:
            # node.setComment('Light Off')
            hsv = (0, 1, 1)
            c.setHSV(hsv)
            node.setColor(c)
        else:
            # node.setComment('Light On')
            hsv = (0, 0, 1)
            c.setHSV(hsv)
            node.setColor(c)

    for node in sel:
        flag = node.isDisplayFlagSet()

        if any(node.type().name() == x for x in types):
            node.removeAllEventCallbacks()
            node.addEventCallback((hou.nodeEventType.FlagChanged, ), flagChanged)
            node.parm('light_enabled').setExpression('hou.pwd().isDisplayFlagSet()', hou.exprLanguage.Python)

            c = hou.Color()

            if not flag:
                hsv = (0, 1, 1)
                c.setHSV(hsv)
                node.setColor(c)
            else:
                hsv = (0, 0, 1)
                c.setHSV(hsv)
                node.setColor(c)


def light_listen():

    def prep(event_type, **kwargs):
        single = kwargs['child_node']

        listenForLight(tuple([single]))
    hou.node("/obj").removeAllEventCallbacks()
    hou.node("/obj").addEventCallback((hou.nodeEventType.ChildCreated,), prep)  # type: ignore

    objs = hou.node("/obj").children()  # type: ignore
    for o in objs:
        print(o.name())
        cb = o.eventCallbacks()
        print(cb)
