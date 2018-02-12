import pyodbc
import os
global Rows


res = []
directories = []
combos = []
zoneres = []
geoarea = ['PNW']#'PSW','NC','NE','SC','SE','SW']


"""Build a list of directories to copy grids from and to."""
def buildDirectories(zone_number_lower, zone_number_upper):
    for zone in range(zone_number_lower, zone_number_upper):
        res.append(zone)
        for area in geoarea:
            
            if zone < 10:
                path1 = 'G:/Working/Treelists_2012_update/%s/' %(area) 
                path2 = '/z0%s/' %(zone)
                path = path1+path2
                directories.append(path)
            else:
                path1 = 'G:/Working/Treelists_2012_update/%s/' %(area) 
                path2 = '/z%s/' %(zone)
                path = path1+path2
                directories.append(path)

    return directories

##def pyMSaccess(SQL):
##    curs.execute(SQL)
##    conn.commit()
##
##        
##def accessExport(SQL):
##    curs.execute(SQL)
##    rows = curs.fetchall()
## #   curs.close()

def main():
    reclass = 1
    combine = 1
    buildDirectories(19,20)
    conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=G:\Working\Treelists_2012_update\PNW\data_analysis\Copy of PNW.accdb; Provider=MSDASQL;') #ms access connection
    curs = conn.cursor() #connection

    
    for d in directories:
        combofileloc = d + '/combo.csv' #add a combo.csv file extension
        print combofileloc
        if os.path.isfile(combofileloc) == True: #test to see if the file exists
####            items = []
####            for item in curs.tables():
####                print item.table_name
####                items.append(item.table_name)
####                
####            print items
            print 'file exists...preparing to process in Microsoft Access'
            combofile = open(combofileloc, 'r')
            combofile.next()

            print combofile
            ##if the combo table exists, delete out the previous zones data
            
            curs.execute("""DROP TABLE Combo""") #execute sql command
            conn.commit()
            print "deleted combo table"
            

            curs.execute("""CREATE TABLE Combo(VALUE_ INT, COUNT_ INT, EVT INT, BPS INT, SCLASS INT, CC INT, DEM_RC INT, ASP_RC INT, SLP_RC INT)""")
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
                tenth = items[9]
                
                curs.execute("""INSERT INTO Combo(VALUE_, COUNT_, EVT, BPS, SCLASS, CC, DEM_RC, ASP_RC, SLP_RC) VALUES  (%s, %s, %s, %s, %s, %s, %s, %s, %s)""" %(second, third, forth, fifth, sixth, seventh, eighth, ninth, tenth)) #append data to appropriate column
                conn.commit()

                
                
            """make table tbl_7"""
            curs.execute("""DROP TABLE tbl_7""") #execute sql command
            conn.commit()
            curs.execute("""SELECT Combo.VALUE_, tbl_Products_Tree_Lifeform.Fuzz_ID INTO tbl_7
FROM Combo INNER JOIN (Canopy_Fuel_NoNull INNER JOIN tbl_Products_Tree_Lifeform ON Canopy_Fuel_NoNull.Master_ID = tbl_Products_Tree_Lifeform.Master_ID) ON (Combo.EVT = tbl_Products_Tree_Lifeform.VEG_evt) AND (tbl_Products_Tree_Lifeform.VEG_bps = Combo.BPS) AND (Combo.SCLASS = tbl_Products_Tree_Lifeform.FR_sclass) AND (Combo.CC = tbl_Products_Tree_Lifeform.FARSITE_cc) AND (Combo.DEM_RC = tbl_Products_Tree_Lifeform.dem_reclass) AND (tbl_Products_Tree_Lifeform.asp_reclass = Combo.ASP_RC) AND (Combo.SLP_RC = tbl_Products_Tree_Lifeform.slp_reclass)
GROUP BY Combo.VALUE_, tbl_Products_Tree_Lifeform.Fuzz_ID;""")
            conn.commit()
            
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

            for c in range(2,8):
                SQL = "SELECT * FROM tbl_%s" %(c)
                curs.execute("""SELECT * FROM tbl_%s""" %(c))
                rows = curs.fetchall()
                txt_writer = open(d +'/tbl_%s.txt' %(c), 'w')
                for row in rows:
                    rowstring = str(row[0]) +','+ str(row[1])+'\n'
                    txt_writer.write(rowstring)
                txt_writer.close()

if __name__ == '__main__':
    main()           
