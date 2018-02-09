# MosaicToNew.py
# Description: mosaic multiple rasters to a new raster dataset
# Requirements: None
# Author: ESRI
# Date: 1/28/04






# Create the Geoprocessor object
import arcgisscripting
gp = arcgisscripting.create()

bpr = 'F:/Working/FPA/2012_rasters/KR_fixes/working_bpr'

try:
    # Set local variables
    InRaster = bpr+"%s%s %(name, /gb_id_001_bpr"; bpr+"/gb_id_002_bpr"
    OutWorkspace = "C:/temp"

    # Process: MosaicToNew
    gp.toolbox = "SA"
    gp.Extent = "-2366000 2269090 253000 3187090"
    gp.MosaicToNewRaster_management(InRaster, OutWorkspace, "seattle7.img", "#", "8_BITS_UNSIGNED", "3","1", "BLEND", "#")

except:
    # Print error message if an error occurs
    gp.GetMessages()
