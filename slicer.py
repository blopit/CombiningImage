from PIL import Image
import math
import os
from tkinter import filedialog

def long_slice(image_path, outdir, slice_size):
    """slice an image into parts slice_size tall"""
    imgg = Image.open(image_path)
    img = imgg.convert('RGB')
    width, height = img.size
    upper = 0
    left = 0
    base = 0
    slices = int(math.ceil(height/slice_size))
    print(height)

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
        #save the slice
        working_slice.save(os.path.join(outdir, str(base + count)+".jpg"), dpi=(300, 300), quality=100, subsampling=0)
        count +=1



mypath = filedialog.askopenfilename()
outpath = filedialog.askdirectory()

print(mypath)
print(outpath)

long_slice(mypath, outpath, 1130)