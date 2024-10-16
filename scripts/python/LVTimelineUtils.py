import hou # type: ignore

def set_quickmark(kwargs):
    # hou.anim.newBookmark("QM 1", int(hou.frame()), int(hou.frame()))
    get_quickmark()
    # print(kwargs)

def get_quickmark():
    marks = hou.anim.bookmarks()
    for mark in marks:
        hou.setFrame(mark.startFrame())