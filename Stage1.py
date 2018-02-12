#!c:/python26/ArcGis10.0/python -u
"""
Created by Jason M. Herynk Systems for Environmental Management 20091230
Modified from a series of Eva Karau, Stacy Drury, and Jason Herynk amls dated from 2007.
This program compiles landfire data for FIREHARM processing.
1. Setup Global Variables
2. Copy Grids from server
3. Clip all grids to 3k boundary
4. Resample grids
5. Create a latitutde and longitude grid
6. Create the NFDR, DBH, BCF, LCR, Site Map, and RSHD grids
7. Create the LAI leaf area index grid
8. Delete ancilliary grids

$Id: Stage1.py 32 2013-03-03 00:06:25Z cwinne $
$URL: svn://refresh.dyndns-free.com/fireharm/trunk/progs/Stage1.py $

"""

"""Setup Global Variables"""
# Description: Copy raster to another format 

###-------------------------------------------------------------------------------
# Create the geoprocessing object
import os, sys
import time
import logging

start = time.time()

import arcgisscripting
gp = arcgisscripting.create()
gp.toolbox="management"
gp.CheckOutExtension("Spatial")
gp.OverWriteOutput = 0
gp.pyramid = "PYRAMIDS 0 NEAREST"

#####################################################
# The following assumes the user is starting in the zone directory
#   only the single zone is processed.
workspace, zone = os.path.split(os.getcwd().replace('\\','/'))
zones = [zone][:3]
# source1 = "g:"
source1 = "f:/landfire"
biosource = "f:/landfire/bio"
mask = '/'.join([workspace, zone, "gis/input/m3kgd"])

# These are lists of grids used in processing below

bio = ['sand', 'silt', 'mxdepth', 'clay']
bases = ['3kgd']
fin_dels = ['asp','slp', 'flm','bps', 'cbd', 'cbh', 'cc', 'ch', 'dem', 'evt']
fuels = ['fbfm40']
# treelists = ['tlg']  # --- old option ---
treelists = ['trlst']
#zipped = ['Grass', 'Trees']
zipped = ['Trees']
nearest = ['sand', 'silt', 'mxdepth', 'clay', 'flm','bps', 'cbd', 'cbh', 'cc', 'ch', 'evt', 'fbfm40', 'dem', 'slp', 'asp', 'tlg', mask]
#nearest = ['sand', 'silt', 'mxdepth', 'clay', 'flm','bps', 'cbd', 'cbh', 'cc', 'ch', 'evt', 'fbfm40', 'dem', 'slp', 'asp']
clips = ['sand', 'silt', 'mxdepth', 'clay', 'flm','bps', 'cbd', 'cbh', 'cc', 'ch', 'evt', 'fbfm40', 'dem', 'slp', 'asp', 'tlg']
#clips = ['sand', 'silt', 'mxdepth', 'clay', 'flm','bps', 'cbd', 'cbh', 'cc', 'ch', 'evt', 'fbfm40', 'dem', 'slp', 'asp']
##bilinear = ['dem', 'slp', 'asp', '3kgd']
#image = ['laif', 'laig']
image = ['laif']


## Basic functions frequently used, best imported from separate modules

mixcase = lambda x: x.replace('\\','/')

def checkdelete(indata,gp):
    try:
        gp.delete_management(indata)
        try: print "Dataset", indata, "Deleted"
        except: pass
    except:
        logger.debug("Clearing extra files for %s" % indata)
        # print gp.GetMessages()
        # try: print "Dataset", indata, "does not exist or is locked"
        # except: pass
        # auxiliary files will mess up processing
        try:
            f = os.path.splitext(indata)[0] + ".aux"
            if os.path.exists(f): 
                os.remove(f)
                try: logger.debug("Removed auxilary file for %s" % indata)
                except: pass
        except: 
            try: logger.debug("Auxilary file for %s does not exist" % indata)
            except: pass

