import hou
import LVLightUtils
from imp import reload

reload(LVLightUtils)

LVLightUtils.light_listen()
hou.hscript('exread "$LV/expressions/LVExpressions.expr"')
