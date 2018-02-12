import os, sys
from win32com.client.gencache import EnsureDispatch as Dispatch

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
    try:
        db.Execute ('CREATE TABLE dtest (id INT, data INT)')
        db.Execute ('INSERT INTO dtest (id, data) VALUES (1, 2)')
    except:
        print 'whoops'
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
##    finally:
db.Close ()
