import glob, arcgisscripting
import os
# Create the Geoprocessor object
gp = arcgisscripting.create()
gp.CheckOutExtension("spatial")
gp.AddToolBox
gp.toolbox = "management"


zones = ['RM_WY']#'EA_IL', 'EA_IN', 'NW_WA', 'SA_PR','NR_MT','CA_CA', 'EA_IA', 'EA_MI', 'EA_MN', 'EA_MO', 'EA_NH', 'EA_NJ', 'EA_OH', 'EA_PA', 'EA_WI', 'EA_WV', 'GB_ID', 'GB_NV', 'GB_UT', 'GB_WY', 'NR_ID','NR_MT', 'NR_ND', 'NW_OR', 'MW_WA', 'RM_CO', 'RM_KS', 'RM_NE', 'RM_SD', 'RM_WY', 'SA_AL', 'SA_AR', 'SA_FL', 'SA_GA', 'SA_KY', 'SA_LA', 'SA_MD','SA_MS', 'SA_NC', 'SA_OK', 'SA_SC', 'SA_TN', 'SA_TX', 'SA_VA', 'SW_AZ', 'SW_NM', 'SW_TX'] #these are FPUs



names = ['_003']#'_001', '_002', '_003', '_004', '_005', '_006', '_007', '_008', '_009', '_010', '_011', '_012', '_013', '_014', '_015']

oldnames = ['_STANDARD0_burnprob.asc_FLP.txt', '_STANDARD0_burnprob.asc', '_STANDARD0_burnprob.asc_MeanIntensity.asc', '_STANDARD0_burnprob.asc_FireSizeList.txt', '_TREATMENTS0_burnprob.asc', '_TREATMENTS0_burnprob.asc_FireSizeList.txt', '_TREATMENTS0_burnprob.asc_FLP.txt', '_TREATMENTS0_burnprob.asc_MeanIntensity.asc']

#directory = 'C:\\Working\FPA\extracted\\simresults\\test'


###-------------------------------------------------------------------------------------------
###First Section: Rename the FPA files into a consistent format
                
##for zone in zones:  
##    for name in names:       
##        for oldname in oldnames:                                                
##            oldfilename = 'C:\\Working\FPA\extracted\\simresults\\%s%s%s' %(zone, name, oldname)
##            newnames = dict()
##            newnames['_STANDARD0_burnprob.asc'] = '%s%s_SB.asc' %(zone, name)
##            newnames['_STANDARD0_burnprob.asc_FLP.txt'] = '%s%s_FLP.csv' %(zone, name)
##            newnames['_STANDARD0_burnprob.asc_MeanIntensity.asc'] = '%s%s_MI.asc' %(zone, name)
##            newnames['_STANDARD0_burnprob.asc_FireSizeList.txt'] = '%s%s_FSL.txt' %(zone, name)
##            newnames['_TREATMENTS0_burnprob.asc'] = '%s%s_TB.asc' %(zone, name)
##            newnames['_TREATMENTS0_burnprob.asc_FireSizeList.txt'] = '%s%s_TFSL.txt' %(zone, name)
##            newnames['_TREATMENTS0_burnprob.asc_FLP.txt'] = '%s%s_TFLP.csv' %(zone, name)
##            newnames['_TREATMENTS0_burnprob.asc_MeanIntensity.asc'] = '%s%s_TMI.asc' %(zone, name)
##            print 'oldfilename = ',oldfilename                
##            if os.access(oldfilename,os.F_OK):                
##                print 'renaming file...', oldfilename
##                newfilename = newnames[oldname]
##                os.rename(oldfilename, newfilename)
##            else:
##                print"file is not fixed or does not exist"
##
##



