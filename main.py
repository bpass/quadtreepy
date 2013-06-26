# -*- coding: utf-8 -*-
#!/usr/bin/env python

from osgeo import gdal
from gdalconst import *

filename = "subset_3_utm2.img"

def initialize():
    print('Initializing')    
    
def readImage():
    print('Reading image')

if __name__ == '__main__':
    dataset = gdal.Open(filename, GA_ReadOnly)
    if dataset is None:
        print("error opening file")
    print 'Driver: ', dataset.GetDriver().ShortName,'/', \
          dataset.GetDriver().LongName
    print 'Size is ',dataset.RasterXSize,'x',dataset.RasterYSize, \
          'x',dataset.RasterCount
    print 'Projection is ',dataset.GetProjection()
    
    geotransform = dataset.GetGeoTransform()
    if not geotransform is None:
        print 'Origin = (',geotransform[0], ',',geotransform[3],')'
        print 'Pixel Size = (',geotransform[1], ',',geotransform[5],')'

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
        print 'Band has a color table with ', \
        band.GetRasterColorTable().GetCount(), ' entries.'
    
    scanline = band.ReadRaster( 0, 0, band.XSize, 1, \
                                     band.XSize, 1, GDT_Float32 )