#!/usr/bin/env python

"""TL_stage1.py builds a list of zones (buildZones) creates Folders based on a directory structure,
and unzips files to a location.

****MUST BE RUN IN PYTHON 2.6 OR GREATER BECAUSE OF THE EXTRACTALL FUNCTION****
"""

__author__ = "Jason M. Herynk"
__copyright__ = "Copyright 2012, SEM llc"
__credits__ = [""]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Jason M. Herynk"
__email__ = "jherynk.sem@gmail.com"
__status__ = "Prototype"

#############################################################################
import sys
import os
import zipfile

def buildZones(zone_number_lower, zone_number_upper):
    """enter the landfire zone number, starting with a zero for zones less than 10."""
    for zone in range (zone_number_lower, zone_number_upper):
        if zone < 10:
            zonenum = 'z0'+'%s' %(zone)
            zoneres.append(zonenum)
        else:
            zonenum = 'z%s' %(zone)
            zoneres.append(zonenum)

def createFoldersUnzip():
    """creates a directoy structure using a workspace location.  Unzips the landfire
grids using the landfire refresh structure."""
    for r in zoneres:
        rootfolder = rootdata + structure1 %(r)
        wsfolder = wsdata 
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
                unzipitem.extractall(wsfolder)
            else:
                print 'file isnt here'

def main():
    """start of the main program"""
    geoarea = ['PNW','NC', 'NE', 'PSW', 'SC', 'SE', 'SW']
    for geo in geoarea:
        products = ['mask0k','cc08','bps','evt08']
        global products # make products a global variable to be used by functions        
        rootdata = 'L:/data/%s' %(geo)
        global rootdata
        wsdata = 'G:/Working/Treelists_2012_update/%s' %(geo)
        global wsdata
        structure1 = '/%s'
        global structure1
        structure2 = '/base/%s%s.zip'
        global structure2
        zoneres = []
        global zoneres
        buildZones(1,100)
        createFoldersUnzip()

if __name__ == '__main__':
    main()      