def rotatefile(name, ext = None, n=9):
    import os
    print "renaming %s", name
    try : name = mixcase('.'.join([name, ext]))
    except: name = mixcase(name)

    rn = lambda S,n: S + str(n)
    try: os.remove(rn(name,n))
    except: pass
    for n in reversed(range(1,n)):
        try: os.rename(rn(name,n),rn(name,n+1))
        except: pass
    try: os.rename(name,rn(name,1))
    except: 
        try: 
            os.remove(rn(name,n+1))
            os.rename(rn(name,n),rn(name,n+1))
        except: pass
    else: pass
    return name

def checkPath(path):
    try: os.makedirs(path)
    except: pass
    return path

def getconfig(path, name = None):
    '''
    Extracts configuration data from .ini file with either a passed name or 
    otherwise the same root name as the calling program.  It first checks 
    starting path, then path of module.
    '''
    import os, sys
    import ConfigParser
    Config = ConfigParser.SafeConfigParser({'filtkey': None})
    Config.optionxform = str
    spath = path + "/"
    ppath, root = os.path.split(sys.argv[0])
    for n in [name, root.split('.')[0]]:
        print('testing for %s' % n)
        for p in [path, ppath]:
            try:
                init = "".join([p, '/', n, ".ini"])
                if os.path.exists(init):
                    break
                print "Initiating configuration from", init
            except:
                pass
    try: 
        Config.read(init)
        #Config.set(('User','startPath',path))
        return Config, init
    except: 
        print("Configuration file does not exist")
        print ("%s" % [name, root.split('.'[0])])
        return None, "Configuration file does not exist"

## Configuration requiring internal functions
#   setup logger

pn = 'Stage1'
logger = logging.getLogger(pn)
logfile = rotatefile('/'.join([workspace, zone, pn + '.log']),99)
logformat = '%(asctime)s %(name)s %(lineno)s %(levelname)s %(message)s'    
try: level = int(cfg.get('User','loglevel'))
except: level = 10
logging.basicConfig(filename=logfile,format=logformat,level=level,filemode='wb')
logger.setLevel(level)


## Functions specific to the __main__ module
def getgeoarea(z):
    GeoArea = {'SE':(37,46,48,54,55,56,98,99),
      'PNW':(1,2,7,8,9,10,18,19), 
      'PSW':(3,4,5,6,13),
      'SW':(12,14,15,16,17,23,24,25,28), 
      'NC':(20,21,22,29,30,31,39,40,41),
      'SC':(26,27,32,33,34,35,36,38,43,44,45),
      'NE':(42,47,49,50,51,52,53,57,58,59,60,61,62,63,64,65,66)}

    for ga,zones in GeoArea.iteritems():
        if z in zones:
            return ga

def rastercopy(copyfrom, copyto):
    if gp.OverWriteOutput:
        checkdelete(copyto,gp)
    try: 
        gp.CopyRaster_management(copyfrom, copyto)
        logger.debug('Grid %s copied from %s' % (copyto, copyfrom))
    except:
        if gp.exists(copyto):
            logmsg = '%s already exists in zone %s' %(copyto, zone)
            print(logmsg)
            logger.warning(logmsg)
        elif not gp.exists(copyfrom):
            logmsg = '%s does not exists' %(copyfrom)
            logger.error(logmsg)
        else:
            logmsg = "Other Copy Error:" + gp.GetMessages()
            logger.error(logmsg)

def zipextract(flai, outfile):    
    from zipfile import ZipFile
    z = ZipFile(flai)
    # setup for read of single file, not used
    L = []
    for f in z.namelist():
        if not os.path.exists(outfile):
            logger.debug("Trying to extract %s", f)
            odir,fn = os.path.split(f)
            if f.endswith('/'):
                os.makedirs(odir)
                logger.debug("made directory %s", odir)
            else:
                try: os.makedirs(os.path.basename(outfile))
                except: pass
                L.append(outfile)
                data = z.read(f)
                logger.debug("extracting %s", outfile)
                unit = open(outfile, 'wb')
                unit.write(data)
                unit.close()
                logger.debug("extracted %s from %s" % (outfile,f))
    return L

