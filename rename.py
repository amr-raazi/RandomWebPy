import glob
import os

print(os.listdir())
filelist = glob.glob(("photos"))
i = 1
for oldname in filelist:
    # ignore directories
    if os.path.isfile(oldname):
        # keep original path
        basepath = os.path.split(oldname)[0]
        newname = os.path.join(basepath, "{}.jpg".format(str(i)))
        i = i + 1
        print("Renaming {} to {}".format(oldname, newname))
        os.rename(oldname, newname)
