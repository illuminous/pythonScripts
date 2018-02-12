# Con_sample.py
# Description: 
#   Performs a conditional if/else evaluation on each cell of an
#   input raster.
# Requirements: None
# Author: ESRI
# Date: Sept 6, 2005

# Import system modules
import arcgisscripting
import os
import sys

# Create the Geoprocessor object
gp = arcgisscripting.create()
path1 = 'H:/fireharmQAQC/zips/Event_Mode/z01_fh_grids/'
res = []
zones = []

products = ['cc.img', 'ch.img', 'pari.img', 'relhumi.img', 'swavgfdi.img', 'vpdi.img', 'wxsradi.img',
            'asp', 'bps', 'cbd', 'cbh', 'cc', 'ch', 'ddayi.img', 'dem', 'evc', 'evt', 'ppti.img', 'slp', 'tavei.img',
            'tdayi.img', 'tmaxi.img', 'tmini.img', 'tnighti.img']

"""Build a list of directories to copy grids from and to."""
def buildDirectories(zone_number_lower, zone_number_upper):
    for zone in range(zone_number_lower, zone_number_upper):
        res.append(zone)
        if zone < 10: #fix the formating if the zone number is less than 10
            path2 = 'z0%s' %(zone)
            zones.append(path2)
        else:
            path1 = 'z%s' %(zone)
            zones.append(path1)

def createEVCmask():
    for z in zones:
        try:
            # Set local variables
            InRaster = path1+z+'_evc_r'
            InTrueRaster = "1"
            InFalseRaster = "-9999"
            OutRaster = path1+z+'_evc_tree'

            # Check out Spatial Analyst extension license
            gp.CheckOutExtension("Spatial")

            # Process: Con
            gp.Con_sa(InRaster, InTrueRaster, OutRaster, InFalseRaster, "VALUE >= 100 and VALUE <= 109")

        except:
            # If an error occurred while running a tool, then print the messages.
            print gp.GetMessages()

def createFolders(root):
    for z in zones:
        rootfolder = path1+z+ '/clipGrids'
        if not os.path.exists(rootfolder):
            os.makedirs(rootfolder)
        else:
            print 'directory already exists'

def createLatLong():
    for z in zones:
        try:
            # Set local variables
            dem = path1 + '%s/clipGrids/dem' %(z)
            print dem
            gp.extent = dem
            gp.SnapRaster = dem
            InExpressionLon = "$$XMAP"
            print InExpressionLon
            InExpressionLat = "$$YMAP"
            OutRasterLon = path1 + '/%s/clipGrids/lon2' %(z)
            OutRasterLat = path1 + '/%s/clipGrids/lat2' %(z)

            # Check out Spatial Analyst extension license
            gp.CheckOutExtension("Spatial")

            # Process: MapAlgebraStatement
            gp.SingleOutputMapAlgebra_sa(InExpressionLon, OutRasterLon)
            gp.SingleOutputMapAlgebra_sa(InExpressionLat, OutRasterLat)

        except:
            # If an error occurred while running a tool, then print the messages.
            print gp.GetMessages()


def intLatLong():
    for z in zones:
        try:
            # Set the input raster dataset
            inRasterLon = path1 + '/%s/clipGrids/lon' %(zone)
            inRasterLat = path1 + '/%s/clipGrids/lat' %(zone)

            # Set the output raster name
            outRasterLon2 = path1 + '/%s/clipGrids/Ilon' %(zone)
            outRasterLat2 = path1 + '/%s/clipGrids/Ilat' %(zone)

            # Check out ArcGIS Spatial Analyst extension license
            gp.CheckOutExtension("Spatial")

            # Process: Int
            gp.Int_sa(inRasterLon, outRasterLon2)
            gp.Int_sa(inRasterLat, outRasterLat2)

        except:
            # If an error occurred while running a tool, then print the messages.
            print gp.GetMessages()

def clipGrids():
    """Clip all grids to the 0kgd boundary before resampling.  This was switched from the 3kgd because the 3k boundary would result in -9999 dem, aspect,
    slope when resampled.  This would also cause 0 values for the longitude field in the poly combine files produced in stage 3 and in the z##poly#.in files created in
    stage 4.  Using the 0kgd will also reduce the amount of area we need to run because there will
    not be overlap between zones."""
    for zone in zones:
        for p in products:
            try:
                print 'Clipping %s' %(p)
                
                kRaster = path1 + '/%s/evc_tree' %(zone)  
                gp.extent = path1 + '/%s/dem' %(zone)
                PRaster = path1 + '/%s/%s' %(zone, p)
                POutRaster = path1 + '/%s/clipGrids/%s' %(zone, p)
                PFalseRaster = '-9999'
                gp.CheckOutExtension("Spatial")
                gp.Con_sa(kRaster, PRaster, POutRaster, PFalseRaster, 'VALUE = 1') ##Check value number in the 3kgd.  This changes occasionally from 1 to 2
                 
            except:
                print gp.GetMessages()
                print 'Grid was not clipped to the 3k boundary'
################################################
##def main()
##    buildDirectories()
##if __name__ == '__main__':
##    main()
    
