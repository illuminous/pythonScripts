def createOutgrids(root):
    outputfile = open(root + '/' + 'fhouttest.out', 'r')
    combofile = open(root + '/' + 'combotest.out', 'r')
    newout = open(root + '/' + 'newout.out', 'wb')
    pixelkey = []
    res2 = []
    value = '10'
    for item in outputfile:
        linelist = item.split()
        pixelkey.append(linelist[0:13])
    for pixel in pixelkey:
        print pixel[0]
        print pixel[1]
        print pixel[2]
        print pixel[3]
        print pixel[4]
        print pixel[5]
        

    

##    print res
##    for c in combofile: #line in combofile
##        combolist = c.split() # create lists
##        for item in combolist:
##            res2.append(item)
##        print res2, 'res2'
##    for rec in res:
##        if rec in res2:
##            print rec
##    for chunk1 in res:
##        for chunk2 in res2:
##            if chunk1 == chunk2:
##                print chunk1, chunk2
##                newout.write(chunk1)
##            else:
##                newout.write('-9999')
##    newout.close()
##    for q, a in zip(res, res2):
##        if q == a:
##            print q, a




    

##        for item in combolist:
##            print item, 'this is item'
##        for ids in outputfile:
##            linelist = ids.split()
##            compare = linelist[0]
##            print compare, 'this is compare'
##            print item, compare, 'are these equal'
##            raw_input()    
##            if item == compare:
##                print 'yup'
##            else:
##                print '-9999'

     

##    for r in res:
##        print r

##            if r == c:
##                print 'true'
##                matches.append(c)
##            else:
##                pass
##    print matches


createOutgrids('J:/event_fireharm/z23/outfiles')
