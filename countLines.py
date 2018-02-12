#!/bin/bash
import os
zone = 'z15'
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
            createchunk = num_lines/chunk
            chunkres.append(createchunk)
            print txtfile, 'has', num_lines, 'lines'
            print 'divided by', chunk, 'equals', createchunk, 'lines'
        else:
            pass

def splitFileSmall(txtfileRoot, chunks):
    splitLen = chunks         # 20 lines per file
    outputBase = txtfileRoot # output.1.txt, output.2.txt, etc.

    input1 = open('L:/event_prep/z15/cleanFiles/outfileclean.txt', 'r').read().split('\n')
        
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

def splitFileBig(txtfileRoot, chunks):
    splitLen = chunks         # 20 lines per file
    outputBase = txtfileRoot # output.1.txt, output.2.txt, etc.

    input1 = open('L:/event_prep/z15/cleanFiles/outfileclean.txt', 'r').readlines()
    input1.writelines("""FIREHARM input file Created by Jason M. Herynk SEM
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
        output.write(''.join(outputData))
        output.close()

        # Increment the counter
        at += 1          
##createFolders('J:/event_prep/z15')
divideLines('L:/event_prep/z15/cleanFiles', 'outfileclean.txt', 19)
##splitFileSmall('L:/event_prep/z15/cleanFiles/fireharm/%spoly' %(zone), chunkres[0])
splitFileBig('L:/event_prep/z15/cleanFiles/fireharm/%spoly' %(zone), chunkres[0])


##Set the file directory

##chunkres = []
##def countLines(txtfileRoot, filename, chunk):
##    allFileNames = os.listdir(txtfileRoot)
##    for txtfile in allFileNames:
##        outfiles = txtfileRoot + '/' + txtfile
##        if txtfile == filename:  ##logic for .outfiles
##            num_lines = sum(1 for line in open(txtfileRoot + '/' + txtfile)) - 2 ##Subtract 26 lines because of the header file in the outfiles
##            createchunk = num_lines/chunk
##            chunkres.append(createchunk)
##            print txtfile, 'has', num_lines, 'lines'
##            print 'divided by', chunk, 'equals', createchunk, 'lines'
##        else:
##            pass
##
##    l = range(1, num_lines)
##    newchunk = [l[x:x+createchunk] for x in xrange(1, len(l), createchunk)]
##    for item in range(1,20):
##        for ls in newchunk:
##            out = open("c:/tmp/blah%s.txt" %(item), "w")
##            out.write(str(ls))
##            print ls[:477]
    
##def slicefile(filename, start, end):
##    for i, line in enumerate(open(filename)):
##        if i >= end:
##            return
##        if start <= i:
##            yield line
##
##out = open("c:/tmp/blah.txt", "w")
##for line in slicefile('J:/daymet_prep/z53/cleanFiles/outfile.txt', 10, 15):
##    out.write(line)
##out.close()        
##  
