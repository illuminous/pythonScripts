#!/usr/bin/python

import string
import sys
import os

# Version & how to run
print 'cleanPoly v1.0  5-25-2010\n'

if len(sys.argv) != 2 :
   print "use:  cleanPoly.py polyFile"
   sys.exit()

polyIn=sys.argv[1]
polyTmp=polyIn+'.temp'
polyBck=polyIn+'.bak'
polyBad=polyIn+'.badPolys'

if not os.path.exists(polyIn):
   print 'Error: Polygon file does not exist - ' + dem
   sys.exit()

# create a backup file
cmdStr = 'cp ' + polyIn + ' ' + polyBck
os.system(cmdStr)

# Open output files
theOutput = open(polyTmp,'wt')
theBad = open(polyBad,'wt')

# Open & read header records & transfer to the output files
theInput = open(polyIn)
header1 = theInput.readline()
header2 = theInput.readline()

theOutput.write(header1)
theOutput.write(header2)
theBad.write(header1)
theBad.write(header2)

# Read each line & process
dataLine = theInput.readline()
while dataLine != '':
   col = dataLine.split()
   latitude = float(col[10])
   longitude = float(col[11])

   # If Lat/Long values are out of range, write the polygon record to the "bad" file
   if (longitude < -127.0)|(longitude > -90.0):
      #print 'BAD:  ' + col[11]
      theBad.write(dataLine)
   else:
      theOutput.write(dataLine)

   dataLine = theInput.readline()

# Close files
theOutput.close
theBad.close
theInput.close

# Rename the temporary output file containing good polygons to that of the input
cmdStr = 'mv ' + polyTmp + ' ' + polyIn
#print cmdStr
os.system(cmdStr)

