#!/usr/bin/python
from tempfile import mkstemp
from shutil import move
from collections import defaultdict
from os import remove, close, system
import sys

def makedict(L):
    D = {}
    for r in L:
        D[tonumber(r[0])] = [tonumber(x) for x in r[1:]]
    return D

def addtype(D = {}, group = None,  _type= None):
    ''' appends item to prexisting dictionary list
        creates entry with list if not exist'''
    D.setdefault(group,[]).append(_type)

def writerow(names,outfileL,cols,D,idL,i):
    L = [x % cols for x in idL]
    for name,unit in zip(names,outfileL):
        rowD = {}
        for x,y in zip(L,D[name]):
            rowD[x] = y
        nowrow = ' '.join([rowD.get(x,'-9999') for x in xrange(cols)])
        unit.write(nowrow + '\n')

##def replace(file, pattern, subst):
##    #Create temp file
##    fh, abs_path = mkstemp()
##    new_file = open(abs_path,'w')
##    old_file = open(file)
##    for line in old_file:
##        new_file.write(line.replace(pattern, subst))
##    #close temp file
##    new_file.close()
##    close(fh)
##    old_file.close()
##    #Remove original file
##    remove(file)
##    #Move new file
##    move(abs_path, file)

def createOutgrids(indir):
    hdrfilename = '/'.join([indir,'reference.asc'])
    hdrfile = open(hdrfilename, 'r')
    hdr = []
    D = {}
    for x,row in enumerate(hdrfile):
        if x >= 6:
            break
        r = row.strip()
        hdr.append(row.strip())
        r = r.split()
        D[r[0]] = r[1]
    hdrfile.close()
    rows = int(D['nrows'])
    cols = int(D['ncols'])
        
    infilename = '/'.join([indir,'out.txt'])
    infile = open(infilename, 'r')
    # combofile =(root + '/' + 'comboevt.asc')
    names = ['PolygonID', 'KBDI', 'PKDBI', 'Spread', 'pSpread', 'FLI',
            'pFLI', 'Flame', 'pFlame', 'CrownI', 'pCrown', 
            'FCons', 'pfCons', 'TrMort', 'pTrMort', 'SoilHt', 'pSoilHt',
             'Emiss', 'pEmiss', 'Scorch', 'pScorch']
    names = names[1:]
    D = {}
    outfileL = []
    for f in names:
        ws = indir+'/'+f
        outfileL.append(open('.'.join([ws,'asc']), 'wb')) # changed this to write to the indirectory so it will work in a loop
        D[f] = []
    for unit in outfileL:
        for line in hdr:
            unit.write(line + '\n')
    idL = []
    i = 0
    for row in infile:
        line = row.strip().split()
        try:
            id = int(line.pop(0)) - 1
        except:
            # error appears to be quoted NULL data before ID
            print row
            print line
            try:
                line = row.strip().split()[1:]
                id = int(line.pop(0))
            except:
                return row,line,infile
        r = id // cols
 
        while i< r:
            #print('we are on row %s' % i)
            #print('IDs are %s' % idL)
            #linelength =  len(D[names[1]])
            #print D[names[1]]
            #print('%s values in row' % len(D[names[1]]))
            writerow(names,outfileL,cols,D,idL,i)
            for f in names:
               D[f] = []
            idL = []
            i += 1
            #print('IDs are %s' % L) 

        idL.append(id)
        for x,val in zip(names,line):
            addtype(D,x,val)
    # Should be done, write data from each row
    while i < rows:
        print(('%s is row, %s is i') % (r,i))
        print id,line,row
        writerow(names,outfileL,cols,D,idL,i)
        for f in names:
           D[f] = []
        idL = []
        i += 1
        #print('IDs are %s' % L) 
    return row,line,infile

#dim = rows,cols = 4564,6423
#infile = '/'.join(['/mnt/hd/fireharm','out.txt'])
##['23','17', '24','27','26','35','22','05','06']:
for z in ['14','15','23']:
    try:
        indir = 'E:/FIREHARM/d.daymetII/z%s/outfiles' %(z)
        row,line,infile = createOutgrids(indir)
    except:pass
#replace('j:/event_fireharm/z23/outfiles/combotest.out', 'x', '55')
      
