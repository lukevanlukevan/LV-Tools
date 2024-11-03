import LVUtils
from importlib import reload



def build_menu():
    def call_wrapper(**kwargs):
        reload(LVUtils)
        LVUtils.createNamedGeo(**kwargs)

    pane = kwargs["pane"]
    ptype = pane.pwd().type().name()
    contextname = pane.pwd().childTypeCategory()

    selected = pane.pwd().selectedItems()

    tkwargs = {
        "pane": pane,
        "selected": selected
    }
    menu = {}

    if ptype == "obj":
        menu["n"] = {
            "type": "script_action",
            "label": "Named Geo",
            "script": lambda: call_wrapper(kwargs)
        }

    if ptype == "redshift_vopnet":
        pass

    return menu