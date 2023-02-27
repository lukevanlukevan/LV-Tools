def onNodeMoved(**kwargs):
    sNote.setPosition(node.position() - diff)

def clearCall(**kwargs):
    node.removeAllEventCallbacks()

if len(hou.selectedItems())<2:
    print("Select parent node and sticky note.")
else:
    node = hou.selectedItems()[0]

    sNote = hou.selectedItems()[1]
    
    diff = node.position()-sNote.position()
    
    #register callback
    if len(node.eventCallbacks()) == 0 :
        node.removeAllEventCallbacks()
        node.setComment("This node hasa a linked sticky note. To unlink, select this node and run the 'Remove Link' shelf tool.")
        node.addEventCallback((hou.nodeEventType.PositionChanged, ), onNodeMoved)
        node.addEventCallback((hou.nodeEventType.BeingDeleted, ), clearCall)
    else:
        node.removeAllEventCallbacks()
        node.setComment("")