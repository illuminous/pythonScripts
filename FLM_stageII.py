#!/usr/bin/env python

"""FLM_stageII.py deletes extra folders and moves esri grid data
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
import shutil
import arcgisscripting
import FLM_stageIa

products = ['fbfm40']
geoarea = 'SW'
wsdata = 'G:/LF_Refreash/FLM30_Refreash/c08/' + geoarea
structure1 = '/%s/%s/fuel/%s08/%s'
structure2 = '/%s/%s'
structure3 = '/%s'


FLM_stageIa.buildZones(1, 100)
zoneres = FLM_stageIa.zoneres

gp = arcgisscripting.create()
gp.toolbox = 'management'

def moveGrids():
    for r in zoneres:
        for p in products:
            rootfolder = wsdata + structure1 %(r, r, p, p)
            ws = wsdata + structure2 %(r, p)
            print rootfolder, ws
            try:
                gp.workspace = 'ws'
                #gp.toolbox = 'management'
                gp.CopyRaster_management(rootfolder, ws)
            except:
                print gp.getmessages(2)


def deleteFolders():
    for r in zoneres:
        for p in products:
            delfolders = wsdata + structure2 %(r, r)
            print delfolders
            try:
                shutil.rmtree(delfolders)
            except:
                print 'folder doesnt exist'
                
def createNonburnMask():
    for r in zoneres:
        for p in products:
            ws = wsdata + structure2 %(r, p)
            print ws
            congrid = wsdata + structure3 %(r) + '/NBMask'
            print congrid
            try:
                gp.CheckOutExtension('Spatial')
                gp.Con_sa(ws, '1', congrid, '0', 'VALUE < 100')
            except:
                print gp.GetMessages()

moveGrids()
deleteFolders()
createNonburnMask()


