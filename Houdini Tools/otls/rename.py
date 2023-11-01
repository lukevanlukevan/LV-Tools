import os
import shutil

root = os.path.dirname(__file__)
print(root)

files = os.listdir(root)

for f in files:
    if f != "rename.py":
        name = f
        # if name.startswith("LV_"):
        #     new_name = name.replace("LV_", "LV.")
        #     os.rename(name, new_name)
        # if name.startswith("LV.LV_"):
        #     new_name = name.replace("LV.LV_", "LV.")
        #     extra = name[6:]
        #     new = "LV." + extra
        #     os.rename(name, new)
        # if f.startswith("."):
        # new_name = name.replace("LV", "LV.", 1)
        # os.rename(os.path.join(root, name), os.path.join(root, name[2:]))
        # if not name.startswith("LV"):
        #     os.rename(os.path.join(root, name), os.path.join(root, "LV." + name))
        # if "_" in name:
        #     test_str = name
        #     res = ''.join([word.capitalize() for word in test_str.split("_")])
        #     print(res.capitalize())
