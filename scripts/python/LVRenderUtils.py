import hou


def snapshot_and_save(kwargs):
    from time import gmtime, strftime
    import shutil

    filename = strftime("Snapshot_%d_%b_%Y_%H_%M_%S", gmtime())
    path = hou.expandString('$HIP')
    outpath = path + "/Snapshots/" + filename

    # get rop

    rop = hou.node("/out")
    children = rop.children()

    rs_rops = list(filter(lambda x: x.type().name() == 'Redshift_ROP', children))
    if len(rs_rops) == 0:
        print("No Redshift_ROP found")
        return
    else:
        rop = rs_rops[0]

        old_range = rop.parm("trange").eval()
        old_output = rop.parm("RS_outputFileNamePrefix").eval()
        old_mplay = rop.parm("RS_renderToMPlay").eval()

        rop.parm("trange").set("off")
        rop.parm("RS_outputFileNamePrefix").set(outpath + ".png")
        # rop.parm("RS_renderToMPlay").set(0)

        rop.parm("execute").pressButton()

        rop.parm("trange").set(old_range)
        rop.parm("RS_outputFileNamePrefix").set(old_output)
        # rop.parm("RS_renderToMPlay").set(old_mplay)

        source_file = hou.hipFile.path()
        destination_file = outpath + ".hip"

        shutil.copy(source_file, destination_file)
        hou.ui.showInFileBrowser(destination_file)
