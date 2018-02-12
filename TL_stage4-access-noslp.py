"""TL_stage4-access-noslp.py - requires the pyodbc package to access microsoft databases"""

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



geoarea = ['PNW','PSW','SC','NE','NC','SE','SW']#add back PSW

dict1 = {'PNW':'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=G:\Working\Treelists_2012_update\PNW\data_analysis\Copy of PNW.accdb; Provider=MSDASQL;',
         'PSW':'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=G:\Working\Treelists_2012_update\PSW\data_analysis\Copy of PSW.accdb; Provider=MSDASQL;',
         'NE':'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=G:\Working\Treelists_2012_update\NE\data_analysis\Copy of NE.accdb; Provider=MSDASQL;',
         'NC':'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=G:\Working\Treelists_2012_update\NC\data_analysis\Copy of NC.accdb; Provider=MSDASQL;',
         'SC':'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=G:\Working\Treelists_2012_update\SC\data_analysis\Copy of SC.accdb; Provider=MSDASQL;',
         'SE':'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=G:\Working\Treelists_2012_update\SE\data_analysis\Copy of SE.accdb; Provider=MSDASQL;',
         'SW':'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=G:\Working\Treelists_2012_update\SW\data_analysis\Copy of SW.accdb; Provider=MSDASQL;'}

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
        buildDirectories(1,2, g)


        
    for d in directories:
        splitter = d.split('/')
        
        databasestr = dict1[splitter[3]]
        print 'working on ', splitter, ' ', splitter[4]
        conn = pyodbc.connect(r'%s' %(databasestr)) #ms access connection
        curs = conn.cursor() #connection
        
        combofileloc = d + '/combo.csv' #add a combo.csv file extension
        print combofileloc
        if os.path.isfile(combofileloc) == True: #test to see if the file exists

            print 'file exists...preparing to process in Microsoft Access'
            combofile = open(combofileloc, 'r')
            combofile.next()

            print combofile
            ##if the combo table exists, delete out the previous zones data
            
            curs.execute("""DROP TABLE Combo""") #execute sql command
            conn.commit()
            print "deleted combo table"
            

            curs.execute("""CREATE TABLE Combo(VALUE_ INT, COUNT_ INT, EVT INT, BPS INT, SCLASS INT, CC INT, DEM_RC INT, ASP_RC INT)""")
            conn.commit()
            print'Re-Building Combo Table'
            for line in combofile: #iterate of the list of files and split out each column
                
                
                items = line.split(',')
                first = items[0]
                second = items[1]
                third = items[2]
                forth = items[3]
                fifth = items[4]
                sixth = items[5]
                seventh = items[6]
                eighth = items[7]
                ninth = items[8]

                
                curs.execute("""INSERT INTO Combo(VALUE_, COUNT_, EVT, BPS, SCLASS, CC, DEM_RC, ASP_RC) VALUES  (%s, %s, %s, %s, %s, %s, %s, %s)""" %(second, third, forth, fifth, sixth, seventh, eighth, ninth)) #append data to appropriate column
                conn.commit()

                
                
