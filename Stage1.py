"""Created by Jason M. Herynk Systems for Environmental Management 20091230
Modified from a series of Eva Karau, Stacy Drury, and Jason Herynk amls dated from 2007.
This program compiles landfire data for FIREHARM processing.
1. Setup Global Variables
2. Copy Grids from server
3. Clip all grids to 3k boundary
4. Resample grids
5. Create a latitutde and longitude grid
6. Create the NFDR, DBH, BCF, LCR, Site Map, and RSHD grids
7. Create the LAI leaf area index grid
8. Delete ancilliary grids"""

"""Setup Global Variables"""
# Description: Copy raster to another format 

###-------------------------------------------------------------------------------
# Create the geoprocessing object
import os, arcgisscripting, string, shutil, tempfile, zipfile
gp = arcgisscripting.create()

# Set input raster workspace
gp.toolbox="management"

# Set location of LANDFIRE data.  These need to be changed/checked with every run.
workspace = 'c:/EMDS'
source1 = 'J:/fsfiles/fe/landfire'
zones = ['z06']
cellsize = '100'

# These are lists of grids used in processing below

bio = ['sand', 'silt', 'mxdepth', 'clay']
bases = ['3kgd']
fin_dels = ['asp','slp', 'flm','bps', 'cbd', 'cbh', 'cc', 'ch', 'dem', 'evt']
fuels = ['fbfm40']
treelists = ['tlg']
zipped = ['Grass', 'Trees']
nearest = ['sand', 'silt', 'mxdepth', 'clay', 'flm','bps', 'cbd', 'cbh', 'cc', 'ch', 'evt', 'fbfm40', 'dem', 'slp', 'asp', '3kgd']
clips = ['sand', 'silt', 'mxdepth', 'clay', 'flm','bps', 'cbd', 'cbh', 'cc', 'ch', 'evt', 'fbfm40', 'dem', 'slp', 'asp', 'tlg']
##bilinear = ['dem', 'slp', 'asp', '3kgd']
image = ['laif', 'laig']

###-------------------------------------------------------------------------------

##"""Copy grids from bases"""
##for zone in zones:
##    for b in bio:
##        print 'Copying %s_%s' %(zone, b)
##        copyfrom = source1 + '/%s/%s_bio/gis/%s_%s' %(zone, zone, zone, b)    
##        copyto = workspace +'/%s/%s_%s' %(zone, zone, b)
##
##        if gp.exists(copyto):
##            print '%s_%s Already exists' %(zone, b)
##        else:
##            gp.CopyRaster_management(copyfrom, copyto)    

for zone in zones:
    for b in bases:
        print 'Copying %s_%s' %(zone, b)
        copyfrom = source1 + '/%s/%s_base/gis/%s_%s' %(zone, zone, zone, b)    
        copyto = workspace +'/%s/%s_%s' %(zone, zone, b)

        if gp.exists(copyto):
            print '%s_%s Already exists' %(zone, b)
        else:
            gp.CopyRaster_management(copyfrom, copyto)
            
"""Copy fin_dels grids"""
for zone in zones:
    for fin_del in fin_dels:
        print 'Copying %s_%s' %(zone, fin_del)
        copyfrom = source1 +'/%s/fin_del/gis/%s_%s' %(zone, zone, fin_del)    
        copyto = workspace + '/%s/%s_%s' %(zone, zone, fin_del)

        if gp.exists(copyto):
            print '%s_%s Already exists' %(zone, fin_del)
        else:
            gp.CopyRaster_management(copyfrom, copyto)  

"""Copy Fuels"""
for zone in zones:
    for fuel in fuels:
        print 'Copying %s_%s' %(zone, fuel)
        copyfrom = source1 + '/%s/fin_del/gis/%s%s' %(zone, zone, fuel)    
        copyto = workspace + '/%s/%s_%s' %(zone, zone, fuel)

        if gp.exists(copyto):
            print '%s_%s Already exists' %(zone, fuel)
        else:
            gp.CopyRaster_management(copyfrom, copyto)

