#!/usr/bin/env python

"""FLM_stageIII.py
def buildDirectories - Builds a list of directories
def copylandfire - copies grid data from the server to a local directory
def combineLandfire - combines grid products
FLM mapping currently requires that buildDirectories and combineLandfire are run before
stage IV.
"""

__author__ = "Jason M. Herynk"
__copyright__ = "Copyright 2011, SEM Systems for Environmental Management"
__credits__ = [""]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Jason M. Herynk"
__email__ = "jherynk.sem@gmail.com"
__status__ = "Prototype"


import sys
import arcpy
from arcpy import env
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")


import os
import zipfile

#Create empty list
res = []
directories = []
combos = []
zoneres = []
geoarea = ['NC','NE','SE','SW']
#Populate empty list 'res' with possible zone values 1-100'
#products = ['evt08', 'bps', 'cbd08', 'sclass08', 'asp', 'dem', 'slp', 'cc08' ] #add sclass
#gp = arcgisscripting.create()

"""Build a list of directories to copy grids from and to."""
def buildDirectories(zone_number_lower, zone_number_upper):
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
    
    try:
        
        ##gp.CopyRaster_management(rootGrid, movedGrid)
        arcpy.ReclassByASCIIFile_3d(rootGrid, asciiFile, movedGrid, 'NODATA')
    except:
        print 'failed to reclass grid', rootGrid


#############################################################################
        


def main():
    reclass = 0
    combine = 1
    buildDirectories(1,100)
    arcpy.CheckOutExtension("3D")
    
    for d in directories:
        if reclass:
            ri = ['dem', 'asp', 'slp']
            for reclass in ri:
                rootGrid = d+'topo/%s/%s' %(reclass, reclass)
                asciiFile = 'G:/Working/Treelists_2012_update/reclassTables/%s.asc' %(reclass)
                movedGrid = rootGrid+'_rc'            
                gridsReclass(rootGrid, asciiFile, movedGrid)
        if combine:
            arcpy.CheckOutExtension("Spatial")

            EVT = d + 'veg/evt08/evt' 
            BPS = d + 'veg/bps/bps'
            SCLASS = d + 'work/sclass08/sclass'
            CC = d + 'fuel/cc08/cc'
            CBD = d + 'fuel/cbd08/cbd'
            DEM = d + 'topo/dem/dem_rc'
            ASP = d + 'topo/asp/asp_rc'
            SLP = d + 'topo/slp/slp_rc'      
            inputs = "'"  '%s' "'" ';' "'" '%s' "'" ';' "'" '%s'"'" ';' "'" '%s'"'" ';' "'" '%s' "'" ';' "'" '%s' "'" ';' "'" '%s'"'" ';' "'" '%s' "'" %(EVT, BPS, SCLASS, CC, CBD, DEM, ASP, SLP)
            outputs = d + '/combo'
            try:
                outCombine = Combine([EVT,BPS,SCLASS,CC,CBD,DEM,ASP,SLP])
                outCombine.save(outputs)
            except:pass

            
if __name__ == '__main__':
    main()            



