

LV Tools
======

A collection of HDAs that I use everyday to make my life easier/better/faster.

### Installation:

For those of you running Houdini 17.5 or later, you have an option for a much easier install. 
Simply create a folder inside your Houdini preferences directory (where the houdini.env typically is) called "packages", and place the LVTools.json file from the download into that package folder. Your preferences directory on Windows is typically in `My Documents\houdiniXX.X`. In OS X it's in `~Library/Preferences/Houdini`.

Then edit LVTools.json and change the "LV" variable to match the LV Tools install path you chose in step 1 (the directory that contains "otls", "scripts", and so on).

### Basic Documentation

 - **LV Alembic**
This is the Alembic ROP wrapped up with some parameters that I regularly use. Not the most exciting HDA but I use this over the Alembic ROP 95% of the time.

 
 - **LV Clip by Attribute**
 Use an input attribute to clip geometry. Really clean, fast, and works on most types of geo. A big plus is that it doesn't need high resolution geo and is about 50 million times faster than a boolean. Works on curves too!
 
 - **LV Mat**
 Another one that is not fancy at all, but I use this almost every time. Rather than hopping to `/mat` and back, this is an on stream material assignment (like the material sop) that automatically assigns dives into a matnet.

- **LV Path**
Simple interface for setting up a path attribute on your geometry. I use this in conjunction with the **LV Alembic** in most cases where I have multiple geo streams that I will be modifying later or exporting to another DCC

- **LV Radial Symmetry**
This node is essentially a kaleidoscope for your input geometry. Utilizes clips and mirrors so its relatively fast. On the debug tab there is a "view guides" option that can help the user line up the geometry.
Mirror mode is an even simpler mode that ensures edges lining up by splitting the geo down the middle. Updates the guides to match.

- **LV Slicer**
Does what it says on the tin. Slices up geometry over a period of time, settable by the parameter menu. Controls for slice duration, angle of rotation, amount of slices, and more!

- **LV Blend by Attribute**
Quick wrap of a wrangle that lerps based on an attribute. I use this more than the blend option on the Blendshape SOP purely out of speed and pride.

- **LV Fit Float**
Inspired by the XK Studio internal tool, this takes some messy attributes you may have on your geo and automatically fits them between 0 and 1, with a ramp for remapping if needed.

- **LV Largest Prim**
Groups or blasts all but the largest primitive. Control for group name.

- **LV Move Along Path**
Barely stable. Outputs point moving along path, controlled by slider. Multiple path mode works *sometimes*. This node is going to be fixed.

- **LV Variant**
Simple wrapper for manually assigning variant. This node will become much more robust in the future.
