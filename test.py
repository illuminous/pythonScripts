import os
import re
import csv
import pickle
import MSAccess
import time

tic = time.clock()
data_source = "G:/Working/Treelists_2012_update/PNW/data_analysis/Copy of PNW.accdb"
user = ''
pwd = ''
mdw = ''

##"""call the buildDirectories def from copy_landfire.py"""
##FLM_stageIII.buildDirectories(1,100)
##directories = FLM_stageIII.directories
##print directories

"""call Access Datbase Class from MSAccess.py"""
db1 = MSAccess.AccessDb(data_source,user,pwd,mdw)

"""Create database connection from set data_source"""
db1conn = db1.getConn()
