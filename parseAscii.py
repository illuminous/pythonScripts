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


# Create the Geoprocessor object
gp = arcgisscripting.create()



path1 = 'J:/event_prep'
res = []
res2 = []
res3 = []
directories = []
combos = []
zoneres = []
mergedres = []
zones = ['z15']
clipgrid = ['z15_id']
products = ['siter', 'evtr', 'nfdrr', 'fbfmr', 'flmr', 'demr', 'aspr', 'slpr',
            'latr', 'lonr', 'lair', 'sdepr', 'sandr', 'siltr', 'clayr', 'rshdr', 'dbhr',
          'bcfr', 'lcrr', 'chr', 'cbdr', 'trlstr']


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
def createFolders(root):
    rootfolder = root + '/' + 'cleanFiles'
    if not os.path.exists(rootfolder):
        os.makedirs(rootfolder)
    else:
        print 'directory already exists'
############################################################
"""flip the ascii formated text into one vertical column"""
def transposeAscii(root):
    for d in directories: #start dirctories loop
        for p in products: #start grid products loop
            part3 = d
            part4 = p
            part5 = '.txt'
            inputfile = part3 + '/' + part4 + part5 #create input file string
            print inputfile
            f = open(inputfile, 'r')
            outfile = open(root + '/' + 'cleanFiles' + '/%s' %(p) + '.asc', 'w') #create output file string
            for line in f.xreadlines():#.split(): #split the line up on whitespaces
                outfile.write(line + '\n') #write the item from the line
            f.close()

############################################################
"""strip the header file from each input file by 1 lines"""
def delHeader(root):
##    allFileNames = os.listdir(root) #return the list of files within a directory
##    for txtfile in allFileNames:
##        if txtfile[-4:] == '.asc':
    for d in directories: #start dirctories loop
        for p in products: #start grid products loop
            part3 = d
            part4 = 'cleanFiles/' + p
            part5 = '.asc'
            ascfile = part3 + '/' + part4 + part5 #create input file string
            print ascfile
            inputfile = open(ascfile, 'r')
            s = inputfile.readlines()
            del s[:12]
            output = open(root +'/'+ 'cleanFiles/'+ '%s' %(p) + '.asc', 'w')
            output.writelines(s)
            print ascfile, 'header has been stripped clean'
        else:
            print ascfile, 'this is not an outfile'

############################################################
"""from the output asc files, merge them all together into one output file"""
def mergeFiles(root):
    filelist = []
    for p in products:
        FileName = root + '/' + 'cleanFiles/' + '%s' %(p) + '.asc'
        filelist.append(FileName)
    #allFileNames = os.listdir(root)
        
