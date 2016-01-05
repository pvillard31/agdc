#__author__ = 'root'


"""
Ingester for landsat datasets.
"""
from __future__ import absolute_import
from datetime import date

from datacube.api.model import DatasetType, Satellite, PercentileMoistureBands, PercentilePrecipitationBands
from datacube.api.query import  list_tiles_as_list
from datacube.api.utils import  get_dataset_data

import logging

logging.basicConfig(level=logging.DEBUG);
_LOG = logging.getLogger('TestCG')

dataset_types = [DatasetType.MOISTURE_PERCENTILE]
min_date = date(2000, 01, 01)
max_date = date(2000, 02, 01)
satellites = [Satellite(i) for i in ['Percentile']]
x_cell = [8]
y_cell = [2]

tiles = list_tiles_as_list(x=x_cell, y=y_cell, acq_min=min_date,
                           acq_max=max_date,
                           satellites=satellites,
                           dataset_types=dataset_types)

print "Number of tiles: {}".format(len(tiles))

result_ds = tiles[0].datasets[DatasetType.MOISTURE_PERCENTILE]
data = get_dataset_data(result_ds)

moisturePercentile65Band = data.get(PercentileMoistureBands._65)
moisturePercentile85Band = data.get(PercentileMoistureBands._85)
moisturePercentile95Band = data.get(PercentileMoistureBands._95)

print "finished moisture percentile"


dataset_types = [DatasetType.PRECIPITATION_PERCENTILE]
min_date = date(2000, 01, 01)
max_date = date(2000, 02, 01)
satellites = [Satellite(i) for i in ['Percentile']]
x_cell = [8]
y_cell = [2]

tiles = list_tiles_as_list(x=x_cell, y=y_cell, acq_min=min_date,
                           acq_max=max_date,
                           satellites=satellites,
                           dataset_types=dataset_types)

print "Number of tiles: {}".format(len(tiles))

result_ds = tiles[0].datasets[DatasetType.PRECIPITATION_PERCENTILE]
data = get_dataset_data(result_ds)

percentilePrecipitation85Band = data.get(PercentilePrecipitationBands._85)
percentilePrecipitation95Band = data.get(PercentilePrecipitationBands._95)
percentilePrecipitation99Band = data.get(PercentilePrecipitationBands._99)
print "finished precipitation percentile"