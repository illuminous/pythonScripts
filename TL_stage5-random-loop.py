from collections import defaultdict
"""TL_stage5-random-loop.py - randomly selects plots from matching plots."""

__author__ = "Jason M. Herynk"
__copyright__ = "Copyright 2012, SEM llc"
__credits__ = [""]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Jason M. Herynk"
__email__ = "jherynk.sem@gmail.com"
__status__ = "Prototype"
import random
import os
directories = []
res =[]
zoneres = []
geoarea = ['PNW','PSW','NC','SW','SC','SE','NE']


"""Build a list of directories to copy grids from and to."""
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

    return directories

def main():
    buildDirectories(1,2)   
    for d in directories:
        print d
        if os.path.isdir(d) == True:
            outfile = open(d+'/outfile.txt', 'w') # open an outfile to hold the results

            cwd = d #path to the working directory
            
            dict7 = defaultdict(list) #memory for evt/bps/sclass/cc/cbd/elv/asp
            dict6 = defaultdict(list) #memory for evt/bps/sclass/cc/cbd/elv
            dict5 = defaultdict(list) #memory for evt/bps/sclass/cc/cbd
            dict4 = defaultdict(list) #memory for evt/bps/sclass/cc
            dict3 = defaultdict(list) #memory for evt/bps/sclass
            dict2 = defaultdict(list) #memory for evt/bps
            dict1 = defaultdict(list) #memory for evt/bps


            combofiles = ['tbl_6.txt','tbl_5.txt', 'tbl_4.txt',
                          'tbl_3.txt', 'tbl_2.txt', 'tbl_1.txt'] #exported filenames from access
            organize = {'tbl_6.txt':dict6, 'tbl_5.txt':dict5,
                        'tbl_4.txt':dict4,'tbl_3.txt':dict3, 'tbl_2.txt':dict2, 'tbl_1.txt':dict1} #dictionary to point the filenames to a dictionary

            ################################################################################
            for combo in combofiles: #start looping over the combined files
                csvfile = open(cwd+'%s' %(combo),'r') #open the file
                for f in csvfile: #start looping on the lines within the file
                    item =f.split(',') #split out the columns by a ,
                    rowID = item[0] #fetch the first column
                    MasterID = item[1] #fetch the second column
                    organize.get(combo)[rowID].append(MasterID.rstrip()) #using the organize dictionary, lookup the correct dictionary and append the items to it wher the rowId is the key, and the MasterID is the value
                
                csvfile.close() #close the file
            #################################################################################
            dictlist = [dict6, dict5, dict4, dict3, dict2, dict1] #list of dictionaries
            for item in dictlist: #iterate over the dictionaries
                #print item
                for x in item: #iterate on the items 1: [1,2,3] within a dictionary       
                    listplots = item.get(x) #fetch the value for each key
                    randomplot = random.choice(listplots) #randomly chose one of the values
                    newdict = {x:randomplot} #create a new dictionary to hold the random selection
                    item.update(newdict) #using the update method, update the dictionary with only the random selection
            merged = dict(dict1.items()+ dict2.items()+ dict3.items()+ dict4.items()+ dict5.items()+ dict6.items()) #merge the dictionaries together starting with the least heterogeneous combination, working to the most heterogeneous
            #################################################################################
            findict = {}
            for i in (merged): #sort the merged dictionary by key and start iterating
                x= int(i)
                y = merged[i]
                findict[x]=y
            for key in sorted(findict.iterkeys()): #sort the merged dictionary by key and start iterating
                
                outstring =  "%s : %s\n" %(key, findict[key]) # create an outfile string
                outfile.write(outstring)
            ##    itemA = int(key)
            ##    itemB = int(merged[key])
            ##    outfile.write(itemA) #write the string to an outfile
            ##    outfile.write(' : ')
            ##    outfile.write(itemB)
            ##    outfile.write('\n')
                
            outfile.close() #close the outfile
        else:pass

if __name__ == '__main__':
    main()  


