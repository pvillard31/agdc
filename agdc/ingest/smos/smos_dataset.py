#!/usr/bin/env python

#===============================================================================
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
#===============================================================================

"""
    smos_dataset.py - dataset class for SMOS datasets.

    This is the implementation of the AbstractDataset class for SMOS
    datasets.
"""
from __future__ import absolute_import

import os
import logging
import re
from lxml import etree
import datetime
from osgeo import gdal

from eotools.execute import execute

from agdc.cube_util import DatasetError
from agdc.ingest import AbstractDataset
from .smos_bandstack import SmosBandstack

#
# Set up logger.
#

LOGGER = logging.getLogger(__name__)

#
# Class definition
#


class SmosDataset(AbstractDataset):
    """Dataset class for sentinel datasets."""

    # pylint: disable=too-many-public-methods
    #
    # This class provides metadata using acessor functions. This is
    # both straight-forward and allows a docstring to be attached to
    # each to document the definition of the metadata being provided.
    #

    PROCESSING_LEVEL_ALIASES = {
        'Pixel Quality': 'PQA',
        'Fractional Cover': 'FC'
        }

    def __init__(self, dataset_path):
        """Opens the dataset and extracts metadata.

        """

        self._satellite_tag = "SMOS"
        self._satellite_sensor = "SMOS"

        #self._dataset_file = os.path.abspath(dataset_path)

        command = "find %s -name '*Soil_Moisture*' | sort" % dataset_path
        result = execute(command)['stdout'].split('\n')

        self._moisture_band_file=result[1]
        self._moisture_dqx_band_file=result[0]
        self._dataset_path = os.path.abspath(dataset_path)



        fileName, fileExtension = os.path.splitext(self._moisture_band_file)

        self._ds = gdal.Open(self._moisture_band_file, gdal.GA_ReadOnly)

        if not self._ds:
            raise DatasetError("Unable to open %s" % self.get_dataset_path())

        self._dataset_size = (os.path.getsize(self._moisture_band_file) + os.path.getsize(self._moisture_dqx_band_file))/1000
        
        LOGGER.debug('Transform = %s', self._ds.GetGeoTransform())
        LOGGER.debug('Projection = %s', self._ds.GetProjection())

        LOGGER.debug('RasterXSize = %s', self._ds.RasterXSize)
        LOGGER.debug('RasterYSize = %s', self._ds.RasterYSize)



        # TODO do stuff
        metadata_file_path = fileName[:fileName.find("_Soil_Moisture")] + '.HDR'
        metadata_file = open(metadata_file_path, 'r')
        self._xml_text = metadata_file.read()
        metadata_file.close()


        tree = etree.parse(metadata_file_path)
        startTime = tree.xpath("//*[local-name() = 'Precise_Validity_Start']")[0].text.split('UTC=')[1]
        endTime = tree.xpath("//*[local-name() = 'Precise_Validity_Stop']")[0].text.split('UTC=')[1]


        m = re.search('.*_\d{8}T\d{6}_\d{8}T\d{6}_(\d{3}).*_Soil_Moisture.*\.tif', os.path.basename(self._moisture_band_file))
        if m:
            dayNumber = m.group(1)

        self._rangeendingdate = endTime.split('T')[0]
        LOGGER.debug('RangeEndingDate = %s', self._rangeendingdate)

        self._rangeendingtime = endTime.split('T')[1]
        LOGGER.debug('RangeEndingTime = %s', self._rangeendingtime)

        self._rangebeginningdate = startTime.split('T')[0]
        LOGGER.debug('RangeBeginningDate = %s', self._rangebeginningdate)

        self._rangebeginningtime = startTime.split('T')[1]
        LOGGER.debug('RangeBeginningTime = %s', self._rangebeginningtime)

        self.scene_start_datetime = self._rangebeginningdate + " " + self._rangebeginningtime
        self.scene_end_datetime = self._rangeendingdate + " " + self._rangeendingtime

        self._dayNumber = int(dayNumber)
        LOGGER.debug('DayNumber = %d', self._dayNumber)

        self._cloud_cover_percentage = 0 #unknown for SMOS
        LOGGER.debug('CloudCover = %f', self._cloud_cover_percentage)

        self._completion_datetime = tree.xpath("//*[local-name() = 'Creation_Date']")[0].text.split('UTC=')[1]
        LOGGER.debug('ProcessedTime = %s', self._completion_datetime)

        band1 = self._ds
        self._width = band1.RasterXSize
        self._height = band1.RasterYSize
        self._gt = band1.GetGeoTransform()
        self._minx = self._gt[0]
        self._miny = self._gt[3] + self._width*self._gt[4] + self._height*self._gt[5]  # from
        self._maxx = self._gt[0] + self._width*self._gt[1] + self._height*self._gt[2]  # from
        self._maxy = self._gt[3]

        LOGGER.debug('min/max x coordinates (%s, %s)',str(self._minx), str(self._maxx))  # min/max x coordinates
        LOGGER.debug('min/max y coordinates (%s, %s)',str(self._miny), str(self._maxy))  # min/max y coordinates

        LOGGER.debug('pixel size (%s, %s)', str(self._gt[1]), str(self._gt[5])) # pixel size

        self._pixelX = self._width
        self._pixelY = self._height

        LOGGER.debug('pixels (%s, %s)', str(self._pixelX), str(self._pixelY)) # pixels

        self._gcp_count = None
        self._mtl_text = None
        self._processor_level = "Moisture"

        AbstractDataset.__init__(self)

    #
    # Methods to extract extra metadata
    #
    def _get_datetime_from_string(self, datetime_string):
        """Determine datetime.datetime value from a string in several possible formats"""
        
        format_string_list=[
                            '%Y-%m-%dT%H:%M:%S.%f', # e.g: 2012-12-28T01:36:14.000
                            '%Y-%m-%d %H:%M:%S.%f', # e.g: 2012-12-28 01:36:14.000 
                            '%Y-%m-%dT%H:%M:%S', # e.g: 2012-12-28T01:36:14 
                            '%Y-%m-%d %H:%M:%S' # e.g: 2012-12-28 01:36:14 
                            ]
        
        datetime_value = None
        
        for format_string in format_string_list:
            try:
                datetime_value =  datetime.datetime.strptime(datetime_string, format_string)
                break
            except ValueError:
                continue
            
        if datetime_value is None:
            raise ValueError("time data '%s' does not match any common format" % datetime_string)
             
        return datetime_value
        
    def _get_directory_size(self):
        """Calculate the size of the dataset in kB."""

        command = "du -sk %s | cut -f1" % self.get_dataset_path()
        LOGGER.debug('executing "%s"', command)
        result = execute(command)

        if result['returncode'] != 0:
            raise DatasetError('Unable to calculate directory size: ' +
                               '"%s" failed: %s' % (command, result['stderr']))

        LOGGER.debug('stdout = %s', result['stdout'])

        return int(result['stdout'])

    def _get_gcp_count(self):
        """N/A for SMOS."""

        return 0

    def _get_mtl_text(self):
        """N/A for SMOS."""

        return None

    def _get_xml_text(self):
        """N/A for SMOS."""

        return None

    #
    # Metadata accessor methods
    #

    def get_dataset_path(self):
        """The path to the dataset on disk."""
        return self._dataset_path

    def get_satellite_tag(self):
        """A short unique string identifying the satellite."""
        return self._satellite_tag

    def get_sensor_name(self):
        """A short string identifying the sensor.

        The combination of satellite_tag and sensor_name must be unique.
        """
        return self._satellite_sensor

    def get_processing_level(self):
        """A short string identifying the processing level or product.

        The processing level must be unique for each satellite and sensor
        combination.
        """

        return self._processor_level.upper()

    def get_x_ref(self):
        """The x (East-West axis) reference number for the dataset.

        In whatever numbering scheme is used for this satellite.
        """
        return self._dayNumber

    def get_y_ref(self):
        """N/A for SMOS."""
        return None

    def get_start_datetime(self):
        """The start of the acquisition.

        This is a datetime without timezone in UTC.
        """
        
        #2011-01-31 02:35:09.897216
        return self._get_datetime_from_string(self.scene_start_datetime)

    def get_end_datetime(self):
        """The end of the acquisition.

        This is a datatime without timezone in UTC.
        """

        return self._get_datetime_from_string(self.scene_end_datetime)

    def get_datetime_processed(self):
        """The date and time when the dataset was processed or created.

        This is used to determine if that dataset is newer than one
        already in the database, and so should replace it.

        It is a datetime without timezone in UTC.
        """
        return self._get_datetime_from_string(self._completion_datetime)

    def get_dataset_size(self):
        """The size of the dataset in kilobytes as an integer."""
        return self._dataset_size

    def get_ll_lon(self):
        """The longitude of the lower left corner of the coverage area."""
        return self._minx

    def get_ll_lat(self):
        """The lattitude of the lower left corner of the coverage area."""
        return self._miny

    def get_lr_lon(self):
        """The longitude of the lower right corner of the coverage area."""
        return self._maxx

    def get_lr_lat(self):
        """The lattitude of the lower right corner of the coverage area."""
        return self._miny

    def get_ul_lon(self):
        """The longitude of the upper left corner of the coverage area."""
        return self._minx

    def get_ul_lat(self):
        """The lattitude of the upper left corner of the coverage area."""
        return self._maxy

    def get_ur_lon(self):
        """The longitude of the upper right corner of the coverage area."""
        return self._maxx

    def get_ur_lat(self):
        """The lattitude of the upper right corner of the coverage area."""
        return self._maxy

    def get_projection(self):
        """The coordinate refererence system of the image data."""
        return self._ds.GetProjection()

    def get_ll_x(self):
        """The x coordinate of the lower left corner of the coverage area.

        This is according to the projection returned by get_projection.
        """
        return self.get_ll_lon()

    def get_ll_y(self):
        """The y coordinate of the lower left corner of the coverage area.

        This is according to the projection returned by get_projection.
        """
        return self.get_ll_lat()

    def get_lr_x(self):
        """The x coordinate of the lower right corner of the coverage area.

        This is according to the projection returned by get_projection.
        """
        return self.get_lr_lon()

    def get_lr_y(self):
        """The y coordinate of the lower right corner of the coverage area.

        This is according to the projection returned by get_projection.
        """
        return self.get_ll_lat()

    def get_ul_x(self):
        """The x coordinate of the upper left corner of the coverage area.

        This is according to the projection returned by get_projection.
        """
        return self.get_ul_lon()

    def get_ul_y(self):
        """The y coordinate of the upper left corner of the coverage area.

        This is according to the projection returned by get_projection.
        """
        return self.get_ul_lat()

    def get_ur_x(self):
        """The x coordinate of the upper right corner of the coverage area.

        This is according to the projection returned by get_projection.
        """
        return self.get_ur_lon()

    def get_ur_y(self):
        """The y coordinate of the upper right corner of the coverage area.

        This is according to the projection returned by get_projection.
        """
        return self.get_ur_lat()

    def get_x_pixels(self):
        """The width of the dataset in pixels."""
        return self._pixelX

    def get_y_pixels(self):
        """The height of the dataset in pixels."""
        return self._pixelY

    def get_gcp_count(self):
        """The number of ground control points?"""
        return self._gcp_count

    def get_mtl_text(self):
        """Text information?"""
        return self._mtl_text

    def get_cloud_cover(self):
        """Percentage cloud cover of the aquisition if available."""
        return self._cloud_cover_percentage

    def get_xml_text(self):
        """XML metadata text for the dataset if available."""
        return self._xml_text

    def get_pq_tests_run(self):
        """The tests run for a Pixel Quality dataset.

        This is a 16 bit integer with the bits acting as flags. 1 indicates
        that the test was run, 0 that it was not.
        """
        return None

    #
    # Methods used for tiling
    #

    def get_geo_transform(self):
        """The affine transform between pixel and geographic coordinates.

        This is a list of six numbers describing a transformation between
        the pixel x and y coordinates and the geographic x and y coordinates
        in dataset's coordinate reference system.

        See http://www.gdal.org/gdal_datamodel for details.
        """
        return self._gt

    def find_band_file(self, file_pattern):
        """Find the file in dataset_dir matching file_pattern and check
        uniqueness.

        Returns the path to the file if found, raises a DatasetError
        otherwise."""
        dataset_dir = self._dataset_path
        if not os.path.isdir(dataset_dir):
            raise DatasetError('%s is not a valid directory' % dataset_dir)
        filelist = [filename for filename in os .listdir(dataset_dir)
                    if re.match(file_pattern, filename)]
        if not len(filelist) == 1:
            raise DatasetError('Unable to find unique match ' +
                               'for file pattern %s' % file_pattern)

        return os.path.join(dataset_dir, filelist[0])


    def stack_bands(self, band_dict):
        """Creates and returns a band_stack object from the dataset.

        band_dict: a dictionary describing the bands to be included in the
        stack.

        PRE: The numbers in the band list must refer to bands present
        in the dataset. This method (or things that it calls) should
        raise an exception otherwise.

        POST: The object returned supports the band_stack interface
        (described below), allowing the datacube to chop the relevent
        bands into tiles.
        """
        return SmosBandstack(self, band_dict)
