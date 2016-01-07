#!/usr/bin/env python
# Test file from Geosciencei Australia for testing mosaic

import subprocess
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy
import rasterio
from rasterio.transform import Affine
from rasterio import crs

# create some synthetic data
a = numpy.random.randint(0, 127, (1000, 1000)).astype('int16')
b = numpy.random.randint(127, 256, (1000, 1000)).astype('int16')

# define an origin for each image, the second image is offset
a_transform = Affine.from_gdal(*[145.0, 0.00025, 0, -34.0, 0, -0.00025])
ulx, uly = (500, 500) * a_transform
b_transform = Affine.from_gdal(*[ulx, 0.00025, 0, uly, 0, -0.00025])

no_data = -999

# generate some random locations for which to turn into no data
x = numpy.random.randint(0, 500, 150)
y = numpy.random.randint(0, 500, 150)
rand_loc1 = (y, x)

# and again for the second image
x = numpy.random.randint(0, 500, 150)
y = numpy.random.randint(0, 500, 150)
rand_loc2 = (y, x)

# insert no data
a[500:, 500:][rand_loc1] = -999
b[0:, 0:][rand_loc2] = -999

# prep for outputing to disk
prj = crs.from_epsg(4326)
fname1 = 'image1.tif'
fname2 = 'image2.tif'
dims = a.shape
dtype = a.dtype.name

with rasterio.open(fname1, mode='w', driver='GTiff', width=dims[1],
                   height=dims[0], count=1, crs=prj, transform=a_transform,
                   nodata=no_data, dtype=dtype) as outds:
    outds.write(a, 1)

with rasterio.open(fname2, mode='w', driver='GTiff', width=dims[1],
                   height=dims[0], count=1, crs=prj, transform=b_transform,
                   nodata=no_data, dtype=dtype) as outds:
    outds.write(b, 1)

# build the vrt's
# we'll look at how the order of files affects the mosaicing process
subprocess.check_call(["gdalbuildvrt", "mosaic1.vrt", "image1.tif", "image2.tif"])
subprocess.check_call(["gdalbuildvrt", "mosaic2.vrt", "image2.tif", "image1.tif"])

ds1 = rasterio.open('mosaic1.vrt', 'r')
ds2 = rasterio.open('mosaic2.vrt', 'r')

img1 = ds1.read(1)
img2 = ds2.read(1)

# subset to the intersected region
subs1 = img1[500:1000, 500:1000]
subs2 = img2[500:1000, 500:1000]

# here we'll see how the ordering of data in the mosaic affects
# no data areas
b1 = subs1 < 127
b2 = subs2 > 127

"""
Low values in b1 should be where there was no data in image2.
High values in b2 should be where there was no data in image1.
This is because the second file is *overwriting* the data from the
first file in the mosaic order.
Pixels with no data in the first image in the mosaic order, will be replaced
by pixels from the second image in the mosaic order.
"""

fig, axes = plt.subplots(2, 2)
axes[0, 0].imshow(img1)
axes[0, 1].imshow(img2)
axes[1, 0].imshow(b1, cmap=cm.Greys_r)
axes[1, 1].imshow(b2, cmap=cm.Greys_r)

axes[0, 0].set_title("Mosaic 1")
axes[0, 1].set_title("Mosaic 2")
axes[1, 0].set_title("Intersection Mosaic 1")
axes[1, 1].set_title("Intersection Mosaic 2")

xlabels = axes[0, 0].get_xticklabels()
xlabels = [label.set_fontsize(8) for label in xlabels]
xlabels = axes[0, 1].get_xticklabels()
xlabels = [label.set_fontsize(8) for label in xlabels]
xlabels = axes[1, 0].get_xticklabels()
xlabels = [label.set_fontsize(8) for label in xlabels]
xlabels = axes[1, 1].get_xticklabels()
xlabels = [label.set_fontsize(8) for label in xlabels]

ylabels = axes[0, 0].get_yticklabels()
ylabels = [label.set_fontsize(8) for label in ylabels]
ylabels = axes[0, 1].get_yticklabels()
ylabels = [label.set_fontsize(8) for label in ylabels]
ylabels = axes[1, 0].get_yticklabels()
ylabels = [label.set_fontsize(8) for label in ylabels]
ylabels = axes[1, 1].get_yticklabels()
ylabels = [label.set_fontsize(8) for label in ylabels]

plt.tight_layout()
plt.show()
