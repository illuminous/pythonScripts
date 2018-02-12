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
ascfiles = ['BurnSev', 'CrownI', 'Emission', 'Flame', 'FuelCons', 'Intensity',
            'ScorchHT', 'SMortAPM', 'SMortAPMD2', 'SMortPM', 'SMortPMD2', 'SoilHeat', 'Spread']
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

for z in ['44']:
    asciiToRaster('e:/fireharm/d.eventIII/z%s/outfiles'%(z))