"""Copy Treelist"""
for zone in zones:
    for tree in treelists:
        print 'Copying %s_%s' %(zone, tree)
        copyfrom = 'k:/fe/fmi/fedat8/TLG/%s_%s' %(zone, tree)    
        copyto = workspace + '/%s/%s_%s' %(zone, zone, tree)

        if gp.exists(copyto):
            print '%s_%s Already exists' %(zone, tree)
        else:
            gp.CopyRaster_management(copyfrom, copyto)
"""Copy LAI"""
for zone in zones:
    for zippe in zipped:
        print 'Copying %s_%s' %(zone, zippe)
        grasslai = source1 + '/%s/%s_bio/gradient/%s%s_img/%sg_av_mxlaii.zip' %(zone, zone, zone, zippe, zone)
        forestlai = source1 + '/%s/%s_bio/gradient/%s%s_img/%sf_av_mxlaii.zip' %(zone, zone, zone, zippe, zone)
        glai = workspace + '/%s/%s_%s.zip' %(zone, zone, zippe)
        flai = workspace + '/%s/%s_%s.zip' %(zone, zone, zippe)
        if os.path.exists(glai):
            print 'GLAI already exists'
            ## zipfile extractall only works in newer versions of python    
####            try:
####                x = zipfile
####                x.extractall(glai)
####            except:
####                print 'no glai to unzip'
        else:
            if os.path.exists(grasslai):
                shutil.copy(grasslai, glai)
                print 'copying grass lai'
                
                
        if os.path.exists(flai):
            print 'FLAI Already Exists'
####            try:
####                x.extractall(flai)
####            except:
####                print 'no flai to unzip'
        else:
            if os.path.exists(forestlai):
                shutil.copy(forestlai, flai)
                print 'copying forest lai' 
#-------------------------------------------------------------------------------------
"""Pause here and unzip the zip files and rename them z##_laig.img, z##_laif.img"""
raw_input("Press ENTER after you have unzipped the z##_Grass, and z##_trees.zip files")
#-------------------------------------------------------------------------------------

"""Clip all grids to the 3kgd boundary before resampling"""
for zone in zones:
    for c in clips:
        try:
            print 'Clipping %s_%s' %(zone, c)
            kRaster = workspace + '/%s/%s_3kgd' %(zone, zone)
            InRaster = workspace + '/%s/%s_%s' %(zone, zone, c)
            OutRaster = workspace + '/%s/%s_%s_p' %(zone, zone, c)
            newname = workspace + '/%s/%s_3kgd_p' %(zone, zone)
            gp.CheckOutExtension("Spatial")
            gp.OverWriteOutput = 1 #Setting to 1 'true' will overwrite grids.  Setting to 0 will not
            gp.CopyRaster_management(kRaster, newname)
            gp.Con_sa(kRaster, InRaster, OutRaster, 1) ##Check value number in the 3kgd.  This changes occasionally from 1 to 2
             
        except:
            print gp.GetMessages()
            print 'Grid was not clipped to the 3k boundary'
        
#-------------------------------------------------------------------------------------
"""Resample either 100 or 1000 meters based on user input NEAREST"""
for zone in zones:
    for near in nearest:
        print 'Preparing to resample grid using nearest method %s_%s' %(zone, near)
        ##raw_input('Enter Resample Size:')
        method = 'NEAREST' ##raw_input('Enter Resampling algorithm to be used when resampling the raster NEAREST, BILINEAR, CUBIC, SEARCH:')
        grid = workspace + '/%s/%s_%s_p' %(zone, zone, near)
        resampled = workspace + '/%s/%sr' %(zone, near)

        if gp.exists(resampled):
            print '%s_%s Already has been resampled' %(zone, near)
        else:
            gp.Resample_management(grid, resampled, cellsize, method)

