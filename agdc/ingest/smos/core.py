#!/usr/bin/env python

# ===============================================================================
# Copyright 2015 Geoscience Australia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================

"""
Ingester for Sentinel datasets.
"""
from __future__ import absolute_import

import re
import os
import logging
from os.path import basename

from osgeo import gdal

from eotools.execute import execute

from agdc.ingest import SourceFileIngester
from agdc.cube_util import DatasetError
from .smos_dataset import SmosDataset

_LOG = logging.getLogger(__name__)


def _is_smos_file(filename):
    """
    Does the given file match a Smos NetCDF file?

    (we could make this more extensive in the future, but it's directly derived from the old find_files() logic.

    :type filename: str
    :rtype: bool
    """
    basename = os.path.basename(filename).lower()
    #basename.startswith('sentinel') and
    #TODO more precise ?
    return filename.endswith(".tif")


class SmosIngester(SourceFileIngester):
    """Ingester class for Smos datasets."""

    def __init__(self, datacube=None, collection=None):
        super(SmosIngester, self).__init__(_is_smos_file, datacube, collection)

    def open_dataset(self, dataset_path):
        """Create and return a dataset object.

        dataset_path: points to the dataset to be opened and have
           its metadata read.
        """

        return SmosDataset(dataset_path)


    def find_datasets(self, source_dir):
        """Return a list of path to the datasets under 'source_dir'.
        Datasets are identified as a directory containing a 'scene01'
        subdirectory.
        Datasets are filtered by path, row, and date range if
        fast filtering is on (command line flag)."""

        _LOG.info('Searching for datasets in %s', source_dir)
        command = "find %s -name '*Soil_Moisture*' | sort" % source_dir
        _LOG.debug('executing "%s"', command)
        result = execute(command)
        assert not result['returncode'], \
            '"%s" failed: %s' % (command, result['stderr'])

        if len(result['stdout'].split('\n')) == 3:
            dataset_list = [source_dir]
        else:
            dataset_list = []

        return dataset_list

    def filter_dataset(self, path, row, date):
        """Return True if the dataset should be included, False otherwise.

        Overridden to allow NULLS for row
        """
        (start_date, end_date) = self.get_date_range()

        (min_path, max_path) = self.get_path_range()

        include = ((max_path is None or path is None or int(path) <= int(max_path)) and
                   (min_path is None or path is None or int(path) >= int(min_path)) and
                   (end_date is None or date is None or date <= end_date) and
                   (start_date is None or date is None or date >= start_date))

        return include

    def preprocess_dataset(self, dataset_list):
        """Performs pre-processing on the dataset_list object.

        dataset_list: list of datasets to be opened and have
           its metadata read.
        """


        return dataset_list
