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



path1 = 'c:/WorkSpace'
res = []
res2 = []
res3 = []
directories = []
combos = []
zoneres = []
zones = ['z53']
clipgrid = ['z53_id']
products = ['siter', 'evtr', 'nfdrr', 'fbfmr', 'flmr']#, 'demr', 'aspr', 'slpr',
##            'latr', 'lonr', 'lair', 'sdepr', 'sandr', 'siltr', 'clayr', 'rshdr', 'dbhr',
##          'bcfr', 'lcrr', 'chr', 'cbdr', 'trlstr']


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
                gp.RasterToASCII_conversion(InRaster, OutAsciiFile)
            except:
                # Print error message if an error occurs
                print gp.GetMessages()

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
            outfile = open(root + '/%s' %(p) + '.asc', 'w') #create output file string
            for line in f.read().split(): #split the line up on whitespaces
                outfile.write(line + '\n') #write the item from the line
            f.close()

############################################################
"""strip the header file from each input file by 11 lines"""
def delHeader(root):
    allFileNames = os.listdir(root) #return the list of files within a directory
    for txtfile in allFileNames:
        if txtfile[-4:] == '.asc':
            inputfile = open(root +'/'+ txtfile, 'r')
            s = inputfile.readlines()
            del s[:11]
            output = open(root +'/'+ txtfile, 'w')
            output.writelines(s)
            print txtfile, 'header has been stripped clean'
        else:
            print txtfile, 'this is not an outfile'

############################################################
"""from the output asc files, merge them all together into one output file"""
def mergeFiles(root):
    allFileNames = os.listdir(root)
    filelist = []
    for txtfile in allFileNames:        
        if txtfile[-4:] == '.asc':            
            filelist.append(root +'/'+ txtfile)
    print filelist
    evtr = filelist[0]
    fbfmr = filelist[1]
    flmr = filelist[2]
    nfdrr = filelist[3]
    siter = filelist[4]
    print evtr
    print fbfmr
    print flmr
    print nfdrr
    print siter
    # need to add the other products into this as well as do some error checking logic
    evtr_open = open(evtr, 'r')
    fbfmr_open = open(fbfmr, 'r')
    flmr_open = open(flmr, 'r')
    nfdrr_open = open(nfdrr, 'r')
    siter_open = open(siter, 'r')
    mergedres = []
    for line in evtr_open:
        if line != '-9999\n':
            merged =(line.rstrip() + ' '+ fbfmr_open.readline().strip()+ ' '+ flmr_open.readline().strip()+ ' '+ nfdrr_open.readline().strip()+ ' '+ siter_open.readline().strip())
            mergedres.append(merged)
    print mergedres
    outputmerged = open(root + '/' + 'outfile.txt', 'w')
    outputmerged.writelines("""this is a header
id flm bla fuck you stupid\n""")
    for item in mergedres:
        newitem = item + '\n'       
        outputmerged.writelines(newitem)
    outputmerged.close()




buildDirectories(53,54)
##genAscii()
##transposeAscii('c:/WorkSpace/z53')
##delHeader('c:/WorkSpace/z53')
mergeFiles('c:/WorkSpace/z53')
        

    
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
