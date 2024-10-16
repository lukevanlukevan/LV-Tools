import hou
import LVLightUtils
from importlib import reload

reload(LVLightUtils)

LVLightUtils.light_listen()
hou.hscript('exread "$LV/expressions/LVExpressions.expr"')
