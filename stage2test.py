import arcgisscripting
gp = arcgisscripting.create()

gp.workspace = "c:/tmp/stagestest/0kgrd"
gp.toolbox = "SA"
gp.Extent = "MAXOF"
gp.Extent = "1 1 512 512"





### ExtractByRectangle_sample.py
### Description: 
###   Extracts the cells of a raster based on a rectangle.
### Requirements: None
### Author: ESRI
### Date: Sept 6, 2005
##
### Import system modules
##import arcgisscripting
##
### Create the Geoprocessor object
##gp = arcgisscripting.create()
##
##try:
##    # Set local variables
##    InRaster = "C:/data/raster1"
##    InRectangle = "20 30 40 80"
##    OutRaster = "C:/data/final_1"
##
##    # Check out Spatial Analyst extension license
##    gp.CheckOutExtension("Spatial")
##
##    # Process: ExtractByRectangle
##    gp.ExtractByRectangle_sa(InRaster, InRectangle, OutRaster, "INSIDE")
##
##except:
##    # If an error occurred while running a tool, then print the messages.
##    print gp.GetMessages()

