#!/usr/bin/env python

"""FLM_stageVII.py builds a list of zones (buildZones) creates Folders based on a directory structure,
and copies FLM final grids to the server.

****MUST BE RUN IN PYTHON 2.6 OR GREATER BECAUSE OF THE EXTRACTALL FUNCTION****
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
import os
import zipfile
import arcgisscripting
gp = arcgisscripting.create()
products = ['flm']
zoneres = []
geoarea = 'SC'
rootdata = 'G:/LF_Refreash/FLM30_Refreash/c01/' + geoarea
wsdata = 'Z:/work/FLM/c01/' + geoarea
structure1 = '/%s'


def buildZones(zone_number_lower, zone_number_upper):
    for zone in range (zone_number_lower, zone_number_upper):
        if zone < 10:
            zonenum = 'z0'+'%s' %(zone)
            zoneres.append(zonenum)
        else:
            zonenum = 'z%s' %(zone)
            zoneres.append(zonenum)
            
def createFoldersServer():
    for r in zoneres:
        rootfolder = rootdata + structure1 %(r)
        wsfolder = wsdata + structure1 %(r)
        print rootfolder
        print wsfolder
        if os.path.exists(rootfolder):
            try:
                os.makedirs(wsfolder)
                print wsfolder
                print 'created'
            except:
                print wsfolder
                print 'Directory Already Exists'

"""Loop over all possible zones and all products, download to a local directory from k."""
def copyFLM():
    for zone in zoneres:
        for p in products:
            gp.toolbox="management"
            ##Set input raster workspace
            gp.workspace = rootdata
            ##Two steps are used to accomadate LANDFIRE formating with a leading zero for values 1-9, i.e z01 rather than z1.
            InRaster2 = rootdata + '/' + '%s/%s' %(zone, p)
            print InRaster2
            OutRaster2 = wsdata + '/' + '%s/%s' %(zone, p)
            print OutRaster2
            try:
                gp.CopyRaster_management(InRaster2, OutRaster2)
            except:
                gp.GetMessages() 

buildZones(1,100)
createFoldersServer()
copyFLM()
