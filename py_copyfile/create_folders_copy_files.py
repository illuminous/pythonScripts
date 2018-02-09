import os, sys, glob, shutil
import arcgisscripting, sys, string, os
import fnmatch
gp = arcgisscripting.create()

##textFile = r'C:\\Documents and Settings\\hkreilick.LTDE7LL7L81\\Desktop\\MTBS\\mtbs_FOD.csv'
##inFile = open(textFile, "r")
##fireNames = []
##recs = 0
##output_location = 'C:\\AllFires'
##
##for line in inFile.readlines():
##    fireNames.append(line)
##    recs = recs + 1
##
##print fireNames
##inFile.close()

##for x in fireNames:
##    print x
##    p = x.rstrip('\n')
##    output_folder = '%s' % (p)
##    gp.CreateFolder_management(output_location, output_folder)
##else:
##    print 'All folders created'

root = 'k:/fe/wolf'
#List of files under a given year
path1 = 'C:\\aMTBS\\1996'
path1 = '%s/1996'%(root)

AllFiles = []
recs = 0

dirList =os.listdir(path1)
for fname in dirList:
    fname2 = fname.upper()
    AllFiles.append(fname2)
    recs = recs + 1

#print AllFiles

#List of all folders under C:\AllFires
path2 = 'C:\\AllFires'
path2 = '%s/AllFires'%(root)

AllFolders = []
recs = 0

dirList =os.listdir(path2)
for fname in dirList:
    AllFolders.append(fname)
    recs = recs + 1

for folder in AllFolders:
    print ' working on folder...', folder
    for file in AllFiles:              
        if fnmatch.fnmatch(file,'%s*'%(folder)):
            shutil.copy('%s/%s'%(path1,file), '%s/%s/%s'%(path2,folder,file))
            print 'copying file', file        
        
                      
    


























##print '-'*60  
##
##for folder in glob.glob(root):
##    print "folder =", folder
##    # select the type of file, for instance *.jpg or all files *.*
##    for file in glob.glob(folder + '/*.*'):
##        # retrieves the stats for the current file as a tuple
##        # (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime)
##        # the tuple element mtime at index 8 is the last-modified-date
##        stats = os.stat(file)
##        unique_name = name.grid(stats[0:11])
##        print 'unique_name'
##
##
##
## f = open(r'c:\test.txt', 'r').read().replace('"', '')
##>>> x = []
##>>> x.extend(f.split(","))
##>>> x
##['aa', ' bb', ' cc']
##>>> len(x)
##3
##
##
## import csv 
##>>> myfile = open(r'c:\test.txt', 'r') 
##>>> data  = csv.reader(myfile, delimiter=',') 
##>>> print data 
##<_csv.reader object at 0x00D41870> 
##>>> for item in data: 
##        print item 
##
##        
##['aaa', 'bbb', 'ccc']
