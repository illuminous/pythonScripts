import csv, Use_MSAccess 
#call Access Datbase Class
db1 = AccessDb(data_source,user,pwd,mdw)
db1conn = db1.getConn()
db1tablenames = db1.getTableNames()
db1gettables = db1.getTables()
tbl_one = db1gettables['one']

#call Table Class
db2 = Table(db1conn, 'one')

#call Recordset Class
sql1 = """SELECT one.*FROM one;"""
db3 = Recordset(db1conn,sql1,dict)
db3.getFieldNames()
db3.hasRows()
pagedthing = db3.paged(pagesize=-1)
csvoutfile = csv.writer(open('c:/temp/pagething.csv', 'wb'), delimiter = ',')
for p in pagedthing:
	print p.keys()
        csvoutfile.write(p.keys())
    

for p in pagedthing:
	print p.values()
        csvoutfile.write(p.values())
        
        

 import csv
>>> w =csv.writer(file('c:/temp/holyshit.csv','wb'), dialect = 'excel')
>>> for p in pagedthing:
	print p.values()
	w.writerows(p.values())
