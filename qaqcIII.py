# GetRasterProperties.py 
# Description: Returns a property of a raster. 
# Requirements: None 
# Author: ESRI 
# Date: 06/10/05 
# Create the Geoprocessor object 
import arcgisscripting, sys, string, os
gp = arcgisscripting.create()

# Set local variables 

grids = ['crowni', 'emiss', 'fcons', 'flame', 'fli', 'flm', 'kbdi', 'pcrown', 'pemiss', 'pfcons', 'pflame', 'pkdbi', 'pscorch', 'psoilht', 'pspread', 'ptrmort', 'scorch', 'soilht', 'spread', 'trmort']
InPropertyType =['MINIMUM','MAXIMUM','MEAN','STD','TOP','LEFT','RIGHT','BOTTOM','CELLSIZEX','CELLSIZEY','VALUETYPE','COLUMNCOUNT','ROWCOUNT','BANDCOUNT']

# Process: GetRasterProperties
outname = 'c:/tmp/z10_dm.csv' 
outfile = open(outname, 'w')
outfile.write('GRID,MINIMUM,MAXIMUM,MEAN,STD,TOP,LEFT,RIGHT,BOTTOM,CELLSIZEX,CELLSIZEY,VALUETYPE,COLUMNCOUNT,ROWCOUNT,BANDCOUNT\n')

for y in grids:
    outfile.write(y+',')
    print'$$$$$$$$$$$$$$$$'
    
    for x in InPropertyType:       
        try:
            InRaster = "c:/fireharm/z10/z10_fin_grids/%s" %(y)
            item = gp.GetRasterProperties(InRaster, x)
            print x, '= ', item
            outfile.write(str(item)+',')
        
        except:
            # Print error message if an error occurs 
            print gp.GetMessages()
    outfile.write('\n')
outfile.close()
