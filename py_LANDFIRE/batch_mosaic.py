# SetNull_sample.py
# Description: Returns NoData if a conditional evaluation is true, or returns the value specified by another  raster if it is false.
# Requirements: None
# Author: ESRI
# Date: 12/01/03

# Import system modules
import sys, string, os, win32com.client

# Create the Geoprocessor object
gp = win32com.client.Dispatch("esriGeoprocessing.GpDispatch.1")
# Check out Spatial Analyst extension license
gp.CheckOutExtension("Spatial")

# Set local variables
p=['17', '18', '19', '20', '21', '22', '23', '24', '28']#'01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '12', '13', '14', '15', '16', ]
ras=['_cbh', '_cc', '_ch', 'fbfm13', 'fbfm40']
# Process: SetNull
for x in p:
        print x
        for i in ras:
            print i
            InRaster = 'E:\\WorkSpace\\fuel1\\z%s%s' %(x, i)
            InFalseRaster = 'E:\\WorkSpace\\fuel1\\z%s%s' %(x, i)
            OutRaster = 'E:\\WorkSpace\\fuel\\f%s\\z%s%s2' %(i, x, i)
            
            #InExpression = 'setnull ([Ingrid] == -9999, [Ingrid])'
            # Process: Set null
            if not gp.Exists(InRaster):
                print InRaster + ' does not exist'
            if gp.Exists(OutRaster):
                print OutRaster + ' exists'
            else:
                gp.SetNull_sa(InRaster, InFalseRaster, OutRaster, "Value = -9999")
                print OutRaster ' created successfully!'

for x in ras:
    print x
            
    gp.WorkSpace ='E:\\WorkSpace\\fuel\\f%s' %(x)
    OutWorkspace = ('E:\\WorkSpace\\mosaics\\')
    print gp.WorkSpace

    try:
        in_raster_datasets = gp.ListRasters()
        in_raster_dataset = in_raster_datasets.next()
        in_rasters = in_raster_dataset
        while in_raster_dataset <> "":
            in_raster_dataset = in_raster_datasets.next()
            in_rasters = in_rasters + ";" + in_raster_dataset
        gp.MosaicToNewRaster_management(in_rasters, OutWorkspace, 'm%s', "#", "#", "120", "#", "#", "#" %(x)) 
        print '%s complete, moving to next layer' %(x)

    except:
        print 'moving on'
        

