# ExtractByMask_sample.py
# Description: 
#   Extracts the cells of a raster that correspond with the areas
#   defined by a mask.
# Requirements: None
# Author: ESRI
# Date: Sept 6, 2005

# Import system modules
import arcgisscripting

# Create the Geoprocessor object
gp = arcgisscripting.create()

##try:
##    # Set local variables
##    InRaster = "G:/Working/Carbon/for_Jason/ExtractTest/pm25_729_10k"
##    InMask = "G:/Working/Carbon/for_Jason/ExtractTest/z101819"
##    OutRaster = "G:/Working/Carbon/for_Jason/ExtractTest/pm25_ext"
##
##    # Check out Spatial Analyst extension license
##    gp.CheckOutExtension("Spatial")
##
##    # Process: ExtractByMask
##    gp.ExtractByMask_sa(InRaster, InMask, OutRaster)
##
##except:
##    # If an error occurred while running a tool, then print the messages.
##    print gp.GetMessages()



try:
    # Set local variables
    outRaster = "G:/Working/Carbon/for_Jason/ExtractTest/combo_ext"

    # Check out Spatial Analyst extension license
    gp.CheckOutExtension("Spatial")

    # Process: Combine...
    gp.Combine_sa("'G:/Working/Carbon/for_Jason/ExtractTest/pm25_ext';'G:/Working/Carbon/for_Jason/ExtractTest/abc_ext';'G:/Working/Carbon/for_Jason/ExtractTest/bp_ext';'G:/Working/Carbon/for_Jason/ExtractTest/cem_ext';'G:/Working/Carbon/for_Jason/ExtractTest/exc_ext';'G:/Working/Carbon/for_Jason/ExtractTest/pm10_ext'", outRaster)

except:
    # If an error occurred while running a tool, then print the messages.
    print gp.GetMessages()
