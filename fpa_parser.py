import glob, arcgisscripting
import os
# Create the Geoprocessor object
gp = arcgisscripting.create()
gp.CheckOutExtension("spatial")
gp.AddToolBox
gp.toolbox = "management"
gp.OverWriteOutput = 0


zones = ['SA_FL', 'SA_VA', 'SW_TX']#'EA_MI', 'GB_ID', 'GB_NV', 'GB_UT', 'GB_WY', 'NR_MT', 'NR_ND', 'NW_OR', 'RM_CO', 'RM_SD', 'RM_WY', 'SA_FL', 'SA_LA', 'SA_TX', 'SW_AZ', 'SW_NM', 'SW_TX']
#zones = ['CA_CA', 'EA_IA', 'EA_IL', 'EA_IN','EA_MI', 'EA_MN', 'EA_MO', 'EA_NH', 'EA_NJ', 'EA_OH', 'EA_PA', 'EA_WI', 'EA_WV', 'GB_ID', 'GB_NV', 'GB_UT', 'GB_WY', 'NR_ID','NR_MT', 'NR_ND', 'NW_OR', 'NW_WA', 'RM_CO', 'RM_KS', 'RM_NE', 'RM_SD', 'RM_WY', 'SA_AL', 'SA_AR', 'SA_FL', 'SA_GA', 'SA_KY', 'SA_LA', 'SA_MD','SA_MS', 'SA_NC', 'SA_OK', 'SA_SC', 'SA_TN', 'SA_TX', 'SA_VA', 'SW_AZ', 'SW_NM', 'SW_TX'] #these are FPUs



names = ['_001','_002', '_003', '_004']#, '_005', '_006', '_007', '_008', '_009', '_010', '_011', '_012', '_013', '_014', '_015']

