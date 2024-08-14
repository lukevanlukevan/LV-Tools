import hou
from canvaseventtypes import *
import nodegraphdisplay as display
import nodegraphview as view
from datetime import datetime


def your_function():
    print("consistent double click")

def createEventHandler(uievent, pending_actions):
    if isinstance(uievent, MouseEvent):
        if (uievent.eventtype == 'mousedown'):
            try:
                if not hou.session.first_click:
                    if hou.session.first_click - datetime.now() > 1000:
                        hou.session.first_click = datetime.now()
                else:
                    second = datetime.now()
                    diff = second - hou.session.first_click
                    mil_diff = diff.total_seconds() * 1000
                    # print(mil_diff)
                    # if diff > 500:
                    if not mil_diff < 200:
                        hou.session.first_click = datetime.now()

                    else:
                        your_function()

            except:
                hou.session.first_click = datetime.now()

        return None, True
    return None, False