def resample(ingrid, outgrid, size, method = 'NEAREST'):
    logmsg = '%s resample %s -> %s at %s' % (method, ingrid, outgrid, size) 
    logger.info(logmsg)
    print(logmsg)
    if gp.exists(outgrid):
        logmsg= '%s Already resampled, %s exists' %(ingrid, outgrid)
        logger.warning(logmsg)
        print logmsg
    elif not gp.exists(ingrid):
        logmsg = 'ingrid %s does not exist' %(ingrid)
        logger.error(logmsg)
        print(logmsg)
    else:
        checkPath(os.path.dirname(outgrid))
        checkdelete(outgrid, gp)
        print ingrid, outgrid, size, method
        try:
            gp.Resample_management(ingrid, outgrid, size, method)
            return 0
        except:
            logger.error("Cannot resample %s at %sm" % (ingrid,size))
            return 1

def clipgrid(InRaster, OutRaster, mask):
    logger.debug("Clipping %s to %s with %s"%(InRaster, OutRaster, mask))
    logger.info("Clipping %s to %s" % (InRaster, OutRaster))
    gp.CheckOutExtension("Spatial")
    gp.OverWriteOutput = 0 #Setting to 1 'true' will overwrite grids.  Setting to 0 will not
    gp.extent = gp.describe(mask).extent
    try:
        print 'Clipping %s with %s to make %s' %(InRaster, mask, OutRaster)
        if gp.OverWriteOutput:
            checkdelete(OutRaster, gp)
        elif not gp.exists(OutRaster):
            try: 
                os.remove(OutRaster + '.aux')
                logmsg = "auxilary file removed for %s" % OutRaster
                logger.warning(logmsg)
            except: pass
        gp.Con_sa(mask, InRaster, OutRaster, 1) ##Check value number in the 3kgd.  This changes occasionally from 1 to 2
        logger.info("Con successful %s", InRaster)
    except:
        if gp.exists(OutRaster):
            logger.warning('%s already exists', OutRaster)
        elif not gp.exists(InRaster):
            logmsg = '%s does not exist' %(InRaster)
            logger.error(logmsg)
            print(logmsg)
        else:
            logmsg = "Con failed to create %s: " % OutRaster
            logmsg += gp.getmessages()
            logger.error(logmsg)
            print logmsg

def copy32tree(gp,cwd,goutL,cfg):
    from collections import defaultdict
    dbdir = cfg.get('dbf','lukup')
    getname = lambda x,y: ''.join([x,y])
    gp.CheckOutExtension('Spatial')
    inD = {}
    outD = {}
    dbfD = {}

    # initialize output file dictionary
    for g in goutL:
        inD[g] = '/'.join([cwd,getname(g,'_p')])
        outD[g] = '/'.join([cwd,getname(g,'_p2')])
        dbfD[g] = '/'.join([dbdir,getname(g,'.dbf')])
    print '-----------------------------'
    print 'goutL', goutL
    print '________________________________'
    print 'inD',inD

    # Special processing for "lcr"
    ingrid = inD['lcr']
    outgrid = outD['lcr']
    #try:
    checkdelete(outgrid,gp)
    gp.IsNull_sa(ingrid,outgrid)
    newgrid = '/'.join([cwd,getname('lcr','_p3')])
    checkdelete(newgrid,gp)
    gp.Con_sa(outgrid, -9999, newgrid, ingrid, "Value = 1")
    gp.BuildRasterAttributeTable_management(newgrid, '#')
    inD['lcr'] = newgrid
    outD['lcr'] = '/'.join([cwd,getname('lcr','_p4')])
    checkdelete(outD['lcr'],gp)
    logger.info("Made %s, set next grid to %s" %(newgrid, outD['lcr']))
    #

    #except:
    #   logger.error("error processing %s", ingrid)
    # Join DBF files to the copied rasters
    ## fieldD = {lcr_p3: lcr_dbf, nfdr_p: nfdr_dbf, dbh_p: dbh_dbf,
    ##        bcf_p: bcf_dbf, site_p: site_dbf}
    print 'Joining dbf files'
    logger.info("Joining dbf tables from %s" % (gout))

    #
    lukL = cfg.get('dbf','lukitem').split(',')
    print '--------------------------------------'
    print lukL
    lukD = dict([x.split(':') for x in lukL])

    # multD sets up a possibility of adding multiple factor in goutL loop
    multD = defaultdict(dict)
    for rule in cfg.get('dbf','mult').split(';'):
        x,y,z = rule.split(':')
        multD[x]['mult'] = y 
        multD[x]['outgrid'] = z

    gp.CheckOutExtension("3d")
    for g in goutL:
        ingrid = inD[g]
        outgrid = outD[g]
        try:
            tab = dbfD[g]
            gp.joinfield(ingrid, 'VALUE', tab, 'VALUE')
            logger.info('joining %s to %s' % (ingrid, tab))
        except:
            logger.error("unable to join %s to %s" % (ingrid, tab))
        try:
            item = lukD[g]
            logger.info('making %s from %s from %s' % (outgrid,ingrid,item))
            gp.Lookup_3d(ingrid, item, outgrid)
            inD[g] = outgrid
        except:
            logmsg = "lookup for ingrid failed: %s" % gp.GetMessages()
            logger.error(logmsg)
    
    # sys.exit()

    # Special processing for bcf
    ingrid = inD['bcf']
    outgrid = '/'.join([cwd,getname('bcf','_p3')])
    checkdelete(outgrid,gp)
    gp.Times_3d(ingrid, 1000, outgrid)
    inD['bcf'] = outgrid

    print '--------------------------------------'
    print inD
    print '--------------------------------------'
    print outD
    print '--------------------------------------'
    print multD
    # sys.exit()

    # Integerize a few of these grids
    #   a multD implementation in above loop would avoid this hardcode
    for g in goutL:
        outgrid = '/'.join([cwd,getname(g,'r')])
        checkdelete(outgrid,gp)
        gp.Int_3d(inD[g],outgrid)
        '''gp.Int_3d(site_p2, site_r)
        gp.Int_3d(nfdr_p2, nfdr_r)
        gp.Int_3d(dbh_p2, dbh_r)
        gp.Int_3d(bcf_p3, bcf_r)
        gp.Int_3d(lcr_p4, lcr_r)'''

