"""FLM_stageV.py
Uses the combo.csv and exports it to an AccessDatabase.
Queries are run where the combo grid combination is matched to
FLM majorities for each combination.  Created 20101126
command to run: comboToAccess()
"""

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
import pickle
import MSAccess
import FLM_stageIII
import time

tic = time.clock()
data_source = "F:/LF_Refreash/FLM_Refreash/Databases/flm_python_outfiles_grid_combine.mdb"
user = ''
pwd = ''
mdw = ''

"""call the buildDirectories def from copy_landfire.py"""
FLM_stageIII.buildDirectories(1,100)
directories = FLM_stageIII.directories
print directories

"""call Access Datbase Class from MSAccess.py"""
db1 = MSAccess.AccessDb(data_source,user,pwd,mdw)

"""Create database connection from set data_source"""
db1conn = db1.getConn()



"""Export the combined grid .csv files to MS Access with formatting."""
def combosToAccess():
    for d in directories: #list is built from copy_landfire.py
        print d
        combofileloc = d + '/combo.csv' #add a combo.csv file extension
        if os.path.isfile(combofileloc) == True: #test to see if the file exists
            print 'file exists...preparing to process in Microsoft Access'
            combofile = open(combofileloc, 'r')
            combofile.next()
            try:
                ##if the combo table exists, delete out the previous zones data               
                sql_delete = "DROP TABLE combo" #execute sql command
                db1conn.Execute(sql_delete)
                print'Building Table'
                db1conn.Execute ('CREATE TABLE combo(rowid INT, value2 INT, count2 INT, evt INT, evc INT, evh INT)') #create a table called combo in MS Access
               
                for line in combofile: #iterate of the list of files and split out each column           
                    items = line.split(',')
                    first = items[0]
                    second = items[1]
                    third = items[2]
                    forth = items[3]
                    fifth = items[4]
                    sixth = items[5]        
                    databasecode = 'INSERT INTO combo(rowid, value2, count2, evt, evc, evh) VALUES  (%s, %s, %s, %s, %s, %s)' %(first, second, third, forth, fifth, sixth) #append data to appropriate column
                    db1conn.Execute(databasecode) #execute
                print 'iterating' #working line by line in the combo.csv file
####################################################
###Cleanup Database
####################################################
                
                sql_delete_five = "DROP TABLE five" #Delete Table five - one
                sql_delete_four = "DROP TABLE four"
                sql_delete_three = "DROP TABLE three"
                sql_delete_two = "DROP TABLE two"
                sql_delete_one = "DROP TABLE one"
                db1.runQuery(sql_delete_five) #EVT Grouped
                db1.runQuery(sql_delete_four) #EVT, EVC, EVH
                db1.runQuery(sql_delete_three) #EVT, EVC
                db1.runQuery(sql_delete_two) #EVT, EVH
                db1.runQuery(sql_delete_one) #EVT

####################################################
##########Combination One
####################################################
                print 'creating table Evt '
                sql_one = """SELECT combo.value2, combo.EVT, Evt.FLM INTO one
                                FROM Evt RIGHT JOIN combo ON Evt.evt = combo.EVT
                                WHERE (((combo.EVT)>0) AND ((Evt.FLM)>0) AND ((combo.value2)>0));"""
                
                db1.runQuery(sql_one)

                """Call Recordset Class from MSAccess.py in a try statement because not every query will return results"""
                try:
                    sql_one_res = 'SELECT one.*FROM one;'

                    db3 = MSAccess.Recordset(db1conn,sql_one_res,dict)
                    table_res = db3.paged(pagesize=-1)

                    one_res = []
                    for row in sorted(table_res):
                        one_list = row.values()
                        one_res.append(one_list)
                    print '********'
                    print row.keys()

                    ###Strip brackets and create strings from list of lists
                    onecsv = open(d +'/one.csv','w')
                    onecsv.write("FLM,EVT,Value\n")
                    for item in one_res:
                        str_item = str(item)[1:-1]                   
                        ##print(str_item)
                        onecsv.write(str_item +'\n')
                    onecsv.close()
                except:
                    print 'query ONE returns null results....going to next'

####################################################
##########Combination Two
####################################################
                print 'creating table EVT EVH'
                sql_two = """SELECT combo.value2, combo.EVT, combo.EVH, EVT_EVH.FLM INTO two
                                FROM combo LEFT JOIN EVT_EVH ON (combo.EVT = EVT_EVH.EVT) AND (combo.EVH = EVT_EVH.EVH)
                                WHERE (((combo.EVT)>0) AND ((combo.EVH)>0) AND ((EVT_EVH.FLM)>0) AND ((combo.value2)>0));"""
                db1.runQuery(sql_two)

                """Call Recordset Class from MSAccess.py in a try statement because not every query will return results"""
                try:
                    sql_two_res = 'SELECT two.*FROM two;'

                    db3 = MSAccess.Recordset(db1conn,sql_two_res,dict)
                    table_res = db3.paged(pagesize=-1)

                    two_res = []
                    for row in sorted(table_res):
                        two_list = row.values()
                        two_res.append(two_list)
                    print '********'
                    print row.keys()

                    ###Strip brackets and create strings from list of lists
                    twocsv = open(d+'/two.csv','w')
                    twocsv.write("EVH,FLM,EVT,Value\n")
                    for item in two_res:
                        str_item = str(item)[1:-1]                   
                        ##print(str_item)
                        twocsv.write(str_item +'\n')
                    twocsv.close()
                except:
                    print 'query TWO returns null results....going to next'
