# Name: MakeRouteEventLayer_Example2.py
# Description:  Make a LINE event layer. Routes and events are in a file geodatabase.
# An error field is added to the new layer. The new layer can be used by other 
# geoprocessing functions.
# Author: ESRI

# Import system modules 
import arcpy
from arcpy import env

# Set workspace
env.workspace = "E:/GIS/projects/LinearReferencing/2018/linearReferencing_Active_Leases_2018.gdb"

# Set local variables
switch = 'From' #Enter 'From' or 'To'
rt = "MP_Feet_Sub_Mod_CreateRoutes"          # based on the historic mileposts
rid = "VLOOKUP" 
tbl = "py_Values"
props = "Vlookup%s POINT MP_Pt_%s" %(switch, switch) 
lyr = "route_events" 

# Execute MakeRouteEventLayer
arcpy.MakeRouteEventLayer_lr (rt, rid, tbl, props, lyr, "#",  "ERROR_FIELD")

##output a layer file
#arcpy.SaveToLayerFile_management("route_events", "c:/working/GIS/linearReferencing/bla.lyr", "ABSOLUTE")

##output to shapefile
arcpy.CopyFeatures_management("route_events", "E:/GIS/projects/LinearReferencing/2018/linearReferencing_Active_Leases_2018.gdb/activeLeases_MP_%s" %(switch))
