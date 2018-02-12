#!/usr/bin/env python

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

# Import system modules
import os
import sys
import csv
import arcgisscripting
import time
tic = time.clock()


# Create the Geoprocessor object
gp = arcgisscripting.create()



path1 = 'G:/daymet_prep'
res = []
res2 = []
res3 = []
directories = []
combos = []
zoneres = []
mergedres = []

products = ['siter', 'evtr', 'nfdrr', 'fbfm40r', 'flmr', 'demr', 'aspr', 'slpr',
            'latr', 'lonr', 'lair', 'mxdepthr', 'sandr', 'siltr', 'clayr', 'rshdr', 'dbhr',
          'bcfr', 'lcrr', 'chr', 'cbdr', 'trlstr']#change to trlstr for event
million = ['lair', 'latr', 'lonr', ]
thousand = ['bcfr', 'lcrr']
hundred = ['dbhr','cbdr']
ten = ['chr'] 


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
def createFolders(root):

    rootfolder = root + '/' + 'cleanFiles'
    if not os.path.exists(rootfolder):
        os.makedirs(rootfolder)
    else:
        print 'directory already exists'
############################################################
"""flip the ascii formated text into one vertical column"""
def transposeAscii(root):

    for p in products: #start grid products loop
        part3 = d
        part4 = p
        part5 = '.txt'
        inputfile = part3 + '/' + part4 + part5 #create input file string
        print inputfile
        f = open(inputfile, 'r')
        outfile = open(root + '/' + 'cleanFiles' + '/%s' %(p) + '.asc', 'w') #create output file string
        for line in f.xreadlines():#.split(): #split the line up on whitespaces                
            itline = line.split()                
            for item in itline:
                outfile.write(item + '\n') #write the item from the line
        f.close()

############################################################
"""strip the header file from each input file by 11 lines"""
def delHeader(root, headerlines):   

    for p in products: #start grid products loop
        part3 = d
        part4 = 'cleanFiles/' + p
        part5 = '.asc'
        ascfile = part3 + '/' + part4 + part5 #create input file string
        print ascfile
        f = open(ascfile, 'r')            
        x = 0 # create iterable
        goodlines = open('c:/tmp/file.txt', 'w')
        for line in f:
            if x > headerlines: #delete first 11 lines of each file
                goodlines.write(line)    
            x+=1
        goodlines.close()
        output = open(root + '/' + 'cleanFiles' + '/%s' %(p) + '.asc', 'w')
        goodopen = open('c:/tmp/file.txt', 'r')
        for item in goodopen:
            output.write(item)
        print ascfile, 'header has been stripped clean'
############################################################
"""8 grids in the list times were converted to integers when downloaded, this
step converts the values back to floats.  Eventually this def should be removed and
addressed in stageI"""
def timesFixer(root):
    for p in million:
        FileName = open(root + '/' + 'cleanFiles/' + '%s' %(p) + '.asc', 'r')
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
        output = open(root + '/' + 'cleanFiles/' + '%s' %(p) + '.asc', 'w')
        calclines = open('c:/tmp/calctmp.txt', 'r')
        for item in calclines:
            output.write(item)
        calclines.close()
            
    for p in thousand:
        FileName = open(root + '/' + 'cleanFiles/' + '%s' %(p) + '.asc', 'r')
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
        output = open(root + '/' + 'cleanFiles/' + '%s' %(p) + '.asc', 'w')
        calclines = open('c:/tmp/calctmp.txt', 'r')
        for item in calclines:
            output.write(item)
        calclines.close()

    for p in hundred:
        FileName = open(root + '/' + 'cleanFiles/' + '%s' %(p) + '.asc', 'r')
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
        output = open(root + '/' + 'cleanFiles/' + '%s' %(p) + '.asc', 'w')
        calclines = open('c:/tmp/calctmp.txt', 'r')
        for item in calclines:
            output.write(item)
        calclines.close()

    for p in ten:
        FileName = open(root + '/' + 'cleanFiles/' + '%s' %(p) + '.asc', 'r')
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
        output = open(root + '/' + 'cleanFiles/' + '%s' %(p) + '.asc', 'w')
        calclines = open('c:/tmp/calctmp.txt', 'r')
        for item in calclines:
            output.write(item)
        calclines.close()
            
