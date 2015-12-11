
# coding: utf-8


# necessary for plot display in jupyter

from datetime import date
import json
import matplotlib
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
#import ogr
#import pandas
from datacube.api.model import DatasetType, Satellite, BANDS, S1Bands
from datacube.api.query import list_tiles_as_list
from datacube.api.utils import get_dataset_data, get_dataset_metadata
from eotools.tiling import generate_tiles
from eotools.coordinates import convert_coordinates

# We define all the parameters we want to retrieve the data
dataset_types = [DatasetType.SIGMA_VV]
min_date = date(2015, 01, 01)
max_date = date(2015, 12, 31)
satellites = [Satellite(i) for i in ['S1']]
x_cell = [88,89,90,91]
y_cell = [25,26]


# We request the tiles according to the parameters and we check that we have the 6 tiles corresponding to our Landsat image
tiles = list_tiles_as_list(x=x_cell, y=y_cell, acq_min=min_date,
                           acq_max=max_date,
                           satellites=satellites,
                           dataset_types=dataset_types)

print "Number of time periods: {}".format(len(tiles))

dataset = tiles[2].datasets[DatasetType.SIGMA_VV]
data = get_dataset_data(dataset)
metadata = get_dataset_metadata(dataset)
samples, lines = metadata.shape
print "Tile file path location: {path}".format(path=dataset.path)
print "Array dimensions:\nx: {x} & y: {y}".format(x=samples, y=lines)


matrix = np.reshape(data.get(S1Bands.SIGMA_VV), (-1, 4000))
plt.imshow(matrix, cmap = cm.Greys_r, vmin=0, vmax=1)
plt.colorbar()

print data.get(S1Bands.SIGMA_VV).min()
print data.get(S1Bands.SIGMA_VV).max()

allVal = []
for tab in data.get(S1Bands.SIGMA_VV):
    for val in tab:
        if val > 0:
            allVal.append(val)


(n, bins) = np.histogram(allVal, bins=100, range=[0,1])  # NumPy version (no plot)
plt.plot(.5*(bins[1:]+bins[:-1]), n)
plt.show()