def makelatlong(odir, ingrid):
    import csv
    from osgeo import gdal
    arc='C:/arcgis/arcexe9x/bin/arc.exe'

    indataset = gdal.Open(ingrid, 0)
    A,B,C,D,E,F = affine = indataset.GetGeoTransform()

    xsize = indataset.RasterXSize
    ysize = indataset.RasterYSize
    xoff = affine[1] / 2
    yoff = affine[5] / 2

    # for asciigrid header
    template=['ncols         REPL\n', 'nrows         REPL\n',
              'xllcorner     REPL\n', 'yllcorner     REPL\n',
              'cellsize      REPL\n', 'NODATA_value  -9999\n']
    replD = {'ncols':xsize, 'nrows':ysize, 'xllcorner':int(A),
             'yllcorner':int(D + ysize * E), 'cellsize': sz}

    header = []
    for row in template:
        key = row.split()[0]
        try:
            header.append(row.replace('REPL',str(replD[key])))
        except KeyError:
            header.append(row)

    # 
    getx = lambda x: A + B * x + xoff
    gety = lambda y: D + E * y + yoff
    
    pcoord = '/'.join([odir,'coords.txt'])
    gcoord = '/'.join([odir,'GEOcoord.txt'])
    prjfile = '/'.join([odir,'LFnat2geo.prj'])
    unit = open(prjfile,'wb')

    unit.write("""input
Projection    ALBERS
Zunits        NO
datum         nad83
Units         METERS
Spheroid      grs1980
Xshift        0.0000000000
Yshift        0.0000000000
Parameters
 29 30  0.000 /* 1st standard parallel
 45 30  0.000 /* 2nd standard parallel
-96  0  0.000 /* central meridian
 23  0  0.000 /* latitude of projection's origin
0.00000 /* false easting (meters)
0.00000 /* false northing (meters)
output
projection geographic
units dd
quadrant nw
datum         nad27
parameters
end""")
    unit.close()

    unit = open(pcoord, 'wb')
    writer = csv.writer(unit)

    # a text file for gp.MakeXYEventlayer might require a header...
    L = [['Xcoord','Ycoord']]
    L = []
    for r in xrange(ysize):
        for c in xrange(xsize):
            L.append([getx(c),gety(r)])
        writer.writerows(L)
        L = []
    unit.close()
    del writer

    aml = '/'.join([odir,'convert.aml'])
    unit = open(aml, 'wb')
    unit.write('project file %s %s %s' % (pcoord, gcoord, prjfile))
    unit.close()

    if os.path.exists(gcoord):
        os.remove(gcoord)
    args = ['arc',"&r %s"% aml]
    os.spawnv(os.P_WAIT,arc,args)

    unit = open(gcoord,'r')
    latasc = open('/'.join([odir,'latr.txt']),'wb')
    lonasc = open('/'.join([odir,'lonr.txt']),'wb')
    latasc.writelines(header)
    lonasc.writelines(header)
    print header
   
    for r in xrange(ysize):
        latL = []
        lonL = []
        for c in xrange(xsize):
            pair = unit.readline().strip().split()
            lon,lat = [int(1000000 * float(x)) for x in pair]
            latL.append(lat)
            lonL.append(lon)
        latasc.write('%s\n' % ' '.join([str(x) for x in latL]))
        lonasc.write('%s\n' % ' '.join([str(-1 * x) for x in lonL]))

    unit.close()
    latasc.close()
    lonasc.close()
    
    return gcoord

