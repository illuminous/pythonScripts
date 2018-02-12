#------------------------------------------------------------------------
# define some variables
#------------------------------------------------------------------------

#define the directory containing the rasters to be split
workspace = 'c:/temp'

#define the number of rows and columns
rows = 3
cols = 5

#define the output file type
fileType = "TIFF"



#------------------------------------------------------------------------
# import 
#------------------------------------------------------------------------

import os, shutil
import arcpy



#------------------------------------------------------------------------
# process the data
#------------------------------------------------------------------------

if os.path.exists(workspace + "/split_rasters"):
    shutil.rmtree(workspace + "/split_rasters")
os.makedirs(workspace + "/split_rasters")

print "raster subsets will be placed in " + workspace + "/split_rasters"

arcpy.env.workspace = workspace
rasterList = arcpy.ListRasters()

for raster in rasterList:
    
    print 'splitting', raster + '_'
    if raster[-4] == '.':
        outBaseName = raster[0:-4] + '_'
    else:
        outBaseName = raster
        
    arcpy.SplitRaster_management(raster, workspace + "/split_rasters", outBaseName, "NUMBER_OF_TILES", fileType, "NEAREST", str(cols) + " " + str(rows),"0 0","0","PIXELS","#","#")

    
    


