"""Stage5.py Event Mode
This script post processes FIREHARM output files.
Section 1 - Creates a list of files to iterate on
Section 2 - Strips the first 25 lines of header files
Created by Jason M. Herynk Systems for Environmental Management"""

import os
from string import split

zones = ['z05']
root = 'C:/event_outfiles/%s/' %zones[0]
mode = '_event_'
extension = '.out'
item = range(1, 21)

result=[]
## Section 1
for i in item:
    for z in zones:
        iterable = '%s' %(i)
        newfile = z + mode + iterable + extension 
        newlist = result.append(newfile)
print 'files are compiling'    

## Section 2    
for res in result:
    input = open(root + '//' + res, 'r') 
    s = input.readlines()
    del s[:26]
    output = open(root + '//' + res, 'w') 
    output.writelines(s)
    output.close
print 'header has been stripped clean'




    
