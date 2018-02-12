import pyodbc
con = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=G:\Working\Treelists_2012_update\PNW\data_analysis\Copy of PNW.accdb; Provider=MSDASQL;')
cur = con.cursor()
string = """SELECT Table3.Field1 INTO contest FROM Table3 WHERE (((Table3.Field1)=3))"""#;#""CREATE TABLE TestTable(symbol varchar(15), leverage double, shares integer, price double)"

cur.execute(string)

con.commit()