"""Resample to 100 for treelist"""
for zone in zones:
    for t in treelists:
        print 'Preparing to resample grid using nearest method %s_%s' %(zone, t)
        cellsize100 = '100' ##raw_input('Enter Resample Size:')
        
        method = 'NEAREST' ##raw_input('Enter Resampling algorithm to be used when resampling the raster NEAREST, BILINEAR, CUBIC, SEARCH:')
        grid = workspace + '/%s/%s_%s_p' %(zone, zone, t)
        resampled = workspace + '/%s/%sr' %(zone, t)
        
        if gp.exists(resampled):
            print '%s_%s Already has been resampled' %(zone, t)
        else:
            gp.Resample_management(grid, resampled, cellsize100, method)
            

"""Resample either 100 or 1000 meters based on user input Image"""
for zone in zones:
    for i in image:
        print 'Preparing to resample grid using nearest method %s_%s' %(zone, i)
        ##raw_input('Enter Resample Size:')
        method = 'NEAREST' ##raw_input('Enter Resampling algorithm to be used when resampling the raster NEAREST, BILINEAR, CUBIC, SEARCH:')
        grid = workspace +'/%s/%s_%s.img' %(zone, zone, i)
        resampled = workspace +'/%s/%s_%s_r.img' %(zone, zone, i)

        if gp.exists(resampled):
            print '%s_%s Already has been resampled' %(zone, i)
        else:
            gp.Resample_management(grid, resampled, cellsize, method)

###-------------------------------------------------------------------------------------
"""Create a latitude and longitude file for DAYMET weather referencing"""
for zone in zones:
    dem = workspace + '/%s/demr' %(zone)
    dempt = workspace + '/%s/%s_dempt_r.shp' %(zone, zone)
    latlon1 = workspace + '/%s/%s_latlon1.shp' %(zone, zone)
    latlon2 = workspace + '/%s/%s_latlon2.shp' %(zone, zone)
    cs = 'c:/Program Files/ArcGIS/Coordinate Systems/Geographic Coordinate Systems/North America/North American Datum 1927.prj'
    cs2 = 'c:/Program Files/ArcGIS/Coordinate Systems/Projected Coordinate Systems/Continental/North America/USA Contiguous Albers Equal Area Conic USGS.prj' 
    if gp.exists(dempt):
        print '%s_dempt_r Already exists' %(zone)
    else:
        gp.RasterToPoint_conversion(dem, dempt)
        gp.project(dempt, latlon1, cs, 'NAD_1927_TO_NAD_1983_NADCON') ##You may need to change this tranformation for Alaska and Hawaii
        gp.addxy(latlon1)
        gp.project(latlon1, latlon2, cs2, 'NAD_1927_TO_NAD_1983_NADCON')  
    try:
        lat_p1 = workspace + '/%s/%s_lat_p1' %(zone, zone)
        lon_p1 = workspace + '/%s/%s_lon_p1' %(zone, zone)
        lat_p2 = workspace + '/%s/%s_lat_p2' %(zone, zone)
        lon_p2 = workspace + '/%s/%s_lon_p2' %(zone, zone)
        lat_r = workspace + '/%s/latr' %(zone)
        lon_r = workspace + '/%s/lonr' %(zone)
        # Process: PointToRaster
        gp.PointToRaster_conversion(latlon2, "POINT_Y", lat_p1, "MOST_FREQUENT", "NONE", cellsize) #make sure you change this 1000 to 100 meters
        gp.PointToRaster_conversion(latlon2, "POINT_X", lon_p1, "MOST_FREQUENT", "NONE", cellsize)
        gp.CheckOutExtension("3d")
        gp.Times_3d(lat_p1, 1000000, lat_p2)
        gp.Times_3d(lon_p1, 1000000, lon_p2)
        gp.Int_3d(lat_p2, lat_r)
        gp.Int_3d(lon_p2, lon_r)
        gp.BuildRasterAttributeTable_management(lat_r, '#')
        gp.BuildRasterAttributeTable_management(lon_r, '#')
    except:
        # Print error message if an error occurs
        gp.GetMessages()
