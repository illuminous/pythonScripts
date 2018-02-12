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

def con(inRaster, fm_grid, output):
    outCon = Con(IsNull(inRaster), fm_grid, inRaster)
    
    outCon.save(output)

def checkNull(inRaster, nullfile):
    print "processing checkNull method"
    Calc =IsNull(inRaster)    
    Calc.save(nullfile)

def integerizeGrid(inRaster, outRaster):
    outInt = Int(inRaster)
    newout = outRaster+'int'
    outInt.save(newout)

def main():
    # Set environment settings
    region = 'PN'
    mode = 'Event'
    env.workspace = "H:/fireharmQAQC/FIREHARM_%s_%s.gdb" %(mode, region)
    geodatabase = "H:/fireharmQAQC/FIREHARM_%s_%s.gdb" %(mode, region)
    geodatabaseFocalMean = "H:/fireharmQAQC/FIREHARM_%s_%s_FocalMean.gdb" %(mode, region)
    geodatabaseNoNull = "H:/fireharmQAQC/FIREHARM_%s_%s_NoNull.gdb" %(mode, region)
    geodatabaseNull = "H:/fireharmQAQC/FIREHARM_%s_%s_NullCheck.gdb" %(mode, region)
    
    zones = ['z10']#['z12', 'z14','z15','z16','z17','z23','z24','z25','z28']
##    rasterCatalogs = ['crowni', 'emissions', 'flame', 'fuelcon','intensity',
##                      'kbdi', 'pcrowni', 'pemission', 'pflame','pfli', 'pfuelcon',
##                      'pkbdi', 'pscorchht', 'psoilh', 'pspread', 'ptreem', 'scorchht',
##                      'soilh', 'spread', 'treem']
    rasterCatalogs = ['burnsev','crowni','smortpm',   'emissions', 'flame',
                      'fuelcon', 'intensity', 'scorchht', 'soilh', 'spread',
                      'smortpmd2', 'smortapm', 'smrtapmd2'] #left out 'burnsev', because its an integer grid
        
    for z in zones:
        for catalog in rasterCatalogs:

            original = geodatabase+'/%s_%s' %(z, catalog)
            fm_grid = geodatabaseFocalMean+'/%s_%s' %(z,catalog)
            noNull_grid = geodatabaseNoNull+'/%s_%s' %(z,catalog)
            nullfile = geodatabaseNull+'/%s_%s' %(z,catalog)
            
            try:
                focalMean(original, fm_grid)
                con(original, fm_grid, noNull_grid)                
                if catalog == 'burnsev':
                    integerizeGrid(noNull_grid, noNull_grid)
                    arcpy.Delete_management(noNull_grid)
                    intRaster = noNull_grid+'int'
                    arcpy.Rename_management(intRaster, noNull_grid)
                checkNull(noNull_grid,nullfile)    

            except:
                pass

if __name__ == "__main__":
    main()            
        
