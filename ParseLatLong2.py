"""Created by Jason M. Herynk Systems for Environmental Management Missoula Montana
This script parses through formated Airtanker Drop location files and converts the latitude and longitude fields from decimal minutes to decimal degrees"""

import os, string

filename = 'G:/working/Airtanker/DropLocations/TESTUNIT2010_Aug1_Nov9.csv'
outfile = open('G:/working/Airtanker/DropLocations/TESTUNITParsedAug_nov9.csv', 'w')
outfile.write('SerialNo,UTC,Latitude,HemNS,Longitude,HemEW,Knots,Heading,Altitude_m,HDOP,NewConn,Entered,Event\n')
parse =  open(filename, 'r')

res = []

print 'Converting Coordinates from Decimal Minutes to Decimal Degrees'
##def parseLatLong(filename):
for line in parse:
    splitter = line.split(',')
    res.append(splitter)
    for r in res:
        """Convert Latitude from Decimal Minutes to Decimal Degrees"""
        latitude = r[2]
        latInt = int(float(latitude))
        latDigits = int(latInt/100)
        latDigitsTest = len(str(latDigits))
        if latDigitsTest == 2:
            latOtherDigits = float(latitude[2:])
            DecimalDegreesConv = latOtherDigits/60
            DecimalDegreesLat2 = latDigits+DecimalDegreesConv
            DecimalDegreesLat = str(round(DecimalDegreesLat2, 5))
        elif latDigitsTest == 1:
            latOtherDigits = float(latitude[1:])
            DecimalDegreesConv = latOtherDigits/60
            DecimalDegreesLat2 = latDigits+DecimalDegreesConv
            DecimalDegreesLat = str(round(DecimalDegreesLat2, 5))

        """Convert Longitude from Decimal Minutes to Decimal Degrees"""
        longitude = r[4]
        longInt = int(float(longitude))
        longDigits = int(longInt/100)
        longDigitsTest =len(str(longDigits))
        if longDigitsTest == 3:
            longOtherDigits = float(longitude[3:])
            longDDConv = longOtherDigits/60
            longDD = longDigits+longDDConv
            DecimalDegreesLong = '-' + str(round(longDD, 5))
        elif longDigitsTest == 2:
            longOtherDigits = float(longitude[2:])                       
            longDDConv = longOtherDigits/60
            longDD = longDigits+longDDConv
            DecimalDegreesLong = '-' + str(round(longDD, 5))
        elif longDigitsTest == 1:
            longOtherDigits = float(longitude[1:])                       
            longDDConv = longOtherDigits/60
            longDD = longDigits+longDDConv
            DecimalDegreesLong = '-' + str(round(longDD, 5))
    zero = str(r[0])
    one = str(r[1])
    two = DecimalDegreesLat
    three= str(r[3])
    four = DecimalDegreesLong
    five = str(r[5])
    six = str(r[6])
    seven = str(r[7])
    eight = str(r[8])
    nine = str(r[9])
    ten = str(r[10])
    eleven = str(r[11])
    tweleve = str(r[12])       
    """Write to the output file"""
    outline = zero+','+one+','+two+','+three+','+four+','+five+','+six+','+seven+','+eight+','+nine+','+ten+','+eleven+','+tweleve
    outfile.write(outline)
print 'Finished'
outfile.close()


