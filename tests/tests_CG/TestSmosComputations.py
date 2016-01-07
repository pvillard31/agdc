#__author__ = 'root'


"""
Ingester for landsat datasets.
"""
from __future__ import absolute_import
from datetime import date

from datacube.api.model import DatasetType, Satellite, SMOSBands, SMOSMetadataKeys
from datacube.api.query import  list_tiles_as_list
from datacube.api.utils import  get_dataset_data,get_dataset_metadata

import logging

logging.basicConfig(level=logging.DEBUG);
_LOG = logging.getLogger('TestCG')

dataset_types = [DatasetType.MOISTURE]
min_date = date(2015, 01, 01)
max_date = date(2015, 12, 31)
satellites = [Satellite(i) for i in ['SMOS']]
x_cell = [0]
y_cell = [4]

tiles = list_tiles_as_list(x=x_cell, y=y_cell, acq_min=min_date,
                           acq_max=max_date,
                           satellites=satellites,
                           dataset_types=dataset_types)

print "Number of tiles: {}".format(len(tiles))

result_ds = tiles[0].datasets[DatasetType.MOISTURE]
data = get_dataset_data(result_ds)
metadata1 = data["metadata"][SMOSMetadataKeys.Moisture_offset.value]
metadata2 = data["metadata"][SMOSMetadataKeys.Moisture_scale_factor.value]
metadata3 = data["metadata"][SMOSMetadataKeys.Moisture_Dqx_offset.value]
metadata4 = data["metadata"][SMOSMetadataKeys.Moisture_Dqx_scale_factor.value]

moistureBand = data.get(SMOSBands.MOISTURE)
moistureDqxBand = data.get(SMOSBands.MOISTURE_DQX)
print "finished"