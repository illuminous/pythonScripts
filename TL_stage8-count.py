import os

"""TL_stage8-count.py - creates summary textfiles of each filling process by zone """

__author__ = "Jason M. Herynk"
__copyright__ = "Copyright 2012, SEM llc"
__credits__ = [""]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Jason M. Herynk"
__email__ = "jherynk.sem@gmail.com"
__status__ = "Prototype"
import csv
import re


geoarea = ['PNW', 'PSW','NC','SW','SC','SE','NE']
dict1 = {}
dict2 = {}
res = []
directories = []
def buildDirectories(zone_number_lower, zone_number_upper):
    for zone in range(zone_number_lower, zone_number_upper):
        res.append(zone)
        for area in geoarea:
            
            if zone < 10:
                path1 = 'G:/Working/Treelists_2012_update/%s/' %(area) 
                path2 = '/z0%s/' %(zone)
                path = path1+path2
                directories.append(path)
            else:
                path1 = 'G:/Working/Treelists_2012_update/%s/' %(area) 
                path2 = '/z%s/' %(zone)
                path = path1+path2
                directories.append(path)




def makecomboDict(combofile):
    combo = open(combofile,'r')
    
    for line in combo:
        splitter = line.split(',')
        treeID = splitter[1]
        countID = splitter[2].rstrip()
        dict1[treeID]=countID


    combo.close()




def main():
    buildDirectories(1,2)
    for d in directories:
        if os.path.isdir(d) == True:
            zone = d[-4:-1]
            print 'Working on', zone, 'iterating file:'
            combofile = d+'/%s_trlst_c08.csv' %(zone)
            makecomboDict(combofile)
            for i in reversed(xrange(7)):
                if i > 0:
                    print i
                    txtfile = open(d+'/tbl_%s.txt' %(i), 'r')
                    for line in txtfile:
                        splitter = line.split(',')
                        treeID = splitter[1].rstrip()
                        #print dict1.get(valueID), i
                        if treeID in dict2:pass
                        else:
                            searchtree = str(dict1.get(treeID))
                            if searchtree == 'None':pass
                            else:
                                dict2[treeID]=searchtree+' '+str(i) 
                    txtfile.close()
            summaryfile=open(d+'/summary.txt', 'w')
            summaryfile.write("treelist, count, fill\n")
##            with open('dict.csv', 'w') as f:  # This creates the file object for the context 
##                                  # below it and closes the file automatically
            l = []
            for k, v in dict2.iteritems(): # Iterate over items returning key, value tuples.
                    
                splitter = v.split(' ')
                    
                l.append('%s, %s, %s\n' % (str(k), str(splitter[0]), str(splitter[1]))) # Build a nice list of strings
            summaryfile.write(''.join(l))  

            dict2.clear()
            dict1.clear()
                  
if __name__ == '__main__':
    main()       
