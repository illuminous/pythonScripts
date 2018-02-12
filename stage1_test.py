"""Created by Jason M. Herynk Systems for Environmental Management 20100820
Modified from a series of Eva Karau, Stacy Drury, and Jason Herynk amls dated from 2007.
This program compiles landfire data for FIREHARM processing.
1. Setup Global Variables
2. Copy Grids from server
3. Clip all grids to 0k boundary
4. Resample grids
5. Create a latitutde and longitude grid
6. Create the NFDR, DBH, BCF, LCR, Site Map, and RSHD grids
7. Create the LAI leaf area index grid
8. Delete ancilliary grids"""

## Import Modules
import os
import arcgisscripting
import string
import shutil
import tempfile
import zipfile
import logging
import time
import datetime

## Create todays Date
today = datetime.date.today()
print "The date is", today

## Create geoprocessing object
gp = arcgisscripting.create()
gp.OverWriteOutput = 1 #1 overwrite, 0 don't overwrite

## Checkout an esri toolbox
gp.toolbox="management"

## Set location of LANDFIRE data.  These need to be changed/checked with every run.

ws_dm = 'G:/daymet_prep'
ws_event = 'G:/event_prep'
cellsize = '100'
eventflag = '1'
lukup = 'G:/LookupTables'
source1 = 'k:/lib/landfire/national'

## Start the logging file
logging.basicConfig(filename='G:/event_prep/%s.log' %(today), filemode='w', format='%(asctime)-6s: %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Stage I logger')
logger.setLevel(logging.INFO)
logger.info("***************************")

##############################
## These are lists of grids used in processing below

bio = ['sand', 'silt', 'mxdepth', 'clay']
bases = ['0kgd']
fin_dels = ['esp','asp','slp','bps', 'cbd', 'cbh', 'cc', 'ch', 'dem', 'evt']
fuels = ['fbfm40']
treelists = ['trlst']
flms = ['flm']
location = ['lat', 'lon']
trees = ['trees']
lai = ['lai']
treesimg = ['trees.img']
predictors = ['bcf', 'dbh', 'lcr', 'nfdr', 'rshd', 'site']
nearest = ['trlst','sand', 'silt', 'mxdepth', 'clay','bps', 'cbd', 'cbh', 'cc', 'ch',
           'evt', 'fbfm40', 'dem', 'slp', 'asp', 'flm', '0kgd'] 
clips = ['trlst','sand', 'silt', 'mxdepth', 'clay', 'bps', 'cbd', 'cbh', 'cc', 'ch',
         'evt', 'fbfm40', 'dem', 'slp', 'asp', 'flm', '0kgd']
fingrids = ['aspr',  'bpsr', 'cbdr', 'chr',  'clayr', 'demr',
            'evtr', 'fbfm40r', 'flmr', 'latr', 'lonr',
            'sandr', 'mxdepthr', 'siltr', 'slpr', 'trlstr', '0kgdr']
finpredictors = ['bcfr', 'dbhr', 'lair', 'nfdrr', 'rshdr', 'siter', 'lcrr']

logger.info("bio:")
logger.info(bio)
logger.info('bases:')
logger.info(bases)
logger.info('fin_dels:')
logger.info(fin_dels)
logger.info('fuels:')
logger.info(fuels)
logger.info('treelist format:')
logger.info(treelists)
logger.info('flms:')
logger.info(flms)
logger.info('nearest neighbor:')
logger.info(nearest)
logger.info('clips:')
logger.info(clips)
logger.info('fingrids:')
logger.info(fingrids)

image = ['laif']#, 'laig']

## setup empty lists for memory allocation
res = []
zones = []


"""Build a list of directories to copy grids from and to."""
def buildDirectories(zone_number_lower, zone_number_upper):
    print "Building Directories"
    logger.info("Building Directories")
    for zone in range(zone_number_lower, zone_number_upper):
        res.append(zone)
        logger.info('zone processing range is:')
        logger.info(zone_number_lower),logger.info(zone_number_upper)
        if zone < 10: #fix the formating if the zone number is less than 10
            path2 = 'z0%s' %(zone)
            zones.append(path2)
        else:
            path1 = 'z%s' %(zone)
            zones.append(path1)

