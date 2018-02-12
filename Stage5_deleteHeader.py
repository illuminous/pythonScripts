"""Stage5.py
This script post processes FIREHARM output files.
Section 1 - Creates a list of files to iterate on
Section 2 - Strips the first 25 lines of header files
Created by Jason M. Herynk Systems for Environmental Management"""

import os
from string import split
resrange=[]
zones=[]
## Section 1

def delHeader(root):
    allFileNames = os.listdir(root)
    for txtfile in allFileNames:
        if txtfile[-4:] == '.out':
            inputfile = open(root +'/'+ txtfile, 'r')
            s = inputfile.readlines()
            del s[:26]
            output = open(root +'/'+ txtfile, 'w')
            output.writelines(s)
            print txtfile, 'header has been stripped clean'
        else:
            print txtfile, 'this is not an outfile'

def buildDirectories(zone_number_lower, zone_number_upper):
    for zone in range(zone_number_lower, zone_number_upper):
        resrange.append(zone)
        if zone < 10: #fix the formating if the zone number is less than 10
            path2 = 'z0%s' %(zone)
            zones.append(path2)
        else:
            path1 = 'z%s' %(zone)
            zones.append(path1)



#buildDirectories(13,14)
zones = ['z14','z15','z21','z23']
root='E:/FIREHARM/d.daymetII/'
#root = 'Z:/work/FH_outgoing/'
for z in zones:
    try:
        root2 = root + z + '/' + 'outfiles/'
        delHeader(root2)
    except:
        pass
    

    