##oldnames = ['_STANDARD0_burnprob.asc_FLP.txt', '_STANDARD0_burnprob.asc', '_STANDARD0_burnprob.asc_MeanIntensity.asc', '_STANDARD0_burnprob.asc_FireSizeList.txt', '_TREATMENTS0_burnprob.asc', '_TREATMENTS0_burnprob.asc_FireSizeList.txt', '_TREATMENTS0_burnprob.asc_FLP.txt', '_TREATMENTS0_burnprob.asc_MeanIntensity.asc']
##
#####-------------------------------------------------------------------------------------------
#####First Section: Rename the FPA files into a consistent format
##                
####for zone in zones:  
####    for name in names:       
####        for oldname in oldnames:                                                
####            oldfilename = 'F:/Working/FPA/2012/1_Data/Corrections/Karin_adjusted_runs/v4/%s%s%s' %(zone, name, oldname)
####            newnames = dict()
####            newnames['_STANDARD0_burnprob.asc'] = '%s%s_SB.asc' %(zone, name)
####            newnames['_STANDARD0_burnprob.asc_FLP.txt'] = '%s%s_FLP.csv' %(zone, name)
####            newnames['_STANDARD0_burnprob.asc_MeanIntensity.asc'] = '%s%s_MI.asc' %(zone, name)
####            newnames['_STANDARD0_burnprob.asc_FireSizeList.txt'] = '%s%s_FSL.txt' %(zone, name)
####            newnames['_TREATMENTS0_burnprob.asc'] = '%s%s_TB.asc' %(zone, name)
####            newnames['_TREATMENTS0_burnprob.asc_FireSizeList.txt'] = '%s%s_TFSL.txt' %(zone, name)
####            newnames['_TREATMENTS0_burnprob.asc_FLP.txt'] = '%s%s_TFLP.csv' %(zone, name)
####            newnames['_TREATMENTS0_burnprob.asc_MeanIntensity.asc'] = '%s%s_TMI.asc' %(zone, name)
####            print 'oldfilename = ',oldfilename                
####            if os.access(oldfilename,os.F_OK):                
####                print 'renaming file...', oldfilename
####                newfilename = newnames[oldname]
####                os.rename(oldfilename, newfilename)
####            else:
####                print"file is not fixed or does not exist"
##
##
#########-------------------------------------------------------------------------------------------
### Second Section: add x, y from files to create a layer
### Set the spatial reference
### NOTE: you must have the "Coordinate Systems" turned on
### To do this click tools/options and check "Coordinate Systems"
### in the General Tab
##print "Add x, y from files to create a layer"
##for zone in zones:
##    for name in names:
##        print zone,name
##        try:
##            # Prepare the variables
##            in_Table = 'F:/Working/FPA/2012/1_Data/Corrections/Karin_adjusted_runs/v4/%s%s_FLP.csv' %(zone, name)
##            in_x = "XPos"
##            in_y = "YPos"
##            out_Layer = "%s%s_Bpr" %(zone, name)
##            #spref = "C:/Program Files/ArcGIS/Coordinate Systems/Geographic Coordinate Systems/North America/North American Datum 1983.prj"
##
##    # Make the XY event...
##            gp.MakeXYEventLayer(in_Table, in_x, in_y, out_Layer)
##
##    # Save to a layer file
##            gp.SaveToLayerFile(out_Layer, 'F:/Working/FPA/2012/2_Uncliped/Corrections/%s%s_BPR.lyr' %(zone, name)) 
##
##        except:
##            # If an error occurred print the message to the screen
##           print gp.GetMessages()
##
##
#############------------------------------------------------------------------------------------------
############# Third Section: convert new feature layers to rasters
##
##print 'Convert new feature layers to rasters'
##
##for zone in zones:
##    for name in names:
##        print "Creating BPR",zone,name
##        try:
##            # Set local variables
##            InFeatures = 'F:/Working/FPA/2012/2_Uncliped/Corrections/%s%s_BPR.lyr' %(zone, name)
##            InField = "PBurn"
##            OutRaster = 'F:/Working/FPA/2012/2_Uncliped/Corrections/%s%s_pb' %(zone, name)
##            InCellSize = "270"
##
##            # Process: FeatureToRaster_conversion
##            gp.FeatureToRaster_conversion(InFeatures, InField, OutRaster, InCellSize)
##
##        except:
##            # Print error message if an error occurs
##            print gp.GetMessages()
##
####'Convert new feature layers to rasters'
##
##for zone in zones:
##    for name in names:
##        print "Creating FIL1",zone,name
##        try:
##            # Set local variables
##            InFeatures = 'F:/Working/FPA/2012/2_Uncliped/Corrections/%s%s_BPR.lyr' %(zone, name)
##            InField = "FIL1"
##            OutRaster = 'F:/Working/FPA/2012/2_Uncliped/Corrections/%s%s_f1' %(zone, name)
##            InCellSize = "270"
##
##            # Process: FeatureToRaster_conversion
##            gp.FeatureToRaster_conversion(InFeatures, InField, OutRaster, InCellSize)
##
##        except:
##            # Print error message if an error occurs
##            print gp.GetMessages()
##
##for zone in zones:
##    for name in names:
##        print "Creating FIL2",zone,name
##        try:
##            # Set local variables
##            InFeatures = 'F:/Working/FPA/2012/2_Uncliped/Corrections/%s%s_BPR.lyr' %(zone, name)
##            InField = "FIL2"
##            OutRaster = 'F:/Working/FPA/2012/2_Uncliped/Corrections/%s%s_f2' %(zone, name)
##            InCellSize = "270"
##
##            # Process: FeatureToRaster_conversion
##            gp.FeatureToRaster_conversion(InFeatures, InField, OutRaster, InCellSize)
##
##        except:
##            # Print error message if an error occurs
##            print gp.GetMessages()
##
##for zone in zones:
##    for name in names:
##        print "Creating FIL3",zone,name
##        try:
##            # Set local variables
##            InFeatures = 'F:/Working/FPA/2012/2_Uncliped/Corrections/%s%s_BPR.lyr' %(zone, name)
##            InField = "FIL3"
##            OutRaster = 'F:/Working/FPA/2012/2_Uncliped/Corrections/%s%s_f3' %(zone, name)
##            InCellSize = "270"
##
##            # Process: FeatureToRaster_conversion
##            gp.FeatureToRaster_conversion(InFeatures, InField, OutRaster, InCellSize)
##
##        except:
##            # Print error message if an error occurs
##            print gp.GetMessages()
##
##for zone in zones:
##    for name in names:
##        print "Creating FIL4",zone,name
##        try:
##            # Set local variables
##            InFeatures = 'F:/Working/FPA/2012/2_Uncliped/Corrections/%s%s_BPR.lyr' %(zone, name)
##            InField = "FIL4"
##            OutRaster = 'F:/Working/FPA/2012/2_Uncliped/Corrections/%s%s_f4' %(zone, name)
##            InCellSize = "270"
##
##            # Process: FeatureToRaster_conversion
##            gp.FeatureToRaster_conversion(InFeatures, InField, OutRaster, InCellSize)
##
##        except:
##            # Print error message if an error occurs
##            print gp.GetMessages()
##
##for zone in zones:
##    for name in names:
##        print "Creating FIL5",zone,name
##        try:
##            # Set local variables
##            InFeatures = 'F:/Working/FPA/2012/2_Uncliped/Corrections/%s%s_BPR.lyr' %(zone, name)
##            InField = "FIL5"
##            OutRaster = 'F:/Working/FPA/2012/2_Uncliped/Corrections/%s%s_f5' %(zone, name)
##            InCellSize = "270"
##
##            # Process: FeatureToRaster_conversion
##            gp.FeatureToRaster_conversion(InFeatures, InField, OutRaster, InCellSize)
##
##        except:
##            # Print error message if an error occurs
##            print gp.GetMessages()
##
##for zone in zones:
##    for name in names:
##        print "Creating FIL6", zone,name
##        try:
##            # Set local variables
##            InFeatures = 'F:/Working/FPA/2012/2_Uncliped/Corrections/%s%s_BPR.lyr' %(zone, name)
##            InField = "FIL6"
##            OutRaster = 'F:/Working/FPA/2012/2_Uncliped/Corrections/%s%s_f6' %(zone, name)
##            InCellSize = "270"
##
##            # Process: FeatureToRaster_conversion
##            gp.FeatureToRaster_conversion(InFeatures, InField, OutRaster, InCellSize)
##
##        except:
##            # Print error message if an error occurs
##            print gp.GetMessages()

