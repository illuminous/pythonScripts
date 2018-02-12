__author__ = "Jason M. Herynk, Systems for Environmental Management, pythonGISwrangler 20120312"
__copyright__ = "Open-Source"
__credits__ = ["GDAL Tutorial"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = ""
__email__ = "jherynk.sem@gmail.com"
__status__ = "Production"


import shutil
import zipfile
import os
import glob
import gdal
from gdalconst import *


class qaqc:       
    def listRasters(self, path): #walk the folders within the directory
        grids = os.walk(path)
        for grid in grids:
            print grid[0] #fetch the first item in the tuple which is the path

            self.getGdalDriver(grid[0]) #using the path, call the GdalDriver function
            
    def getGdalDriver(self, filename):        
        dataset = gdal.Open( filename, GA_ReadOnly )
        if dataset is None:
            pass
        else:        
            print 'Dataset: ', filename
            print 'this is filename ', filename
            print 'Driver: ', dataset.GetDriver().ShortName,'/', \
              dataset.GetDriver().LongName            
            print 'Size is ',dataset.RasterXSize,'x',dataset.RasterYSize, \
              'x',dataset.RasterCount            
            print 'Projection is ',dataset.GetProjection()            
            print 'RasterCount is ', dataset.RasterCount
            #print dataset.GetGCPCount()

            outfile.write(filename+',')
            outfile.write(str(dataset.RasterXSize)+',')
            outfile.write(str(dataset.RasterYSize)+',')
            outfile.write(str(dataset.RasterCount)+',')
            #outfile.write((dataset.GetProjection()+','))
            
            geotransform = dataset.GetGeoTransform()
            if not geotransform is None:
                print 'Origin = (',geotransform[0], ',',geotransform[3],')'                
                print 'Pixel Size = (',geotransform[1], ',',geotransform[5],')'
                OrginX = geotransform[0]
                OrginY = geotransform[3]
                PixelSizeX = geotransform[1]
                PixelSizeY = geotransform[5]
                outfile.write(str(OrginX)+','+str(OrginY)+',')
                outfile.write(str(PixelSizeX)+','+str(PixelSizeY)+',\n')
        

        

x = qaqc()
outfile = open("c:/tmp/fireharmqaqc.csv", "w")
outfile.write("filename, xsize, ysize, bands, originx, originy, pixelsizex, pixelsizey\n")
x.listRasters('C:/fireharm/z10/z10_fin_grids')
outfile.close()

    
