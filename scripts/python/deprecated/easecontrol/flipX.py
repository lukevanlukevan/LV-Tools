import hou
pane_tab = hou.ui.paneTabOfType(hou.paneTabType.ChannelEditor)
keyframes = pane_tab.graph().selectedKeyframes()

kfs = []
okfs = []
val = []

i = -1;

for parm in keyframes.keys():
    for key in keyframes[parm]:
        kfs.append(key)
        #okfs.append(key.value())
        okfs.append(key)
        val.append(key.value())
    parm.deleteAllKeyframes()


kfs.reverse()

for parm in keyframes.keys():
    for index in range(len(kfs)):
        
        #declare new vs old: in X, we want value to swap + invert slope
        newKey = kfs[index] #newkey created from unflipped keys
        
        accel = okfs[index].accel()
        inAccel = okfs[index].inAccel()
        
        slope = okfs[index].slope()
        inSlope = okfs[index].inSlope()
        
        print(accel)
        
        #do reversing
        
        newKey.setSlope(slope * -1)
        newKey.setInSlope(inSlope  * -1)
        newKey.setAccel(accel)
        newKey.setInAccel(inAccel)
        newKey.setValue(val[index])
        
        #set keyframe
        parm.setKeyframe(newKey)
        
        


        
        
        
        
    