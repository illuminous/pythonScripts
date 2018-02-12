"""Created by Jason M. Herynk, Systems for Environmental Management
20100903.  This script reads in FVS carbon.out files, looks for error codes
and outputs a csv file with the stand id and associated error code"""
import os, re

##Search everyline where STAND ID = a 5 digit code
StandId = re.compile(r'STAND ID= [0-9]{1,7}')

##Search criteria for Warning messages and error codes, ignors FVS14 code.
WARNING = re.compile(r'WARNING: INITIAL')

##Specify the file name into a list for iteration.
inputfiles = [ 'sn_fl5','sn_fl6', 'bm', 'so', 'ca', 'ls', 'tt', 'ut', 'wc', 'ws', 'ci', 'cr', 'cs', 'ec', 'em', 'ie', 'nc', 'ne', 'pn', 'sn_fl1-4', ]


##Iterate on every file
for i in inputfiles:
    filename = 'g:/working/carbon/carbon_%s.out' %(i)
    parse =  open(filename, 'r')
    outputs = 'g:/working/carbon/Modified/carbon_%s.csv' %(i)
    outputfile = open(outputs, 'w')
    ##Create a header for the output file.
    outputfile.write('StandID, Error\n')
##Read everyline in the file
    for line in parse:
        readPlot = StandId.findall(line)
        readWarning = WARNING.findall(line)
##Read the StandID 
        for treelist in readPlot:
            pass
##Read the Warning message associated with the StandID
        for message in readWarning:
            ##Read the next two lines after inital Warning message line.
            nextline1 = parse.next()
            nextline2 = parse.next()
            ##Remove the newline character by stripping it.  
            formatline = line.rstrip()
            formatnextline1 = nextline1.rstrip()
            formatnextline2 = nextline2.rstrip()
            ##Format the file for comma delimited.  
            finaloutput = treelist + ','+ formatline + formatnextline1 + formatnextline2 + '\n'
            ##Write the file back to the outputfile location.
            outputfile.writelines(finaloutput)


