
"""TL_stage9-summaryCount.py - requires pyodbc - uses an access database to summarize
textfile outputs."""

__author__ = "Jason M. Herynk"
__copyright__ = "Copyright 2012, SEM llc"
__credits__ = [""]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Jason M. Herynk"
__email__ = "jherynk.sem@gmail.com"
__status__ = "Prototype"
import pyodbc
import os
global Rows
res = []
directories = []



geoarea = ['PNW','PSW','NC','NE','SC','SE','SW']#add back PSW



"""Build a list of directories to copy grids from and to."""
def buildDirectories(zone_number_lower, zone_number_upper, geoarea):
    for zone in range(zone_number_lower, zone_number_upper):
        res.append(zone)

        if zone < 10:
            path1 = 'G:/Working/Treelists_2012_update/%s' %(geoarea) 
            path2 = '/z0%s/' %(zone)
            path = path1+path2
            directories.append(path)
        else:
            path1 = 'G:/Working/Treelists_2012_update/%s' %(geoarea) 
            path2 = '/z%s/' %(zone)
            path = path1+path2
            directories.append(path)

    return directories


def main():    
    for g in geoarea:
        buildDirectories(1,100, g)        
    for d in directories:
        splitter = d.split('/')
        print 'working on ', splitter[4]

        conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=G:\Working\Treelists_2012_update\progs\summaryCount.accdb; Provider=MSDASQL;') #ms access connection
        curs = conn.cursor() #connection
        
        combofileloc = d + '/summary.txt' #add a combo.csv file extension
        
        if os.path.isfile(combofileloc) == True: #test to see if the file exists

            print 'file exists...preparing to process in Microsoft Access'
            combofile = open(combofileloc, 'r')
            combofile.next()
            
            curs.execute("""DROP TABLE summary""") #execute sql command
            conn.commit()
            print "deleted summary table"
            

            curs.execute("""CREATE TABLE summary(treelist INT, COUNT_ INT, fill INT)""")
            conn.commit()
            print'Re-Building Combo Table'
            for line in combofile: #iterate of the list of files and split out each column
                
                
                items = line.split(',')
                first = items[0]
                second = items[1]
                third = items[2]               
                curs.execute("""INSERT INTO summary(treelist, COUNT_, fill) VALUES  (%s, %s, %s)""" %(first, second, third)) #append data to appropriate column
                conn.commit()
            
            """make table tbl_summaryCount"""
            curs.execute("""DROP TABLE tbl_summaryCount""") #execute sql command
            conn.commit()
            curs.execute("""SELECT Summary.fill, Sum(Summary.COUNT_) AS SumOfCOUNT_ INTO tbl_summaryCount
FROM Summary
GROUP BY Summary.fill;""")
            conn.commit()

            SQL = "SELECT * FROM tbl_summaryCount"
            curs.execute("""SELECT * FROM tbl_summaryCount""")
            rows = curs.fetchall()
            txt_writer = open(d +'/%s_summaryCount.txt'%(splitter[4]), 'w')
            txt_writer.write('fill, sumofCount\n')
            for row in rows:
                rowstring = str(row[0]) +','+ str(row[1]) +'\n'
                
                txt_writer.write(rowstring)
            txt_writer.close()
    conn.close()
if __name__ == '__main__':
    main()           