def dolatlong(cellsize):
    import os
    import logging
    logger = logging.getLogger(__name__)
    gp.extent = ''
    ##"""Create a latitude and longitude file for DAYMET weather referencing"""
    # cellsize = int(cfg.get('Main', 'cellsize').split(':')[0])
    odir = '/'.join([outdir, "xy" + str(cellsize)])
    checkPath(odir)
    
    dem = '/'.join([outdir, 'r' + str(cellsize), 'dem'])
    mask = '/'.join([outdir, 'r' + str(cellsize), 'm3kgd'])
    dempt = '/'.join([odir, 'dempt.shp'])
    latlon1 = '/'.join([odir, 'latlon1.shp'])
    latlon2 = '/'.join([odir, 'latlon2.shp'])
    lat_p1 = '/'.join([odir, 'latp1'])
    lon_p1 = '/'.join([odir, 'lonp1'])
    lat_p2 = '/'.join([odir, 'latp2'])
    lon_p2 = '/'.join([odir, 'lonp2'])
    lat_r = '/'.join([odir, 'latr'])
    lon_r = '/'.join([odir, 'lonr'])
    

    # move projection to config file or extract from input grids

    cs = 'c:/Program Files (x86)/ArcGIS/Coordinate Systems/Geographic Coordinate Systems/North America/North American Datum 1927.prj'
    cs2 = 'c:/Program Files (x86)/ArcGIS/Coordinate Systems/Projected Coordinate Systems/Continental/North America/USA Contiguous Albers Equal Area Conic USGS.prj' 


    # presumably, if dempt exists, this section can be skipped....
    #   however -- errors can occur downstream after dempt creation
    #   the quick but slow work around to this is to wipe out xy100

    # dempt is no longer needed....but still is for now
    if gp.exists(dempt):
        logmsg = '%s dempt Already exists, processing skipped' %(zone)
        logger.warning(logmsg)
        print(logmsg)
    else:
        logger.debug('Making %s' % dempt)
        gp.RasterToPoint_conversion(dem, dempt)

    # quick dash method of preventing redo of latlong processing
    geocoord = '/'.join([odir,'geocoord.txt'])
    if not gp.exists(geocoord):
        try:
            geocoord = makelatlong(odir,dem)
            unit = open(geocoord, 'r')
        except:
            dolatlong_old(cellsize,outdir,odir)

        #
        # OLD WAY (note memory usage - which can blow up)
        # unit = open('geocoord.txt')
        # L = [x.strip().split() for x in unit]
        # 2,622,284 private (KB) for z05



