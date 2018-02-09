# ---------------------------------------------------------------------------
# Make_New_CMBRF.py
# Created on: Thu Jul 20 2006 11:21:27 AM
# ---------------------------------------------------------------------------

# Import system modules
import sys, string, os, win32com.client

# Create the Geoprocessor object
gp = win32com.client.Dispatch("esriGeoprocessing.GpDispatch.1")
# Load required toolboxes...
gp.AddToolbox("C:/Program Files/ArcGIS/ArcToolbox/Toolboxes/Conversion Tools.tbx")

# helper processes
def AddPrintMessage(msg, severity):
    if severity == 0:
        gp.AddMessage(msg)
        print "message: " + msg
    elif severity == 1:
        gp.AddWarning(msg)
        print "Warning: " + msg
    elif severity == 2:
        gp.AddError(msg)
        print "ERROR: " + msg

# Write Aml file
def WriteAmlLine (amlLine):
    amlFile = "E:\\WorkSpace2\\Make_New_FBFM40.aml"
    try:
        fileWrangler = open(amlFile, "a")
        fileWrangler.write(amlLine + " \n")
        fileWrangler.close()
    except:
       AddPrintMessage("-error creating Make_New_FBFM40 aml", 2)
       raise exception

def WriteAmlFile():
    WriteAmlLine("/* Set workspace, convert dbase to info tab, join tab to fuel, create FBFM40")
    WriteAmlLine("&echo &off ")
    WriteAmlLine("w E:\WorkSpace2 ")
    WriteAmlLine("&sv num = 1 ")
    WriteAmlLine("&do &while [exists %num%FBFM40 -grid] ")
    WriteAmlLine("  &sv num = %num% + 1 ")
    WriteAmlLine("&end ")
    WriteAmlLine("dbaseinfo Final.dbf %num%FBFM40.tab define ")
    WriteAmlLine("fbfm13 fbfm13 10 10 i ")
    WriteAmlLine("fbfm40 fbfm40 10 10 i ")
    WriteAmlLine("canopy canopy 10 10 i ")
    WriteAmlLine("cbh13mx10 cbh13mx10 10 10 i ")
    WriteAmlLine("cbh40mx10 cbh40mx10 10 10 i ")
    WriteAmlLine("end")
    WriteAmlLine("dropitem CMBRF.vat CMBRF.vat fbfm13 fbfm40 cbh13mx10 cbh40mx10 canopy")
    WriteAmlLine("joinitem CMBRF.vat %num%FBFM40.tab CMBRF.vat value")
    WriteAmlLine("GRID")
    WriteAmlLine("  %num%FBFM40 = cmbrf.FBFM40")
    WriteAmlLine("q")
    WriteAmlLine("joinitem %num%FBFM40.vat FBFM40COLOR.TAB %num%FBFM40.vat value")
    WriteAmlLine("/* EOF" )

# main process:
try:
    print " "
    AddPrintMessage("PROGRAM START", 0)
    # Play Jeopardy wav file.
    file = "thinkmusic.wav"
    winsound.PlaySound(file, winsound.SND_FILENAME|winsound.SND_ASYNC)
    # Local variables...
    Final_Table = "E:\\WorkSpace2\\Workshop_Prog.mdb\\Final_Table"
    Final_dbf = "E:\\WorkSpace2\\Final.dbf"
    Workshop_Prog = "E:\\WorkSpace2\\"
    # clean-up messes
    AddPrintMessage("-prepwork & cleaning up", 0)
    # makes sure E:\WorkSpace2 exists
    if not gp.exists("E:\\WorkSpace2"):
        AddPrintMessage("-WorkSpace2 does not exist", 2)
    # Delete aml if it already exists
    if gp.Exists("E:\\WorkSpace2\\Make_New_FBFM40.aml"):
        os.remove("E:\\WorkSpace2\\Make_New_FBFM40.aml")    
    # Delete Database file Final.dbf if it exists
    if gp.Exists("E:\\WorkSpace2\\Final.dbf"):
        os.remove("E:\\WorkSpace2\\Final.dbf")
    # Process: Table To Table...
    AddPrintMessage("-creating new table", 0)
    gp.TableToTable_conversion(Final_Table, Workshop_Prog, "Final.dbf", "", "VALUE VALUE VISIBLE;EVTR EVTR VISIBLE;FBFM13 FBFM13 VISIBLE;FBFM40 FBFM40 VISIBLE;Canopy Canopy VISIBLE;CBH13mx10 CBH13mx10 VISIBLE;CBH40mx10 CBH40mx10 VISIBLE", "")
    # creating AML
    AddPrintMessage("-creating Make_New_FBFM40 AML", 0)
    WriteAmlFile()
    # running AML
    AddPrintMessage("-running Make_New_FBFM40 AML", 0)
    os.system('arc \"&run E:\\WorkSpace2\\Make_New_FBFM40.aml"')
    # removing AML
    AddPrintMessage("-removing table Make_New_FBFM40 AML", 0)
    os.remove("E:\\WorkSpace2\\Make_New_FBFM40.aml")
    # Delete Database file Final.dbf
    AddPrintMessage("-removing dbase file final.dbf", 0)
    os.remove("E:\\WorkSpace2\\Final.dbf")
    # Done
    AddPrintMessage("PROGRAM COMPLETE", 0)
    #raw_input ("Press enter to continue...")

# error handler
except:
    AddPrintMessage("PROGRAM FAILURE", 2)
    err = gp.GetMessages()
    AddPrintMessage(err, 2)
    #raw_input ("Press enter to continue...")

#EOF
