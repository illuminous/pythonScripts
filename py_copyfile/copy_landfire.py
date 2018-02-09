# Copy_landfire.py
# Description: Copy rasters from K:
# Requirements: None
# Author: Jason M. Herynk
# Date: 20100119

# Create the geoprocessing object
import arcgisscripting
gp = arcgisscripting.create()


#Set Global
zero = 0

#Create empty list
res = []

#Populate empty list 'res' with possible zone values 1-100'
products = ['evc']
for zone in range(1, 100):
    res.append(zone)

# Set input raster workspace
gp.workspace = "K:/fe/landfire"

gp.toolbox="management"

#Loop over all possible zones and all products, download to a local directory from k
for zone in res:
    for p in products:
        print zone
        ##Two steps are used to accomadate LANDFIRE formating with a leading zero for values 1-9, i.e z01 rather than z1.
        if zone < 10:
            InRaster = 'K:/lib/landfire/national/z%i%i/fin_del/gis/z%i%i_%s' %(zero, zone, zero, zone, p)            
            OutRaster = 'G:/EVC/z%i%i_%s' %(zero, zone, p)
            try:
                gp.overwriteoutput = 0
                gp.CopyRaster_management(InRaster, OutRaster)
            except:
                gp.GetMessages()    
        else:
            InRaster2 = 'K:/lib/landfire/national/z%i/fin_del/gis/z%i_%s' %(zone, zone, p)
            OutRaster2 = 'G:/EVC/z%i_%s' %(zone, p)
            try:
                gp.overwriteoutput = 0
                gp.CopyRaster_management(InRaster2, OutRaster2)
            except:
                gp.GetMessages() 
            
