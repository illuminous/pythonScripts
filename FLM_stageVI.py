"""FLM_stageVI.py
Converts CSV files to ESRI dbase File Format
Command to Execute: csvToDbase()"""

__author__ = "Jason M. Herynk"
__copyright__ = "Copyright 2011, SEM Systems for Environmental Management"
__credits__ = [""]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Jason M. Herynk"
__email__ = "jherynk.sem@gmail.com"
__status__ = "Prototype"

import os
import re
import csv
import FLM_stageIII
import time
import arcgisscripting

tic = time.clock() #Start the timer

gp = arcgisscripting.create()
directories = [] #clear list from memory

"""call the buildDirectories def from FLM_stageIII.py"""
FLM_stageIII.buildDirectories(1,100)
directories = FLM_stageIII.directories
print directories

####################################################
##########Convert CSV's to ESRI Dbase File
####################################################
                    

csv_list = ['one', 'two', 'three', 'four', 'five']

def csvToDbase():    
    for d in directories: #list is built from FLM_stageIII.py
        print d
        for item in csv_list:
            csvfileloc = d + '/%s.csv' %(item) #add a combo.csv file extension
            if os.path.isfile(csvfileloc) == True:
                try:             
                    print 'Converting csv files'
                    gp.OverWriteOutput = 1
                    gp.TableToDbase_conversion(csvfileloc, d)
                except:
                    # If an error occurred print the message to the screen
                    print gp.GetMessages()       
            else:
                print 'csv path does not exist'
    
csvToDbase()
toc = time.clock()
totaltime = toc - tic
print 'Total Processing Time Equals'
print totaltime
