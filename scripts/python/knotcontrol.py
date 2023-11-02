import hou

def doDist(kwargs, ramp_basis):
    p = kwargs['parms'][0]
    v = p.eval()
    keys = v.keys()
    new_keys = []
    num_keys = len(v.basis())
    values = v.values()

    new_basis = (ramp_basis, ) * (num_keys + 1)

    if ramp_basis == hou.rampBasis.Constant:
        new_basis = (ramp_basis, ) * (num_keys + 1)
        for i in range(len(keys)):
            new_keys.append(1/(num_keys) * i)
    else:
        pass

    new_ramp = hou.Ramp(new_basis, list(new_keys), list(v.values()))
    
    p.set(new_ramp)