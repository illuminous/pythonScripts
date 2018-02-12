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
try:
  # Monty Python Quote
  print "\nMonty Python quote:"\
  "\n'NOBODY expects the Spanish Inquisition!\'\n"
  # Set Local Variables
  env.overwriteOutput = True
  arcpy.CheckOutExtension("spatial")
  FireDangerPath = "C:\\WorkSpace\\Projects\\FireDanger"
  ##inDataPath = FireDangerPath+"\\Raw_Data\\bytype\\fh_event"
  inDataPath = "C:\\WorkSpace\\FireDanger_Temp\\fh_event"
  evalPath = FireDangerPath+"\\USA\\eval_data"
  BaseRasterPath = FireDangerPath+"\\USA\\base_layers"
  LayerList = ["emissions","fuelcon","scorchht","treem"] ##["crowni","flame","spread","intensity"]##,"emissions","fuelcon","scorchht","soilh","treem"]
  MapZones = ['03']##['01','02','03','07','08','09','10','19']##['04','05','06','12','13','14','15','16','17'] ##['01','02','03','07','08','09','10','18','19','20','21','22','29','30']
  # Loop throuh the map zones
  for MapZone in MapZones:
    print "MapZone "+MapZone
    for Layer in LayerList:
      print "\tWorking on "+Layer
      # Set layer and path variables
      inLayer = "z"+MapZone+"_"+Layer
      RawDataPath = inDataPath+"\\z"+MapZone+".gdb"
      outPath = evalPath+"\\z"+MapZone+".gdb"
      env.workspace= RawDataPath
      # If the layer is crowni, scorchht or treem, then recalculate nonforested pixel
      FrstMaskList = ["crowni","scorchht","treem"]
      if Layer in FrstMaskList:
        print "\t"*2+"Reclassifying the NonForested cells to zero..."
        # Get the
        env.extent= "MINOF"
        RasterResolution = arcpy.GetRasterProperties_management(inLayer,"CELLSIZEX")
        # set the forest mask layer
        MaskRaster = BaseRasterPath+"\\"+"z"+MapZone+".gdb\\"+"frst_mask"+str(RasterResolution)
        # Reclassify the nonforested pixels (value = 1) with a con statement
        ForestExpression = "Value = 2"
        tmpRaster = Con(MaskRaster,inLayer,"0",ForestExpression)
      else:
        tmpRaster = Raster(inLayer)
      # Reclassify to High(2)/NotHigh(1)
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
  arcpy.CheckInExtension("spatial")
# ** RUN TIME STATS ***********************************************************#
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