def dolatlong_old(cellsize,outdir,odir):
    import os
    import logging
    logger = logging.getLogger(__name__)
    gp.extent = ''
    ##"""Create a latitude and longitude file for DAYMET weather referencing"""
    # cellsize = int(cfg.get('Main', 'cellsize').split(':')[0])
    odir = '/'.join([outdir, "xy" + str(cellsize)])
    checkPath(odir)
    
    dem = '/'.join([outdir, 'r' + str(cellsize), 'dem'])
    mask = '/'.join([outdir, 'r' + str(cellsize), 'm3kgd'])
    dempt = '/'.join([odir, 'dempt.shp'])
    latlon1 = '/'.join([odir, 'latlon1.shp'])
    latlon2 = '/'.join([odir, 'latlon2.shp'])
    lat_p1 = '/'.join([odir, 'latp1'])
    lon_p1 = '/'.join([odir, 'lonp1'])
    lat_p2 = '/'.join([odir, 'latp2'])
    lon_p2 = '/'.join([odir, 'lonp2'])
    lat_r = '/'.join([odir, 'latr'])
    lon_r = '/'.join([odir, 'lonr'])
    

    # move projection to config file or extract from input grids
    archome = 'c:/Program Files (x86)/ArcGIS/Desktop10.0/Coordinate Systems'
    cs = 'Geographic Coordinate Systems/North America/North American Datum 1927.prj'
    cs = 'Geographic Coordinate Systems/North America/NAD 1927.prj'
    cs2 = 'Projected Coordinate Systems/Continental/North America/USA Contiguous Albers Equal Area Conic USGS.prj' 
    cs = '/'.join([archome,cs])
    cs2 = '/'.join([archome,cs2])


    # presumably, if dempt exists, this section can be skipped....
    #   however -- errors can occur downstream after dempt creation
    #   the quick but slow work around to this is to wipe out xy100

    if gp.exists(dempt):
        logmsg = '%s dempt Already exists, processing skipped' %(zone)
        logger.warning(logmsg)
        print(logmsg)
    else:
        logger.debug('Making %s' % dempt)
        gp.RasterToPoint_conversion(dem, dempt)
    if not gp.exists(latlon2):
        print "Lat Long conversion %s" % cellsize
        checkdelete(latlon1,gp)
        gp.project(dempt, latlon1, cs, 'NAD_1927_TO_NAD_1983_NADCON') 
        ##You may need to change this tranformation for Alaska and Hawaii
        gp.addxy(latlon1)
        gp.project(latlon1, latlon2, cs2, 'NAD_1927_TO_NAD_1983_NADCON')
        logger.info('lat long point files created')
    else:
        logmsg = '%s lready exists, processing skipped' %(latlon2)
        logger.warning(logmsg)
        return
    try:
        # Process: PointToRaster
        todelete =  [lat_p1, lat_p2, lon_p1, lon_p2, lat_r, lon_r]
        trash = [checkdelete(x,gp) for x in todelete]

        gp.extent = gp.describe(mask).extent
        gp.PointToRaster_conversion(latlon2, "POINT_Y", lat_p1, "MOST_FREQUENT", "NONE", cellsize) #make sure you change this 1000 to 100 meters
        gp.PointToRaster_conversion(latlon2, "POINT_X", lon_p1, "MOST_FREQUENT", "NONE", cellsize)
        # this is all in the table.  Why not just calculate right there?
        gp.CheckOutExtension("3d")
        gp.Times_3d(lat_p1, 1000000, lat_p2)
        gp.Times_3d(lon_p1, 1000000, lon_p2)
        print "EXTENT is:", gp.extent
        gp.Int_3d(lat_p2, lat_r)
        gp.Int_3d(lon_p2, lon_r)

        ## SKIPPED:
        ##  ERROR 000521: The number of unique values exceeds the limit.
        # gp.BuildRasterAttributeTable_management(lat_r, '#')
        # gp.BuildRasterAttributeTable_management(lon_r, '#')
        logger.info('lat long grids produced')
    except:
        # Print error message if an error occurs
        logmsg = 'failed to create lat long grids'
        print('%s : %s' %(logmsg, gp.GetMessages()))
        logger.error('%s : %s' %(logmsg, gp.GetMessages()))

