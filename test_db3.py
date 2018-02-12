import os,re,win32com.client, copy_landfire
"""Open a MS Access Database"""
db=win32com.client.Dispatch(r'ADODB.Connection')
result=win32com.client.Dispatch(r'ADODB.Recordset')
database="c:/temp/flm_python_outfiles_grid_combine.mdb"
source="PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE=%s"%(database)
db.Open(source)
print 'database open'


"""call the buildDirectories def from copy_landfire.py"""

copy_landfire.buildDirectories(1,2)
directories = copy_landfire.directories
print directories

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
                db.Execute(sql_delete)
                print'Building Table'
                db.Execute ('CREATE TABLE combo(rowid INT, value2 INT, count2 INT, evt INT, evc INT, evh INT)') #create a table called combo in MS Access
               
                for line in combofile: #iterate of the list of files and split out each column           
                    items = line.split(',')
                    first = items[0]
                    second = items[1]
                    third = items[2]
                    forth = items[3]
                    fifth = items[4]
                    sixth = items[5]        
                    databasecode = 'INSERT INTO combo(rowid, value2, count2, evt, evc, evh) VALUES  (%s, %s, %s, %s, %s, %s)' %(first, second, third, forth, fifth, sixth) #append data to appropriate column
                    db.Execute(databasecode) #execute
                print 'iterating' #working line by line in the combo.csv file
                
####################################################
###Run Access Queries to match combo tables to FLM majorities
####################################################
                
##                sql_delete_five = "DROP TABLE five" #Delete Table five - one
##                sql_delete_four = "DROP TABLE four"
##                sql_delete_three = "DROP TABLE three"
##                sql_delete_two = "DROP TABLE two"
##                sql_delete_one = "DROP TABLE one"
##                db.Execute(sql_delete_five) #EVT Grouped
##                db.Execute(sql_delete_four) #EVT, EVC, EVH
##                db.Execute(sql_delete_three) #EVT, EVC
##                db.Execute(sql_delete_two) #EVT, EVH
##                db.Execute(sql_delete_one) #EVT
##                ### Setup sqlcode
##                print 'creating table Evt grouped'
##                sql_five = """SELECT combo.value2, Evtgrouped.evtg, Evtgrouped.FLM INTO five
##                                FROM (EVT_LUT LEFT JOIN Evtgrouped ON EVT_LUT.System_group_Code = Evtgrouped.evtg) RIGHT JOIN combo ON EVT_LUT.EVT_Code = combo.EVT
##                                GROUP BY combo.value2, Evtgrouped.evtg, Evtgrouped.FLM
##                                HAVING (((Evtgrouped.evtg)>0) AND ((Evtgrouped.FLM)>0) AND ((combo.VALUE2)>0));"""
##                print 'creating table EVT, EVC, EVH'
##                sql_four = """SELECT combo.value2, combo.EVT, combo.EVC, combo.EVH, EVT_EVC_EVH.FLM INTO four
##                                FROM combo LEFT JOIN EVT_EVC_EVH ON (combo.EVT = EVT_EVC_EVH.EVT) AND (combo.EVC = EVT_EVC_EVH.EVC) AND (combo.EVH = EVT_EVC_EVH.EVH)
##                                WHERE (((combo.EVT)>0) AND ((combo.EVC)>0) AND ((combo.EVH)>0) AND ((EVT_EVC_EVH.FLM)>0) AND ((combo.value2)>0));"""
##                print 'creating table EVT, EVC'
##                sql_three = """SELECT combo.value2, EVT_EVC.EVT, EVT_EVC.EVC, EVT_EVC.FLM INTO three
##                                FROM EVT_EVC RIGHT JOIN combo ON (EVT_EVC.EVT = combo.EVT) AND (EVT_EVC.EVC = combo.EVC)
##                                WHERE (((EVT_EVC.EVT)>0) AND ((EVT_EVC.EVC)>0) AND ((EVT_EVC.FLM)>0) AND ((combo.value2)>0));"""
##                print 'creating table EVT EVH'
##                sql_two = """SELECT combo.value2, combo.EVT, combo.EVH, EVT_EVH.FLM INTO two
##                                FROM combo LEFT JOIN EVT_EVH ON (combo.EVT = EVT_EVH.EVT) AND (combo.EVH = EVT_EVH.EVH)
##                                WHERE (((combo.EVT)>0) AND ((combo.EVH)>0) AND ((EVT_EVH.FLM)>0) AND ((combo.value2)>0));"""
##                print 'creating table Evt '
##                sql_one = """SELECT combo.value2, combo.EVT, Evt.FLM INTO one
##                                FROM Evt RIGHT JOIN combo ON Evt.evt = combo.EVT
##                                WHERE (((combo.EVT)>0) AND ((Evt.FLM)>0) AND ((combo.value2)>0));"""
##                ###Run sql code
##                db.Execute(sql_five)
##                db.Execute(sql_four)
##                db.Execute(sql_three)
##                db.Execute(sql_two)
##                db.Execute(sql_one)
##
##                fivecsv = open("c:/temp/fivetest.csv", 'w')
##                five = ("""SELECT five.*
##                            FROM five;""")
##                db.(five)
##                results = db.fetchall()
##                print results
##                res = []
##                res.append(five)
##                fivecsv.write(five)
                
            finally:
                print 'processing.....' 
                print d
        else:
            print d
            print ' file does not exist...going to the next file' # file did not exist so go to the next one in the list 'd'
combosToAccess() #execute the def combosToAccess, remove this if you want to call the def from another program
##db.Close () #close the database
