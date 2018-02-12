import os, re
filename = 'g:/working/carbon/carbon_bm.out'
parse =  open(filename, 'r')

##Search everyline where STAND ID = a 5 digit code
StandId = re.compile(r'STAND ID= [0-9]{5}')
##
WARNING = re.compile(r'WARNING: INITIAL')


##warningstorage = []
##plotstorage = []

outputs = open('g:/working/carbon/programs/carbon_bm.csv', 'w')
outputs.write('StandID, Error\n')

        
for line in parse:
    readPlot = StandId.findall(line)
    readWarning = WARNING.findall(line)
    for treelist in readPlot:
        pass
      #  print treelist
    for message in readWarning:
      #  print line
        nextline1 = parse.next()
       # print nextline1
        nextline2 = parse.next()
       # print nextline2
##        if treelist not in plotstorage:
##            plotstorage.append(treelist)
        formatline = line.rstrip()
        formatnextline1 = nextline1.rstrip()
        formatnextline2 = nextline2.rstrip()
        finaloutput = treelist + ','+ formatline + formatnextline1 + formatnextline2 + '\n'
        
        outputs.writelines(finaloutput)

    

