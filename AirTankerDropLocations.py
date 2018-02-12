import os

#class Airtanker:
def getUserinput():
    filename = raw_input('Enter Directory of Latitude Technologies CSV file....')
    print 
    output = raw_input('Enter Directory of the Parsed output file....')
    print 
    return filename, output

##def stripHeader():
##    readfilename = open(filename, 'r')
##    header = readfilename.readlines()
##    del header[:1]
##    output.writelines(header)
##    output.close

    #def parseLatLong(filename):
