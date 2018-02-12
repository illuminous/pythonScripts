
"""TL_stage6-remap.py - remaps an esri grid using a formatted textfile """

__author__ = "Jason M. Herynk"
__copyright__ = "Copyright 2012, SEM llc"
__credits__ = [""]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Jason M. Herynk"
__email__ = "jherynk.sem@gmail.com"
__status__ = "Prototype"

import os
import arcpy
from arcpy import env
from arcpy.sa import *


geoarea = ['PNW', 'PSW','NC','SW','SC','SE','NE']
res = []
directories = []
def buildDirectories(zone_number_lower, zone_number_upper):
    for zone in range(zone_number_lower, zone_number_upper):
        res.append(zone)
        for area in geoarea:
            
            if zone < 10:
                path1 = 'G:/Working/Treelists_2012_update/%s' %(area) 
                path2 = '/z0%s/' %(zone)
                path = path1+path2
                directories.append(path)
            else:
                path1 = 'G:/Working/Treelists_2012_update/%s' %(area) 
                path2 = '/z%s/' %(zone)
                path = path1+path2
                directories.append(path)

def remap(inRaster, inRemapFile, outRaster):
    out = ReclassByASCIIFile(inRaster, inRemapFile, "NODATA")
    out.save(outRaster)

def build(inRaster):
    arcpy.BuildRasterAttributeTable_management(inRaster, "Overwrite")

def main():
    arcpy.env.overwriteOutput = True
    arcpy.CheckOutExtension("Spatial")
    buildDirectories(1,2)
    for d in directories:
        if os.path.isdir(d) == True:
            inRaster = d+'/combo'
            inRemapFile = d+'/outfile.txt'
            zone = d[-4:-1]
            outRaster = d+'/%s_trlst_c08'%(zone)
            remap(inRaster, inRemapFile, outRaster)
            build(outRaster)

        
if __name__ == '__main__':
    main()       