def derivegrids(cellsize):
    ##--------------------------------------------------------------------
    ##"""Create the NFDR, DBH, BCF, LCR, Site Map, and RSHD grids. """
    # Set the input files
    #      Should be in config file.....
    # lukup = workspace +'/%s/LookupTables' % (zone) #global
    cs2 = 'c:/Program Files (x86)/ArcGIS/Coordinate Systems/Projected Coordinate Systems/Continental/North America/USA Contiguous Albers Equal Area Conic USGS.prj' 
    lukup = 'z:/work/FH' + '/LookupTables'
    
    # following code is eliminated through defined rename in config file
    # Rename fbfm40 and mxdepth, this is achieved from configuration setup:
    #   i.e., sand,silt,mxdepth:sdepr,clay for gridlist (mxdepth -> sdepr)

    # Set the workspace
    gp.workspace =  '%s/%s' % (workspace,zone)
    rsampdir = workspace + '/%s/gis/r%s' % (zone, cellsize)
    gp.extent = gp.describe('/'.join([rsampdir,'m3kgd'])).extent
    goutL = []

    gp.OverWriteOutput = 1
    # gp.OverWriteOutput = 0

    # Make 
    grps = cfg.get('dbf','groups').split(',')
    print "grps is", grps
    gisdir = '/'.join([gp.workspace, cfg.get('Main','outdir')])
    print gisdir
    print 'grps', grps
    logger.info('Processing %s -- resample to %s' % (grps, rsampdir))
    for g in grps:
        try:
            # gin, gout = [gapath(x) for x in g.split(':')]
            gin, gout = g.split(':')
            print '--------------------------'
            print "gin, gout", gin, gout
            copyfrom = '/'.join([gisdir,gin])

        except:
            logger.debug("ingrid is set to outgrid: %s" % g)
            gin = gout = g
            copyfrom = '/'.join([gisdir,gin + 'r'])
        copyto = '/'.join([rsampdir,gout + '_p'])
        goutL.append(gout)
        checkdelete(copyto, gp)
        errorcode = resample(copyfrom,copyto,int(cellsize))
        if errorcode:
            logmsg = "Resample of %s failed: %s" % \
                    (copyfrom, gp.GetMessages())
            logger.error(logmsg)
            print gp.GetMessages()
            print 'Section 4'
            checkdelete(copyto,gp)
            gp.projectraster(copyfrom,copyto,cs2,'#',int(cellsize))
    copy32tree(gp,rsampdir,goutL,cfg)
    # sys.exit()
    ##--------------------------------------------------------------------
    """Create the leaf area index grid.  LAI."""
    laiext = ['r', 'p1', 'p1g', 'p2', 'r1', 'r2']
    
    outworkspace = workspace + '/%s' %(zone)
    odir = '/'.join([workspace,zone,"gis/r" + str(cellsize)])
    xxL = ['r', 'p1', 'p1g', 'p2', 'r1', 'r2']
    xxlist = ['/'.join([odir, y]) for y in ["laift_" + x for x in ['r', 'p1', 'p1g', 'p2', 'r1', 'r2']]]
    laif_r = odir + '/flai'
    laift_p1 = odir +'/laift_p1'
    laift_p1g = odir + '/laift_p1'
    laift_p2 = odir + '/laift_p2'
    laift_r1 = odir + '/laift_r1'
    laift_r2 = odir + '/lair'
    outworkspace = odir

    if gp.exists(laift_r2):
        logmsg = '%s Already exists, skipping section' %(laift_r2)
        logger.info(logmsg)
        print logmsg
    else:
        # Set the input raster dataset
        for f in [laift_p1, laift_p2, laift_r2, laift_r2]:
            checkdelete(f, gp)
        # Process: Times
        # Check out ArcGIS 3D Analyst extension license
        
        gp.OverWriteOutput = 1
        gp.CheckOutExtension("3d")
        logger.debug('Making %s from %s' % (laift_p1, laif_r))
        gp.Times_3d (laif_r, 0.000183113851036882, laift_p1)
        
        gp.RasterToOtherFormat_conversion(laift_p1, outworkspace, "GRID")
        
        gp.CheckOutExtension("Spatial")
        gp.Con_sa(laift_p1g, 0.000001, laift_p2, laift_p1g, 'Value == 0')
        gp.Times_3d(laift_p2, 1000000, laift_r1)
        gp.Int_3d(laift_r1, laift_r2)
        logger.debug('con grid created for LAI')
        print 'con grid'
           
