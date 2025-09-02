import LVUtils
import LVNodes
from importlib import reload
from functools import partial

def build_menu(kwargs, radialmenu):

    def call_func(func, kwargs):
        reload(LVUtils)
        reload(LVNodes)
        if func == "createNamedGeo":
            LVUtils.createNamedGeo(kwargs)
        elif func == "openControls":
            LVUtils.openControls()
        elif func == "changeColor":
            LVUtils.colorControl()
        elif func == "childNull":
            LVUtils.createChildNull(kwargs)
        elif func == "createFocusTarget":
            LVNodes.createRSFocusTarget(kwargs)
        elif func == "scenefilePreview":
            LVUtils.scenefile_preview()
        elif func == "createRSMaterial":
            LVUtils.createRSMaterial(kwargs)

    pane = kwargs["pane"]
    ptype = pane.pwd().type().name()
    contextname = pane.pwd().childTypeCategory()
    selected = pane.pwd().selectedItems()

    menu = {}

    directions = ["n", "s", "e", "w", "ne", "nw", "se", "sw"]
    items = []

    if ptype == "obj":
        items.append({
            "type": "script_action",
            "label": "Named Geo",
            "icon": "$LV/lv.svg",
            "script": lambda **kwargs: call_func("createNamedGeo",kwargs),
        })

    items.append({
            "type": "script_action",
            "label": "Open Controls",
            "icon": "$LV/lv.svg",
            "script": lambda **kwargs: call_func("openControls", kwargs),
        })
    items.append({
            "type": "script_action",
            "label": "Change Color",
            "icon": "$LV/lv.svg",
            "script": lambda **kwargs: call_func("changeColor", kwargs),
        })
    if ptype == "geo":
        items.append({
                "type": "script_action",
                "label": "Create Ouput Null",
                "icon": "$LV/lv.svg",
                "script": lambda **kwargs: call_func("childNull", kwargs),
            })
    if any([n.type().name() == "cam" for n in selected]):
        items.append({
            "type": "script_action",
            "label": "Create Focus Target",
            "icon": "$LV/lv.svg",
            "script": lambda **kwargs: call_func("createFocusTarget", kwargs),
        })

    items.append({
        "type": "script_action",
        "label": "Viewport Snapshot",
        "icon": "$LV/lv.svg",
        "script": lambda **kwargs: call_func("scenefilePreview", kwargs),
    })

    if ptype == "mat":
        items.append({
                "type": "script_action",
                "label": "Create RS Material",
                "icon": "$LV/lv.svg",
                "script": lambda **kwargs: call_func("createRSMaterial", kwargs),
            })

    for i, item in enumerate(items):

        menu[directions[i]] = item


    radialmenu.setRadialMenu(menu)