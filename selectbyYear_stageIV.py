import arcgisscripting
import sys, traceback, os
from dbfpy import dbf
gp = arcgisscripting.create()
gp.workspace = "F:/landcover/analysis5"
res = []
firefile = open('f:/landcover/analysis5/NR_ID_001_0_FinResults.csv' , 'r')
for year in firefile:
    yearnewyear = str(year).split(',')
    year = yearnewyear[0]
    threadnewline = yearnewyear[1]
    thread = str(threadnewline.rstrip('\n'))
    ##For shapefile expression, fields are double quoted (") and text values are single quoted (')
    output = "%s_%s_select.shp" %(year, thread)
    command = '"YEAR" = %s AND "THREAD_NUM" = %s' %(year, thread)
    intersect = '%s_%s_intersect.shp' %(year,thread)
    print command
    
    try:
        # Process: Find all stream crossings (points)
        gp.select_analysis("NR_ID_001_0.shp", output,  command)
        gp.Intersect_analysis(output, intersect, "#", '#', "input")

    except:
        # If an error occurred while running a tool, print the messages.
        print gp.GetMessages()



    db = dbf.Dbf('F:/landcover/analysis5/%s_%s_intersect.dbf' %(year,thread))

    for rec in db:
        ##print rec[1], ',', rec[7],',', rec[8]
        apple = str(rec[1]) +','+str(rec[2])+','+str(rec[7])+','+ str(rec[13])
        res.append(apple)


newfile = open('F:/landcover/analysis5/Results.txt', 'w')
newfile.write('FireNum,'+'Thread,'+'Year,'+'Acres\n')
orange = set(res) #uniqify list
print orange
for item in orange:
    newfile.write(item)
    newfile.write('\n')
firefile.close()
newfile.close()











