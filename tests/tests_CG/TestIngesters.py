#__author__ = 'root'


"""
Ingester for landsat datasets.
"""
from __future__ import absolute_import

import logging
import gdal
import struct
from gdalconst import *


from agdc.ingest.landsat.core import LandsatIngester
from agdc.ingest.sentinel1.core import SentinelIngester
from agdc.ingest.smos.core import SmosIngester

logging.basicConfig(level=logging.DEBUG)
_LOG = logging.getLogger('TestCG')

sat = 3


if sat == 1:
    from agdc.ingest import run_ingest
    run_ingest(LandsatIngester)

if sat == 2:
    from agdc.ingest import run_ingest
    run_ingest(SentinelIngester)

if sat == 3:
    from agdc.ingest import run_ingest
    run_ingest(SmosIngester)

if sat == 4:
    dataset = gdal.Open( "/data/agdc/S1_orthorect/water_after.img", GA_ReadOnly )
    if dataset is None:
        print 'error reading s1 dataset'
    else:
        print 'ok, s1 dataset reading ok'



        cols = dataset.RasterXSize
        rows = dataset.RasterYSize
        bands = dataset.RasterCount
        driver = dataset.GetDriver().LongName

        geotransform = dataset.GetGeoTransform()
        print cols , ' columns'
        print rows, ' rows'
        print bands, ' bands'
        print driver, ' driver'
        print  geotransform

        originX = geotransform[0]
        originY = geotransform[3]
        pixelWidth = geotransform[1]
        pixelHeight = geotransform[5]
        print 'origin X', originX
        print 'originY', originY
        print 'pixelWidth', pixelWidth
        print 'pixelHeight',pixelHeight


        band = dataset.GetRasterBand(1)
        print 'Band Type=',gdal.GetDataTypeName(band.DataType)
        min = band.GetMinimum()
        max = band.GetMaximum()
        if min is None or max is None:
            (min,max) = band.ComputeRasterMinMax(1)
        print 'Min=%.3f, Max=%.3f' % (min,max)
        if band.GetOverviewCount() > 0:
            print 'Band has ', band.GetOverviewCount(), ' overviews.'
        if not band.GetRasterColorTable() is None:
            print 'Band has a color table with ', band.GetRasterColorTable().GetCount(), ' entries.'

        # TODO range
        for i in range(0, 1):
                # def ReadRaster(self, xoff, yoff, xsize, ysize, buf_xsize = None, buf_ysize = None, buf_type = None, band_list = None )
            scanline = band.ReadRaster( 0, i, band.XSize, 1, band.XSize, 1, GDT_Float32 )
            tuple_of_floats = struct.unpack('f' * band.XSize, scanline)
            print 'Line ', i, ' has ', len(tuple_of_floats), " values."