############################################################
"""from the output asc files, merge them all together into one output file"""
def mergeFiles(root):

    filelist = []
    for p in products:
        FileName = root + '/' + 'cleanFiles/' + '%s' %(p) + '.asc'
        filelist.append(FileName)
    print filelist
    filelist.sort()
    print filelist
    aspr = filelist[0]
    bcfr = filelist[1]
    cbdr = filelist[2]
    chrr = filelist[3]
    clayr = filelist[4]
    dbhr = filelist[5]
    demr = filelist[6]
    evtr = filelist[7]
    fbfm40r = filelist[8]
    flmr = filelist[9]
    lair = filelist[10]
    latr = filelist[11]
    lcrr = filelist[12]
    lonr = filelist[13]
    mxdepthr = filelist[14]
    nfdrr = filelist[15]
    rshdr = filelist[16]
    sandr = filelist[17]
    siltr = filelist[18]
    siter = filelist[19]
    slpr = filelist[20]
    trlstr = filelist[21]
    # need to add some error checking logic
    aspr_open = open(aspr, 'r')
    bcfr_open = open(bcfr, 'r')
    cbdr_open = open(cbdr, 'r')
    chrr_open = open(chrr, 'r')
    clayr_open = open(clayr, 'r')
    dbhr_open = open(dbhr, 'r')
    demr_open = open(demr, 'r')
    evtr_open = open(evtr, 'r')
    fbfm40r_open = open(fbfm40r, 'r')
    flmr_open = open(flmr, 'r')
    lair_open = open(lair, 'r')
    latr_open = open(latr, 'r')
    lcrr_open = open(lcrr, 'r')
    lonr_open = open(lonr, 'r')
    mxdepthr_open = open(mxdepthr, 'r')
    nfdrr_open = open(nfdrr, 'r')
    rshdr_open = open(rshdr, 'r')
    sandr_open = open(sandr, 'r')   
    siltr_open = open(siltr, 'r')
    siter_open = open(siter, 'r')
    slpr_open = open(slpr, 'r')
    trlstr_open = open(trlstr, 'r')
    outputmerged = open(root + '/' + 'cleanFiles/' + 'outfile.txt', 'w')
##    outputmerged.writelines("""FIREHARM input file Created by Jason M. Herynk SEM
##site evt nfdr fb40 flm treel dem asp slp lat lon lai sdep sand silt clay rshd dbh bcf lcr ch cbd \n""")
    
    for line in siter_open:
        merged =(line.rstrip() + ' '+ evtr_open.readline().strip()+ ' '+ nfdrr_open.readline().strip()+ ' '+ fbfm40r_open.readline().strip()+ ' '+ flmr_open.readline().strip()
                 + ' '+ trlstr_open.readline().strip()+ ' '+ demr_open.readline().strip()+ ' ' +aspr_open.readline().strip()+ ' '+ slpr_open.readline().strip()
                 + ' '+ latr_open.readline().strip() + ' '+ lonr_open.readline().strip() + ' '+ lair_open.readline().strip()+ ' '+ mxdepthr_open.readline().strip()
                 + ' '+ sandr_open.readline().strip()+ ' '+ siltr_open.readline().strip()+ ' '+ clayr_open.readline().strip()+ ' '+ rshdr_open.readline().strip()
                 + ' '+ dbhr_open.readline().strip()+ ' '+ bcfr_open.readline().strip()+ ' '+ lcrr_open.readline().strip()+ ' '+ chrr_open.readline().strip()
                 + ' '+ cbdr_open.readline().strip())        
        
        outputmerged.write(merged)
        outputmerged.write('\n')
    outputmerged.close()
############################################################
"""Remove no data -9999 lines and print to file"""
def cleanOutfile(root):
    for d in directories:
        outputmerged = open(root + '/' + 'cleanFiles/' + 'outfile.txt', 'r')
        outputclean = open(root + '/' + 'cleanFiles/' + 'outfileclean.txt', 'w')
        x=0
        for line in outputmerged:
            x+=1
            if line[:5] == '-9999':
                pass
            else:
                newline = str(x)+' '+line
                outputclean.write(newline)

############################################################
"""Create a reference asci grid that you can joinitem on later"""
def createReference(root):
    res10 = []
    outputmerged = open(root + '/' + 'evtr.txt', 'r')
    combo = open(root + '/' + 'cleanFiles/' + 'comboevt.asc', 'w')
    source = outputmerged.readlines()
    x = 0
    y=0
    for item in source:
        x+=1
        if x <= 6:
            combo.write(item)
        else:
            firstitem = str(item).split()
            for blow in firstitem:
                y+=1
                if blow == '-9999':
                    combo.write('-9999'+ ' ')
                else:
                    combo.write(str(y) + ' ')
            combo.write('\n')
    combo.close()    


############################################################
"""Main: Commands to Run"""
buildDirectories(36,37)
##directories.remove('G:/event_prep/z27')
##directories.remove('G:/event_prep/z28')
##directories.remove('G:/event_prep/z29')
##directories.remove('G:/event_prep/z30')
##directories.remove('G:/event_prep/z31')
##directories.remove('G:/event_prep/z38')
##directories.remove('G:/event_prep/z39')
##directories.remove('G:/event_prep/z40')
##directories.remove('G:/event_prep/z43')
##directories.remove('G:/event_prep/z45')
##directories.remove('G:/event_prep/z46')
##directories.remove('G:/event_prep/z47')
##directories.remove('G:/event_prep/z48')
##directories.append('G:/event_prep/z10')
for d in directories:
    genAscii()
    createFolders(d)
    transposeAscii(d)
    delHeader(d, 11) 
    timesFixer(d)
    mergeFiles(d)
    cleanOutfile(d)
    createReference(d) # dont forget to delete header 

toc = time.clock()
processingtime = toc-tic
print processingtime
print 'seconds'