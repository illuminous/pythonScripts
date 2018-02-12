"""FLM Automation  Created by Jason M. Herynk
Systems for Environmental Management
20101126"""

import os, re, csv, pickle, copy_landfire, MSAccess

data_source = "c:/temp/flm_python_outfiles_grid_combine.mdb"
user = ''
pwd = ''
mdw = ''

"""call the buildDirectories def from copy_landfire.py"""
copy_landfire.buildDirectories(1,2)
directories = copy_landfire.directories
print directories

"""call Access Datbase Class from MSAccess.py"""
db1 = MSAccess.AccessDb(data_source,user,pwd,mdw)

"""Create database connection from set data_source"""
db1conn = db1.getConn()



"""Export the combined grid .csv files to MS Access with formatting."""
def combosToAccess():
    for d in directories: #list is built from copy_landfire.py
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
###Run Access Queries to match combo tables to FLM majorities
####################################################
                
##                sql_delete_five = "DROP TABLE five" #Delete Table five - one
##                sql_delete_four = "DROP TABLE four"
##                sql_delete_three = "DROP TABLE three"
##                sql_delete_two = "DROP TABLE two"
                sql_delete_one = "DROP TABLE one"
##                db1.runQuery(sql_delete_five) #EVT Grouped
##                db1.runQuery(sql_delete_four) #EVT, EVC, EVH
##                db1.runQuery(sql_delete_three) #EVT, EVC
##                db1.runQuery(sql_delete_two) #EVT, EVH
                db1.runQuery(sql_delete_one) #EVT
                ### Setup sqlcode
                print 'creating table Evt grouped'
                sql_five = """SELECT combo.value2, Evtgrouped.evtg, Evtgrouped.FLM INTO five
                                FROM (EVT_LUT LEFT JOIN Evtgrouped ON EVT_LUT.System_group_Code = Evtgrouped.evtg) RIGHT JOIN combo ON EVT_LUT.EVT_Code = combo.EVT
                                GROUP BY combo.value2, Evtgrouped.evtg, Evtgrouped.FLM
                                HAVING (((Evtgrouped.evtg)>0) AND ((Evtgrouped.FLM)>0) AND ((combo.VALUE2)>0));"""
                print 'creating table EVT, EVC, EVH'
                sql_four = """SELECT combo.value2, combo.EVT, combo.EVC, combo.EVH, EVT_EVC_EVH.FLM INTO four
                                FROM combo LEFT JOIN EVT_EVC_EVH ON (combo.EVT = EVT_EVC_EVH.EVT) AND (combo.EVC = EVT_EVC_EVH.EVC) AND (combo.EVH = EVT_EVC_EVH.EVH)
                                WHERE (((combo.EVT)>0) AND ((combo.EVC)>0) AND ((combo.EVH)>0) AND ((EVT_EVC_EVH.FLM)>0) AND ((combo.value2)>0));"""
                print 'creating table EVT, EVC'
                sql_three = """SELECT combo.value2, EVT_EVC.EVT, EVT_EVC.EVC, EVT_EVC.FLM INTO three
                                FROM EVT_EVC RIGHT JOIN combo ON (EVT_EVC.EVT = combo.EVT) AND (EVT_EVC.EVC = combo.EVC)
                                WHERE (((EVT_EVC.EVT)>0) AND ((EVT_EVC.EVC)>0) AND ((EVT_EVC.FLM)>0) AND ((combo.value2)>0));"""
                print 'creating table EVT EVH'
                sql_two = """SELECT combo.value2, combo.EVT, combo.EVH, EVT_EVH.FLM INTO two
                                FROM combo LEFT JOIN EVT_EVH ON (combo.EVT = EVT_EVH.EVT) AND (combo.EVH = EVT_EVH.EVH)
                                WHERE (((combo.EVT)>0) AND ((combo.EVH)>0) AND ((EVT_EVH.FLM)>0) AND ((combo.value2)>0));"""
                print 'creating table Evt '
                sql_one = """SELECT combo.value2, combo.EVT, Evt.FLM INTO one
                                FROM Evt RIGHT JOIN combo ON Evt.evt = combo.EVT
                                WHERE (((combo.EVT)>0) AND ((Evt.FLM)>0) AND ((combo.value2)>0));"""
                ###Run sql code

##                db1.runQuery(sql_five)
##                db1.runQuery(sql_four)
##                db1.runQuery(sql_three)
##                db1.runQuery(sql_two)
                db1.runQuery(sql_one)

                """Call Recordset Class from MSAccess.py"""
                sql_one_res = 'SELECT one.*FROM one;'

                db3 = MSAccess.Recordset(db1conn,sql_one_res,dict)
                table_res = db3.paged(pagesize=-1)

                one_res = []
                for row in table_res:
                    one_list = row.values()
                    one_res.append(one_list)
                print one_res

                onecsv = open('c:/temp/one.csv','w')
                for item in one_res:
                    s1 = ','.join(str(item))
                    onecsv.writelines(s1)
                    onecsv.close()

            finally:
                print 'processing.....' 
                print d
        else:
            print d
            print ' file does not exist...going to the next file' # file did not exist so go to the next one in the list 'd'
combosToAccess() #execute the def combosToAccess, remove this if you want to call the def from another program
##db1.closeConn() #close the database
##"""call Recordset Class from MSAccess.py"""
##db3 = Recordset(db1conn,sql1,dict)
