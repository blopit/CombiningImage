from PIL import Image
import tkinter as tk
from tkinter import filedialog
import glob
import numpy as np
import os



def combine(mypath, savepath):
    basewidth = 800
    buffer = 0

    onlyfiles = glob.glob("%s/*.gif" % mypath)
    onlyfiles.extend(glob.glob("%s/*.png" % mypath))

    #savepath = mypath + "/%s.jpg" % os.path.basename(mypath).strip()

    print(mypath)
    print(savepath)

    onlyfiles = sorted(onlyfiles, key=lambda x: float(x.rpartition('/')[2].rpartition('.')[0]))

    imgs = [Image.open(i) for i in onlyfiles]
    min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]

    imgr = []

    idx = 0
    for i in imgs:
        idx += 1
        if idx == len(imgs):
            buffer = 0

        wpercent = (basewidth / float(i.size[0]))
        hsize = int((float(i.size[1]) * float(wpercent)))
        inew = i.resize((basewidth, hsize), Image.ANTIALIAS)

        new = Image.new('RGB', (basewidth, hsize + buffer), (250, 238, 212, 0))
        new.paste(inew, (0, 0))

        imgr.append(new)

    #print(mypath)

    imgs_comb = np.vstack((np.asarray(i) for i in imgr))
    imgs_comb = Image.fromarray(imgs_comb)
    imgs_comb.save(savepath, dpi=(300, 300), quality=100, subsampling=0)


rootdir = filedialog.askdirectory()
savedir = "/Users/shrenilpatel/Documents/Axed/Merged"

filenames= os.listdir (rootdir)

for x in filenames:
    fullpath = os.path.join(rootdir, x)
    if os.path.isdir(fullpath):
        print(fullpath)

        #if "therapist" not in x.lower():
        #    continue

        try:
            os.mkdir(os.path.join(savedir, x))
        except:
            pass

        try:
            combine(fullpath, os.path.join(os.path.join(savedir, x), x + " - No Bubbles.png"))
        except:
            pass

        for y in os.listdir (fullpath):
            fullpath2 = os.path.join(fullpath, y)
            if os.path.isdir(fullpath2):
                print(fullpath2)

                try:
                    combine(fullpath2, os.path.join(os.path.join(savedir, x), x + " - Bubbles.png"))
                except:
                    pass

                #os.mkdir(os.path.join(os.path.join(savedir, x), y))


"""for subdir, dirs, files in os.walk(rootdir):
    for dir in dirs:
        print (os.path.join(subdir, dir))"""


