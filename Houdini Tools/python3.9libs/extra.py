import hou
from canvaseventtypes import *
import nodegraphdisplay as display
import nodegraphview as view
from datetime import datetime


def do_stuff(uievent):
    if isinstance(uievent, MouseEvent):
        if (uievent.eventtype == 'mousedown'):
            ctrl = uievent.modifierstate.ctrl
            shift = uievent.modifierstate.shift
            alt = uievent.modifierstate.alt
            if (ctrl and shift and not alt):
                try:
                    pos = uievent.mousepos
                    editor = uievent.editor
                    items = editor.networkItemsInBox(pos, pos, for_select=True)
                    node = items[-1][0]

                    name = node.name()

                    name = "OUT_" + name

                    null = node.createOutputNode('null', name)
                    null.moveToGoodPosition()
                    return True
                except:
                    return False
    else:
        return False
