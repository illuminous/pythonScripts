#!/bin/bash
import os
zone = 'z16'
numlinesres = []
chunkres = []

def createFolders(root):
    rootfolder = root + '/' + 'cleanFiles' +'/fireharm'
    if not os.path.exists(rootfolder):
        os.makedirs(rootfolder)
    else:
        print 'directory already exists'

def divideLines(txtfileRoot, filename, chunk):
    allFileNames = os.listdir(txtfileRoot)
    for txtfile in allFileNames:
        outfiles = txtfileRoot + '/' + txtfile
        if txtfile == filename:  ##logic for .outfiles
            num_lines = sum(1 for line in open(txtfileRoot + '/' + txtfile))  ##Subtract 26 lines because of the header file in the outfiles
            numlinesres.append(num_lines)
            createchunk = num_lines/chunk
            chunkres.append(createchunk)
            print txtfile, 'has', num_lines, 'lines'
            print 'divided by', chunk, 'equals', createchunk, 'lines'
        else:
            pass

def splitFileSmall(txtfileRoot, chunks):
    splitLen = chunks         # 20 lines per file
    outputBase = txtfileRoot # output.1.txt, output.2.txt, etc.

    input1 = open('L:/event_prep/z16/cleanFiles/outfileclean.txt', 'r').read().split('\n')
    input1.write("""FIREHARM input file Created by Jason M. Herynk SEM
site evt nfdr fb40 flm treel dem asp slp lat lon lai sdep sand silt clay rshd dbh bcf lcr ch cbd \n""")      
    at = 1 
    for lines in range(0, len(input1), splitLen):
        print lines
        # First, get the list slice
        outputData = input1[lines:lines+splitLen]
        output = open(outputBase + str(at) + '.in', 'w')
        # Now open the output file, join the new slice with newlines
        # and write it out. Then close the file.
        output = open(outputBase + str(at)+ '.in', 'w')
        output.write('\n'.join(outputData))
        output.close()

        # Increment the counter
        at += 1


##########################################################################
def splitFileBig(txtfileRoot, chunks):
    splitLen = chunks         # 20 lines per file
    outputBase = txtfileRoot # output.1.txt, output.2.txt, etc.

    input1 = open('L:/event_prep/z17/cleanFiles/outfileclean.txt', 'r').readlines()
##    input1.write("""FIREHARM input file Created by Jason M. Herynk SEM
##site evt nfdr fb40 flm treel dem asp slp lat lon lai sdep sand silt clay rshd dbh bcf lcr ch cbd \n""")    
    at = 1 
    for lines in range(0, len(input1), splitLen):
        print lines
        # First, get the list slice
        outputData = input1[lines:lines+splitLen]
        output = open(outputBase + str(at) + '.in', 'w')
        # Now open the output file, join the new slice with newlines
        # and write it out. Then close the file.
        output = open(outputBase + str(at)+ '.in', 'w')
        output.write(''.join(outputData))
        output.close()

        # Increment the counter
        at += 1          

##############################################################################
def splitFileBigger(txtfileRoot, numchunks, numlines):
    outputBase = txtfileRoot # output.1.txt, output.2.txt, etc.
    poly = 0 #start polygon counter    
    recordres = [] # create empty list to store chunk line breaks
    for record in range(0, numlines, numchunks):
        recordres.append(record)
    
    for lines in recordres: #loop over lines within a chunk break               
        output = open(outputBase + str(poly) + '.in', 'w')
        output.write("""FIREHARM input file Created by Jason M. Herynk SEM
site evt nfdr fb40 flm treel dem asp slp lat lon lai sdep sand silt clay rshd dbh bcf lcr ch cbd \n""")
        linenum = 0
        for line in open('J:/event_prep/z16/cleanFiles/trlstr.asc'):
            
            if linenum > int(lines) and linenum < int(numchunks):
                print lines, linenum, numchunks
                output.write(''.join(line))
            linenum+=1
        poly+=1
        print poly
##            
##            print poly
##            else:
##                poly+=1
               
                
##            elif linenum > int(lines) and linenum > int(splitLen):
####                output.close()
##         poly+=1       

##def splitBMF(txtfileRoot, chunks, numlines):
                
    






createFolders('J:/event_prep/z16')
divideLines('J:/event_prep/z16/cleanFiles', 'trlstr.asc', 19)
##splitFileSmall('L:/event_prep/z15/cleanFiles/fireharm/%spoly' %(zone), chunkres[0])
##splitFileBig('J:/event_prep/z17/cleanFiles/fireharm/%spoly' %(zone), chunkres[0])
splitFileBigger('J:/event_prep/z16/cleanFiles/fireharm/%spoly' %(zone), chunkres[0], numlinesres[0])


