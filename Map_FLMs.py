import copy_landfire, arcgisscripting
gp = arcgisscripting.create()



"""call the buildDirectories def from copy_landfire.py"""
copy_landfire.buildDirectories(1,2)
directories = copy_landfire.directories
print directories

###Create Duplicate Combo Grids
for d in directories:
    gp.workspace = d
    gp.toolbox = 'management'
    combo = d + '/combo'
    combo1 = d +'/combo1'
    combo2= d +'/combo2'
    combo3 = d +'/combo3'
    combo4 =d +'/combo4'
    combo5 = d +'/combo5'
    print 'creating duplicate combo grids 1-5'
##    gp.CopyRaster_management(combo, combo1)
##    gp.CopyRaster_management(combo, combo2)
##    gp.CopyRaster_management(combo, combo3)
##    gp.CopyRaster_management(combo, combo4)
##    gp.CopyRaster_management(combo, combo5)

###Set location of .dbf files
    ##one_dbf = d + '/one.xls'
    two_dbf = d + '/one.dbf'
    three_dbf = d + '/one.dbf'
    four_dbf = d + '/one.dbf'
    five_dbf = d + '/five.txt'
    oneFix_ = d
    try:
        gp.TableToDbase_conversion(five_dbf, oneFix)
    except:
    # If an error occurred print the message to the screen
        print gp.GetMessages()

###Joinitem database majority outfiles to grids
##    gp.toolbox = 'arc'
##    gp.joinitem = (combo1, one_tab, combo1, 'value')
    
###reset the directories list to null
d = []
