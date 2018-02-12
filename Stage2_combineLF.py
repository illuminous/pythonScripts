#!c:/python26/ArcGIS10.0/python -u
##!/usr/bin/env python

"""parse shit


"""
__author__ = "Jason M. Herynk"
__copyright__ = "Copyright 2011, SEM Systems for Environmental Management"
__credits__ = [""]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Jason M. Herynk"
__email__ = "jherynk.sem@gmail.com"
__status__ = "Prototype"

# $Id: Stage2_combineLF.py 32 2013-03-03 00:06:25Z cwinne $
# $URL: svn://refresh.dyndns-free.com/fireharm/trunk/progs/Stage2_combineLF.py $

# Import system modules
import os
import sys
import csv
import arcgisscripting
import time
tic = time.clock()


# Create the Geoprocessor object
gp = arcgisscripting.create()



path1 = 'G:/event_prep'
res = []
res2 = []
res3 = []
directories = []
combos = []
zoneres = []
mergedres = []

products = ['siter', 'evt', 'nfdrr', 'fbfm', 'flm', 'dem', 'asp', 'slp',
            'latr', 'lonr', 'lair', 'mxdepthr', 'sand', 'silt', 'clay', 'rshdr', 'dbhr',
          'bcfr', 'lcrr', 'ch', 'cbd', 'tlg']#change to trlstr for event

million = ['lair', 'latr', 'lonr', ]
thousand = ['bcfr', 'lcrr']
hundred = ['dbhr','cbd']
ten = ['ch'] 


products = ['siter', 'evt', 'nfdrr', 'fbfm', 'flm', 'dem', 'asp', 'slp',
            'latr', 'lonr', 'lair', 'sand', 'silt', 'clay', 'dbhr',
          'bcfr', 'lcrr', 'ch', 'cbd', 'tlg']#change to trlstr for event

# products = ['siter']
############################################################
"""Build a list of directories to copy grids from and to."""
def buildDirectories(zone_number_lower, zone_number_upper):
    for zone in range(zone_number_lower, zone_number_upper):
        res.append(zone)
        if zone < 10: #fix the formating if the zone number is less than 10
            path2 = '/z0%s' %(zone)
            path = path1+path2
            directories.append(path)
        else:
            path2 = '/z%s' %(zone)
            path = path1+path2
            directories.append(path)

    return directories

############################################################
"""Export a ascii formated txt file from an ESRI Grid"""
def genAscii():
    for d in directories: #start dirctories loop
        for p in products: #start grid products loop
            try:
                # Set local variables
                part1 = d
                part2 = p
                InRaster = part1 + '/' + part2 #create input file string
                print InRaster
                OutAsciiFile = InRaster + '.txt' #create output file string
                print OutAsciiFile
                # Process: RasterToASCII_conversion
                gp.OverWriteOutput = 1
                gp.RasterToASCII_conversion(InRaster, OutAsciiFile)
            except:
                # Print error message if an error occurs
                print gp.GetMessages()
############################################################
"""Export a ascii formated txt file from an ESRI Grid"""
def genAscii2(cfg,products):
    from shutil import copy2 as copy
    import logging
    logger = logging.getLogger(__name__)

    gp.OverWriteOutput = 1
    outpath = checkPath('/'.join([startpath, cfg.get('Main','outpath')]))
    print 'OUTPATH exists', outpath, os.path.exists(outpath)
    print 'Making', checkPath(outpath)
    for grid in products:
        # Set local variables
        if grid in cfg.get('Main','coordlist').split(','):
            inpath = cfg.get('Main','coordpath')
            # copy('/'.join([inpath,grid + '.txt']),outpath)
        else:
            inpath = cfg.get('Main','inpath')
        InRaster = '/'.join([startpath, inpath, grid])
        OutAsciiFile = '/'.join([outpath, grid + '.txt'])
        logger.info("Processing %s, InRaster %s, Out %s" % 
                (grid, InRaster, OutAsciiFile))
        try:
            print('genAscii, IN: %s  OUT: %s' % (InRaster, OutAsciiFile))
            # Process: RasterToASCII_conversion
            gp.RasterToASCII_conversion(InRaster, OutAsciiFile)
        except:
            # Print error message if an error occurs
            print gp.GetMessages()
        
############################################################
def createFolders(root):
    rootfolder = root + '/' + 'cleanFiles'
    if not os.path.exists(rootfolder):
        os.makedirs(rootfolder)
    else:
        print 'directory already exists'
