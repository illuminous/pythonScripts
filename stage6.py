"""This script post processes FIREHARM output files.
Section 1 - def delColumns - deletes columns from a txt file.
Section 2 - Iterates over zone numbers and calls def delColumns

Created by Jason M. Herynk Systems for Environmental Management"""

##Import stuff you need
import os
from string import split

##########################
"""Section 1: delColumns deletes columns that you specify.  In this case I keep columns
in place 0, 2, 3, and  22:40.
"""

def delColumns(root):    
    allFileNames = os.listdir(root)
    for txtfile in allFileNames:
        if txtfile[-4:] == '.out':
            data = open(root +'/'+ txtfile, 'r')
            wholefile = data.readlines()
            newlist = []
            newlist2 = []
            print txtfile, 'working on file'
            for x in wholefile:  
                Splitter = x.split(' ')
                newlist = [elem for elem in Splitter if elem != '']
                newlist2.append(newlist[0])
                newlist2.append(newlist[2])
                newlist2.append(newlist[3])
                newlist2.extend(newlist[22:40])
                newlist2.append('\n')
            modlist = ' '.join(newlist2)   
            output = open(root + '//' + txtfile, 'w')
            output.writelines(modlist)
            output.close()
##########################
"""Section 2: This runs the program.  I loop over a list of zones and pass
the root2 argument to the def delColumns"""

zones = ['z27']
root = 'H:/daymet_fireharm/'

for z in zones:
    root2 = root + z + '/' + 'outfiles'
    delColumns(root2)