#####-------------------------------------------------------------------------------------------
##### Second Section: add x, y from files to create a layer
##### Set the spatial reference
##### NOTE: you must have the "Coordinate Systems" turned on
##### To do this click tools/options and check "Coordinate Systems"
##### in the General Tab
##print "Add x, y from files to create a layer"
##for zone in zones:
##    for name in names:
##        print name
##        try:
##            # Prepare the variables
##            in_Table = 'C:\\Working\\FPA\\renamed\\%s%s_FLP.csv' %(zone, name)
##            in_x = "XPos"
##            in_y = "YPos"
##            out_Layer = "%s%s_Pbr" %(zone, name)
##            spref = "C:\\Program Files\\ArcGIS\\Coordinate Systems\\Geographic Coordinate Systems\\North America\\North American Datum 1983.prj"
##
##    # Make the XY event...
##            gp.MakeXYEventLayer(in_Table, in_x, in_y, out_Layer, spref)
##
##    # Save to a layer file
##            gp.SaveToLayerFile(out_Layer, 'C:/Working/FPA/layers/%s%s_Pbr.lyr' %(zone, name)) 
##
##        except:
##            # If an error occurred print the message to the screen
##           print gp.GetMessages()




#######------------------------------------------------------------------------------------------
####### Third Section: convert new feature layers to rasters

##print "Convert new feature layers to rasters"
##
##
##for zone in zones:
##    for name in names:
##        print name
##        try:
##            # Set local variables
##            InFeatures = 'C:\\Working\\FPA\\layers\\%s%s_Pbr.lyr' %(zone, name)
##            InField = "PBurn"
##            OutRaster = 'C:\\Working\\FPA\\PBR_Raster\\%s%s_Pb' %(zone, name)
##            InCellSize = "270"
##
##            # Process: FeatureToRaster_conversion
##            gp.FeatureToRaster_conversion(InFeatures, InField, OutRaster, InCellSize)
##
##        except:
##            # Print error message if an error occurs
##            print gp.GetMessages()



##print "Convert new feature layers to rasters Fil1"
##
##
##for zone in zones:
##    for name in names:
##        print name
##        try:
##            # Set local variables
##            InFeatures = 'C:\\Working\\FPA\\layers\\%s%s_Pbr.lyr' %(zone, name)
##            InField = "Fil1"
##            OutRaster = 'C:\\Working\\FPA\\Fil1_Raster\\%s%s_F1' %(zone, name)
##            InCellSize = "270"
##
##            # Process: FeatureToRaster_conversion
##            gp.FeatureToRaster_conversion(InFeatures, InField, OutRaster, InCellSize)
##
##        except:
##            # Print error message if an error occurs
##            print gp.GetMessages()
##
##print "Convert new feature layers to rasters Fil2"
##
##for zone in zones:
##    for name in names:
##        print name
##        try:
##            # Set local variables
##            InFeatures = 'C:\\Working\\FPA\\layers\\%s%s_Pbr.lyr' %(zone, name)
##            InField = "Fil2"
##            OutRaster = 'C:\\Working\\FPA\\Fil2_Raster\\%s%s_F2' %(zone, name)
##            InCellSize = "270"
##
##            # Process: FeatureToRaster_conversion
##            gp.FeatureToRaster_conversion(InFeatures, InField, OutRaster, InCellSize)
##
##        except:
##            # Print error message if an error occurs
##            print gp.GetMessages()

