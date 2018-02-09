"""Stage5.py
This script post processes FIREHARM output files.
Section 1 - Creates a list of files to iterate on
Section 2 - Strips the first 25 lines of header files
Created by Jason M. Herynk Systems for Environmental Management"""

import os
from string import split

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



zones = ['z38']
root = 'J:/event_fireharm/'
for z in zones:
    root2 = root + z + '/' + 'outfiles'
    delHeader(root2)
    

    
