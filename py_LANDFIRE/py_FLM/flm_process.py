# Fuel Loading Model Production
#Step 1. combine raster data

# Import system modules
import arcgisscripting, time, os.path, os

# Create the Geoprocessor object
gp = arcgisscripting.create(9.3)
############################################################
#globals
############################################################
dirname = 'c:/tmp'
"""Set the dirname variable to your local workspace 'c:/tmp'.  Subdirectories will be created for
each zone."""

base = 'J:/fsfiles/fe/landfire'
"""Set the base variable to the location of the LANDFIRE source data.  'J:/fsfiles/fe/landfire'"""

sub = '/fin_del/gis'
sub2 = '_base/gis'
"""sub is a file extension"""

zones = ['42']#, '43', '44', '45', '36', '35', '32', '26', '34', '27', '33', '38', '31', '39', '40','30', '29', '25']
"""create a list of zones that you would like to include"""

products = ['evt', 'evc', 'evh', '3kgd']
"""create a list of products for each zone that you would like to include"""

combos = ['one', 'two', 'three', 'four', 'five']



##class FLM:
##    def __init__(self, dirname, base, sub):
##        self.dirname = dirname
##        self.base = base
##        self.sub = sub
##    def info(self):
##        return(sel.dirname, self.base, self.sub)
        
####    def makedirectory(self):
##for zone in zones:
##    path = dirname+'/z%s' %(zone)
##    if os.path.exists(path):
##        print "\n folder exists\n"
##        print path
##    else:
##        os.makedirs(path)
##        print "\n making new directory \n"
##        print path
####
######    def copyraster(self):
for zone in zones:
    for p in products:
        print zone , p
        try:
            # Set input raster workspace
            workspace = base + '/z%s' %(zone) + sub
            gp.workspace = workspace
            grid = '/z%s_%s' %(zone, p)
            inraster = gp.workspace + grid
            outraster = dirname + '/z%s' %(zone) + grid
            
            gp.toolbox="management"

            # Copy Redlands.tif to output ArcSDE workspace with configuration keyword RASTER
            gp.CopyRaster_management(inraster, outraster)
            #########
        except:
            # If an error occurred while running a tool, then print the messages.
            print gp.GetMessages()
#### def copy3kgrd            
for zone in zones:
    for p in products:
        print zone , p
        try:
            workspace2 = base + '/z%s' %(zone) +'/z%s' %(zone) + sub2
            gp.workspace = workspace2
            grid2 = '/z%s_%s' %(zone, p)
            inraster2 = gp.workspace + grid2
            outraster2 = dirname + '/z%s' %(zone) + grid2
            
            gp.toolbox="management"

            # Copy Redlands.tif to output ArcSDE workspace with configuration keyword RASTER
            gp.CopyRaster_management(inraster2, outraster2)
            

        except:
            # If an error occurred while running a tool, then print the messages.
            print gp.GetMessages()

####    def combine(self):
for zone in zones:
    try:
        grid = '/z%s' %(zone)
        gp.workspace = dirname + grid
        rasters = gp.ListRasters('*', 'GRID')
        # Create the multivalue string for the Analysis Union tool
        inputs = ""
        # For each feature class in the list, append it to the variable inputs
        #
        for ras in rasters:
                inputs += ras + ";"
        
        outraster = dirname + '/z%s' %(zone) + grid + '_combo' 
        # Check out Spatial Analyst extension license
        gp.CheckOutExtension("Spatial")

        gp.Combine_sa(inputs, outraster)

    except:
            # If an error occurred while running a tool, then print the messages.
            print gp.GetMessages()

##for zone in zones:
##    for c in combos:
##        try:
            


##
##    def exporttables(self):
##for zone in zones:
##    try:
##        # Set the workspace, then export list of SDE table
##        grid = '/z%s' %(zone)
##        gp.Workspace = dirname + grid
##
##        rasters = gp.ListRasters('*', 'GRID')
##        inputs = dirname + '/z%s' %(zone)+'/z%s_combo' %(zone)
##        
####        for ras in rasters:
####            if ras == dirname + '/z%s' %(zone)+'/z%s_combo' %(zone):
####                inputs += ras + ";"
##
##        outraster = dirname + '/z%s' %(zone) + grid +'_combo'
##        gp.TableToDbase_conversion(inputs+'.tab', outraster+'.dbf')
##
##    except:
##        # If an error occurred print the message to the screen
##        print gp.GetMessages()
##
### Get a list of grids in the workspace.
###
####rasters = gp.ListRasters("*", "GRID")
##
##for raster in rasters:
##    print raster


##products = ['evt', 'evc', 'evh']

##from time import clock
##start = time.clock()
##def FLMList(
##res = []
##for zone in zones:
##    for p in products:
##        print zone , p    
##        try:
##            # Set local variables
##            outRaster = "C:/working/FLM/c08/combo%s" %(zone)
##            I = "C:/working/FLM/c08/d_z%s_%s08/z%s_%s08" %(zone, p, zone, p)
##            res.append(I)
##            print 'Result is: '
##            print res
##            evt1 = res[0]
##            evc1 = res[1]
##            evh1 = res[2]
##            combo = 
##            zone2 = res[3:6]
##            zone3 = res[6:9]
##            zone4 = res[9:12]
##            zone5 = res[12:15]
##            zone6 = res[15:18]
##            zone7 = res[18:21]
                
            # Check out Spatial Analyst extension license
##            gp.CheckOutExtension("Spatial")
##
##            # Process: Combine...
##            gp.Combine_sa("zone1[0], zone1[1], zone", outRaster)

##        except:
##            # If an error occurred while running a tool, then print the messages.
##            print gp.GetMessages()
##
##elapsed = (time.clock()- start)
##print 'Commutation time is:'
##print elapsed
