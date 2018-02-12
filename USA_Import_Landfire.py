# Name: R. Brion Salter                                                        #
# USDA Forest Service, PNW Research Station                                    #
# Date: 09/17/2008                                                             #
# Last Revision: 09/15/2011                                                    #
# Purpose: This script prepares the raw LANDFIRE rasters for the USA           #
#          MapZone centric FireDanger Fragstats Analyses.                      #
#          1. Sets the background value to Null                                #
#          2. Reclassifies the layer to NotHigh(1)/High(2)                     #

# Import system modules
import arcpy, string, sys, os, time, traceback
from arcpy import env
from arcpy.sa import *
#
timestamp = time.clock()
try:
  # Monty Python Quote
  print "Monty Python Quote:\n'And now for something completely different'\n"
  # Local variables...
  env.overwriteOutput = True
  arcpy.CheckOutExtension("spatial")
  BasePath = "C:\\WorkSpace\\Projects\\FireDanger"
  LF_Types = ['evc','cbd','cbh','fbfm40']##['flm','cbd', 'cbh', 'fbfm40', 'flm', 'frcc', 'mfri', 'pls', 'prs']
  ##MapZones = ['01','02','03','07','08','09','10','18','19','20','21','22','29','30']
  ##MapZones = ['04','05','06','12','13','14','15','16','17']
  MapZones = ['32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49']
  for MapZone in MapZones:
    print "Working on MapZone "+MapZone+":"
    ##inDataPath = BasePath+"\\Raw_Data\\bytype\\landfire\\z"+MapZone+".gdb"
    inDataPath = "C:\\WorkSpace\\FireDanger_Temp\\landfire\\z"+MapZone+".gdb"
    for LF_Type in LF_Types:
      print "\t"+string.upper(LF_Type)
      LF_Raster = "z" + MapZone+"_"+LF_Type
      RawData =  inDataPath + "\\"+LF_Raster
      outGDB = "z"+MapZone+".gdb"
      outDataPath = BasePath+"\\USA\\eval_data"
      # Create outGDB if it doesn't exist
      outRasterPath = outDataPath+"\\"+outGDB
      if not arcpy.Exists(outRasterPath):
        arcpy.CreateFileGDB_management(outDataPath,outGDB,"CURRENT")
      env.workspace = inDataPath
      # Set the Background value to Null
      NullExpression = "VALUE < 0"
      print "\tSetting the background value to Null"
      NullRaster = SetNull(LF_Raster,LF_Raster,NullExpression)
      # Reclassify the original mapzone data to a single integer value
      print "\tReclassifying..."
      if LF_Type == 'evc':
        ReclassExpression = "VALUE >= 101 AND VALUE <= 110"
        OutCon = Con(NullRaster,2,1,ReclassExpression)
        OutCon.save(outRasterPath+"\\"+LF_Type)
      if LF_Type == 'cbd':
        ReclassExpression = "VALUE > 15"
        OutCon = Con(NullRaster,2,1,ReclassExpression)
        OutCon.save(outRasterPath+"\\"+LF_Type)
      if LF_Type == 'cbh':
        ReclassExpression = "VALUE > 0 AND VALUE < 20"
        OutCon = Con(NullRaster,2,1,ReclassExpression)
        OutCon.save(outRasterPath+"\\"+LF_Type)
      if LF_Type == 'fbfm40':
        ReclassExpression = "VALUE IN (104,105,124,146,148,165,166,189,202,203,145,147,204,107,108,109,149)"
        OutCon = Con(NullRaster,2,1,ReclassExpression)
        OutCon.save(outRasterPath+"\\"+LF_Type)
      if LF_Type == 'flm':
        ReclassExpression = "VALUE IN (31,71,72,81,82,83,91,92,93,41,101,102)"
        OutCon = Con(NullRaster,2,1,ReclassExpression)
        OutCon.save(outRasterPath+"\\"+LF_Type)
      if LF_Type == 'frcc':
        ReclassExpression = "VALUE = 3"
        OutCon = Con(NullRaster,2,1,ReclassExpression)
        OutCon.save(outRasterPath+"\\"+LF_Type)
      if LF_Type == 'mfri':
        print "\t"*2+"Mean fire return interval >= 80 years"
        ReclassExpression = "VALUE >= 14 AND VALUE <= 22"
        OutCon = Con(NullRaster,2,1,ReclassExpression)
        OutCon.save(outRasterPath+"\\"+LF_Type+"080")
        print "\t"*2+"Mean fire return interval >= 150 years"
        ReclassExpression = "VALUE >= 18 AND VALUE <= 22"
        OutCon = Con(NullRaster,2,1,ReclassExpression)
        OutCon.save(outRasterPath+"\\"+LF_Type+"150")
      if LF_Type == 'pls':
        ReclassExpression = "VALUE IN (1,2)"
        OutCon = Con(NullRaster,2,1,ReclassExpression)
        OutCon.save(outRasterPath+"\\"+LF_Type)
      if LF_Type == 'prs':
        ReclassExpression = "VALUE >= 11 AND VALUE <= 20"
        OutCon = Con(NullRaster,2,1,ReclassExpression)
        OutCon.save(outRasterPath+"\\"+LF_Type)
      # Clean up
      arcpy.ResetEnvironments()
      del(NullRaster)
  arcpy.CheckInExtension("spatial")
#*** RUN TIME STATS ***********************************************************#
  me = os.path.splitext(os.path.basename(sys.argv[0]))[0]
  delta = time.clock()-timestamp
  if delta < 60:
    rdelta = round(delta,1)
    units = "seconds"
  elif delta >= 60 and delta < 3600:
    rdelta = round(delta / 60,2)
    units = "minutes"
  else:
    rdelta = round(delta / 3600,2)
    units = "hours"
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
  # generate a message string for any geoprocessing tool errors
  msgs = seperator + "\nGP ERRORS:\n" + arcpy.GetMessages(2)
  # return gp messages for use with a script tool
  arcpy.AddError(msgs)
  arcpy.AddError(pymsg)
  # print messages for use in Python/PythonWin
  print msgs
  print pymsg
  #*** RUN TIME STATS ***********************************************************#
  delta = time.clock()-timestamp
  if delta < 60:
    rdelta = round(delta,1)
    units = "seconds"
  elif delta >= 60 and delta < 3600:
    rdelta = round(delta / 60,2)
    units = "minutes"
  else:
    rdelta = round(delta / 3600,2)
    units = "hours"
  timestamp = time.clock()
  print "SCRIPT FAILED:\tElapsed time in " + units + ": " + str(rdelta)
  #Play wav file to let me know it has failed!
  file='Windows XP Error.wav'
  from winsound import PlaySound, SND_FILENAME, SND_ASYNC
  PlaySound(file, SND_FILENAME|SND_ASYNC)