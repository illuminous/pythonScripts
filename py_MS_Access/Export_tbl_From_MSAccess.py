import os,re,win32com.client
connection=win32com.client.Dispatch(r'ADODB.Connection')
result=win32com.client.Dispatch(r'ADODB.Recordset')

#ignore this function, it does the sorting
def rev_val_srt(a,b):  #sort a list by descending count (stored in the second array index of a or b)
    return -cmp(a[1],b[1])




# Variables to be changed
database="G:/lfrdb/z02_LFRDB_20081204.mdb"  #name & location of database

mydata=dict()  #someplace to store the data in memory

#ignore these two lines
source="PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE=%s"%(database)


##query="""SELECT tbl_Products.VEG_evt, tbl_Products.VEG_esp, tbl_Products.FR_sclass, tbl_fire_effects_FLM.FLM, Count(tbl_fire_effects_FLM.FLM) AS CountOfFLM
##FROM tbl_fire_effects_FLM INNER JOIN tbl_Products ON tbl_fire_effects_FLM.Master_ID = tbl_Products.Master_ID
##GROUP BY tbl_Products.VEG_evt, tbl_Products.VEG_esp, tbl_Products.FR_sclass, tbl_fire_effects_FLM.FLM
##ORDER BY tbl_Products.VEG_evt, tbl_Products.VEG_esp;""" #paste SQL query created in Access here

table = """z01_Map_Attributes"""
connection.Open(source)
result.Open(table,connection,1,3) #open the query against the database, returns a result-set
while not result.EOF: #iterate over the records, one row at a time
    #retrieve this row's data, by column (0-based array index, so column 1 is result.Fields.Item(0).Value)

    result.MoveNext() #move to the next record in line
result.Close() #close the result-set
connection.Close()


#open an outfile
outfile = open("C:/tmp/MA.dbf",'w')
outfile.write(table)

###write a header - turn this off if reading into Arc Info table
##outfile.write("EVT,ESP,FR_Sclass,FLM,Count\n")
##
##for col1 in mydata: #for every EVT
##    for col2 in mydata[col1]: #for every ESP in this EVT
##        for col3 in mydata[col1][col2]:#for every SClass
##            temp_list=[] #temporary list for sor
##            for col4 in mydata[col1][col2][col3]: #for every FLM in this ESP/EVT/sclass combo
##                temp_list.append([col4,mydata[col1][col2][col3][col4]]) #store a pair of values - the first is the FLM, the second is the count
##            temp_list.sort(rev_val_srt)
##            
##            #now highest count FLM is at the front of this list:
##            highest_FLM = temp_list[0][0] #grab 1st entry in list, and FLM code
##            highest_count = temp_list[0][1] #grab 1st entry in list, and count
##
##            majority=1 #flag, set to 0 if multiple entries have same count as majority
##            for i in range(1,len(temp_list)): #compare cur_count to remaining counts.
##                cur_count=temp_list[i][1] #grab the count of the current entry in the remainder of temp_list
##                if highest_count==cur_count:
##                    majority=0
##                    break
##            if majority:
##                outfile.write("%s,%s,%s,%s,%s\n"%(col1,col2,col3,highest_FLM,highest_count))
##
##outfile.close()  
