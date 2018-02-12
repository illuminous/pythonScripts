import os, arcgisscripting, time
tic = time.clock()
# Create the Geoprocessor object
gp = arcgisscripting.create()
gp.CheckOutExtension("spatial")
gp.AddToolBox
gp.toolbox = "management"
gp.OverWriteOutput = 0

zones = ['CA_CA']#, 'EA_IA', 'EA_IL', 'EA_IN','EA_MI', 'EA_MN', 'EA_MO', 'EA_NH', 'EA_NJ', 'EA_OH', 'EA_PA', 'EA_WI', 'EA_WV', 'GB_ID', 'GB_NV', 'GB_UT', 'GB_WY', 'NR_ID','NR_MT', 'NR_ND', 'NW_OR', 'NW_WA', 'RM_CO', 'RM_KS', 'RM_NE', 'RM_SD', 'RM_WY', 'SA_AL', 'SA_AR', 'SA_FL', 'SA_GA', 'SA_KY', 'SA_LA', 'SA_MD','SA_MS', 'SA_NC', 'SA_OK', 'SA_SC', 'SA_TN', 'SA_TX', 'SA_VA', 'SW_AZ', 'SW_NM', 'SW_TX'] #these are FPUs
names = ['_001']#,'_002', '_003', '_004', '_005', '_006', '_007', '_008', '_009', '_010', '_011', '_012', '_013', '_014', '_015']

for zone in zones:
    for name in names:
        print zone, name
        try:
            coordysFPU = "C:/Program Files/ArcGIS/Coordinate Systems/Geographic Coordinate Systems/North America/North American Datum 1983.prj"
            coordsys = "C:/Program Files/ArcGIS/Coordinate Systems/Projected Coordinate Systems/Continental/North America/USA Contiguous Albers Equal Area Conic USGS.prj"
            InMask = 'G:/Working/FPA/Ancillary/fpa_09'
            InWhereClause = "FPU_Code = '%s%s'" % (zone, name)
            LFRaster = 'G:/Working/Carbon/geo/FVS_Outputs/comboall'                 
            OutRaster3 = 'G:/Working/Carbon/geo/FVS_Outputs/extracts/fpu/%s%s_c' %(zone, name)
            OutRasterABC = 'G:/Working/Carbon/geo/FVS_Outputs/extracts/fpu/%s%s_abc' % (zone, name)
            OutRasterBP = 'G:/Working/Carbon/geo/FVS_Outputs/extracts/fpu/%s%s_bp' % (zone, name)
            OutRasterCEM = 'G:/Working/Carbon/geo/FVS_Outputs/extracts/fpu/%s%s_cem' % (zone, name)
            OutRasterEX = 'G:/Working/Carbon/geo/FVS_Outputs/extracts/fpu/%s%s_ex' % (zone, name)
            OutRasterPM10 = 'G:/Working/Carbon/geo/FVS_Outputs/extracts/fpu/%s%s_pm10' % (zone, name)
            OutRasterPM25 = 'G:/Working/Carbon/geo/FVS_Outputs/extracts/fpu/%s%s_pm25' % (zone, name)
            kms = OutRaster3 

            print "Defining Projection"
            gp.DefineProjection_Management(LFRaster, coordsys)

            print "Create Mask OutRaster3"
            ##gp.ExtractByAttributes_sa(InMask, InWhereClause, OutRaster3)
            Ras = gp.Describe(kms)

            print Ras.Extent
            print InWhereClause
            tempEnvironment8 = gp.extent
            gp.extent = Ras.Extent

            print "Clipping Grid to Mask and Creating OutRaster4"
            gp.ExtractByMask_sa(LFRaster, OutRaster3, OutRasterABC)
            gp.ExtractByMask_sa(LFRaster, OutRaster3, OutRasterBP)
            gp.ExtractByMask_sa(LFRaster, OutRaster3, OutRasterCEM)
            gp.ExtractByMask_sa(LFRaster, OutRaster3, OutRasterEX)
            gp.ExtractByMask_sa(LFRaster, OutRaster3, OutRasterPM10)
            gp.ExtractByMask_sa(LFRaster, OutRaster3, OutRasterPM25)
            print "next one"
        except:
            # Print error message if an error occurs
            gp.GetMessages()

toc = time.clock()
totaltime = toc - tic
print 'Total Processing Time Equals'
print totaltime
