import os, sys, copy_landfire
from win32com.client.gencache import EnsureDispatch as Dispatch

##"""Open the grid combination csv file, skip the header with the .next method"""
##combofileloc = "c:/temp/dog.csv" 
##combofile = open(combofileloc, 'r')
##combofile.next()
##print 'connecting to db'

"""call the buildDirectories def from copy_landfire.py"""
#Create empty list
res = []
directories = []
combos = []
copy_landfire.buildDirectories(1,2)

"""open the MS Access database"""
DATABASE_FILEPATH = r"c:\temp\FLM_Python_Outfiles_Grid_Combine.accdb"
CONNECTION_STRING = "Provider=Microsoft.Jet.OLEDB.4.0; data Source=%s" % \
DATABASE_FILEPATH

if os.path.exists (DATABASE_FILEPATH):
    os.remove (DATABASE_FILEPATH)

adox = Dispatch ("ADOX.Catalog")
adox.Create (CONNECTION_STRING)
adox = None
db = Dispatch ('ADODB.Connection')
db.Open (CONNECTION_STRING)
print 'datbase open'   

def combosToAccess():
    for d in directories: #list is built from copy_landfire.py
        combofileloc = d + '/combo.csv'
        combofile = open(combofileloc, 'r')
        combofile.next()
        try:
            db.Execute ('CREATE TABLE combo(rowid INT, value2 INT, count2 INT, evt INT, evc INT, evh INT)')

            print'Building Table'
             
            for line in combofile:
                print 'iterating'
                items = line.split(',')
                first = items[0]
                second = items[1]
                third = items[2]
                forth = items[3]
                fifth = items[4]
                sixth = items[5]
                       
                databasecode = 'INSERT INTO combo(rowid, value2, count2, evt, evc, evh) VALUES  (%s, %s, %s, %s, %s, %s)' %(first, second, third, forth, fifth, sixth)
                db.Execute(databasecode)

        finally:
            db.Close ()  
##except:
##    print 'whoops'



##    try:
##        db.Execute ('SELECT id, newdata FROM dtest')
##    except:
##    print "FAILED as expected"
##    else:
##    print "SUCCEEDED unexpectedly"
##
##    try:
##    db.Execute ('SELECT id, data FROM dtest')
##    except:
##    print "FAILED unexpectedly"
##    else:
##    print "SUCCEEDED as expected"
##
##    adox = Dispatch ("ADOX.Catalog")
##    adox.ActiveConnection = db
##    adox.Tables ("dtest").Columns ("data").Name = "newdata"
##    adox.Tables.Refresh ()
##    finally:
##    db.Close ()
##
##    db = Dispatch ('ADODB.Connection')
##    db.Open (CONNECTION_STRING)
##    try:
##
##    try:
##    db.Execute ('SELECT id, data FROM dtest')
##    except:
##    print "FAILED as expected"
##    else:
##    print "SUCCEEDED unexpectedly"
##
##    try:
##    db.Execute ('SELECT id, newdata FROM dtest')
##    except:
##    print "FAILED unexpectedly"
##    else:
##    print "SUCCEEDED as expected"
##

