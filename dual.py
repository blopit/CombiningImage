import sys

from PIL import Image
import tkinter as tk
from tkinter import filedialog
import glob
import numpy as np
import os
import math

root = tk.Tk()
root.withdraw()

basewidth = 800
buffer = 0

mypath = filedialog.askdirectory()
onlyfiles = glob.glob("%s/*.gif" % mypath)
#onlyfiles.extend(glob.glob("%s/*.jpg" % mypath))
#onlyfiles.extend(glob.glob("%s/*.jpeg" % mypath))
onlyfiles.extend(glob.glob("%s/*.png" % mypath))

savepath = mypath + "/%s.jpg" % os.path.basename(mypath).strip()

print(onlyfiles)


onlyfiles = sorted(onlyfiles, key=lambda x: float(x.rpartition('/')[2].rpartition('.')[0]))

imgs    = [ Image.open(i) for i in onlyfiles ]
min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]

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

print(mypath)

imgs_comb = np.vstack( (np.asarray( i ) for i in imgr ) )
imgs_comb = Image.fromarray( imgs_comb)
imgs_comb.save( savepath, dpi=(300, 300), quality=100, subsampling=0)

def long_slice(image_path, outdir, slice_size):
    """slice an image into parts slice_size tall"""
    img = Image.open(image_path)
    width, height = img.size
    upper = 0
    left = 0
    base = 0
    slices = int(math.ceil(height/slice_size))
    print("Image height: ", height)
    print("Total slices: ", slices)

    count = 1
    for slice in range(slices):
        #if we are at the end, set the lower bound to be the bottom of the image
        if count == slices:
            lower = height
        else:
            lower = int(count * slice_size)

        bbox = (left, upper, width, lower)
        working_slice = img.crop(bbox)
        upper += slice_size
        print("Saving slice", count)
        working_slice.save(os.path.join(outdir, str(base + count)+".jpg"), dpi=(300, 300), quality=100, subsampling=0)
        count +=1

mpath = savepath
outpath =  os.path.dirname(mpath) + "/slices"

try:
    # Create target Directory
    os.mkdir(outpath)
    print("Directory ", outpath,  " Created ")

    try:
        long_slice(mpath, outpath, 1000)
    except:
        pass

except FileExistsError:
    print("Directory ", outpath,  " already exists")