def createFolders():
    print "Creating Folders"
    logger.info("Creating Folders")
    for z in zones:
        eventrootfolder = ws_event + '/' + z
        dmrootfolder = ws_dm + '/' + z  
        try:
            os.makedirs(eventrootfolder)
            os.makedirs(dmrootfolder)
            print eventrootfolder, 'created'
            print dmrootfolder, 'created'            
            logger.info('created')
            logger.info(eventrootfolder)
            logger.info(dmrootfolder)                        
        except:
            print eventrootfolder,'Directory Already Exists'
            print dmrootfolder,'Directory Already Exists'
            logger.info('EventMode Directory Already Exists')
            logger.info('DaymetMode Directory Already Exists')


def lookMissing():
    print "Looking for Missing Grids"
    logger.info("Looking for Missing Grids")
    for fin in fingrids: #loop over the final outputs to check if they are there
        eventgrid = ws_event + '/' + '%s' %(zone) + '/' +  fin          
        daymetgrid = ws_dm + '/' + '%s' %(zone) + '/' + fin 
        if gp.exists(eventgrid) == False:
            missing_event.append(fin[:-1])
            logger.warning("event grid doesnt exist")
            logger.warning(fin)
        else:
            logger.info('event grid exists')
            logger.info(fin)
        if gp.exists(daymetgrid) == False:
            missing_dm.append(fin[:-1])
            logger.warning("daymet grid doesnt exist")
            logger.warning(fin)
        else:
            logger.info('daymet grid exists')
            logger.info(fin)
    for finp in finpredictors: # append predictor grids to new missing list
        eventgridII = ws_event + '/' + '%s' %(zone) + '/' +  finp          
        daymetgridII = ws_dm + '/' + '%s' %(zone) + '/' + finp     
        if gp.exists(eventgridII) == False:
 
            missing_eventII.append(finp[:-1])
            logger.warning("eventII grid doesnt exist")
            logger.warning(finp)
        else:
            logger.info('event grid exists')
            logger.info(finp)
        if gp.exists(daymetgridII) == False:
            missing_dmII.append(finp[:-1])
            logger.warning("eventII grid doesnt exist")
            logger.warning(finp)
        else:
            logger.info('event grid exists')
            logger.info(finp)
    print "Missing Event Grids:", missing_event
    print "Missing EventII Grids:", missing_eventII
    print "Missing Daymet Grids:", missing_dm
    print "Missing DaymetII Grids:", missing_dmII
    
def mainEvent(zone):
    print "Starting Main Event Processing"
    logger.info("Starting Main Event Processing")
    ##for zone in zones:
    check0kgd = ws_event +'/'+'%s' %(zone) +'/'+'%s_0kgd' %(zone)
    print check0kgd
    if gp.exists(check0kgd): #check for the 0kgd, required for clipping
        pass
    else:
        copyBases(ws_event, zone, '0kgd')

    checkDEM = ws_event +'/%s' %(zone) +'/'+'%s_dem' %(zone)
    print 'checkDEM'
    if gp.exists(checkDEM): #check for the DEM, required for lat long shape
        pass
    else:
        copyBases(ws_event, zone, '0kgd') 

    for grid in missing_event:
        if grid in bio:
            copyBio(ws_event, zone, grid)
            clipGrids(ws_event, zone, grid)
            resampleGrids(ws_event, zone, grid, '100')
        if grid in fin_dels:
            copyFinDels(ws_event, zone, grid)
            clipGrids(ws_event, zone, grid)
            resampleGrids(ws_event, zone, grid, '100')
        if grid in fuels:
            copyFB40(ws_event, zone, grid)
            clipGrids(ws_event, zone, grid)
            resampleGrids(ws_event, zone, grid, '100')
        if grid in treelists:
            copyTLG(ws_event, zone, grid)
            clipGrids(ws_event, zone, grid)
            resampleGrids(ws_event, zone, grid, '100')
        if grid in flms:
            copyFLM(ws_event, zone, grid)
            clipGrids(ws_event, zone, grid)
            resampleGrids(ws_event, zone, grid, '100')
        if grid in location:
            latlongShp(ws_event, zone, '100')
        if grid in bases:
            clipGrids(ws_event, zone, grid)
            resampleGrids(ws_event, zone, grid, '100')
        else:
            pass
    for grid in missing_eventII:
        if grid in predictors:
            createGrids(ws_event, zone)                

        if grid in lai:
            copyLAI(ws_event, zone, trees[0])
            renameGrid(ws_event, zone, 'f_av_mxlaii.img', 'trees.img')
            clipGrids(ws_event, zone, trees[0])
            resampleGrids(ws_event, zone, trees[0], '100')
            createLAI(ws_event, zone)
        else:
            pass
