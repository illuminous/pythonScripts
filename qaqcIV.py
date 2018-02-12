# GetRasterProperties.py 
# Description: Returns a property of a raster. 
# Requirements: None 
# Author: ESRI 
# Date: 06/10/05 
# Create the Geoprocessor object 
import arcgisscripting, sys, string, os
gp = arcgisscripting.create()

# Set local variables 
dm = 0
event = 1
InPropertyType =['MINIMUM','MAXIMUM','MEAN','STD','TOP','LEFT','RIGHT','BOTTOM','CELLSIZEX','CELLSIZEY','VALUETYPE','COLUMNCOUNT','ROWCOUNT','BANDCOUNT']

def rasterProperties(zone, grids, outfile):
    for y in grids:
        outfile.write(y+',')
        print'$$$$$$$$$$$$$$$$'        
        for x in InPropertyType:       
            try:
                InRaster = "c:/fireharm/z%s/z%s_fin_grids/%s" %(zone, zone, y)
                item = gp.GetRasterProperties(InRaster, x)
                print x, '= ', item
                outfile.write(str(item)+',')
            
            except:
                # Print error message if an error occurs 
                print gp.GetMessages()
        outfile.write('\n')
    outfile.close()

def main(zone):
    if dm:
        grids = ['crowni', 'emiss', 'fcons', 'flame', 'fli', 'flm', 'kbdi', 'pcrown', 'pemiss', 'pfcons', 'pflame', 'pkdbi', 'pscorch', 'psoilht', 'pspread', 'ptrmort', 'scorch', 'soilht', 'spread', 'trmort']
        # Process: GetRasterProperties
        outname = 'c:/tmp/z%s_dm.csv' %(zone)
        outfile = open(outname, 'w')
        outfile.write('GRID,MINIMUM,MAXIMUM,MEAN,STD,TOP,LEFT,RIGHT,BOTTOM,CELLSIZEX,CELLSIZEY,VALUETYPE,COLUMNCOUNT,ROWCOUNT,BANDCOUNT\n')
        rasterProperties(zone, grids, outfile)
    if event:
        grids_ev = ['burnsev', 'crowni', 'emission', 'flame', 'fuelcons', 'intensity', 'scorchht', 'smortapm', 'smortapmd2', 'smortpm', 'smortpmd2', 'soilheat', 'spread']       
        outname = 'c:/tmp/z%s_event.csv' %(zone) 
        outfile_ev = open(outname, 'w')
        outfile_ev.write('GRID,MINIMUM,MAXIMUM,MEAN,STD,TOP,LEFT,RIGHT,BOTTOM,CELLSIZEX,CELLSIZEY,VALUETYPE,COLUMNCOUNT,ROWCOUNT,BANDCOUNT\n')        
        rasterProperties(zone, grids_ev, outfile_ev)