for zone in zones:
    for name in names:
        print zone, name
        try:
            coordysFPU = "C:/Program Files/ArcGIS/Coordinate Systems/Geographic Coordinate Systems/North America/North American Datum 1983.prj"
            coordsys = "C:/Program Files/ArcGIS/Coordinate Systems/Projected Coordinate Systems/Continental/North America/USA Contiguous Albers Equal Area Conic USGS.prj"
            InMask = 'C:/Working/FPA/2012_Layers/fpa_09'
            InWhereClause = "FPU_Code = '%s%s'" % (zone, name)
            LFRaster = 'C:/Working/KR_Stamps/%s%s_pb' %(zone, name)                 
            OutRaster3 = 'C:/Working/pb/%s%s_c' % (zone, name)
            OutRaster4 = 'C:/Working/pb/%s%s_pb' % (zone, name)
            kms = OutRaster3 

            print "Defining Projection"
            gp.DefineProjection_Management(LFRaster, coordsys)

            print "Create Mask OutRaster3"
            gp.ExtractByAttributes_sa(InMask, InWhereClause, OutRaster3)
            Ras = gp.Describe(kms)

            print Ras.Extent
            print InWhereClause
            tempEnvironment8 = gp.extent
            gp.extent = Ras.Extent

            print "Clipping Grid to Mask and Creating OutRaster4"
            gp.ExtractByMask_sa(LFRaster, OutRaster3, OutRaster4)

            print "next one"
        except:
            # Print error message if an error occurs
            gp.GetMessages()

