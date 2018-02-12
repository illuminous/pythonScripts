import arcpy
from arcpy import env
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")

arcpy.env.overwriteOutput = True





def focalMean(inRaster, output):
    print "calculating focal mean for ", inRaster
    # Set local variables
    
    neighborhood = NbrRectangle(5, 5, "CELL")

    # Check out the ArcGIS Spatial Analyst extension license
    arcpy.CheckOutExtension("Spatial")

    # Execute FocalStatistics
    outFocalStatistics = FocalStatistics(inRaster, neighborhood, "MEAN","DATA")

    # Save the output 
    outFocalStatistics.save(output)

def con(inRaster, output):
    outCon = Con(IsNull(inRaster), output, inRaster)
    newout = output+'1'
    outCon.save(newout)

def checkNull(inRaster, nullfile):
    print "processing checkNull method"
    Calc =IsNull(inRaster)    
    Calc.save(nullfile)

def main():
    # Set environment settings
    env.workspace = "H:/fireharmQAQC/FIREHARM_Event_PS.gdb"
    geodatabase = "H:/fireharmQAQC/FIREHARM_Event_PS.gdb"
    geodatabaseNoNull = "H:/fireharmQAQC/FIREHARM_Event_PS_NoNull.gdb"
    geodatabaseNull = "H:/fireharmQAQC/FIREHARM_Event_PS_NullCheck.gdb"
    
    zones = ['z13']#'z03', 'z04', 'z05', 'z06', 'z13']
    rasterCatalogs = ['crowni']#,'smortpm',   'emissions', 'flame',
                      #'fuelcon', 'intensity', 'scorchht', 'soilh', 'spread',
                      #'smortpmd2', 'smortapm', 'smrtapmd2'] #left out 'burnsev', because its an integer grid
        
    for z in zones:
        for catalog in rasterCatalogs:

            original = geodatabase+'/%s_%s' %(z, catalog)
            fm_grid = geodatabaseNoNull+'/%s_%s' %(z,catalog)
            nullfile = geodatabaseNull+'/%s_%s' %(z,catalog)
            
##            try:
            focalMean(original, fm_grid)
            con(original, fm_grid)
##            checkNull(fm_grid,nullfile)
                
##
##            except:
##                pass

            
        
