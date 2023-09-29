import hou
import os
import json

folderpath = hou.getenv("LV")

def save(kwargs):

    p = kwargs['parms'][0]
    v = p.eval()
    keys = v.keys()
    ramp_basis = v.basis()[0]
    new_keys = []
    num_keys = len(v.basis())
    values = v.values()

    basis_type = 0
    if ramp_basis == hou.rampBasis.Linear:
        basis_type = 0
    elif ramp_basis == hou.rampBasis.Constant:
        basis_type = 1
    elif ramp_basis == hou.rampBasis.CatmullRom:
        basis_type = 2
    elif ramp_basis == hou.rampBasis.MonotoneCubic:
        basis_type = 3
    elif ramp_basis == hou.rampBasis.Bezier:
        basis_type = 4
    elif ramp_basis == hou.rampBasis.BSpline:
        basis_type = 5
    elif ramp_basis == hou.rampBasis.Hermite:
        basis_type = 6

    plot_values = [v.lookup(i*0.1) for i in range(10)]
    ramp = {
        "ramp_basis": basis_type,
        "ramp_keys": str(keys),
        "ramp_values": str(values),
        "plot_values": plot_values
    }
    
    saveJson(ramp)

def saveJson(ramp):
    prefs = ramp
    with open(f"{folderpath}\prefs.json", "w") as outfile:
        json.dump(prefs, outfile)

def load(kwargs, ramp_basis):
    p = kwargs['parms'][0]

    if os.path.isfile(f"{folderpath}\prefs.json"):

        with open(f"{folderpath}\prefs.json", "r") as openfile:
            json_object = json.load(openfile)

            basis_type = json_object["ramp_basis"]
            basis = None
            if basis_type == 0:
                basis = hou.rampBasis.Linear
            elif basis_type == 1:
                basis = hou.rampBasis.Constant
            elif basis_type == 2:
                basis = hou.rampBasis.CatmullRom
            elif basis_type == 3:
                basis = hou.rampBasis.MonotoneCubic
            elif basis_type == 4:
                basis = hou.rampBasis.Bezier
            elif basis_type == 5:
                basis = hou.rampBasis.BSpline
            elif basis_type == 6:
                basis = hou.rampBasis.Hermite

            keys = json_object["ramp_keys"].strip("()")
            keys = keys.split(", ")
            keys = list(dict.fromkeys(keys))
            new_keys = []
            for k in keys:
                new_keys.append(float(k))

            values = json_object["ramp_values"].strip("()")
            values = values.split(", ")
            values = list(dict.fromkeys(values))
            new_values = []
            for val in values:
                new_values.append(float(val))

            new_basis = (basis, ) * len(new_keys)

            new_ramp = hou.Ramp(new_basis, new_keys, new_values)
        
            p.set(new_ramp)