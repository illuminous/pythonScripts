import os
import arcpy
from arcpy import env

class SetUp:
    """Initialize the source directory, and local directory variables.  Create two dictionaries to hold a range
    and zone results"""
    def __init__(self, sourcedir, localdir):
        self.sourcedir = sourcedir
        self.localdir = localdir
        self.res = res=[]
        self.zones = zones=[]
        self.rasters = rasters=[]
        
    def buildZonelist(self, zone_number_lower, zone_number_upper):
        """Build a list of directories to copy grids from and to."""
        for zone in range(zone_number_lower, zone_number_upper):
            self.res.append(zone)
            if zone < 10: #fix the formating if the zone number is less than 10
                path2 = 'z0%s' %(zone)
                self.zones.append(path2)
            else:
                path1 = 'z%s' %(zone)
                self.zones.append(path1)

    def createFolders(self, directory):
        """Creates the directory structure."""
        for z in self.zones:
            try:
                os.makedirs(directory+'/%s' %(z))
            except:
                print 'Directory already exists'

    def listRasters(self,directory, wildcard, raster_type):
        """List the esri raster items in a directory"""
        env.workspace = directory
        rasterList = arcpy.ListRasters(wildcard, raster_type)
        for dataset in rasterList:
            self.rasters.append(str(dataset))

    def copyRasters(self, directory):
        """Copy esri items to a directory"""
        env.workspace = directory
        arcpy.Copy_management(in_data, out_data, data_type)
        
    
if __name__ == '__main__':
    """Runs the main program"""
    print 'start'
    lf = SetUp('K:/lib/landfire/national', 'c:/tmp/lolipop2')
    lf.buildZonelist(1,15)
    lf.createFolders(lf.localdir)
    print 'stop'
    for z in lf.zones:
        lf.listRasters(lf.sourcedir+'/%s/fin_del/gis'%(z), "*", "GRID")
        for item in lf.rasters:
            print item

    allgrids = []