for zone in zones:
    for name in names:
        print zone, name
        try:
            coordysFPU = "C:/Program Files/ArcGIS/Coordinate Systems/Geographic Coordinate Systems/North America/North American Datum 1983.prj"
            coordsys = "C:/Program Files/ArcGIS/Coordinate Systems/Projected Coordinate Systems/Continental/North America/USA Contiguous Albers Equal Area Conic USGS.prj"
            InMask = 'C:/Working/FPA/2012_Layers/fpa_09'
            InWhereClause = "FPU_Code = '%s%s'" % (zone, name)
            LFRaster = 'C:/Working/KR_Stamps/%s%s_f1' %(zone, name)                 
            OutRaster3 = 'C:/Working/pb/%s%s_c' % (zone, name)
            OutRaster4 = 'C:/Working/f1/%s%s_f1' % (zone, name)
            kms = OutRaster3 

            print "Defining Projection"
            gp.DefineProjection_Management(LFRaster, coordsys)

            print "Create Mask OutRaster3"
 ##           gp.ExtractByAttributes_sa(InMask, InWhereClause, OutRaster3)
            Ras = gp.Describe(kms)

            print Ras.Extent
            print InWhereClause
            tempEnvironment8 = gp.extent
            gp.extent = Ras.Extent

            print "Clipping Grid to Mask and Creating OutRaster4"
            gp.ExtractByMask_sa(LFRaster, OutRaster3, OutRaster4)

            print "next one"
        except:
            # Print error message if an error occurs
            gp.GetMessages()

for zone in zones:
    for name in names:
        print zone, name
        try:
            coordysFPU = "C:/Program Files/ArcGIS/Coordinate Systems/Geographic Coordinate Systems/North America/North American Datum 1983.prj"
            coordsys = "C:/Program Files/ArcGIS/Coordinate Systems/Projected Coordinate Systems/Continental/North America/USA Contiguous Albers Equal Area Conic USGS.prj"
            InMask = 'C:/Working/FPA/2012_Layers/fpa_09'
            InWhereClause = "FPU_Code = '%s%s'" % (zone, name)
            LFRaster = 'C:/Working/KR_Stamps/%s%s_f2' %(zone, name)                 
            OutRaster3 = 'C:/Working/pb/%s%s_c' % (zone, name)
            OutRaster4 = 'C:/Working/f2/%s%s_f2' % (zone, name)
            kms = OutRaster3 

            print "Defining Projection"
            gp.DefineProjection_Management(LFRaster, coordsys)

            print "Create Mask OutRaster3"
 ##           gp.ExtractByAttributes_sa(InMask, InWhereClause, OutRaster3)
            Ras = gp.Describe(kms)

            print Ras.Extent
            print InWhereClause
            tempEnvironment8 = gp.extent
            gp.extent = Ras.Extent

            print "Clipping Grid to Mask and Creating OutRaster4"
            gp.ExtractByMask_sa(LFRaster, OutRaster3, OutRaster4)

            print "next one"
        except:
            # Print error message if an error occurs
            gp.GetMessages()

for zone in zones:
    for name in names:
        print zone, name
        try:
            coordysFPU = "C:/Program Files/ArcGIS/Coordinate Systems/Geographic Coordinate Systems/North America/North American Datum 1983.prj"
            coordsys = "C:/Program Files/ArcGIS/Coordinate Systems/Projected Coordinate Systems/Continental/North America/USA Contiguous Albers Equal Area Conic USGS.prj"
            InMask = 'C:/Working/FPA/2012_Layers/fpa_09'
            InWhereClause = "FPU_Code = '%s%s'" % (zone, name)
            LFRaster = 'C:/Working/KR_Stamps/%s%s_f3' %(zone, name)                 
            OutRaster3 = 'C:/Working/pb/%s%s_c' % (zone, name)
            OutRaster4 = 'C:/Working/f3/%s%s_f3' % (zone, name)
            kms = OutRaster3 

            print "Defining Projection"
            gp.DefineProjection_Management(LFRaster, coordsys)

            print "Create Mask OutRaster3"
 ##           gp.ExtractByAttributes_sa(InMask, InWhereClause, OutRaster3)
            Ras = gp.Describe(kms)

            print Ras.Extent
            print InWhereClause
            tempEnvironment8 = gp.extent
            gp.extent = Ras.Extent

            print "Clipping Grid to Mask and Creating OutRaster4"
            gp.ExtractByMask_sa(LFRaster, OutRaster3, OutRaster4)

            print "next one"
        except:
            # Print error message if an error occurs
            gp.GetMessages()