def mainDaymet(zone):
    print "Starting Main Daymet Processing"
    logger.info("Starting Main Daymet Processing")
    ##for zone in zones:
    check0kgd = ws_dm +'/'+'%s' %(zone) +'/'+'%s_0kgd' %(zone)
    print check0kgd
    if gp.exists(check0kgd): #check for the 0kgd, required for clipping
        pass
    else:
        copyBases(ws_dm, zone, '0kgd')

    checkDEM = ws_dm +'/%s' %(zone) +'/'+'%s_dem' %(zone)
    print 'checkDEM'
    if gp.exists(checkDEM): #check for the DEM, required for lat long shape
        pass
    else:
        copyBases(ws_dm, zone, '0kgd') 

    for grid in missing_dm:
        if grid in bio:
            copyBio(ws_dm, zone, grid)
            clipGrids(ws_dm, zone, grid)
            resampleGrids(ws_dm, zone, grid, '1000')
        if grid in fin_dels:
            copyFinDels(ws_dm, zone, grid)
            clipGrids(ws_dm, zone, grid)
            resampleGrids(ws_dm, zone, grid, '1000')
        if grid in fuels:
            copyFB40(ws_dm, zone, grid)
            clipGrids(ws_dm, zone, grid)
            resampleGrids(ws_dm, zone, grid, '1000')
        if grid in treelists:
            print 'treelist section'
            copyTLG(ws_dm, zone, grid)
            clipGrids(ws_dm, zone, grid)
            resampleGrids(ws_dm, zone, grid, '1000')
        if grid in flms:
            copyFLM(ws_dm, zone, grid)
            clipGrids(ws_dm, zone, grid)
            resampleGrids(ws_dm, zone, grid, '1000')
        if grid in location:
            print 'lat long section'
            latlongShp(ws_dm, zone, '1000')
        if grid in bases:
            clipGrids(ws_dm, zone, grid)
            resampleGrids(ws_dm, zone, grid, '1000')
             
        else:
            pass
    for grid in missing_dmII:
        if grid in predictors:
            createGrids(ws_dm, zone)                

        if grid in lai:
            copyLAI(ws_dm, zone, trees[0])
            renameGrid(ws_dm, zone, 'f_av_mxlaii.img', 'trees.img')
            clipGrids(ws_dm, zone, trees[0])
            resampleGrids(ws_dm, zone, trees[0], '1000')
            createLAI(ws_dm, zone)
        else:
            pass
######################################################################################################
def copyBases(workspace, zone, grid):
    print "Copying Base Directory Grids"
    logger.info("Copying Base Directory Grids")
    print 'Copying %s_%s' %(zone, grid)
    copyfrom = source1 + '/%s/%s_base/gis/%s_%s' %(zone, zone, zone, grid)
    print copyfrom
    copyto = workspace +'/%s/%s_%s' %(zone, zone, grid)
    print copyto
    if gp.exists(copyto):
        print '%s_%s Already exists' %(zone, grid)
    else:
        gp.CopyRaster_management(copyfrom, copyto)
            

def copyBio(workspace, zone, grid):
    print "Copying Bio Directory Grids"
    logger.info("Copying Bio Directory Grids")
    print 'Copying %s_%s' %(zone, grid)
    logger.info('Copying %s_%s' %(zone, grid))
    copyfrom = source1 + '/%s/%s_bio/gis/%s_%s' %(zone, zone, zone, grid)
    logger.info('Copying from:')
    logger.info(copyfrom)
    copyto = workspace +'/%s/%s_%s' %(zone, zone, grid)
    logger.info(copyto)
    logger.info('Coying to:')
    if gp.exists(copyto):
        print '%s_%s Already exists' %(zone, grid)
    else:
        gp.CopyRaster_management(copyfrom, copyto)  


