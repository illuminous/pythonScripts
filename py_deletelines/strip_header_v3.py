import os
from string import split

zones = ['z06']
root = 'C:/daymet_outfiles/%s/outfiles' %zones[0]
mode = '_dm_'
extension = '.out'
item = range(1, 21)

result=[]

for i in item:
    for z in zones:
        iterable = '%s' %(i)
        newfile = z + mode + iterable + extension 
        newlist = result.append(newfile)
    
    
##for res in result:
##    input = open(root + '//' + res, 'r') 
##    s = input.readlines()
##    del s[:26]
##    output = open(root + '//' + res, 'w') 
##    output.writelines(s)
##    output.close
##print 'header has been stripped clean'

for res in result:
    newlist = []
    
    data = open(root + '//' + res, 'r')
    wholefile = data.readlines()
    I = iter(wholefile)
    Item = I.next()
    for Item in open('c:/daymet_outfiles/z06/outfiles/test20.txt'):
        Splitter = Item.split(' ')
        newlist = [elem for elem in Splitter if elem != '']
##        newlist.append(Splitter[14])
##        newlist.append(Splitter[23])
##        newlist.append(Splitter[30])
##        newlist.extend(Splitter[153:260])
##        newlist.append('\n')
##        newlist2 = [elem for elem in newlist if elem != '']
##        modlist = ' '.join(newlist2)   
##        print modlist
##        output = open('c:/tmp/test4.txt', 'w')
##        output.writelines(modlist)
##        output.close()


    
