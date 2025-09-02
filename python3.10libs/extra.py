import hou
from canvaseventtypes import *
import nodegraphdisplay as display
import nodegraphview as view
from datetime import datetime


def do_stuff(uievent):
    createEventHandler(uievent)
    # print("consistent double click")


def createEventHandler(uievent):

    if isinstance(uievent, MouseEvent):
        if (uievent.eventtype == 'mousewheel'):
            node_dive(uievent)
        if (uievent.eventtype == 'mousedown'):
            try:

                if not hou.session.first_click:
                    if hou.session.first_click - datetime.now() > 1000:
                        hou.session.first_click = datetime.now()
                else:
                    second = datetime.now()
                    diff = second - hou.session.first_click
                    mil_diff = diff.total_seconds() * 1000
                    # if diff > 500:
                    if not mil_diff < 200:
                        hou.session.first_click = datetime.now()

                    else:
                        ctrl = uievent.modifierstate.ctrl
                        shift = uievent.modifierstate.shift
                        if (ctrl and shift):
                            pos = uievent.mousepos
                            editor = uievent.editor
                            items = editor.networkItemsInBox(pos, pos, for_select=True)
                            node = items[-1][0]

                            name = node.name()

                            name = "OUT_" + name

                            null = node.createOutputNode('null', name)
                            null.moveToGoodPosition()

            except:
                hou.session.first_click = datetime.now()

        return None, True
    return None, False

def node_dive(uievent):
    try:
        ctrl = uievent.modifierstate.ctrl

        if ctrl:
            net = hou.ui.paneTabUnderCursor()
            netpos = net.cursorPosition()
            b = net.visibleBounds()
            min = b.min()
            max = b.max()
            tl = hou.Vector2(min.x(), max.y())
            br = hou.Vector2(max.x(), min.y())

            visnodes = net.networkItemsInBox(net.posToScreen(tl), net.posToScreen(br), for_select=True)
            sorted_visnodes = sorted([node[0] for node in visnodes if node[1] == "node"], key=lambda x: (netpos - x.position()).length())
            hero = sorted_visnodes[0]

            if uievent.wheelvalue > 0:
                net.cd(hero.path())
            else:
                net.setCurrentNode(hero.parent())
    except:
        pass