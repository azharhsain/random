# -*- coding: utf-8 -*-
import os
from qgis.core import *
from qgis.gui import *
from qgis.analysis import *
from qgis.networkanalysis import *
from qgis.utils import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore
from qgis import core
from qgis.utils import iface
import osgeo.gdal
import gdal
from gdalconst import *
from osgeo import gdal
from osgeo.gdalnumeric import *
from osgeo.gdalconst import *
import gdal
import math
import qgis.analysis
import csv
import string
import gc
from itertools import *
import processing
from shutil import copyfile
import time
from qgis.analysis import QgsZonalStatistics

#Nighlights rasters list
nlight = ['F142002', 'F142003', 'F152000', 'F152001', 'F152002', 'F152003', 'F152004', 'F152005', 'F152006', 'F152007', 'F162004', 'F162005', 'F162006', 'F162007', 'F162008', 'F162009', 'F182010', 'F182011', 'F182012', 'F182013']
transform = 'bin'

for x in nlight:

    #Your directory
    os.chdir("/Users/azharhussain/Dropbox/GCP_Reanalysis/RA_Files/Azhar/Nightlights/Income/Data/shp")

    bins = numpy.array([0, 0.565356, 1.722871, 4.195489, 8.903278, 63])

    for z in range(0,len(bins)-1):

        #Nightlight rasters
        NL = "Raw_NL/{}.tif".format(x)
        raster = gdal.Open(NL)
        data1 = raster.GetRasterBand(1).ReadAsArray().astype(numpy.float64)

        df = numpy.array(data1)

        dataOut = ((df >= bins[z]) & (df <bins[z+1]))
        outFile = "{}_{}_bin{}.tif".format(transform, x, z+1)

        #Write the out file
        driver = gdal.GetDriverByName("GTiff")
        rasterOut = driver.Create(outFile, raster.RasterXSize, raster.RasterYSize, 1, gdalconst.GDT_Float64)
        CopyDatasetInfo(raster,rasterOut)
        bandOut=rasterOut.GetRasterBand(1)
        BandWriteArray(bandOut, dataOut)

        #Close the datasets
        raster = None
        bandOut = None
        rasterOut = None

        for var in ['BRA_adm2', 'NUTS_3', 'CHN_adm3', 'USA_adm2', 'IND_adm2', 'IDN_adm1']:

            #The shapefile you want to compute nightlights product for
            input = "{}".format(var)
            shapefile = "{}.shp".format(input)
            temp_name = "temporarybin"

            #Name of the CSV file that will be output
            out_csv = "/Users/azharhussain/Dropbox/GCP_Reanalysis/RA_Files/Azhar/Nightlights/Income/Data/NL/{}_{}_{}{}_NL_new.csv".format(input, x, transform,z+1)
            vbaselayer = QgsVectorLayer(shapefile, "adm2", "ogr")

            #Reproject the SHP into robinson CRS (so that the area is constant within pixels)
            QgsVectorFileWriter.writeAsVectorFormat(vbaselayer,"{}.shp".format(temp_name),"utf-8",QgsCoordinateReferenceSystem(4326),"ESRI Shapefile")
            vlayer = QgsVectorLayer("{}.shp".format(temp_name), "projected", "ogr")
            QgsMapLayerRegistry.instance().addMapLayer(vlayer)

            #ZS calculation
            zoneStat = QgsZonalStatistics (vlayer, outFile, 'nl_', 1)
            zoneStat.calculateStatistics(None)

            #Export csv
            QgsVectorFileWriter.writeAsVectorFormat(vlayer, "{}".format(out_csv), "utf-8", None, "CSV", layerOptions ='GEOMETRY=AS_WKT')
            QgsMapLayerRegistry.instance().removeMapLayer(vlayer.id())

            #Remove the temporary files
            for var in ['cpg', 'dbf', 'prj', 'qpj', 'shx', 'shp']:
                os.remove("{}.{}".format(temp_name, var))

        os.remove(outFile)
