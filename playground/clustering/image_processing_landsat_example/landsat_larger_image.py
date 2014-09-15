from  PIL import Image, ImageEnhance, ImageFilter

import gdalnumeric
from skimage.filter import canny
from scipy import ndimage
from skimage.filter import sobel
from skimage.morphology import watershed
import numpy as np


basepath = "/home/vortex/Desktop/LAYERS/lorenzo/tiles/2003_02/LE71690602003035SGS00/rgb/"
file = "projected_5.tif"
image = Image.open(basepath + file)



src = "/home/vortex/Desktop/LAYERS/lorenzo/tiles/1995/Mosaic/test_clipped/m1995.tif"

dst = "/home/vortex/Desktop/LAYERS/lorenzo/tiles/1995/Mosaic/test_clipped/enanched3.tif"
dst_sobel = "/home/vortex/Desktop/LAYERS/lorenzo/tiles/1995/Mosaic/test_clipped/enanched_sobel.tif"
dst_sobel2 = "/home/vortex/Desktop/LAYERS/lorenzo/tiles/1995/Mosaic/test_clipped/enanched_sobel2.tif"
dst_segmentation = "/home/vortex/Desktop/LAYERS/lorenzo/tiles/1995/Mosaic/test_clipped/enanched_sobel_seg.tif"


# image = Image.open(src)
#
#
# im = image.convert('L')
# contr = ImageEnhance.Contrast(im)
# im = contr.enhance(2)
# # bright = ImageEnhance.Brightness(im)
# # im = bright.enhance(1)
# im.save(dst, "tiff")


# sobel2

# SEGMENTATION
image_array = gdalnumeric.LoadFile(src)
for a in image_array:
    print ("a %s") % a
    print ("-----------")
    for b in a:
        print ("%s") % b
    break
markers = np.zeros_like(image_array)
markers[image_array < 90] =1
markers[image_array > 90 ] = 2
markers[image_array > 110] = 3


segmentation = watershed(image_array, markers)
print segmentation
gdalnumeric.SaveArray(segmentation, dst_segmentation, format="GTiff")