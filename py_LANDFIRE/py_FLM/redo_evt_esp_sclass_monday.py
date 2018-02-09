import os,re,win32com.client
connection=win32com.client.Dispatch(r'ADODB.Connection')
result=win32com.client.Dispatch(r'ADODB.Recordset')

#ignore this function, it does the sorting
def rev_val_srt(a,b):  #sort a list by descending count (stored in the second array index of a or b)
    return -cmp(a[1],b[1])




# Variables to be changed
database="C:/AWORKSPACE/flm_workspace/flm_production/MasterDB/FLM_MajorityCalls_20070403.mdb"  #name & location of database

mydata=dict()  #someplace to store the data in memory

#ignore these two lines
source="PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE=%s"%(database)


query="""SELECT tbl_Products.VEG_evt, tbl_Products.VEG_esp, tbl_Products.FR_sclass, tbl_fire_effects_FLM.FLM, Count(tbl_fire_effects_FLM.FLM) AS CountOfFLM
FROM tbl_fire_effects_FLM INNER JOIN tbl_Products ON tbl_fire_effects_FLM.Master_ID = tbl_Products.Master_ID
GROUP BY tbl_Products.VEG_evt, tbl_Products.VEG_esp, tbl_Products.FR_sclass, tbl_fire_effects_FLM.FLM
ORDER BY tbl_Products.VEG_evt, tbl_Products.VEG_esp;""" #paste SQL query created in Access here
connection.Open(source)
result.Open(query,connection,1,3) #open the query against the database, returns a result-set
while not result.EOF: #iterate over the records, one row at a time
    #retrieve this row's data, by column (0-based array index, so column 1 is result.Fields.Item(0).Value)

    #rework the following:
    col1=result.Fields.Item(0).Value  #maybe EVT?
    col2=result.Fields.Item(1).Value #maybe ESP?
    col3=result.Fields.Item(2).Value #maybe FR_Sclass?
    col4=result.Fields.Item(3).Value #maybe FLM?
    col5=int(result.Fields.Item(4).Value) #FLM count?
    #add data to memory, as a dictionary type
    if col1 and col2 and col3 and col4:#make sure these are all valid
        col1=int(col1)
        col2=int(col2)
        col3=int(col3)
        col4=int(col4)
        if not mydata.has_key(col1):
            mydata[col1]=dict()
        if not mydata[col1].has_key(col2):
            mydata[col1][col2]=dict()
        if not mydata[col1][col2].has_key(col3):
            mydata[col1][col2][col3]=dict()
        if not mydata[col1][col2][col3].has_key(col4):
            mydata[col1][col2][col3][col4]=dict()
        mydata[col1][col2][col3][col4]=col5    #this is a dictionary that stores ESP/EVT/Fr_Sclass/FLM combinations, and stores the count for each combination


    result.MoveNext() #move to the next record in line
result.Close() #close the result-set
connection.Close()



#open an outfile
outfile = open("C:/AWORKSPACE/flm_workspace/flm_production/Python_Majority_Outfiles/evt_esp_sclass.csv",'w') 

#write a header - turn this off if reading into Arc Info table
outfile.write("EVT,ESP,FR_Sclass,FLM,Count\n")

for col1 in mydata: #for every EVT
    for col2 in mydata[col1]: #for every ESP in this EVT
        for col3 in mydata[col1][col2]:#for every SClass
            temp_list=[] #temporary list for sor
            for col4 in mydata[col1][col2][col3]: #for every FLM in this ESP/EVT/sclass combo
                temp_list.append([col4,mydata[col1][col2][col3][col4]]) #store a pair of values - the first is the FLM, the second is the count
            temp_list.sort(rev_val_srt)
            
            #now highest count FLM is at the front of this list:
            highest_FLM = temp_list[0][0] #grab 1st entry in list, and FLM code
            highest_count = temp_list[0][1] #grab 1st entry in list, and count

            majority=1 #flag, set to 0 if multiple entries have same count as majority
            for i in range(1,len(temp_list)): #compare cur_count to remaining counts.
                cur_count=temp_list[i][1] #grab the count of the current entry in the remainder of temp_list
                if highest_count==cur_count:
                    majority=0
                    break
            if majority:
                outfile.write("%s,%s,%s,%s,%s\n"%(col1,col2,col3,highest_FLM,highest_count))

outfile.close()  