##    for txtfile in allFileNames:
##        for p in products:
##            if txtfile[-4:] == '.asc' and p in products:            
##                filelist.append(root +'/'+ txtfile)
    print filelist
    aspr = filelist[0]
    bcfr = filelist[1]
    cbdr = filelist[2]
    chrr = filelist[3]
    clayr = filelist[4]
    dbhr = filelist[5]
    demr = filelist[6]
    evtr = filelist[7]
    fbfmr = filelist[8]
    flmr = filelist[9]
    lair = filelist[10]
    latr = filelist[11]
    lcrr = filelist[12]
    lonr = filelist[13]
    nfdrr = filelist[14]
    rshdr = filelist[15]
    sandr = filelist[16]
    sdepr = filelist[17]
    siltr = filelist[18]
    siter = filelist[18]
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
    fbfmr_open = open(fbfmr, 'r')
    flmr_open = open(flmr, 'r')
    lair_open = open(lair, 'r')
    latr_open = open(latr, 'r')
    lcrr_open = open(lcrr, 'r')
    lonr_open = open(lonr, 'r')
    nfdrr_open = open(nfdrr, 'r')
    rshdr_open = open(rshdr, 'r')
    sandr_open = open(sandr, 'r')
    sdepr_open = open(sdepr, 'r')
    siltr_open = open(siltr, 'r')
    siter_open = open(siter, 'r')
    slpr_open = open(slpr, 'r')
    trlstr_open = open(trlstr, 'r')
    
    for line in siter_open:
        merged =(line.rstrip() + ' '+ evtr_open.readline().strip()+ ' '+ nfdrr_open.readline().strip()+ ' '+ fbfmr_open.readline().strip()+ ' '+ flmr_open.readline().strip()
                 + ' '+ trlstr_open.readline().strip()+ ' '+ demr_open.readline().strip()+ ' ' +aspr_open.readline().strip()+ ' '+ slpr_open.readline().strip()
                 + ' '+ latr_open.readline().strip()+ ' '+ lonr_open.readline().strip()+ ' '+ lair_open.readline().strip()+ ' '+ sdepr_open.readline().strip()
                 + ' '+ sandr_open.readline().strip()+ ' '+ siltr_open.readline().strip()+ ' '+ clayr_open.readline().strip()+ ' '+ rshdr_open.readline().strip()
                 + ' '+ dbhr_open.readline().strip()+ ' '+ bcfr_open.readline().strip()+ ' '+ lcrr_open.readline().strip()+ ' '+ chrr_open.readline().strip()
                 + ' '+ cbdr_open.readline().strip())
        mergedres.append(merged)

    outputmerged = open(root + '/' + 'cleanFiles/' + 'outfile.txt', 'w')
    outputmerged.writelines("""FIREHARM input file Created by Jason M. Herynk SEM
site evt nfdr fb40 flm treel dem asp slp lat lon lai sdep sand silt clay rshd dbh bcf lcr ch cbd \n""")
    for item in mergedres:
        newitem = item + '\n'       
        outputmerged.writelines(newitem)
    outputmerged.close()

############################################################
def createReference(root):
    res10 = []
    res11 = []
    outputmerged = open(root + '/' + 'evtrII.txt', 'r')
    combo = open(root + '/' + 'cleanFiles/' + 'combo.asc', 'w')
    for item in outputmerged.read().split(): #split the line up on whitespaces
        res10.append(item)
        print res10
##    combo.write("""ncols         432
##nrows         460
##xllcorner     889335
##yllcorner     1446965
##cellsize      1000
##NODATA_value  -9999
##""")
    for(offset, item) in enumerate(res10):
        print offset, item
        if item == '\n-9999':
            newline = item[0:1]
            minus9 = item[1:]
            combo.write(newline)
            finitem = str(offset + 1)
            combo.write(finitem + ' ')
        else:
            finitem = str(offset + 1)
            combo.write(finitem + ' ')
    combo.close()

############################################################
"""Main: Commands to Run"""
                     
buildDirectories(15,16)
##genAscii()
##createFolders('J:/event_prep/z15')
##transposeAscii('J:/event_prep/z15')
##delHeader('J:/event_prep/z15')
##mergeFiles('J:/event_prep/z15')
createReference('J:/event_prep/z15')        

    
##def createChunks(low, high):
##    for chunk in range(low, high):
##        res2.append(str(chunk))
##    print res2
##
##def genClip():
##    for d in directories:
##        for chunk in res2:
##           for c in clipgrid:
##               gridextent = d + '/' + c + chunk 
##               res3.append(gridextent)
##               for p in products:
##                   clipitem = d + '/' + p + chunk
##                   clipout = clipitem+'_2'
##                   print clipitem
##                   print clipout
##                   gp.extent = gridextent
##                   setextent = gp.extent
##                   print setextent
##                   try:
##                       gp.clip_management(clipitem, setextent, clipout)
##                   except:
##                       print 'shit'



##createChunks(1,21)
##genClip()









        


##    res2.append(line)
##for item in baditems:
##    for value in line:
##        if line != item:
##            res.append(line)

##for item in res:
##    for key in baditems:
##        if item != key:
##            res2.append(item)
##        else:
##            pass
##f.close()
