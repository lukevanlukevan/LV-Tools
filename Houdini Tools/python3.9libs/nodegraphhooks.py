import hou
from canvaseventtypes import *
import nodegraphdisplay as display
import nodegraphview as view

import extra
from importlib import reload


def createEventHandler(uievent, pending_actions):
    reload(extra)
    if extra.do_more(uievent):
        return None, True
    else:
        return None, False