##            """make table tbl_7"""
##            curs.execute("""DROP TABLE tbl_7""") #execute sql command
##            conn.commit()
##            curs.execute("""SELECT Combo.VALUE_, tbl_Products_Tree_Lifeform.Fuzz_ID INTO tbl_7
##FROM Combo INNER JOIN (Canopy_Fuel_NoNull INNER JOIN tbl_Products_Tree_Lifeform ON Canopy_Fuel_NoNull.Master_ID = tbl_Products_Tree_Lifeform.Master_ID) ON (Combo.EVT = tbl_Products_Tree_Lifeform.VEG_evt) AND (tbl_Products_Tree_Lifeform.VEG_bps = Combo.BPS) AND (Combo.SCLASS = tbl_Products_Tree_Lifeform.FR_sclass) AND (Combo.CC = tbl_Products_Tree_Lifeform.FARSITE_cc) AND (Combo.DEM_RC = tbl_Products_Tree_Lifeform.dem_reclass) AND (tbl_Products_Tree_Lifeform.asp_reclass = Combo.ASP_RC) AND (Combo.SLP_RC = tbl_Products_Tree_Lifeform.slp_reclass)
##GROUP BY Combo.VALUE_, tbl_Products_Tree_Lifeform.Fuzz_ID;""")
##            conn.commit()
            
            """make table tbl_6"""
            curs.execute("""DROP TABLE tbl_6""") #execute sql command
            conn.commit()
            curs.execute("""SELECT Combo.VALUE_, tbl_Products_Tree_Lifeform.Fuzz_ID INTO tbl_6
FROM (Canopy_Fuel_NoNull INNER JOIN tbl_Products_Tree_Lifeform ON Canopy_Fuel_NoNull.Master_ID = tbl_Products_Tree_Lifeform.Master_ID) INNER JOIN Combo ON (Combo.EVT = tbl_Products_Tree_Lifeform.VEG_evt) AND (tbl_Products_Tree_Lifeform.VEG_bps = Combo.BPS) AND (Combo.SCLASS = tbl_Products_Tree_Lifeform.FR_sclass) AND (Combo.CC = tbl_Products_Tree_Lifeform.FARSITE_cc) AND (Combo.DEM_RC = tbl_Products_Tree_Lifeform.dem_reclass) AND (tbl_Products_Tree_Lifeform.asp_reclass = Combo.ASP_RC)
GROUP BY Combo.VALUE_, tbl_Products_Tree_Lifeform.Fuzz_ID;""")
            conn.commit()
            
            """make table tbl_5"""
            curs.execute("""DROP TABLE tbl_5""") #execute sql command
            conn.commit()
            curs.execute("""SELECT Combo.VALUE_, tbl_Products_Tree_Lifeform.Fuzz_ID INTO tbl_5
FROM Combo INNER JOIN (Canopy_Fuel_NoNull INNER JOIN tbl_Products_Tree_Lifeform ON Canopy_Fuel_NoNull.Master_ID = tbl_Products_Tree_Lifeform.Master_ID) ON (Combo.EVT = tbl_Products_Tree_Lifeform.VEG_evt) AND (tbl_Products_Tree_Lifeform.VEG_bps = Combo.BPS) AND (Combo.SCLASS = tbl_Products_Tree_Lifeform.FR_sclass) AND (Combo.CC = tbl_Products_Tree_Lifeform.FARSITE_cc) AND (Combo.DEM_RC = tbl_Products_Tree_Lifeform.dem_reclass)
GROUP BY Combo.VALUE_, tbl_Products_Tree_Lifeform.Fuzz_ID;""")
            conn.commit()
            
            """make table tbl_4"""
            curs.execute("""DROP TABLE tbl_4""") #execute sql command
            conn.commit()
            curs.execute("""SELECT Combo.VALUE_, tbl_Products_Tree_Lifeform.Fuzz_ID INTO tbl_4
FROM Combo INNER JOIN (Canopy_Fuel_NoNull INNER JOIN tbl_Products_Tree_Lifeform ON Canopy_Fuel_NoNull.Master_ID = tbl_Products_Tree_Lifeform.Master_ID) ON (Combo.EVT = tbl_Products_Tree_Lifeform.VEG_evt) AND (tbl_Products_Tree_Lifeform.VEG_bps = Combo.BPS) AND (Combo.SCLASS = tbl_Products_Tree_Lifeform.FR_sclass) AND (Combo.CC = tbl_Products_Tree_Lifeform.FARSITE_cc)
GROUP BY Combo.VALUE_, tbl_Products_Tree_Lifeform.Fuzz_ID;""")
            conn.commit()
            
            """make table tbl_3"""
            curs.execute("""DROP TABLE tbl_3""") #execute sql command
            conn.commit()
            curs.execute("""SELECT Combo.VALUE_, tbl_Products_Tree_Lifeform.Fuzz_ID INTO tbl_3
FROM Combo INNER JOIN (Canopy_Fuel_NoNull INNER JOIN tbl_Products_Tree_Lifeform ON Canopy_Fuel_NoNull.Master_ID = tbl_Products_Tree_Lifeform.Master_ID) ON (Combo.EVT = tbl_Products_Tree_Lifeform.VEG_evt) AND (tbl_Products_Tree_Lifeform.VEG_bps = Combo.BPS) AND (Combo.SCLASS = tbl_Products_Tree_Lifeform.FR_sclass)
GROUP BY Combo.VALUE_, tbl_Products_Tree_Lifeform.Fuzz_ID;""")
            conn.commit()
            
            """make table tbl_2"""
            curs.execute("""DROP TABLE tbl_2""") #execute sql command
            conn.commit()
            curs.execute("""SELECT Combo.VALUE_, tbl_Products_Tree_Lifeform.Fuzz_ID INTO tbl_2
FROM (Canopy_Fuel_NoNull INNER JOIN tbl_Products_Tree_Lifeform ON Canopy_Fuel_NoNull.Master_ID = tbl_Products_Tree_Lifeform.Master_ID) INNER JOIN Combo ON (Combo.EVT = tbl_Products_Tree_Lifeform.VEG_evt) AND (tbl_Products_Tree_Lifeform.VEG_bps = Combo.BPS)
GROUP BY Combo.VALUE_, tbl_Products_Tree_Lifeform.Fuzz_ID;""")
            conn.commit()

            """make table tbl_1"""
            curs.execute("""DROP TABLE tbl_1""") #execute sql command
            conn.commit()
            curs.execute("""SELECT Combo.VALUE_, tbl_Products_Tree_Lifeform.Fuzz_ID INTO tbl_1
FROM Canopy_Fuel_NoNull INNER JOIN (Combo INNER JOIN tbl_Products_Tree_Lifeform ON (tbl_Products_Tree_Lifeform.asp_reclass = Combo.ASP_RC) AND (tbl_Products_Tree_Lifeform.dem_reclass = Combo.DEM_RC) AND (Combo.EVT = tbl_Products_Tree_Lifeform.VEG_evt)) ON Canopy_Fuel_NoNull.Master_ID = tbl_Products_Tree_Lifeform.Master_ID
GROUP BY Combo.VALUE_, tbl_Products_Tree_Lifeform.Fuzz_ID;""")
            conn.commit()
            


            for c in range(1,7):
                SQL = "SELECT * FROM tbl_%s" %(c)
                curs.execute("""SELECT * FROM tbl_%s""" %(c))
                rows = curs.fetchall()
                txt_writer = open(d +'/tbl_%s.txt' %(c), 'w')
                for row in rows:
                    rowstring = str(row[0]) +','+ str(row[1])+'\n'
                    txt_writer.write(rowstring)
                txt_writer.close()
    conn.close()
if __name__ == '__main__':
    main()           
