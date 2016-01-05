#__author__ = 'root'


"""
Ingester for landsat datasets.
"""
from __future__ import absolute_import
from datetime import date

from datacube.api.model import DatasetType, Satellite, PrecipitableWaterForecastBands
from datacube.api.query import  list_tiles_as_list
from datacube.api.utils import  get_dataset_data

import logging

logging.basicConfig(level=logging.DEBUG);
_LOG = logging.getLogger('TestCG')

dataset_types = [DatasetType.PRECIPITABLE_WATER_FORECAST]
min_date = date(2016, 01, 01)
max_date = date(2017, 02, 01)
satellites = [Satellite(i) for i in ['Forecast']]
x_cell = [8]
y_cell = [2]

tiles = list_tiles_as_list(x=x_cell, y=y_cell, acq_min=min_date,
                           acq_max=max_date,
                           satellites=satellites,
                           dataset_types=dataset_types)

print "Number of tiles: {}".format(len(tiles))

result_ds = tiles[0].datasets[DatasetType.PRECIPITABLE_WATER_FORECAST]
data = get_dataset_data(result_ds)

precipitableWaterForecast1Bands = data.get(PrecipitableWaterForecastBands._1)
precipitableWaterForecast3Bands = data.get(PrecipitableWaterForecastBands._3)
precipitableWaterForecast5Bands = data.get(PrecipitableWaterForecastBands._5)

print "finished precipitable forecast"