##print "Convert new feature layers to rasters Fil3"
##
##for zone in zones:
##    for name in names:
##        print name
##        try:
##            # Set local variables
##            InFeatures = 'C:\\Working\\FPA\\layers\\%s%s_Pbr.lyr' %(zone, name)
##            InField = "Fil3"
##            OutRaster = 'C:\\Working\\FPA\\Fil3_Raster\\%s%s_F3' %(zone, name)
##            InCellSize = "270"
##
##            # Process: FeatureToRaster_conversion
##            gp.FeatureToRaster_conversion(InFeatures, InField, OutRaster, InCellSize)
##
##        except:
##            # Print error message if an error occurs
##            print gp.GetMessages()
####
##print "Convert new feature layers to rasters Fil4"
##
##for zone in zones:
##    for name in names:
##        print name
##        try:
##            # Set local variables
##            InFeatures = 'C:\\Working\\FPA\\layers\\%s%s_Pbr.lyr' %(zone, name)
##            InField = "Fil4"
##            OutRaster = 'C:\\Working\\FPA\\Fil4_Raster\\%s%s_F4' %(zone, name)
##            InCellSize = "270"
##
##            # Process: FeatureToRaster_conversion
##            gp.FeatureToRaster_conversion(InFeatures, InField, OutRaster, InCellSize)
##
##        except:
##            # Print error message if an error occurs
##            print gp.GetMessages()
##
##print "Convert new feature layers to rasters Fil5"
##
##for zone in zones:
##    for name in names:
##        print name
##        try:
##            # Set local variables
##            InFeatures = 'C:\\Working\\FPA\\layers\\%s%s_Pbr.lyr' %(zone, name)
##            InField = "Fil5"
##            OutRaster = 'C:\\Working\\FPA\\Fil5_Raster\\%s%s_F5' %(zone, name)
##            InCellSize = "270"
##
##            # Process: FeatureToRaster_conversion
##            gp.FeatureToRaster_conversion(InFeatures, InField, OutRaster, InCellSize)
##
##        except:
##            # Print error message if an error occurs
##            print gp.GetMessages()
##
##print "Convert new feature layers to rasters Fil6"
##
##for zone in zones:
##    for name in names:
##        print name
##        try:
##            # Set local variables
##            InFeatures = 'C:\\Working\\FPA\\layers\\%s%s_Pbr.lyr' %(zone, name)
##            InField = "Fil6"
##            OutRaster = 'C:\\Working\\FPA\\Fil6_Raster\\%s%s_F6' %(zone, name)
##            InCellSize = "270"
##
##            # Process: FeatureToRaster_conversion
##            gp.FeatureToRaster_conversion(InFeatures, InField, OutRaster, InCellSize)
##
##        except:
##            # Print error message if an error occurs
##            print gp.GetMessages()
#####------------------------------------------------------------------------------------------
##### Forth Section: Clip Rasters to FPA FPU extents and reproject to landfire
##
##






for zone in zones:
    print zone
    for name in names:
        print names
        try:
            #coordysFPU = "C:\Program Files\ArcGIS\Coordinate Systems\Geographic Coordinate Systems\North America\North American Datum 1983.prj"
            coordsys = "C:\Program Files\ArcGIS\Coordinate Systems\Projected Coordinate Systems\Continental\North America\USA Contiguous Albers Equal Area Conic USGS.prj"
            InMask = 'C:/working/FPA/fpa_270'
            InWhereClause = "FPU_ID = '%s%s'" % (zone, name)
            LFRaster = 'C:\\working\\FPA\\PBR_Raster\\%s%s_PB' %(zone, name)                 
            #OutRaster = 'C:\\working\\FPA\\Fil2_Raster_clip\\%s%s_o' % (zone, name)
            IntRaster = 'C:\\working\\FPA\\PBR_Raster_clip\\%s%s_i' % (zone, name)
            OutRaster2 = 'C:\\working\\FPA\\PBR_Raster_clip\\%s%s_2' % (zone, name)
            OutRaster3 = 'C:\\working\\FPA\\PBR_Raster_clip\\%s%s_c' % (zone, name)
            OutRaster4 = 'C:\\working\\FPA\\PBR_Raster_clip\\%s%s_PB' % (zone, name)
            kms = 'C:\\working\\FPA\\PBR_Raster_clip\\%s%s_c' % (zone, name)
