
"""TL_stage10-NLCD-Mask.py - uses an evt grid to stamp on the NLCD masks to the final treelist grids """

__author__ = "Jason M. Herynk"
__copyright__ = "Copyright 2011, SEM Systems for Environmental Management"
__credits__ = [""]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Jason M. Herynk"
__email__ = "jherynk.sem@gmail.com"
__status__ = "Prototype"


import sys
import os

import arcpy
from arcpy import env
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")


#Create empty list
res = []
directories = []

geoarea = ['PNW','PSW','NC','NE','SC','SE','SW']


"""Build a list of directories to copy grids from and to."""
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

    return directories

def extractbyMaskNLCD(inRaster, mask, evtRaster, outRaster):
   ## try:
    outExtractByMask = ExtractByMask(inRaster, mask)
    outCon = Con(evtRaster, evtRaster,  outExtractByMask, "VALUE<=95")
    outCon.save(outRaster)
##    except:
##        pass

def build(inRaster):
    arcpy.BuildRasterAttributeTable_management(inRaster, "Overwrite")
#############################################################################
        


def main():

    buildDirectories(1,100)
    arcpy.CheckOutExtension("3D")
    arcpy.env.overwriteOutput = True
    for d in directories:
        if os.path.isdir(d) == True:
            arcpy.CheckOutExtension("Spatial")
            splitter = d.split('/')
            print splitter[4]
            inRaster = d+'%s_trlst_c08'%(splitter[4])
            mask = d+'base/mask0k/mask0k'
            evtRaster = d+'veg/evt08/evt'
            outRaster = d+'%s_trlst_c08'%(splitter[4])
            extractbyMaskNLCD(inRaster, mask, evtRaster, outRaster)
            build(outRaster)

            
if __name__ == '__main__':
    main()            



