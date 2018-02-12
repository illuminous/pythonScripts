# Copy_landfire.py
# Description: Copy rasters from K:
# Requirements: None
# Author: Jason M. Herynk
# Date: 20100119

# Create the geoprocessing object
import sys, arcgisscripting

#Create empty list
res = []
directories = []
combos = []
#Populate empty list 'res' with possible zone values 1-100'
products = ['evt', 'evc', 'evh']

"""Build a list of directories to copy grids from and to."""
def buildDirectories(zone_number_lower, zone_number_upper):
    for zone in range(zone_number_lower, zone_number_upper):
        res.append(zone)
        if zone < 10:
            path = 'G:/Working/FLM/FLM_Refreash/PNW/z0%s/z0%s' %(zone,zone)
            directories.append(path)
        else:
            path = 'G:/Working/FLM/FLM_Refreash/PNW/z%s/z%s' %(zone,zone)
            directories.append(path)

    return directories



"""Loop over all possible zones and all products, download to a local directory from k."""
def copyLandfire():
    for zone in res:
        for p in products:
            gp.toolbox="management"
            ##Set input raster workspace
            gp.workspace = "K:/fe/landfire"
            print zone
            ##Two steps are used to accomadate LANDFIRE formating with a leading zero for values 1-9, i.e z01 rather than z1.
            if zone < 10:
                InRaster = 'K:/fe/landfire/z%i%i/fin_del/gis/z%i%i_%s' %(zero, zone, zero, zone, p)            
                OutRaster = 'F:/LANDFIRE/z%i%i_%s' %(zero, zone, p)
                try:
                    gp.CopyRaster_management(InRaster, OutRaster)
                except:
                    gp.GetMessages()    
            else:
                InRaster2 = 'K:/fe/landfire/z%i/fin_del/gis/z%i_%s' %(zone, zone, p)
                OutRaster2 = 'F:/LANDFIRE/z%i_%s' %(zone, p)
                try:
                    gp.CopyRaster_management(InRaster2, OutRaster2)
                except:
                    gp.GetMessages() 

##def extractLandfire():

"""Combine the EVT, EVC, and EVH layers and call it combo"""
def combineLandfire():
    for d in directories:
        print d
        gp = arcgisscripting.create()
        gp.CheckOutExtension('Spatial')
        EVT = d + '/evt' 
        EVC = d + '/evc'
        EVH = d + '/evh'
        inputs = "'"  '%s' "'" ';' "'" '%s' "'" ';' "'" '%s' "'" %(EVT, EVC, EVH)
        outputs = d + '/combo'
        try:
            gp.Combine_sa(inputs, outputs)
        except:
            print gp.GetMessages()
##combineLandfire()