##        if gp.exists (OutRaster4):
##            print OutRaster4 + "exists"
##        else:
            #Process:  Copy Raster, using copy from aml
            gp.copy(LFRaster, IntRaster)
            #gp.Times_sa(LFRaster, 10000, OutRaster) 
            #gp.Int_sa(OutRaster, IntRaster, "INTEGER")
            gp.DefineProjection_Management(IntRaster, coordsys)
            gp.copy(IntRaster, OutRaster2)
            #Process:  Extract by zone mask delet this....gp.AddToolbox("C:/Program Files/ArcGIS/ArcToolbox/Toolboxes/Spatial Analyst Tools.tbx")
            #gp.ExtractByMask_sa(OutRaster2, InMask2, OutRaster3)
            #gp.Con_sa(OutRaster2, InMask, OutRaster3, "Value >= 0")
            gp.ExtractByAttributes_sa(InMask, InWhereClause, OutRaster3)
            Ras = gp.Describe(kms)
            print Ras.Extent
            print InWhereClause
            tempEnvironment7 = gp.extent
            gp.extent = Ras.Extent
            #gp.ExtractByAttributes_sa(OutRaster2, InWhereClause, OutRaster3)
            gp.ExtractByMask_sa(OutRaster2, OutRaster3, OutRaster4)
            gp.delete_management(IntRaster)
            #gp.delete_management(OutRaster)
            gp.delete_management(OutRaster2)
            gp.delete_management(OutRaster3)
            print "next one"
        except:
            # Print error message if an error occurs
            print gp.GetMessages()
##
##for zone in zones:
##    print zone
##    for name in names:
##        print names
##        try:
##            #coordysFPU = "C:\Program Files\ArcGIS\Coordinate Systems\Geographic Coordinate Systems\North America\North American Datum 1983.prj"
##            coordsys = "C:\Program Files\ArcGIS\Coordinate Systems\Projected Coordinate Systems\Continental\North America\USA Contiguous Albers Equal Area Conic USGS.prj"
##            InMask = 'C:/working/FPA/fpa_270'
##            InWhereClause = "FPU_ID = '%s%s'" % (zone, name)
##            LFRaster = 'C:\\working\\FPA\\Fil2_Raster\\%s%s_F2' %(zone, name)                 
##            #OutRaster = 'C:\\working\\FPA\\Fil2_Raster_clip\\%s%s_o' % (zone, name)
##            IntRaster = 'C:\\working\\FPA\\Fil2_Raster_clip\\%s%s_i' % (zone, name)
##            OutRaster2 = 'C:\\working\\FPA\\Fil2_Raster_clip\\%s%s_2' % (zone, name)
##            OutRaster3 = 'C:\\working\\FPA\\Fil2_Raster_clip\\%s%s_c' % (zone, name)
##            OutRaster4 = 'C:\\working\\FPA\\Fil2_Raster_clip\\%s%s_F2' % (zone, name)
##            kms = 'C:\\working\\FPA\\Fil2_Raster_clip\\%s%s_c' % (zone, name)
####        if gp.exists (OutRaster4):
####            print OutRaster4 + "exists"
####        else:
##            #Process:  Copy Raster, using copy from aml
##            gp.copy(LFRaster, IntRaster)
##            #gp.Times_sa(LFRaster, 10000, OutRaster) 
##            #gp.Int_sa(OutRaster, IntRaster, "INTEGER")
##            gp.DefineProjection_Management(IntRaster, coordsys)
##            gp.copy(IntRaster, OutRaster2)
##            #Process:  Extract by zone mask delet this....gp.AddToolbox("C:/Program Files/ArcGIS/ArcToolbox/Toolboxes/Spatial Analyst Tools.tbx")
##            #gp.ExtractByMask_sa(OutRaster2, InMask2, OutRaster3)
##            #gp.Con_sa(OutRaster2, InMask, OutRaster3, "Value >= 0")
##            gp.ExtractByAttributes_sa(InMask, InWhereClause, OutRaster3)
##            Ras = gp.Describe(kms)
##            print Ras.Extent
##            print InWhereClause
##            tempEnvironment7 = gp.extent
##            gp.extent = Ras.Extent
##            #gp.ExtractByAttributes_sa(OutRaster2, InWhereClause, OutRaster3)
##            gp.ExtractByMask_sa(OutRaster2, OutRaster3, OutRaster4)
##            gp.delete_management(IntRaster)
##            #gp.delete_management(OutRaster)
##            gp.delete_management(OutRaster2)
##            gp.delete_management(OutRaster3)
##            print "next one"
##        except:
##            # Print error message if an error occurs
##            print gp.GetMessages()


