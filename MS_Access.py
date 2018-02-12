import os,re,win32com.client
connection=win32com.client.Dispatch(r'ADODB.Connection')
result=win32com.client.Dispatch(r'ADODB.Recordset')

#ignore this function, it does the sorting
def rev_val_srt(a,b):  #sort a list by descending count (stored in the second array index of a or b)
    return -cmp(a[1],b[1])




# Variables to be changed
database="C:/treelists/treelist_archive/z01/treelistshell_median_z01.mdb" #name & location of database

mydata=dict()  #someplace to store the data in memory

#ignore these two lines
source="PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE=%s"%(database)


query="""Select tbl_TL_Median_Grid.Species_ID FROM tbl_TL_Median_Grid WHERE (((tbl_TL_Median_Grid.Species_ID)Like '***SPP'));"""
#paste SQL query created in Access here
connection.Open(source)
result.Open(query,connection,1,3) #open the query against the database, returns a result-set
while not result.EOF: #iterate over the records, one row at a time
    #retrieve this row's data, by column (0-based array index, so column 1 is result.Fields.Item(0).Value)
    col1=result.Fields.Item(0).Value  #maybe EVT?
    if col1:
        col1=int(col1)
        if not mydata.has_key(col1):
            mydata[col1]=dict()
    result.MoveNext()

    #rework the following:
    
result.Close() #close the result-set
connection.Close()
