# ASCIIToRaster_sample.py
# Description: 
#   Converts an ASCII file representing raster data to a raster.
# Requirements: None
# Author: ESRI
# Date: Oct 20, 2005

# Import system modules
import arcgisscripting

# Create the Geoprocessor object
gp = arcgisscripting.create()
gp.OverWriteOutput = 1
ext = '.asc'
#ascfiles = ['z28_TrMort']
ascfiles = ['KBDI', 'PKDBI', 'Spread', 'pSpread', 'FLI',
            'pFLI', 'Flame', 'pFlame', 'CrownI', 'pCrown', 
            'FCons', 'pfCons', 'TrMort', 'pTrMort', 'SoilHt', 'pSoilHt',
             'Emiss', 'pEmiss', 'Scorch', 'pScorch']
def asciiToRaster(root):
    for grid in ascfiles:
        InAsciiFile = root + '/' + '%s' %(grid) + ext
        print InAsciiFile
        OutRaster = root + '/' + '%s' %(grid)
        print OutRaster
        try:
            # Process: ASCIIToRaster_conversion
            gp.OverWriteOutput = 1
            gp.ASCIIToRaster_conversion(InAsciiFile, OutRaster, "FLOAT")

        except:
            # Print error message if an error occurs
            print gp.GetMessages()

for zone in ['14','15','21','23']:
    try:
        asciiToRaster('E:/fireharm/d.daymetII/z%s/outfiles' %(zone))
    except:
        pass
