from PIL import Image
import math
import os
from tkinter import filedialog

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

mypath = filedialog.askopenfilename()
outpath = os.path.dirname(mypath) + "/slices"

try:
    # Create target Directory
    os.mkdir(outpath)
    print("Directory ", outpath,  " Created ")

    try:
        long_slice(mypath, outpath, 1000)
    except:
        pass

except FileExistsError:
    print("Directory ", outpath,  " already exists")

