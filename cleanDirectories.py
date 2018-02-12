import os
import arcgisscripting
gp = arcgisscripting.create()

# Set input raster workspace
gp.toolbox="management"
workspace = 'J:/event_prep'
zones = ['z01', 'z02', 'z03', 'z04', 'z05', 'z06', 'z07', 'z24','z25', 'z31', 'z38', 'z39', 'z40', 'z43','z15','z36','z37', 'z42','z41','z44','z49','z50','z51', 'z56', 'z55','z98','z99', 'z46', 'z45','z48','z54', 'z58', 'z59',
         'z57','z53', 'z47', 'z52','z62','z61', 'z60', 'z63','z64','z65', 'z66'] # removed 33, 32, 34, 35, 26 because of missing treelist
bases = ['aspr','bcfr', 'c', 'cbdr', 'chr', 'clayr', 'dbhr', 'demr','evtr',
         'fbfmr', 'flmr', 'lair', 'latr', 'lcrr', 'lonr', 'nfdrr', 'pol', 'polw',
         'polx', 'polz', 'rshdr', 'sandr', 'sdepr', 'siltr', 'siter', 'slpr',
         'tlgr']

res = []
chunks = []

"""Build a list of directories to copy grids from and to."""
def buildDirectories(zone_number_lower, zone_number_upper):
    for zone in range(zone_number_lower, zone_number_upper):
        if zone < 10: #fix the formating if the zone number is less than 10
            path2 = 'z0%s' %(zone)
            path = path2
            res.append(path)
        else:
            path2 = 'z%s' %(zone)
            path = path2
            res.append(path)

    print res


"""Build a list of directories to copy grids from and to."""
def buildChunks(zone_number_lower, zone_number_upper):
    for zone in range(zone_number_lower, zone_number_upper):
        chunks.append(zone)
    print chunks


    return directories
def deleteGrids():
    """Delete Management"""
    for r in res:
        print r
        for b in bases:
            for chunk in chunks:
                try:
                    grid = workspace +'/%s/%s%s' %(r, b, chunk)
                    
                    gp.delete_management(grid)
                except:
                    print 'didnot delete %s' %(chunk)

buildChunks(1,21)
buildDirectories(1,100)
