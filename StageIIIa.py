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
import arcgisscripting
import os
import zipfile

#Create empty list
res = []
res2 = []
res3 = []
directories = []
combos = []
zoneres = []
geoarea = 'SW'
#Populate empty list 'res' with possible zone values 1-100'
clipgrid = ['z53_id']
products = ['siter', 'evtr']#, 'nfdrr', 'fbfmr', 'flmr', 'demr', 'aspr', 'slpr',
 #           'latr', 'lonr', 'lair', 'sdepr', 'sandr', 'siltr', 'clayr', 'rshdr', 'dbhr',
#          'bcfr', 'lcrr', 'chr', 'cbdr', 'trlstr']

gp = arcgisscripting.create()

"""Build a list of directories to copy grids from and to."""
def buildDirectories(zone_number_lower, zone_number_upper):
    for zone in range(zone_number_lower, zone_number_upper):
        res.append(zone)
        if zone < 10:
            path1 = 'L:/daymet_prep'
            path2 = '/z0%s' %(zone)
            path = path1+path2
            directories.append(path)
        else:
            path1 = 'L:/daymet_prep'
            path2 = '/z%s' %(zone)
            path = path1+path2
            directories.append(path)

    return directories

def createChunks(low, high):
    for chunk in range(low, high):
        res2.append(str(chunk))
    print res2

def genClip():
    for d in directories:
        for chunk in res2:
           for c in clipgrid:
               gridextent = d + '/' + c + chunk 
               res3.append(gridextent)
               for p in products:
                   clipitem = d + '/' + p + chunk
                   clipout = clipitem+'_2'
                   print clipitem
                   print clipout
                   gp.extent = gridextent
                   setextent = gp.extent
                   print setextent
                   try:
                       gp.clip_management(clipitem, setextent, clipout)
                   except:
                       print 'shit'


buildDirectories(53,54)
createChunks(1,21)
genClip()
##combineLandfire()