def clipGrids(workspace, zone, grid):
    """Clip all grids to the 0kgd boundary before resampling.  This was switched from the 3kgd because the 3k boundary would result in -9999 dem, aspect,
    slope when resampled.  This would also cause 0 values for the longitude field in the poly combine files produced in stage 3 and in the z##poly#.in files created in
    stage 4.  Using the 0kgd will also reduce the amount of area we need to run because there will
    not be overlap between zones."""
    try:
        print 'Clipping %s_%s' %(zone, grid)
        logger.info("Clipping %s_%s" %(zone, grid))
        kRaster = workspace + '/%s/%s_0kgd' %(zone, zone)
        InRaster = workspace + '/%s/%s_%s' %(zone, zone, grid)
        OutRaster = workspace + '/%s/%s_%s_p' %(zone, zone, grid)
        newname = workspace + '/%s/%s_0kgd_p' %(zone, zone)
        if gp.exists(OutRaster): print OutRaster, 'Already exists'
        else:
            gp.CheckOutExtension("Spatial")
            gp.Con_sa(kRaster, InRaster, OutRaster, 1) ##Check value number in the 3kgd.  This changes occasionally from 1 to 2         
    except:
        print gp.GetMessages()
        print 'Grid was not clipped to the 3k boundary'


def resampleGrids(workspace, zone, grid, cellsize):
    """Resample first to 100 then to 1000 meters based on user input NEAREST"""

    print 'Preparing to resample grid using nearest method %s_%s' %(zone, grid)
    logger.info('Preparing to resample grid using nearest method %s_%s' %(zone, grid))
    method = 'NEAREST' ##raw_input('Enter Resampling algorithm to be used when resampling the raster NEAREST, BILINEAR, CUBIC, SEARCH:')
    clipgrid = workspace + '/%s/%s_%s_p' %(zone, zone, grid)
    resampled = workspace + '/%s/%sr' %(zone, grid)
    
    if gp.exists(resampled):
        print '%s_%s Already has been resampled' %(zone, grid)
    else:
        gp.Resample_management(clipgrid, resampled, cellsize, method)

        
def copyFinDels(workspace, zone, grid):
    print 'Copying %s_%s' %(zone, grid)
    logger.info('Copying %s_%s' %(zone, grid))
    copyfrom = source1 + '/%s/fin_del/gis/%s_%s' %(zone, zone, grid)    
    copyto = workspace +'/%s/%s_%s' %(zone, zone, grid)
    if gp.exists(copyto):
        print '%s_%s Already exists' %(zone, grid)
    else:
        gp.CopyRaster_management(copyfrom, copyto)


def copyFB40(workspace, zone, grid):
    print 'Copying %s_%s' %(zone, grid)
    logger.info('Copying %s_%s' %(zone, grid))
    copyfrom = source1 + '/%s/fin_del/gis/%s%s' %(zone, zone, grid)    
    copyto = workspace + '/%s/%s_%s' %(zone, zone, grid)
    if gp.exists(copyto):
        print '%s_%s Already exists' %(zone, grid)
    else:
        gp.CopyRaster_management(copyfrom, copyto)


def copyTLG(workspace, zone, grid):
    print 'Copying %s_%s' %(zone, grid)
    logger.info('Copying %s_%s' %(zone, grid))
    copyfrom = 'G:/Treelists/%s_trlst/%s_trlst' %(zone, zone)    
    copyto = workspace + '/%s/%s_%s' %(zone, zone, grid)
    if gp.exists(copyto):
        print '%s_%s Already exists' %(zone, grid)
    else:
        
        gp.CopyRaster_management(copyfrom, copyto)
                

