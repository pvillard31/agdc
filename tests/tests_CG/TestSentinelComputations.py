#__author__ = 'root'


"""
Ingester for landsat datasets.
"""
from __future__ import absolute_import
from datetime import date

from datacube.api.model import DatasetType, Satellite
from datacube.api.query import  list_tiles_as_list
from datacube.api.utils import  get_dataset_data

import logging

logging.basicConfig(level=logging.DEBUG);
_LOG = logging.getLogger('TestCG')

dataset_types = [DatasetType.SIGMA_VV]
min_date = date(2015, 01, 01)
max_date = date(2015, 12, 31)
satellites = [Satellite(i) for i in ['S1']]
x_cell = [89]
y_cell = [26]

tiles = list_tiles_as_list(x=x_cell, y=y_cell, acq_min=min_date,
                           acq_max=max_date,
                           satellites=satellites,
                           dataset_types=dataset_types)

print "Number of time periods: {}".format(len(tiles))

nbar_ds = tiles[0].datasets[DatasetType.SIGMA_VV]
data = get_dataset_data(nbar_ds)