############################################################
"""flip the ascii formated text into one vertical column"""
def transposeAscii(cfg,products):
    outpath = checkPath('/'.join([startpath, cfg.get('Main','outpath')]))
    for grid in products:
        infile = '/'.join([outpath, grid + '.txt'])
        outfile = open('/'.join([outpath, grid + '.asc']),'wb')
        print infile
        try:
            f = open(infile, 'r')
            for line in f.xreadlines():#.split(): #split the line up on whitespaces                
                outline = [x + '\n' for x in line.split()]
                outfile.writelines(outline) #write the item from the line
            f.close()
        except IOError:
            print "Error opening %s" % infile

############################################################
"""flip the ascii formated text into one vertical column"""
def processAscii(cfg,products):
    from itertools import izip
    def fixlist(L,mag,indices,keepD):
        # print L
        # print mag
        # print indices
        for i in indices:
            if L[i] not in keepD[i]:
                L[i] = str(int(L[i]) / (10.0 ** mag))
        # sys.exit()
        return L

    keepD = {}
    magD = {}
    for opt in cfg.options('scale'):
        k,v = cfg.get('scale',opt).split(':')
        magD[int(k)] = [products.index(x) for x in v.split(',')]
        for k in v.split(','):
            i = products.index(k)
            keepD[i] = ['-9999']
            try:
                keepD[i].append(cfg.get(k, 'keep'))
            except:
                print 'not for', k
                pass
    print magD
    print keepD
                
    readL = []
    outpath = cfg.get('Main','outpath')
    for grid in products:
        infile = '/'.join([outpath, grid + '.txt'])
        readL.append(open(infile, 'r'))

    headL = []
    count = 0
    for row in izip(*[x for x in readL]):
        # line = [x.strip() for x in row]
        headL.append(row)
        count += 1
        if count == 6:
            break

    # Headers should be identical on each gridasc file.
    for x in headL:
        if len(set(x)) != 1:
            print 'ERROR: files differ'
            print set(x)

            
    # '''
    readL = []
    for grid in products:
        infile = '/'.join([outpath, grid + '.txt'])
        readL.append(open(infile, 'r'))
    # '''

    # L = []
    # outfile = open(rotatefile('/'.join([outpath, 'CombineA.dat'])),'wb')
    outfix = open(rotatefile('/'.join([outpath, 'CombineB.dat'])),'wb')
    outclean = open(rotatefile('/'.join([outpath, 'CleanT.dat'])),'wb')
    combo = open('/'.join([outpath, 'Reference.asc']), 'wb')
    for x in headL:
        combo.write(x[0])
    # combo.writelines(headL)
    pnum = 0
    linenum = 0
    for row in izip(*[x for x in readL]):
        gascL = []
        line = [x.strip().split(' ') for x in row]
        linenum += 1
        if linenum <= 6:
            print line[0]
            continue
        for pixel in izip(*[x for x in line]):
            pnum += 1
            # print pixel
            # L.append(pixel)
            # outline = ' '.join([x for x in pixel]) + '\n'
            # outfile.write(outline )
            for k,v in magD.iteritems():
                pixel = fixlist(list(pixel),k,v,keepD)
            # print pixel
            outline = ' '.join(pixel)
            outfix.write('%s\n' % outline)
            # outclean.write(outline)
            # gascL.append({'-9999':'-9999'}.get(pixel[0],pchar))
            if pixel[0] == '-9999':
                gascL.append('-9999')
            else:
                pchar = str(pnum)
                outline = '%s %s\n' % (pchar, outline)
                outclean.write(outline)
                gascL.append(pchar)

        combo.write('%s\n' % ' '.join(gascL))

    # outfile.close()
    outfix.close()
    outclean.close()
    # combo.close()
    logger.info('Outfile %s written to %s' % ('CleanT.dat',outpath))
    
############################################################
def delHeader(cfg,products,headerlines):
    """
    strip the header file from each input file by 11 lines
    improvement:
        strip in initial conversion of .txt -> .asc (genAscii function)
    """

    inpath = '/'.join([startpath, cfg.get('Main','outpath')])
    outpath = checkPath('/'.join([inpath, 'clean']))
    for p in products: #start grid products loop
        ascfile = '/'.join([inpath, p + '.asc'])
        outfile = open('/'.join([outpath, p + '.asc']),'wb')
        print ascfile
        f = open(ascfile, 'r')            
        x = 0 # create iterable
        goodlines = open('c:/tmp/file.txt', 'w')
        for line in f:
            if x > headerlines: #delete first 11 lines of each file
                goodlines.write(line)    
            x+=1
        goodlines.close()
        # output = open(root + '/' + 'cleanFiles' + '/%s' %(p) + '.asc', 'w')
        goodopen = open('c:/tmp/file.txt', 'r')
        for item in goodopen:
            outfile.write(item)
        print ascfile, 'header has been stripped clean'
