import hou

node = hou.pwd()
cam = hou.pwd().parm('cam')
link = hou.item(cam.eval())

def enableMask():
    if(link == None):
        pass
    else:
        ptg = link.parmTemplateGroup()
        
        vm = hou.properties.parmTemplate('viewport', 'viewport_mask')
        
        vmf = hou.FolderParmTemplate('View Mask', 'View Mask', parm_templates=((vm),))
        
        ptg.append(vmf)
        try:
            link.setParmTemplateGroup(ptg)
            link.parm("maskoverlay").set(node.path())
            link.parm("maskaspect").setExpression('ch("resx")/ch("resy")')
        except hou.Error:
            print("Failed to set View Mask. Camera may already have view mask options exposed.")
    
