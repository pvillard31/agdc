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

import os
import logging
from os.path import basename

from osgeo import gdal

from eotools.execute import execute

from agdc.ingest import SourceFileIngester
from agdc.cube_util import DatasetError
from .sentinel_dataset import SentinelDataset

_LOG = logging.getLogger(__name__)


def _is_sentinel_file(filename):
    """
    Does the given file match a Sentinel NetCDF file?

    (we could make this more extensive in the future, but it's directly derived from the old find_files() logic.

    :type filename: str
    :rtype: bool
    """
    basename = os.path.basename(filename).lower()
    #basename.startswith('sentinel') and
    #TODO more precise ?
    return filename.endswith(".img")


class SentinelIngester(SourceFileIngester):
    """Ingester class for Sentinel datasets."""

    def __init__(self, datacube=None, collection=None):
        super(SentinelIngester, self).__init__(_is_sentinel_file, datacube, collection)

    def open_dataset(self, dataset_path):
        """Create and return a dataset object.

        dataset_path: points to the dataset to be opened and have
           its metadata read.
        """

        return SentinelDataset(dataset_path)

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
