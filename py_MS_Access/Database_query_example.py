import win32com.client
MTDB_filename=r'c:/MTDB_test.mdb'  # name of you Access database file
source="PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE=%s"%(MTDB_filename)
connection=win32com.client.Dispatch(r'ADODB.Connection')
result=win32com.client.Dispatch(r'ADODB.Recordset')      
connection.Open(source)
query = """SELECT * from AllModels;"""
result.Open(query,connection,1,3)
# not sure exactly how but you should be able to get a record count
# at this point - result.count maybe?

while not result.EOF:
    # do line by line operations on the query result if needed
    print result.fields.Item(2).Value   #print value in the 3rd field
    result.MoveNext()

result.Close()  # close the recordset
connection.Close()  #close the connection to the database