############################################################
"""8 grids in the list times were converted to integers when downloaded, this
step converts the values back to floats.  Eventually this def should be removed and
addressed in stageI"""
def timesFixer(cfg,ten,hundred,thousand,million):
    outpath = checkPath('/'.join([startpath, cfg.get('Main','outpath'), 'clean']))
    for p in million:
        logger.debug('Processing %s for million' % p)
        fn = '/'.join([outpath, '%s.asc' %(p)])
        FileName = open(fn, 'r')
        calclines = open('c:/tmp/calctmp.txt', 'w')
        for item in FileName:
            if item == '-9999\n':
                calclines.write(item)
            elif p == 'lair' and item == '1\n':
                calclines.write(item)
            else:
                calc = str(float(item)/1000000)
                calclines.write(calc)
                calclines.write('\n')
        FileName.close()
        calclines.close()
        output = open(fn, 'w')
        calclines = open('c:/tmp/calctmp.txt', 'r')
        for item in calclines:
            output.write(item)
        calclines.close()
        output.close()
            
    for p in thousand:
        logger.debug('Processing %s for thousand' % p)
        fn = '/'.join([outpath, '%s.asc' %(p)])
        FileName = open(fn, 'r')        
        calclines = open('c:/tmp/calctmp.txt', 'w')
        for item in FileName:
            if item == '-9999\n':
                calclines.write(item)
            elif p == 'lcrr' and item == '1000\n':
                calclines.write(item)
            else:
                calc = str(float(item)/1000)
                calclines.write(calc)
                calclines.write('\n')
        FileName.close()
        calclines.close()
        output = open(fn , 'w')
        calclines = open('c:/tmp/calctmp.txt', 'r')
        for item in calclines:
            output.write(item)
        calclines.close()
        output.close()

    for p in hundred:
        logger.debug('Processing %s for hundred' % p)
        fn = '/'.join([outpath, '%s.asc' %(p)])
        FileName = open(fn, 'r')
        calclines = open('c:/tmp/calctmp.txt', 'w')
        for item in FileName:
            if item == '-9999\n':
                calclines.write(item)
            else:
                calc = str(float(item)/100)
                calclines.write(calc)
                calclines.write('\n')
        FileName.close()
        calclines.close()
        output = open(fn, 'w')
        calclines = open('c:/tmp/calctmp.txt', 'r')
        for item in calclines:
            output.write(item)
        calclines.close()
        output.close()

    for p in ten:
        logger.debug('Processing %s for ten' % p)
        fn = '/'.join([outpath, '%s.asc' %(p)])
        FileName = open(fn, 'r')
        calclines = open('c:/tmp/calctmp.txt', 'w')
        for item in FileName:
            if item == '-9999\n':
                calclines.write(item)
            else:
                calc = str(float(item)/10)
                calclines.write(calc)
                calclines.write('\n')
        FileName.close()
        calclines.close()
        output = open(fn, 'w')
        calclines = open('c:/tmp/calctmp.txt', 'r')
        for item in calclines:
            output.write(item)
        output.close()
        calclines.close()
            
############################################################
"""from the output asc files, merge them all together into one output file"""
def mergeFiles(cfg,products):
    import logging
    logger = logging.getLogger(__name__)
    outpath = cfg.get('Main','outpath')
    inpath = checkPath('/'.join([startpath, outpath, 'clean']))
    fD = {}
    for p in products:
        fn = '/'.join([inpath, '%s.asc' %(p)])
        fD[p] = open(fn,'r')

    # return fD
    outputmerged = open('/'.join([inpath, 'outfile.txt']), 'wb')
    #outputmerged = open(root + '/' + 'cleanFiles/' + 'outfile.txt', 'w')
##    outputmerged.writelines("""FIREHARM input file Created by Jason M. Herynk SEM
##site evt nfdr fb40 flm treel dem asp slp lat lon lai sdep sand silt clay rshd dbh bcf lcr ch cbd \n""")
    print fD.keys()
    for line in fD['siter'].xreadlines():
        # '''
        merged =(line.rstrip() + ' '+ fD['evt'].readline().strip()+ ' '+ fD['nfdrr'].readline().strip()+ ' '+ fD['fbfm'].readline().strip()+ ' '+ fD['flm'].readline().strip()
                 + ' '+ fD['tlg'].readline().strip()+ ' '+ fD['dem'].readline().strip()+ ' ' + fD['asp'].readline().strip()+ ' '+ fD['slp'].readline().strip()
                 + ' '+ fD['latr'].readline().strip() + ' '+ fD['lonr'].readline().strip() + ' '+ fD['lair'].readline().strip()+ ' '+ fD['sdepr'].readline().strip()
                 + ' '+ fD['sand'].readline().strip()+ ' '+ fD['silt'].readline().strip()+ ' '+ fD['clay'].readline().strip()+ ' '+ fD['m3kgd'].readline().strip()
                 + ' '+ fD['dbhr'].readline().strip()+ ' '+ fD['bcfr'].readline().strip()+ ' '+ fD['lcrr'].readline().strip()+ ' '+ fD['ch'].readline().strip()
                 + ' '+ fD['cbd'].readline().strip())        
        # '''
        outputmerged.write(merged)
        outputmerged.write('\n')
    outputmerged.close()
    return None