def copyFLM(workspace, zone, grid):
    print 'Copying %s_%s' %(zone, grid)
    logger.info('Copying %s_%s' %(zone, grid))
    copyfrom = 'G:/LF_national/FLMs/%s/%s_%s' %(zone, zone, grid)    
    copyto = workspace + '/%s/%s_%s' %(zone, zone, grid)
    copyfromII = 'k:/lib/landfire/national/%s/fin_del/gis/%s_%s' %(zone, zone, grid)

    if gp.exists(copyto):
        print '%s_%s Already exists' %(zone, grid)
    else:
        try:
            gp.CopyRaster_management(copyfrom, copyto)
        except:
            gp.CopyRaster_management(copyfromII, copyto)


def copyLAI(workspace, zone, grid):
    """Copy LAI"""
    print 'Copying %s_%s' %(zone, grid)
    logger.info('Copying %s_%s' %(zone, grid))
    ##grasslai = source1 + '/%s/%s_bio/gradient/%s%s_img/%sg_av_mxlaii.zip' %(zone, zone, zone, grid, zone)
    forestlai = source1 + '/%s/%s_bio/gradient/%s%s_img/%sf_av_mxlaii.zip' %(zone, zone, zone, grid, zone)
    ##glai = workspace + '/%s/%s_%s.zip' %(zone, zone, grid)
    flai = workspace + '/%s/%s_%s.zip' %(zone, zone, grid)
    if os.path.exists(flai):
        print 'FLAI Already Exists'
##        try:
##            x.extractall(flai)
##        except:
##            print 'no flai to unzip'
    else:
        if os.path.exists(forestlai):
            shutil.copy(forestlai, flai)
            print 'copying forest lai' 


def latlongShp(workspace, zone, cellsize):
    """Create a latitude and longitude file for DAYMET weather referencing"""
    print "Create Latitude and Longitude Reference:"
    logger.info("Create Latitude and Longitude Reference:")
    dem = workspace + '/%s/demr' %(zone) #change back to dem for daymet mode
    gp.extent = dem 
    dempt = workspace + '/%s/%s_dempt_r.shp' %(zone, zone)
    latlon1 = workspace + '/%s/%s_latlon1.shp' %(zone, zone)
    latlon2 = workspace + '/%s/%s_latlon2.shp' %(zone, zone)
    #cs = 'c:/Program Files/ArcGIS/Coordinate Systems/Geographic Coordinate Systems/North America/North American Datum 1927.prj'
    cs = 'c:/Program Files/ArcGIS/Coordinate Systems/Geographic Coordinate Systems/North America/North American Datum 1983.prj'
    cs2 = 'c:/Program Files/ArcGIS/Coordinate Systems/Projected Coordinate Systems/Continental/North America/USA Contiguous Albers Equal Area Conic USGS.prj'

    try:
        gp.RasterToPoint_conversion(dem, dempt)
        gp.project(dempt, latlon1, cs)#'NAD_1927_TO_NAD_1983_NADCON') ##You may need to change this tranformation for Alaska and Hawaii
        gp.addxy(latlon1)
        gp.project(latlon1, latlon2, cs2)#'NAD_1927_TO_NAD_1983_NADCON')         
        lat_p1 = workspace + '/%s/%s_lat_p1' %(zone, zone)
        lon_p1 = workspace + '/%s/%s_lon_p1' %(zone, zone)
        lat_p2 = workspace + '/%s/%s_lat_p2' %(zone, zone)
        lon_p2 = workspace + '/%s/%s_lon_p2' %(zone, zone)
        lat_r = workspace + '/%s/latr' %(zone)
        lon_r = workspace + '/%s/lonr' %(zone)
        ##gp.delete_management(lat_r, lon_r)
        ##gp.delete_management(lat_p1, lon_p1, lat_p2, lon_p2, lat_r, lon_r)

        # Process: PointToRaster
        print 'made it here'
        gp.PointToRaster_conversion(latlon2, "POINT_Y", lat_p1, "MOST_FREQUENT", "NONE", cellsize) #make sure you change this 1000 to 100 meters
        gp.PointToRaster_conversion(latlon2, "POINT_X", lon_p1, "MOST_FREQUENT", "NONE", cellsize)
        gp.CheckOutExtension("3d")
        gp.Times_3d(lat_p1, 1000000, lat_p2)
        gp.Times_3d(lon_p1, 1000000, lon_p2)
        gp.Int_3d(lat_p2, lat_r)
        gp.Int_3d(lon_p2, lon_r)
    except:
        pass


