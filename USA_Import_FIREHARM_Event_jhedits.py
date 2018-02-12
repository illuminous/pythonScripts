# Name: R. Brion Salter                                                        #
# USDA Forest Service, PNW Research Station                                    #
# Date: 01/07/2009                                                             #
# Last Revision: 09/17/2011                                                    #
# Purpose: This script mosaics, masks, and projects the zone probablity data   #
#          for the USA analysis area by LANDFIRE Map Zone...                   #
#                                                                              #
#
# Import system modules
import arcpy, string, sys, os, time, traceback
from arcpy import env
from arcpy.sa import *
#
timestamp = time.clock()

MapZones = []
def buildZones(zone_number_lower, zone_number_upper):
    for zone in range (zone_number_lower, zone_number_upper):
        if zone < 10:
            zonenum = 'z0'+'%s' %(zone)
            MapZones.append(zonenum)
        else:
            zonenum = 'z%s' %(zone)
            MapZones.append(zonenum)

def reclassNonforest(Layer, MaskRaster):
    print "\t"*2+"Reclassifying the NonForested cells to zero..."
    # Get the
    env.extent= "MINOF"
    RasterResolution = arcpy.GetRasterProperties_management(Layer,"CELLSIZEX")
    # set the forest mask layer
    
    # Reclassify the nonforested pixels (value = 1) with a con statement
    ForestExpression = "Value = 1"
    tmpRaster = Con(MaskRaster,Layer,"0",ForestExpression)
      
def reclass(Layer):
    print "\t"*2+"Reclassifying values to High/NotHigh..."
    if Layer == "crowni":
      ReclassExpression = "Value > 5000"
      ReclassRaster = Con(tmpRaster,2,1,ReclassExpression)
    if Layer == "emissions":
      ReclassExpression = "Value > 100"
      ReclassRaster = Con(tmpRaster,2,1,ReclassExpression)
    if Layer == "flame":
      ReclassExpression = "Value > 2"
      ReclassRaster = Con(tmpRaster,2,1,ReclassExpression)
    if Layer == "intensity":
      ReclassExpression = "Value > 400"
      ReclassRaster = Con(tmpRaster,2,1,ReclassExpression)
    if Layer == "fuelcon":
      ReclassExpression = "Value > 50"
      ReclassRaster = Con(tmpRaster,2,1,ReclassExpression)
    if Layer == "scorchht":
      ReclassExpression = "Value > 2"
      ReclassRaster = Con(tmpRaster,2,1,ReclassExpression)
    if Layer == "soilh":
      ReclassExpression = "Value > 60"
      ReclassRaster = Con(tmpRaster,2,1,ReclassExpression)
    if Layer == "spread":
      ReclassExpression = "Value > 83.3"
      ReclassRaster = Con(tmpRaster,2,1,ReclassExpression)
    if Layer == "treem":
      ReclassExpression = "Value > 70"
      ReclassRaster = Con(tmpRaster,2,1,ReclassExpression)
    ReclassRaster.save(outPath+"\\"+Layer)
    # Clean up
    arcpy.ResetEnvironments()

def timeStats():
    me = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    delta = time.clock()-timestamp
    if delta < 60:
      rdelta = round(delta,1)
      units = "seconds"
    else:
      rdelta = round(delta / 60,2)
      units = "minutes"
    timestamp = time.clock()
    print "\n" + me,"successfully finished:",str(time.asctime()),"\nTotal time in " + units + ":",str(rdelta),"\n"
    #Play wav file to let me know it has finished!
    file='tada.wav'
    from winsound import PlaySound, SND_FILENAME, SND_ASYNC
    PlaySound(file, SND_FILENAME|SND_ASYNC)

def main():
    buildZones(1,2)
    try:
        env.overwriteOutput = True
        arcpy.CheckOutExtension("spatial")
        LayerList = ["emissions","fuelcon","scorchht","treem"] ##["crowni","flame","spread","intensity"]##,"emissions","fuelcon","scorchht","soilh","treem"]

        for MapZone in MapZones:
            print "MapZone "+MapZone
            for Layer in LayerList:
                print "\tWorking on "+Layer
                # Set layer and path variables
                
#                inLayer = MapZone+"_"+Layer
#                RawDataPath = inDataPath+"\\"+MapZone+"_fh_grids"

#                outPath = inDataPath+"/outest"
#                env.workspace= RawDataPath
            #####################################
            # If the layer is crowni, scorchht or treem, then recalculate nonforested pixel
                FrstMaskList = ["crowni","scorchht","treem"]
                MaskRaster = 'H:/fireharmQAQC/zips/Event_Mode/z01_fh_grids/%s_evc_tree' %(MapZone)
                if Layer in FrstMaskList:                    
                    reclassNonforest(Layer, MaskRaster)
                else:
                    tmpRaster = Raster(inLayer)
                    global tmpRaster
                    reclass(Layer)
            #####################################  
            # Reclassify to High(2)/NotHigh(1)

            #  arcpy.CheckInExtension("spatial")
            # ** RUN TIME STATS ***********************************************************#
            timeStats()
    #******************************************************************************#
    except:
        # get the traceback object
        tb = sys.exc_info()[2]
        # tbinfo contains the line number that the code failed on and the code from that line
        tbinfo = traceback.format_tb(tb)[0]
        # concatenate information together concerning the error into a message string
        seperator = "********************************************************************************"
        pymsg = "PYTHON ERRORS:\nTraceback Info:\n" + tbinfo + "\nError Info:\n    " + str(sys.exc_type)+ ": " + str(sys.exc_value)
        # generate a message string for any ArcGIS tool errors
        msgs = seperator + "\nArcGIS ERRORS:\n" + arcpy.GetMessages(2)
        # return ArcGIS messages for use with a script tool
        arcpy.AddError(msgs)
        arcpy.AddError(pymsg)
        # print messages for use in Python/PythonWin
        print msgs
        print pymsg
        print "\nSCRIPT FAILED..."
        #Play wav file to let me know it has failed!
        file='Windows XP Error.wav'
        from winsound import PlaySound, SND_FILENAME, SND_ASYNC
        PlaySound(file, SND_FILENAME|SND_ASYNC)
