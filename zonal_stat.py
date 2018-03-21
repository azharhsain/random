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
nlight = ['F101992', 'F101993', 'F101994', 'F121994', 'F121995', 'F121996', 'F121997', 'F121998', 'F121999', 'F141997', 'F141998', 'F141999', 'F142000', 'F142001', 'F142002', 'F142003', 'F152000', 'F152001', 'F152002', 'F152003', 'F152004', 'F152005', 'F152006', 'F152007', 'F162004', 'F162005', 'F162006', 'F162007', 'F162008', 'F162009', 'F182010', 'F182011', 'F182012', 'F182013']

#Transformation list
transform_list = ['log', 'poly1', 'poly2', 'poly3', 'poly4', 'poly5', 'poly6', 'poly7', 'poly8']

#Transformation
for transform in transform_list:

    for x in nlight:

        #Your directory
        os.chdir("/Users/azharhussain/Dropbox/GCP_Reanalysis/RA_Files/Azhar/Nightlights/Income/Data/shp")

        #Nightlight rasters
        outFile = "{}_{}.tif".format(transform, x)
        NL = "Raw_NL/{}.tif".format(x)
        raster = gdal.Open(NL)
        data1 = raster.GetRasterBand(1).ReadAsArray().astype(numpy.float64)

        if transform=='log':
            dataOut = numpy.log(data1, dtype=float64)
            infs = dataOut == -inf
            dataOut[infs] = 0
        elif transform=='poly1':
            dataOut = numpy.power(data1, 1, dtype=float64)
        elif transform=='poly2':
            dataOut = numpy.power(data1, 2, dtype=float64)
        elif transform=='poly3':
            dataOut = numpy.power(data1, 3, dtype=float64)
        elif transform=='poly4':
            dataOut = numpy.power(data1, 4, dtype=float64)
        elif transform=='poly5':
            dataOut = numpy.power(data1, 5, dtype=float64)
        elif transform=='poly6':
            dataOut = numpy.power(data1, 6, dtype=float64)
        elif transform=='poly7':
            dataOut = numpy.power(data1, 7, dtype=float64)
        elif transform=='poly8':
            dataOut = numpy.power(data1, 8, dtype=float64)
        else:
            dataOut = numpy.power(data1, 1, dtype=float64)

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

        for var in ['IND_adm2', 'NUTS_3', 'USA_adm2', 'IDN_adm1', 'BRA_adm2', 'CHN_adm3']:

            #The shapefile you want to compute nightlights product for
            input = "{}".format(var)
            shapefile = "{}.shp".format(input)
            temp_name = "temporary"

            #Name of the CSV file that will be output
            out_csv = "/Users/azharhussain/Dropbox/GCP_Reanalysis/RA_Files/Azhar/Nightlights/Income/Data/NL/{}_{}_{}_NL.csv".format(input, x, transform)
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
