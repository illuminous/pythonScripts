# CopyRaster_sample.py
# Description: Copy raster to another format 
# Requirements: None
# Author: ESRI
# Date: 1/28/04

# Create the geoprocessing object
import arcgisscripting
gp = arcgisscripting.create()

# Set input raster workspace
zones = ['z14']#'z15', 'z31', 'z40', 'z43', 'z24', 'z28', 'z39', 'z25', 'z38', 'z27']
grids = ['scorchht', 'crowni', 'emissions', 'flame', 'fuelcon', 'intensity', 'kbdi', 'pcrowni', 'pemission', 'pflame', 'pfli',
         'pfuelcon', 'pkbdi', 'pscorchht', 'psoilh', 'pspread', 'ptreem', 'soilh', 'spread', 'treem']
lfgrids = ['cbd', 'cbh', 'fbfm40', 'flm', 'frcc', 'mfri', 'pls', 'prs']
ws = "L:/daymet_prep/"
ws2 = "K:/lib/landfire/national/"
gp.workspace = "H:/daymet_prep"
gp.toolbox="management"

def copyFHgrids():
    for z in zones:
        for g in grids:
            try:
                inras = ws + z + '/' + z + '_' + g
                print inras
                outras = ws + z + '/' + 'fin_grids/' + z + '_' + g
                print outras
                gp.CopyRaster_management(inras, outras)
            except:
                print 'grid already exists in fin grids directory'

def copyLFgrids():
    for z in zones:
        for l in lfgrids:
            if l == 'fbfm40':
                try:
                    lf40ras = ws2 + z + '/' + 'fin_del/' + 'gis/' + z + l
                    print lf40ras
                    lf40out = ws + z + '/' + 'fin_grids/' + z + l
                    print lf40out
                    gp.CopyRaster_management(lf40ras, lf40out)
                except:
                    pass
            else:
                try:
                   lfinras = ws2 + z + '/' + 'fin_del/' + 'gis/' + z + '_' + l
                   print lfinras
                   lfoutras2 = ws + z + '/' + 'fin_grids/' + z + '_' + l
                   print lfoutras2
                   gp.CopyRaster_management(lfinras, lfoutras2)
                except:
                    pass
                    