###---------------------------------------------------------------------
##    ------------------------------Begin----------------------------
###---------------------------------------------------------------------
##
if __name__ == '__main__':

    import string, shutil, tempfile
    import ConfigParser

    gapath = lambda x:x.replace('ZONE',zone).replace('GEOAREA',ga)
    cfg, initfile = getconfig(os.getcwd().replace('\\','/'))
    ga = getgeoarea(int(zone[1:]))

    #outdir = '/'.join([workspace, zone, "gis"])
    predD = {}
    outdir = '/'.join([workspace, zone, cfg.get('Main', 'outdir')])
    basedir = '/'.join([outdir, 'input'])
    checkPath(basedir)
    groups = cfg.get('Main', 'predictorGroups').split(',')
    logger.setLevel(10)
    for group in groups:
        # need a class for zone name....
        #indir = '/'.join([source1, zone, zone + '_bio'])
        print group, zone
        indir = cfg.get(group,'src').replace('ZONE',zone).replace('GEOAREA',ga)
        gridlist = cfg.get(group, 'gridlist')
        try: pre = cfg.get(group, 'pre').replace('ZONE',zone)
        except: pre = ''
        print("%s grids include: %s" % (group, gridlist))
        for g in gridlist.split(','):
            # gout is the basename of grid to use
            try:
                gin, gout = [gapath(x) for x in g.split(':')]
            except:
                gin = gout = g
            logger.debug('infile is %s, outfile is %s' %(gin, gout))
            copyfrom =  '/'.join([indir, pre + gin])
            copyto = '/'.join([basedir, gout])
            print 'Copying %s to %s' %(copyfrom, copyto)
            
            # copy
            if cfg.has_option(group,'zip') and cfg.getboolean(group,'zip'):
                copyfrom, copyto = (x + '.zip' for x in [copyfrom, copyto])
                flai = copyto
                print "copying", copyfrom,'->',flai
                if not os.path.exists(flai):
                    shutil.copy(copyfrom, copyto)
                    print 'copying forest lai'
                    logger.info("Copying %s to %s" % (copyfrom, copyto))
                    logger.debug('Copying %s to working directory', copyfrom)
                else:
                    msgtxt = 'FLAI zipfile exists: ' + flai
                    logger.info(msgtxt)
                    print msgtxt
                copyto = flai.replace('zip','img')
                if not os.path.exists(copyto):
                    try:
                        # x.extractall(flai)
                    
                        c2list = zipextract(flai, copyto)
                        print "trying to unzip", copyto
                    except:
                        print('Problem unzipping %s for %s' % (g, flai))
                        logger.warning("Problem unzipping %s for %s" % (g, flai))
                predD[gout] = copyto
            else:
                predD[gout] = copyto
                if not os.path.exists(copyto):
                    try:
                        rastercopy(copyfrom, copyto)
                    except:
                        logger.error("rastercopy failed")
                else:
                    logger.info('recopy of %s to %s skipped' % 
                            (copyfrom, copyto))
                
            # clip

            if bool(cfg.get(group, 'clip', vars = {'clip':'True'})):
                clipped = '/'.join([outdir, gout])
                clipgrid(predD[gout], clipped, mask)
                predD[gout] = clipped
            D = {}
            # resample the clipped grids
            if cfg.get(group, 'resample') == 'nearest':
                for sz in cfg.get('Main', 'cellsize').split(':'):
                    resamp = '/'.join([outdir, 'r' + str(sz), gout])
                    resample(predD[gout], resamp, int(sz), 'NEAREST')
                    predD[gout] = resamp
        print('done copying %s grids' % group)
        logger.info('done copying %s grids' % group)                            
    #
    #####----------------------------------------------------------------------

    logger.setLevel(level)
    for sz in cfg.get('Main', 'cellsize').split(':'):
        dolatlong(sz)
        pass
        derivegrids(str(sz))

    ###------------------------------------------------------------------
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

        # Simple time calculation following program completion
    elapsed = time.time() - start
    min = int(elapsed/60)
    print("Elapsed time was %d min %.3f sec" % (min, elapsed - min * 60))
    logger.info("Elapsed time was %d min %.3f sec" % (min, elapsed - min * 60))