#-------------------------------------------------------------------------------------
"""Create the NFDR, DBH, BCF, LCR, Site Map, and RSHD grids. """
for zone in zones:
    
    # Set the input files
    lukup = workspace +'/%s/LookupTables' %(zone) #global
    # Rename fbfm40 and mxdepth
    oldfbfm40 = workspace + '/%s/fbfm40r' %(zone)
    newfbfm40 = workspace + '/%s/fbfmr' %(zone)
    gp.rename(oldfbfm40, newfbfm40)
    oldmxdepth = workspace + '/%s/mxdepthr' %(zone)
    newsdep = workspace + '/%s/sdepr' %(zone)
    gp.rename(oldmxdepth, newsdep)
    # Grids to copy
    FBFM40_r = workspace +'/%s/fbfmr' %(zone)
    ch_r = workspace +'/%s/chr' %(zone)
    evt_r = workspace +'/%s/evtr' %(zone)
    tlg_r = workspace +'/%s/tlgr' %(zone)
    kgd_r = workspace +'/%s/3kgdr' %(zone)
    bps_r = workspace +'/%s/bpsr' %(zone)
    # Grids to create p for prep
    nfdr_p = workspace +'/%s/%s_nfdr_p' %(zone, zone)
    dbh_p = workspace +'/%s/%s_dbh_p' %(zone, zone)
    bcf_p = workspace +'/%s/%s_bcf_p' %(zone, zone)
    lcr_p = workspace +'/%s/%s_lcr_p' %(zone, zone)
    rshd_p = workspace +'/%s/%s_rshd_p' %(zone, zone)
    site_p = workspace +'/%s/%s_site_p' %(zone, zone)
    # Grids to create p2 for prep
    site_p2 = workspace +'/%s/%s_site_p2' %(zone, zone)
    nfdr_p2 = workspace +'/%s/%s_nfdr_p2' %(zone, zone)
    dbh_p2 = workspace +'/%s/%s_dbh_p2' %(zone, zone)
    bcf_p2 = workspace +'/%s/%s_bcf_p2' %(zone, zone)
    lcr_p2 = workspace +'/%s/%s_lcr_p2' %(zone, zone)
    bcf_p3 = workspace +'/%s/%s_bcf_p3' %(zone, zone)
    lcr_p3 = workspace +'/%s/%s_lcr_p3' %(zone, zone)
    lcr_p4 = workspace +'/%s/%s_lcr_p4' %(zone, zone)
    #Grids to create r for resampled and reclassified
    nfdr_r = workspace +'/%s/nfdrr' %(zone)
    dbh_r = workspace +'/%s/dbhr' %(zone)
    bcf_r = workspace +'/%s/bcfr' %(zone)
    lcr_r = workspace +'/%s/lcrr' %(zone)
    rshd_r = workspace +'/%s/rshdr' %(zone)
    site_r = workspace +'/%s/siter' %(zone)
    # Location of DBF Lookup Tables
    nfdr_dbf = lukup + '/NFDR.dbf' #National Fire Danger Rating
    dbh_dbf = lukup + '/DBH.dbf' # Diameter at breast height
    bcf_dbf = lukup + '/BCF.dbf' # Bark Conversion Factor
    lcr_dbf = lukup + '/LCR.dbf' # Live Crown Ratio
    site_dbf = lukup + '/bps.dbf' # Site Map
    try:
        gp.OverWriteOutput = 1
        # Set the workspace
        gp.workspace = workspace +'/%s' %(zone)

        # Make copies
        gp.CopyRaster_management(FBFM40_r, nfdr_p)
        gp.CopyRaster_management(ch_r, dbh_p)
        gp.CopyRaster_management(evt_r, bcf_p)
        gp.CopyRaster_management(tlg_r, lcr_p)
        gp.CopyRaster_management(kgd_r, rshd_r) # all rshd values set to 1.
        gp.CopyRaster_management(bps_r, site_p)

        # Carefully process the 32 bit and novalue treelist
        gp.CheckOutExtension('Spatial')
        gp.IsNull_sa(lcr_p, lcr_p2)
        gp.Con_sa(lcr_p2, -9999, lcr_p3, lcr_p, "Value = 1")
        gp.BuildRasterAttributeTable_management(lcr_p3, '#')
        # Join DBF files to the copied rasters
        gp.joinfield(lcr_p3, 'VALUE', lcr_dbf, 'VALUE')
        gp.joinfield(nfdr_p, 'VALUE', nfdr_dbf, 'VALUE')
        gp.joinfield(dbh_p, 'Value', dbh_dbf, 'VALUE')
        gp.joinfield(bcf_p, 'VALUE', bcf_dbf, 'VALUE')
        gp.joinfield(site_p, 'VALUE', site_dbf, 'VALUE')

