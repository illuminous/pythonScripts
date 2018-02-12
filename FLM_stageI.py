#!/usr/bin/env python

"""FLM_stageI.py builds a list of zones (buildZones) creates Folders based on a directory structure,
and unzips files to a location.

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

products = ['evt08', 'evc08', 'evh08']
zoneres = []
geoarea = 'SW'
rootdata = 'G:/data/' + geoarea
wsdata = 'G:/LF_Refreash/FLM30_Refreash/c08/' + geoarea
structure1 = '/%s'
structure2 = '/veg/%s%s.zip'

def buildZones(zone_number_lower, zone_number_upper):
    for zone in range (zone_number_lower, zone_number_upper):
        if zone < 10:
            zonenum = 'z0'+'%s' %(zone)
            zoneres.append(zonenum)
        else:
            zonenum = 'z%s' %(zone)
            zoneres.append(zonenum)

def createFoldersUnzip():
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
    
        for p in products:
            vegdata = rootfolder + structure2 %(r, p)
            print vegdata
            if os.path.exists(vegdata):
                os.chdir(wsfolder)
                destination = os.getcwd()
                unzipitem = zipfile.ZipFile(vegdata)
                print unzipitem
##                zipitems = unzipitem.namelist()
##                print zipitems
                unzipitem.extractall(wsfolder)
            else:
                print 'file isnt here'

##buildZones(1,100)
##createFoldersUnzip()