####################################################
##########Combination Three
####################################################
                print 'creating table EVT, EVC'
                sql_three = """SELECT combo.value2, EVT_EVC.EVT, EVT_EVC.EVC, EVT_EVC.FLM INTO three
                                FROM EVT_EVC RIGHT JOIN combo ON (EVT_EVC.EVT = combo.EVT) AND (EVT_EVC.EVC = combo.EVC)
                                WHERE (((EVT_EVC.EVT)>0) AND ((EVT_EVC.EVC)>0) AND ((EVT_EVC.FLM)>0) AND ((combo.value2)>0));"""
                db1.runQuery(sql_three)

                """Call Recordset Class from MSAccess.py in a try statement because not every query will return results"""
                try:
                    sql_three_res = 'SELECT three.*FROM three;'

                    db3 = MSAccess.Recordset(db1conn,sql_three_res,dict)
                    table_res = db3.paged(pagesize=-1)

                    three_res = []
                    for row in sorted(table_res):
                        three_list = row.values()
                        three_res.append(three_list)
                    print '********'
                    print row.keys()

                    ###Strip brackets and create strings from list of lists
                    threecsv = open(d+'/three.csv','w')
                    threecsv.write("FLM,EVC,EVT,Value\n")
                    for item in three_res:
                        str_item = str(item)[1:-1]                   
                        ##print(str_item)
                        threecsv.write(str_item +'\n')
                    threecsv.close()
                except:
                    print 'query THREE returns null results....going to next'
####################################################
##########Combination Four
####################################################
                print 'creating table EVT, EVC, EVH'
                sql_four = """SELECT combo.value2, combo.EVT, combo.EVC, combo.EVH, EVT_EVC_EVH.FLM INTO four
                                FROM combo LEFT JOIN EVT_EVC_EVH ON (combo.EVT = EVT_EVC_EVH.EVT) AND (combo.EVC = EVT_EVC_EVH.EVC) AND (combo.EVH = EVT_EVC_EVH.EVH)
                                WHERE (((combo.EVT)>0) AND ((combo.EVC)>0) AND ((combo.EVH)>0) AND ((EVT_EVC_EVH.FLM)>0) AND ((combo.value2)>0));"""
                db1.runQuery(sql_four)

                """Call Recordset Class from MSAccess.py in a try statement because not every query will return results"""
                try:
                    sql_four_res = 'SELECT four.*FROM four;'

                    db3 = MSAccess.Recordset(db1conn,sql_four_res,dict)
                    table_res = db3.paged(pagesize=-1)

                    four_res = []
                    for row in sorted(table_res):
                        four_list = row.values()
                        four_res.append(four_list)
                    print '********'
                    print row.keys()

                    ###Strip brackets and create strings from list of lists
                    fourcsv = open(d+'/four.csv','w')
                    fourcsv.write("EVH,FLM,EVC,EVT,Value\n")
                    for item in four_res:
                        str_item = str(item)[1:-1]                   
                        ##print(str_item)
                        fourcsv.write(str_item +'\n')
                    fourcsv.close()
                except:
                    print 'query FOUR returns null results....going to next'
####################################################
##########Combination Five
####################################################
                print 'creating table Evt grouped'
                sql_five = """SELECT combo.value2, Evtgrouped.evtg, Evtgrouped.FLM INTO five
                                FROM (EVT_LUT LEFT JOIN Evtgrouped ON EVT_LUT.System_group_Code = Evtgrouped.evtg) RIGHT JOIN combo ON EVT_LUT.EVT_Code = combo.EVT
                                GROUP BY combo.value2, Evtgrouped.evtg, Evtgrouped.FLM
                                HAVING (((Evtgrouped.evtg)>0) AND ((Evtgrouped.FLM)>0) AND ((combo.VALUE2)>0));"""
                db1.runQuery(sql_five)

                """Call Recordset Class from MSAccess.py in a try statement because not every query will return results"""
                try:
                    sql_five_res = 'SELECT five.*FROM five;'

                    db3 = MSAccess.Recordset(db1conn,sql_five_res,dict)
                    table_res = db3.paged(pagesize=-1)

                    five_res = []
                    for row in sorted(table_res):
                        five_list = row.values()
                        five_res.append(five_list)
                    print '********'
                    print row.keys()

                    ###Strip brackets and create strings from list of lists
                    fivecsv = open(d+'/five.csv','w')
                    fivecsv.write("FLM,Value,EVTg\n")
                    for item in five_res:
                        str_item = str(item)[1:-1]                   
                        ##print(str_item)
                        fivecsv.write(str_item +'\n')
                    fivecsv.close()
                except:
                    print 'query FIVE returns null results....going to next'

            finally:
                print 'processing.....' 
                
        else:
            print ' file does not exist...going to the next file' # file did not exist so go to the next one in the list 'd'

##################################
####Commands to Execute###########

combosToAccess() #execute the def combosToAccess, remove this if you want to call the def from another program
db1.closeConn() #close the database

toc = time.clock()
totaltime = toc - tic
print 'Total Processing Time Equals'
print totaltime