##        # reclass by the appropriate join field
        gp.CheckOutExtension("3d")
        gp.Lookup_3d(site_p, 'Site', site_p2)
        gp.Lookup_3d(nfdr_p, 'NFDR', nfdr_p2)
        gp.Lookup_3d(dbh_p, 'DBH', dbh_p2)
        gp.Lookup_3d(bcf_p, 'BCF', bcf_p2)
        gp.Lookup_3d(lcr_p3, 'RATIO2', lcr_p4)
        
        # Integerize a few of these grids
        gp.Int_3d(site_p2, site_r)
        gp.Int_3d(nfdr_p2, nfdr_r)
        gp.Int_3d(dbh_p2, dbh_r)
        gp.Times_3d(bcf_p2, 1000, bcf_p3)
        gp.Int_3d(bcf_p3, bcf_r)
        gp.Int_3d(lcr_p4, lcr_r)
    except:
        print gp.GetMessages()
        print 'Section 4'
#####-----------------------------------------------------------------------------------
"""Create the leaf area index grid.  LAI."""
for zone in zones:
    laif_r = workspace +'/%s/%s_laif_r.img' %(zone, zone)
    laift_p1 = workspace +'/%s/%s_laift_p1.img' %(zone, zone)    
    laift_p1g = workspace +'/%s/%s_laift_p1' %(zone, zone)
    laift_p2 = workspace +'/%s/%s_laift_p2' %(zone, zone)
    laift_r1 = workspace +'/%s/%s_laift_r1' %(zone, zone)
    laift_r2 = workspace +'/%s/lair' %(zone)
    outworkspace = workspace + '/%s' %(zone)

    if gp.exists(laift_r2):
        print '%s_laift_r Already exists' %(zone)
    else:
        # Set the input raster dataset

        # Process: Times
        # Check out ArcGIS 3D Analyst extension license
        
        gp.OverWriteOutput = 1
        gp.CheckOutExtension("3d")
        gp.Times_3d (laif_r, 0.000183113851036882, laift_p1)
        #print 'converted to real units'
        gp.RasterToOtherFormat_conversion(laift_p1, outworkspace, "GRID")
##        print 'converted to grid'
        gp.CheckOutExtension("Spatial")
        gp.Con_sa(laift_p1g, 0.000001, laift_p2, laift_p1g, 'Value == 0')
        gp.Times_3d(laift_p2, 1000000, laift_r1)
        gp.Int_3d(laift_r1, laift_r2)
        print 'con grid'
###----------------------------------------------------------------------------------    
##"""Delete Management"""
##for zone in zones:
##    for b in bases:
##        try:
##            grid = workspace +'/%s/%s_%s' %(zone, zone, b)
##            grid = workspace +'/%s/%s_%s_p' %(zone, zone, b)
##            gp.delete_management(grid)
##        except:
##            print 'didnot delete bases'
##    for f in fin_dels:
##        try:
##            grid = workspace +'/%s/%s_%s' %(zone, zone, f)
##            grid = workspace +'/%s/%s_%s_p' %(zone, zone, f)
##            gp.delete_management(grid)
##        except:
##            print 'didnot delete findels'
##    for f in fuels:
##        try:
##            grid = workspace +'/%s/%s_%s' %(zone, zone, f)
##            grid = workspace +'/%s/%s_%s_p' %(zone, zone, f)
##            gp.delete_management(grid)
##        except:
##            print 'didnot delete fuels'
##    for t in treelists:
##        try:
##            grid = workspace +'/%s/%s_%s' %(zone, zone, t)
##            grid = workspace +'/%s/%s_%s_p' %(zone, zone, t)
##            gp.delete_management(grid)
##        except:
##            print 'didnot delete treelists'