for zone in zones:
    for name in names:
        print zone, name
        try:
            coordysFPU = "C:/Program Files/ArcGIS/Coordinate Systems/Geographic Coordinate Systems/North America/North American Datum 1983.prj"
            coordsys = "C:/Program Files/ArcGIS/Coordinate Systems/Projected Coordinate Systems/Continental/North America/USA Contiguous Albers Equal Area Conic USGS.prj"
            InMask = 'C:/Working/FPA/2012_Layers/fpa_09'
            InWhereClause = "FPU_Code = '%s%s'" % (zone, name)
            LFRaster = 'C:/Working/KR_Stamps/%s%s_f4' %(zone, name)                 
            OutRaster3 = 'C:/Working/pb/%s%s_c' % (zone, name)
            OutRaster4 = 'C:/Working/f4/%s%s_f4' % (zone, name)
            kms = OutRaster3 

            print "Defining Projection"
            gp.DefineProjection_Management(LFRaster, coordsys)

            print "Create Mask OutRaster3"
 ##           gp.ExtractByAttributes_sa(InMask, InWhereClause, OutRaster3)
            Ras = gp.Describe(kms)

            print Ras.Extent
            print InWhereClause
            tempEnvironment8 = gp.extent
            gp.extent = Ras.Extent

            print "Clipping Grid to Mask and Creating OutRaster4"
            gp.ExtractByMask_sa(LFRaster, OutRaster3, OutRaster4)

            print "next one"
        except:
            # Print error message if an error occurs
            gp.GetMessages()

for zone in zones:
    for name in names:
        print zone, name
        try:
            coordysFPU = "C:/Program Files/ArcGIS/Coordinate Systems/Geographic Coordinate Systems/North America/North American Datum 1983.prj"
            coordsys = "C:/Program Files/ArcGIS/Coordinate Systems/Projected Coordinate Systems/Continental/North America/USA Contiguous Albers Equal Area Conic USGS.prj"
            InMask = 'C:/Working/FPA/2012_Layers/fpa_09'
            InWhereClause = "FPU_Code = '%s%s'" % (zone, name)
            LFRaster = 'C:/Working/KR_Stamps/%s%s_f5' %(zone, name)                 
            OutRaster3 = 'C:/Working/pb/%s%s_c' % (zone, name)
            OutRaster4 = 'C:/Working/f5/%s%s_f5' % (zone, name)
            kms = OutRaster3 

            print "Defining Projection"
            gp.DefineProjection_Management(LFRaster, coordsys)

            print "Create Mask OutRaster3"
 ##           gp.ExtractByAttributes_sa(InMask, InWhereClause, OutRaster3)
            Ras = gp.Describe(kms)

            print Ras.Extent
            print InWhereClause
            tempEnvironment8 = gp.extent
            gp.extent = Ras.Extent

            print "Clipping Grid to Mask and Creating OutRaster4"
            gp.ExtractByMask_sa(LFRaster, OutRaster3, OutRaster4)

            print "next one"
        except:
            # Print error message if an error occurs
            gp.GetMessages()

for zone in zones:
    for name in names:
        print zone, name
        try:
            coordysFPU = "C:/Program Files/ArcGIS/Coordinate Systems/Geographic Coordinate Systems/North America/North American Datum 1983.prj"
            coordsys = "C:/Program Files/ArcGIS/Coordinate Systems/Projected Coordinate Systems/Continental/North America/USA Contiguous Albers Equal Area Conic USGS.prj"
            InMask = 'C:/Working/FPA/2012_Layers/fpa_09'
            InWhereClause = "FPU_Code = '%s%s'" % (zone, name)
            LFRaster = 'C:/Working/KR_Stamps/%s%s_f6' %(zone, name)                 
            OutRaster3 = 'C:/Working/pb/%s%s_c' % (zone, name)
            OutRaster4 = 'C:/Working/f6/%s%s_f6' % (zone, name)
            kms = OutRaster3 

            print "Defining Projection"
            gp.DefineProjection_Management(LFRaster, coordsys)

            print "Create Mask OutRaster3"
 ##           gp.ExtractByAttributes_sa(InMask, InWhereClause, OutRaster3)
            Ras = gp.Describe(kms)

            print Ras.Extent
            print InWhereClause
            tempEnvironment8 = gp.extent
            gp.extent = Ras.Extent

            print "Clipping Grid to Mask and Creating OutRaster4"
            gp.ExtractByMask_sa(LFRaster, OutRaster3, OutRaster4)

            print "next one"
        except:
            # Print error message if an error occurs
            gp.GetMessages()
