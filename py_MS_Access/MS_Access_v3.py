import os, sys
from win32com.client.gencache import EnsureDispatch as Dispatch

                     




"""Open the grid combination csv file, skip the header with the .next method, and split out each column by the comma delimiter"""
combofileloc = "c:/temp/dog.csv" 
combofile = open(combofileloc, 'r')
combofile.next()
print 'connecting to db'

DATABASE_FILEPATH = r"c:\temp\test.accdb"
CONNECTION_STRING = "Provider=Microsoft.Jet.OLEDB.4.0; data Source=%s" % \
DATABASE_FILEPATH

if os.path.exists (DATABASE_FILEPATH):
    os.remove (DATABASE_FILEPATH)

adox = Dispatch ("ADOX.Catalog")
adox.Create (CONNECTION_STRING)
adox = None
db = Dispatch ('ADODB.Connection')
db.Open (CONNECTION_STRING)
print 'made it to here'   
try:
##    db.Execute ('CREATE TABLE dtest (id INT, data INT)')
##    db.Execute ('INSERT INTO dtest (id, data) VALUES (1, 2)')
    db.Execute ('CREATE TABLE combo(rowid INT, value2 INT, count2 INT, evt INT, evc INT, evh INT)')
##    db.Execute ('INSERT INTO combo(rowid, value2, count2, evt, evc, evh) VALUES (1, 2, 3, 4, 5, 6)')
##    print' it worked'
     
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
finally:
    db.Close ()
