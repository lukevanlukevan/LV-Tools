import hou

node = hou.selectedItems()[0]

sNote = hou.selectedItems()[1]

diff = node.position()-sNote.position()

def onNodeMoved(**kwargs):
    sNote.setPosition(node.position() - diff)

def clearCall(**kwargs):
    node.removeAllEventCallbacks()

def linkNodes():
    if len(hou.selectedItems())<2:
        print("Select parent node and child node.")
    else:
        
        #register callback
        if len(node.eventCallbacks()) == 0 :
            node.removeAllEventCallbacks()
            node.setComment("This node has a linked node. To unlink, reactivate the script.")
            node.addEventCallback((hou.nodeEventType.PositionChanged, ), onNodeMoved)
            node.addEventCallback((hou.nodeEventType.BeingDeleted, ), clearCall)
        else:
            node.removeAllEventCallbacks()
            node.setComment("")