############################################################
"""Remove no data -9999 lines and print to file"""
def cleanOutfile(root):
    import logging
    logger = logging.getLogger(__name__)
    outpath = cfg.get('Main','outpath')
    inpath = '/'.join([startpath, outpath, 'clean'])
    outputmerged = open('/'.join([inpath, 'outfile.txt']), 'r')
    outputclean = open('/'.join([inpath, 'outfileclean.txt']), 'wb')
    x=0
    print 'starting rewrite'
    for line in outputmerged.xreadlines():
        x+=1
        if line[:5] == '-9999':
            pass
        else:
            newline = str(x)+' '+line
            outputclean.write(newline)
    print('have read %s lines' % x)

############################################################
"""Create a reference asci grid that you can joinitem on later"""
def createReference(cfg):
    import logging
    logger = logging.getLogger(__name__)
    outpath = cfg.get('Main','outpath')
    inpath = checkPath('/'.join([startpath, outpath, 'clean']))

    res10 = []
    outputmerged = open('/'.join([inpath, 'outfile.txt']), 'r')
    combo = open('/'.join([inpath, 'comboevt.asc']), 'wb')
    combo.write("""ncols         5226
nrows         5449
xllcorner     -37215
yllcorner     1879835
cellsize      100
NODATA_value  -9999""")

    source = outputmerged.xreadlines()
    x = 0
    for item in source:
        firstitem = str(item).split()
        for blow in firstitem:
            x+=1
            if blow == '-9999':
                combo.write('-9999'+ ' ')
            else:
                combo.write(str(x) + ' ')
        combo.write('\n')
    combo.close()    


############################################################
"""Main: Commands to Run"""
if __name__ == '__main__':

    import logging
    from functions import checkPath, getconfig, rotatefile
    mx = lambda x: x.replace('\\','/')

    startpath = mx(os.getcwd())
    cfg, initfile = getconfig(startpath)

    
    pn = 'Stage2'
    logger = logging.getLogger(pn)
    logfile = rotatefile('/'.join([startpath, pn + '.log']), 99)
    logformat = '%(asctime)s %(name)s %(lineno)s %(levelname)s %(message)s'    
    try: level = int(cfg.get('User','loglevel'))
    except: level = 10
    logging.basicConfig(filename=logfile,format=logformat,level=level,filemode='wb')
    logger.setLevel(level)
    
    products = cfg.get('Main','products').split(',')
    logger.info('Working directory: %s Inifile: %s' %(startpath, initfile))
    ##buildDirectories(42,43)

    # sys.exit() works for idle setup.
    # sys.exit()
    ###################

    logger.info('Converting grid to ascii format')
    nowtoc = time.clock()
    genAscii2(cfg,products)
    newtic = time.clock()
    logmsg = 'genAscii2 took %s seconds' % str(newtic - nowtoc)
    # print logmsg
    logger.info(logmsg)

    nowtoc = newtic
    print 'starting processAscii'
    processAscii(cfg,cfg.get('Main','productOUT').split(','))
    newtic = time.clock()
    logger.info('processAscii took %s' % str(newtic - nowtoc))

    '''
    nowtic = time.clock()
    logger.info('Transposing ascii grids')
    transposeAscii(cfg,products)
    thistime = time.clock() - nowtic
    print "transposeAscii time:", thistime
    logger.info('transposeAscii completed in %s' % (thistime))
    logger.info('Deleting header on transposed files')
    delHeader(cfg, products, 11)
    logger.info('Fixing variable magnitude')
    timesFixer(cfg,ten,hundred,thousand,million)
    logger.info('merging products')
    mergeFiles(cfg,products)
    logger.info('Clean outfiles')
    cleanOutfile(cfg)
    

    nowtoc = newtic
    print 'starting createReference'
    logger.info('creating reference file')
    ## createReference(cfg) # dont forget to delete header 
    newtic = time.clock()
    logger.info('createReference took %ss' % str(newtic - nowtoc))
    '''


    toc = time.clock()
    processingtime = toc-tic
    min = int(processingtime/60)
    print("Elapsed time was %d min %.3f sec" % (min, processingtime - min * 60))
    logger.info("Elapsed time was %d min %.3f sec" % (min, processingtime - min * 60))
    print processingtime
    print 'seconds'
