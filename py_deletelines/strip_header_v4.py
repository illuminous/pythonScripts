"""This script post processes FIREHARM output files.
Section 1 - Creates a list of files to iterate on
Section 2 - Strips the first 25 lines of header files
Section 3 - Removes columns of data and resaves the file
Created by Jason M. Herynk Systems for Enviornmental Management"""

import os
from string import split

zones = ['z06']
root = 'C:/daymet_outfiles/%s/outfiles' %zones[0]
mode = '_dm_'
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

##Section 3
for res in result:
    ##data = open('c:/daymet_outfiles/z06/outfiles/test20.txt', 'r')
    data = open(root + '//' + res, 'r')
    wholefile = data.readlines()
    newlist = []
    newlist2 = []
    print 'working on file'
    print res
    for x in wholefile:  
        Splitter = x.split(' ')
        newlist = [elem for elem in Splitter if elem != '']
        newlist2.append(newlist[0])
        newlist2.append(newlist[2])
        newlist2.append(newlist[3])
        newlist2.extend(newlist[22:39])
        newlist2.append('\n')
    modlist = ' '.join(newlist2)   
    output = open(root + '//' + res, 'w')
    ##output = open('c:/daymet_outfiles/z06/outfiles/test20return.txt', 'w')
    output.writelines(modlist)
    output.close()


    
