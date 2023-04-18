

LV Tools
======

A collection of HDAs that I use everyday to make my life easier/better/faster.

Free to use! If you would like to support me, you can do so at [Gumroad](https://wobblypictures.gumroad.com/) or [buy me a coffee](https://www.buymeacoffee.com/lukevan).

### Installation:

For those of you running Houdini 17.5 or later, you have an option for a much easier install. 
Simply create a folder inside your Houdini preferences directory (where the houdini.env typically is) called "packages", and place the LVTools.json file from the download into that package folder. Your preferences directory on Windows is typically in `My Documents\houdiniXX.X`. In OS X it's in `~Library/Preferences/Houdini`.

Then edit LVTools.json and change the "LV" variable to match the LV Tools install path you chose in step 1 (the directory that contains "otls", "scripts", and so on).

I have added some basic scripts, please feel free to give feedback on Discord.

### Basic Documentation (WIP)
<details>
 
 - **LV 3D Print Output**
>Send models to a slicer of your choice! Only tested with Cura, known to not work with PrusaSlicer just yet. Requests can be made at: https://discord.gg/6NuB4zwWKg

 - **LV Alembic**
>This is the Alembic ROP wrapped up with some parameters that I regularly use. Not the most exciting HDA but I use this over the Alembic ROP 95% of the time.

 - **LV Balancer**
>This is the Alembic ROP wrapped up with some parameters that I regularly use. Not the most exciting HDA but I use this over the Alembic ROP 95% of the time.
 
 - **LV Clip by Attribute**
 >Use an input attribute to clip geometry. Really clean, fast, and works on most types of geo. A big plus is that it doesn't need high resolution geo and is about 50 million times faster than a boolean. Works on curves too!

 - **LV Cycle Attribute**
>Cycle input attribute over time. Controls for the shape of remap, loop duration, direction, amount of loops and more.

 - **LV Delete Pieces**
>Deleted connected pieces of geometry based on a bounding object.

 - **LV Gnomon**
>Simple gnomon for checking orientation of points.

 - **LV Make Blend**
>The blend tool from Adobe Illustrator.
 
 - **LV Mat**
 >Another one that is not fancy at all, but I use this almost every time. Rather than hopping to `/mat` and back, this is an on stream material assignment (like the material sop) that automatically assigns dives into a matnet.

- **LV Path**
>Simple interface for setting up a path attribute on your geometry. I use this in conjunction with the **LV Alembic** in most cases where I have multiple geo streams that I will be modifying later or exporting to another DCC

- **LV Radial Symmetry**
>This node is essentially a kaleidoscope for your input geometry. Utilizes clips and mirrors so its relatively fast. On the debug tab there is a "view guides" option that can help the user line up the geometry.
Mirror mode is an even simpler mode that ensures edges lining up by splitting the geo down the middle. Updates the guides to match.

- **LV Simple ROP**
>Simple wrapper for the Redshift ROP with parameters that I often use exposed and in easy access.

 - **LV Simple Retime**
>Wrapper for Labs Simple Retime with some controls for ease of use exposed.

- **LV Slicer**
>Does what it says on the tin. Slices up geometry over a period of time, settable by the parameter menu. Controls for slice duration, angle of rotation, amount of slices, and more!

 - **LV Split and Path**
>Split geometry and assign `s@path` attribute. Stack them up to organize geometry for export with LV Alembic.

- **LV Blend by Attribute**
>Quick wrap of a wrangle that lerps based on an attribute. I use this more than the blend option on the Blendshape SOP purely out of speed and pride.

- **LV Fit Float**
>Inspired by the XK Studio internal tool, this takes some messy attributes you may have on your geo and automatically fits them between 0 and 1, with a ramp for remapping if needed.

- **LV Largest Piece**
>Groups or blasts all but the largest piece or primitive. Control for group name.

- **LV Move Along Path**
>Outputs point moving along path, controlled by slider. Multiple path mode works *sometimes*. This node is going to be fixed.

- **LV UV 2 World**
>Translate object UVs to worldspace for scattering or deforming. Used in conjunction with LV World 2 UV.

- **LV World 2 UV**
>Transform UV space alignment back to world space for deformation or editing. Used in conjunction with LV UV 2 World.

- **LV Variant**
>Simple wrapper for manually assigning variant. This node will become much more robust in the future.

</details>
