import arcpy
arcpy.env.overwriteOutput = True

def createRasterCatalog(geodatabase, rastercatalog):
    arcpy.CreateRasterCatalog_management(geodatabase, rastercatalog)

def rasterToGeodatabase(Input_Rasters, output_geodatabase):
   arcpy.RasterToGeodatabase_conversion(Input_Rasters, output_geodatabase)
rasterCatalogs = ['smortpm']#'burnsev', 'crowni', 'emissions', 'flame', 'fuelcon', 'intensity', 'scorchht', 'soilh', 'spread', 'smortpmd2', 'smortapm', 'smrtapmd2']
#rasterCatalogs = ['crowni', 'emissions', 'flame', 'fuelcon','intensity', 'kbdi', 'pcrowni', 'pemission', 'pflame','pfli', 'pfuelcon',  'pkbdi', 'pscorchht', 'psoilh', 'pspread', 'ptreem', 'scorchht', 'soilh', 'spread', 'treem']
#zones = ['z01','z02','z07','z08','z09','z10','z18','z19']
#zones = ['z03', 'z04', 'z05', 'z06', 'z13']
#zones = ['z12', 'z14','z15','z16','z17','z23','z24','z25','z28']
zones = ['z20', 'z21','z22','z29','z30','z31','z40','z39','z41']
#zones = ['z26','z27','z33','z34','z35','z36','z32','z38','z43','z44']
#zones = ['z37']
for catalog in rasterCatalogs:
    arcpy.env.workspace = "H:/fireharmQAQC/FIREHARM_Event_NC.gdb"
    geodatabase = "H:/fireharmQAQC/FIREHARM_Event_NC.gdb"    
    try:
        createRasterCatalog(geodatabase, catalog)
    except:
        pass
    for z in zones:

        try:
            gridname = '%s_%s' %(z, catalog)
            output = geodatabase+'/%s' %(catalog)
            rasterToGeodatabase(gridname, output)
        except:
            pass
                
        
