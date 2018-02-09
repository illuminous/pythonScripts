# Import system modules
#First Section creates mask for removing 3km buffer on grids
#Second Section copies all western grids off K, then removes buffer, then deletes original
#Third Section mosaics to new -GRID CANNOT EXIST, and IT WON'T OVERWRITE, and joinsitem at end

import arcgisscripting, os
# Create the Geoprocessor object
gp = arcgisscripting.create()
gp.CheckOutExtension("spatial")
gp.AddToolBox
gp.toolbox = "management"
# amlfilename2 = "C:\\WorkSpace\\datalist\\grid_aml\\joinitem.aml"

w = ['z20', 'z22', 'z21']#, '22']#, '02', '03', '04', '05', '06', '07', '08', '09', '10', '12', '13', '14', '15', '16', '17', '18', '19', '20',
    #'21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '33', '34'] #these are western zones remapped by fuels
#e = ['31', '32', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51',
    #'52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '98', '99']
#a = ['67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '97', '77', '78']


zone = w
name = ['_tlg']#_001', '_002', '_003', '_004', '_005', '_006', '_007', '_008', '_009', '_010']#_bps', '_cbd', '_ch', '_cbh', '_cc', '_clay', '_dem', '_evt','_fb40','_flm', '_sand', '_sdep', '_silt']
        #done '_bps', '_cbd', '_cbh', '_cc', '_clay', '_dem', '_evt'

#Second Section:  Copies grids from K, extracts by mask to remove 3km buffer, and deletes original
for x in zone:
    print x
    for i in name:
        print i
        coordysFPU = "C:\Program Files\ArcGIS\Coordinate Systems\Geographic Coordinate Systems\North America\North American Datum 1983.prj"
        coordsys = "C:\Program Files\ArcGIS\Coordinate Systems\Projected Coordinate Systems\Continental\North America\USA Contiguous Albers Equal Area Conic USGS.prj"
        InMask = 'C:\\working\\r1\\20_21_22_dis_fin_Buffer.shp'
        #LFRaster = 'C:\\working\\r1\\TLGs\\%s%s' %(x, i)                 
        OutRaster = 'C:\\working\\r1\\TLGs\\%s%s' % (x, i)
        OutRaster2 = 'C:\\working\\r1\\TLGs\\out\\%s%s_2' % (x, i)
        OutRaster3 = 'C:\\working\\r1\\TLGs\\out\\%s%s_r' % (x, i)
        if gp.exists (OutRaster3):
            print OutRaster3 + "exists"
        else:
            #Process:  Copy Raster, using copy from aml
            #gp.copy(LFRaster, OutRaster)
            #gp.ASCIIToRaster_conversion(LFRaster, OutRaster, "FLOAT")
            gp.DefineProjection_Management(OutRaster, coordsys)
            gp.copy(OutRaster, OutRaster2)
            #Process:  Extract by zone mask delet this....gp.AddToolbox("C:/Program Files/ArcGIS/ArcToolbox/Toolboxes/Spatial Analyst Tools.tbx")
            gp.ExtractByMask_sa(OutRaster2, InMask, OutRaster3)
            gp.delete_management(OutRaster)
            gp.delete_management(OutRaster2)
            
#Third Section:  Creates new mosaic, and performs joinitem at end
for x in zone:
    print x
    gp.WorkSpace ='C:\\working\\r1\\TLGs\\out\\'
    OutWorkspace = 'C:\\working\\r1\\TLGs\\out\\'
    #tabs = 'C:\\WorkSpace\\datalist\\LANDFIRE_CSV\\tabs\\z%s.tab' %(x)
    #OutRaster3 = 'C:\\working\\FPA\\20090201_west\\mt\\out\\%s%s_r' % (x, i) #needed for the input grid in the aml to run joinitem
    rasters = gp.ListRasters("*%s%s_r*"%(x, i), "GRID") 
    raster = rasters.next()
    namegrid = '%s%s_m'%(x, i)
    mystring=""
    while raster:
        mystring+=(raster) + "; "
        raster = rasters.next()
    else:
        mystring=mystring.rstrip("; ") # r meaning strip the ; on the right
        gp.MosaicToNewRaster_management(mystring, OutWorkspace, namegrid, "#", "#", "#", "#", "MAXIMUM", "#")
        print 'mosaic complete!'
       