##for zone in zones:
##    print zone
##    for name in names:
##        print names
##        try:
##            #coordysFPU = "C:\Program Files\ArcGIS\Coordinate Systems\Geographic Coordinate Systems\North America\North American Datum 1983.prj"
##            coordsys = "C:\Program Files\ArcGIS\Coordinate Systems\Projected Coordinate Systems\Continental\North America\USA Contiguous Albers Equal Area Conic USGS.prj"
##            InMask = 'C:/working/FPA/fpa_270'
##            InWhereClause = "FPU_ID = '%s%s'" % (zone, name)
##            LFRaster = 'C:\\working\\FPA\\Fil6_Raster\\%s%s_F6' %(zone, name)                 
##            #OutRaster = 'C:\\working\\FPA\\Fil2_Raster_clip\\%s%s_o' % (zone, name)
##            IntRaster = 'C:\\working\\FPA\\Fil6_Raster_clip\\%s%s_i' % (zone, name)
##            OutRaster2 = 'C:\\working\\FPA\\Fil6_Raster_clip\\%s%s_2' % (zone, name)
##            OutRaster3 = 'C:\\working\\FPA\\Fil6_Raster_clip\\%s%s_c' % (zone, name)
##            OutRaster4 = 'C:\\working\\FPA\\Fil6_Raster_clip\\%s%s_F6' % (zone, name)
##            kms = 'C:\\working\\FPA\\Fil6_Raster_clip\\%s%s_c' % (zone, name)
####        if gp.exists (OutRaster4):
####            print OutRaster4 + "exists"
####        else:
##            #Process:  Copy Raster, using copy from aml
##            gp.copy(LFRaster, IntRaster)
##            #gp.Times_sa(LFRaster, 10000, OutRaster) 
##            #gp.Int_sa(OutRaster, IntRaster, "INTEGER")
##            gp.DefineProjection_Management(IntRaster, coordsys)
##            gp.copy(IntRaster, OutRaster2)
##            #Process:  Extract by zone mask delet this....gp.AddToolbox("C:/Program Files/ArcGIS/ArcToolbox/Toolboxes/Spatial Analyst Tools.tbx")
##            #gp.ExtractByMask_sa(OutRaster2, InMask2, OutRaster3)
##            #gp.Con_sa(OutRaster2, InMask, OutRaster3, "Value >= 0")
##            gp.ExtractByAttributes_sa(InMask, InWhereClause, OutRaster3)
##            Ras = gp.Describe(kms)
##            print Ras.Extent
##            print InWhereClause
##            tempEnvironment7 = gp.extent
##            gp.extent = Ras.Extent
##            #gp.ExtractByAttributes_sa(OutRaster2, InWhereClause, OutRaster3)
##            gp.ExtractByMask_sa(OutRaster2, OutRaster3, OutRaster4)
##            gp.delete_management(IntRaster)
##            #gp.delete_management(OutRaster)
##            gp.delete_management(OutRaster2)
##            gp.delete_management(OutRaster3)
##            print "next one"
##        except:
##            # Print error message if an error occurs
##            print gp.GetMessages()

######### Fifth Section:  Creates new mosaic
##for zone in zones:
##    print zone
##    for name in names:
##        print name
##        gp.WorkSpace ='C:\\working\\FPA\\MT_20090608\\test\\out'
##        OutWorkspace ='C:\\working\\FPA\\MT_20090608\\test\\out'
##        OutRaster4 = 'C:\\working\\FPA\\MT_20090608\\test\\out\\%s%s_f3' % (zone, name)
##        rasters = gp.ListRasters("*%s%s_f3*"%(zone, name), "GRID") 
##        raster = rasters.next()
##        namegrid = '%s%s_f3'%(zone, name)
##        mystring=""
##        while raster:
##            mystring+=(raster) + "; "
##            raster = rasters.next()
##        else:
##            mystring=mystring.rstrip("; ") # r meaning strip the ; on the right
##            gp.MosaicToNewRaster_management(mystring, OutWorkspace, namegrid,  "#", "#", "#", "#", "FIRST", "#")
##            print 'mosaic complete!'
