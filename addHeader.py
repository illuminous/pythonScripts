
import os
workDIR = 'J:/event_fireharm/z25/infiles'
res = []
# this is a multiline string
header = """FIREHARM input file Created by Jason M. Herynk SEM
site evt nfdr fb40 flm treel dem asp slp lat lon lai sdep sand silt clay rshd dbh bcf lcr ch cbd \n"""


dirList = os.listdir(workDIR)
print dirList
for item in dirList:    
    criteria = item[-9:-5]
    if item[-9:-5] == 'poly':
        print item
        res.append(item)

for fileobj in res:
    filepath = workDIR + '/' + fileobj
    print filepath
    output = open(filepath, 'r').read()
    output2 = open(filepath, 'w')
    output2.write(header)
    output2.write(output)
    output2.close()




        
##old_wd = os.getcwd() # <--- store the initial wd
##os.chdir(workDIR)
##try:
##    with open('test.in','w') as outfile:
##        outfile.write(header)
##        with open('z16poly00.in','r') as datafile:
##            for line in datafile:
##                outfile.write(line)
##finally:
##    os.chdir(old_wd)  # <--- back to the initial wd
