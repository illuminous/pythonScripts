#!/usr/bin/env python

"""TL_stage2-combine_reduced.py """

__author__ = "Jason M. Herynk"
__copyright__ = "Copyright 2012, SEM llc"
__credits__ = [""]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Jason M. Herynk"
__email__ = "jherynk.sem@gmail.com"
__status__ = "Prototype"


import sys
import arcpy
import os
import zipfile
from arcpy import env
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")

#Create empty list
res = []
directories = []
combos = []
zoneres = []
geoarea = ['PNW']#'SE', 'SW']#,'NC','NE','SC','SE','SW']



def buildDirectories(zone_number_lower, zone_number_upper):
    """Build a list of directories to copy grids from and to."""
    for zone in range(zone_number_lower, zone_number_upper):
        res.append(zone)
        for area in geoarea:            
            if zone < 10:
                path1 = 'G:/Working/Treelists_2012_update/%s/' %(area) 
                path2 = '/z0%s/' %(zone)
                path = path1+path2
                directories.append(path)
            else:
                path1 = 'G:/Working/Treelists_2012_update/%s/' %(area) 
                path2 = '/z%s/' %(zone)
                path = path1+path2
                directories.append(path)

    return directories

def gridsReclass(rootGrid, asciiFile, movedGrid):
    """Reclassifies raster grids using a text file"""    
    try:
        arcpy.ReclassByASCIIFile_3d(rootGrid, asciiFile, movedGrid, 'NODATA')
    except:
        print 'failed to reclass grid', rootGrid

def deleteGrid(inGrid):
    """deletes a raster grid"""
    try:        
        arcpy.Delete_management(inGrid)
    except:
        pass
#############################################################################
        


def main():
    reclass = 0 #flags for sections.  0 = false, 1 = true
    combine = 1
    buildDirectories(1,2)
    arcpy.CheckOutExtension("3D")
    
    for d in directories:
        if reclass:
            ri = ['dem', 'asp', 'slp']
            for reclass in ri:
                rootGrid = d+'topo/%s/%s' %(reclass, reclass)
                asciiFile = 'G:/Working/Treelists_2012_update/reclassTables/%s.asc' %(reclass)
                movedGrid = rootGrid+'_rc'
                deleteGrid(movedGrid)
                gridsReclass(rootGrid, asciiFile, movedGrid)

        if combine:
            arcpy.CheckOutExtension("Spatial")

            EVT = d + 'veg/evt08/evt' 
            BPS = d + 'veg/bps/bps'
            SCLASS = d + 'work/sclass08/sclass'
            CC = d + 'fuel/cc08/cc'
            DEM = d + 'topo/dem/dem_rc'
            ASP = d + 'topo/asp/asp_rc'
            outputs = d + '/combo'
            try:
                deleteGrid(outputs)
                outCombine = Combine([EVT,BPS,SCLASS,CC,DEM,ASP])
                outCombine.save(outputs)
            except:pass

            
if __name__ == '__main__':
    main()            



