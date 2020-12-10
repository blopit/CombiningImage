import sys

from PIL import Image
import tkinter as tk
from tkinter import filedialog
import glob
import numpy as np

root = tk.Tk()
root.withdraw()

basewidth = 800
buffer = 56

mypath = filedialog.askdirectory()
onlyfiles = glob.glob("%s/*.tif" % mypath)
savepath = mypath + "/full.tiff"

onlyfiles = sorted(onlyfiles, key=lambda x: float(x.rpartition('/')[2].rpartition('.')[0]))

imgs    = [ Image.open(i) for i in onlyfiles ]
# pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
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

"""
images = map(Image.open, onlyfiles)
widths, heights = zip(*(i.size for i in images))

max_width = max(widths)
sum_height = sum(heights)

new_im = Image.new('RGB', (max_width, sum_height))

y_offset = 0
for im in images:
  new_im.paste(im, (0, y_offset))
  y_offset += im.size[0]
"""

#new_im.save()

imgs_comb = np.vstack( (np.asarray( i ) for i in imgr ) )
imgs_comb = Image.fromarray( imgs_comb)
imgs_comb.save( savepath, dpi=(300, 300), quality=100, subsampling=0)