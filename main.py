# -*- coding: utf-8 -*-
#!/usr/bin/env python
""" 
Program to open GDAL images and reclassify 
them using a quadtree structure
"""
import quadtree
import struct
from osgeo import gdal
from gdalconst import *

filename = "subset_3_utm2.img"

def initialize():
    """ Opens a GDAL dataset """
    print('Initializing')
    dataset = gdal.Open(filename, GA_ReadOnly)
    return dataset

def readImage(dataset, xsize, ysize):
    """ Reads a GDAL image into a 2D array """
    print('Reading image')
    grid = [[0 for x in xrange(ysize)] for x in xrange(xsize)]
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
    print band.XSize, '/', band.YSize

    for y in range(band.YSize):
        scanline = band.ReadRaster(0,y, band.XSize, 1, \
                                    band.XSize, 1, GDT_Float32)
        tuple_of_floats = struct.unpack('f' * band.XSize, scanline)

        for x in range(band.XSize):
            #print tuple_of_floats[x]
            grid[x][y] = tuple_of_floats[x]

    return grid


def saveGrid(grid):
    f = open('grid.txt','w')
    print f
    for x in range(len(grid)):
        f.write('\n')
        for y in range(len(grid[0])):
            f.write(str(grid[x][y]))
    f.close()

def createImage(dataset, datagrid, dst_filename):
    print('Creating image')
    format = "HFA"
    driver = gdal.GetDriverByName( format )
    metadata = driver.GetMetadata()
    if metadata.has_key(gdal.DCAP_CREATE) \
       and metadata[gdal.DCAP_CREATE] == 'YES':
        print 'Driver %s supports Create() method.' % format
    if metadata.has_key(gdal.DCAP_CREATECOPY) \
       and metadata[gdal.DCAP_CREATECOPY] == 'YES':
        print 'Driver %s supports CreateCopy() method.' % format

    print 'Copying'
    dst_ds = driver.CreateCopy( dst_filename, dataset, 0 )

def reclassify(grid):
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] > 24 or grid[x][y] < 21:
                grid[x][y] = 4
            elif grid[x][y] == 21:
                grid[x][y] = 3
            elif grid[x][y] == 22:
                grid[x][y] = 2
            else:
                grid[x][y] = 1

    return grid


if __name__ == '__main__':

    dataset = initialize()
    xsize = dataset.RasterXSize
    ysize = dataset.RasterYSize
    print 'Size: ', xsize, '/', ysize
    print 'Driver: ', dataset.GetDriver().ShortName

    datagrid = readImage(dataset,xsize,ysize)
    saveGrid(datagrid)
    datagrid = reclassify(datagrid)
    createImage(dataset, datagrid, 'testimg1.img')

    xxx = quadtree.quadtree()

    dataset = None
    """
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
                                     """