def createGrids(workspace, zone):
    """Create the NFDR, DBH, BCF, LCR, Site Map, and RSHD grids. """
    print "Creating Predictor Grids:"
    logger.info("Creating Predictor Grids:")
    for zone in zones:

        # Grids to copy
        FBFM40_r = workspace +'/%s/fbfm40r' %(zone)
        ch_r = workspace +'/%s/chr' %(zone)
        evt_r = workspace +'/%s/evtr' %(zone)
        tlg_r = workspace +'/%s/trlstr' %(zone) #change back to trlstr
        kgd_r = workspace +'/%s/0kgdr' %(zone) #change back to 0kgdr for daymet mode
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
            # Set the workspace
            gp.workspace = workspace +'/%s' %(zone)
##            gp.delete_management(nfdr_p)
##            gp.delete_management(dbh_p)
##            gp.delete_management(bcf_p)
##           ## gp.delete_management(lcr_p)
##            gp.delete_management(rshd_p)
##            gp.delete_management(site_p)
##
##            gp.delete_management(site_p2)
##            gp.delete_management(nfdr_p2)
##            gp.delete_management(dbh_p2)
##            gp.delete_management(bcf_p2)
##           ## gp.delete_management(lcr_p2)            
##            gp.delete_management(bcf_p3)
##            gp.delete_management(lcr_p3)
##            gp.delete_management(lcr_p4)
##
##            gp.delete_management(nfdr_r)
##            gp.delete_management(dbh_r)
##            gp.delete_management(bcf_r)
##           ## gp.delete_management(lcr_r)
##            gp.delete_management(rshd_r)
##            gp.delete_management(site_r)
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


def createLAI(workspace, zone):
    """Create the leaf area index grid.  LAI."""
    laif_r = workspace +'/%s/treesr' %(zone) #change back to no 1 for daymet
    laift_p1 = workspace +'/%s/%s_laift_p1' %(zone, zone)    
    ##laift_p1g = workspace +'/%s/%s_laift_p1' %(zone, zone)
    laift_p2 = workspace +'/%s/%s_laift_p2' %(zone, zone)
    laift_r1 = workspace +'/%s/%s_laift_r1' %(zone, zone)
    laift_r2 = workspace +'/%s/lair' %(zone)
    outworkspace = workspace + '/%s' %(zone)

    if gp.exists(laift_r2):
        print '%s_laift_r Already exists' %(zone)
    else:
        try:
            gp.CheckOutExtension("3d")
            gp.Times_3d (laif_r, 0.000183113851036882, laift_p1)
            
            ##gp.RasterToOtherFormat_conversion(laift_p1, outworkspace, "GRID")
            
            gp.CheckOutExtension("Spatial")
            gp.Con_sa(laift_p1, 0.000001, laift_p2, laift_p1, 'Value == 0')
            gp.Times_3d(laift_p2, 1000000, laift_r1)
            gp.Int_3d(laift_r1, laift_r2)
            print 'con grid'
        except:
            pass


def renameGrid(workspace, zone, inGrid, outGrid):
    laiImage = workspace+'/%s/%s' %(zone, zone)+ inGrid
    outworkspace = workspace+'/%s' %(zone)

    laiTrees = workspace+'/%s/%s_'%(zone, zone) +outGrid
    print laiImage, laiTrees
    try:
        gp.rename(laiImage, laiTrees)
        gp.RasterToOtherFormat_conversion(laiTrees, outworkspace, "GRID")
    except:pass
    
buildDirectories(36,37)
##zones.remove('z27')
##zones.remove('z28')
##zones.remove('z29')
##zones.remove('z30')
##zones.remove('z31')
##zones.remove('z36')
##zones.remove('z37')

for zone in zones:
    createFolders()
for zone in zones:
    print zone
    missing_event = [] #create the lists
    missing_dm = []
    missing_eventII = []
    missing_dmII = []
    lookMissing()
    mainEvent(zone)
    mainDaymet(zone)


