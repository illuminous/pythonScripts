import arcgisscripting
import os
import sys
import string
gp = arcgisscripting.create(9.3)
gp.toolbox = "management"

zoneres = []

def buildZones(zone_number_lower, zone_number_upper):
    for zone in range (zone_number_lower, zone_number_upper):
        if zone < 10:
            zonenum = 'z0'+'%s' %(zone)
            zoneres.append(zonenum)
        else:
            zonenum = 'z%s' %(zone)
            zoneres.append(zonenum)
            
def defineProjection(grid):
    cs = 'c:/Program Files/ArcGIS/Coordinate Systems/Projected Coordinate Systems/Continental/North America/USA Contiguous Albers Equal Area Conic USGS.prj'
    gp.defineprojection(grid, cs)
    
def listRasters(path): #walk the folders within the directory
    gp.workspace = path
    rasters = gp.ListRasters("", "ALL")
    for grid in rasters:
        print grid #fetch the first item in the tuple which is the path
        try:
            rasterband = grid
            desc = gp.Describe(rasterband)
            print desc.Height
            print desc.Width
            print desc.MeanCellHeight
            print desc.MeanCellWidth
            print desc.PixelType
            ## print desc.NoDataValue
            ## print desc.PrimaryField
            ## print desc.TableType
            desc = gp.describe(rasterband)
            print desc.Bandcount
            print desc.CompressionType
            print desc.Format
            extent = desc.Extent
            print extent.xmin, extent.ymin, extent.xmax, extent.ymax
            ## print desc.MExtent
            ## print desc.ZExtent
            spatialref = desc.SpatialReference            
            if spatialref.Name == 'Unknown':
                defineProjection(str(rasterband))
                print spatialref.Name
            else:
                print spatialref.Name
            print '#############'
            rasterStats(path, grid)       
        except:pass

def rasterStats(path, grid):
    gp.workspace = path
    print path
    InRaster = path+'/'+grid
    InPropertyType=['MINIMUM','MAXIMUM','MEAN','STD','UNIQUEVALUECOUNT','TOP','LEFT','RIGHT','BOTTOM','CELLSIZEX','CELLSIZEY','VALUETYPE','COLUMNCOUNT','ROWCOUNT','BANDCOUNT']        
    #Output file        
    for x in InPropertyType:
        try:
            item = gp.GetRasterProperties(InRaster, x)
            print item
        except:
            # Print error message if an error occurs 
            print gp.GetMessages()
##    try:
##        
##        outname = 'c:/tmp/rastprops%s.csv' %(grid)
##        OutFile=open(outname,'w')
##
##        # Process: GetRasterProperties 
## ##       for PropertyType in PropertyTypes:
##            
######            try:

##        zmin = gp.GetRasterProperties(InRaster, InPropertyType)
##        print 'wtf'
##        print zmin
##            print InRaster, 'this is grid'
##            Property = gp.GetRasterProperties(InRaster, PropertyType)
##            print Property
##            gp.AddMessage('%s=%s'%(PropertyType,Property))
##            OutFile.write('%s=%s\n'%(PropertyType,Property))
####            except:
####                # Print error message if an error occurs 
####                gp.AddMessage(gp.GetMessages(2))


listRasters('C:/fireharm/z10/z10_fin_grids')
