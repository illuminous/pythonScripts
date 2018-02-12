import arcgisscripting
import sys, traceback, os
from dbfpy import dbf
gp = arcgisscripting.create()
gp.workspace = "f:/landcover/analysis5"
res = []
firefile = open('f:/landcover/analysis5/NR_ID_001_0_FinResults.csv' , 'r')
for year in firefile:
    yearnewyear = str(year).split(',')
    year = yearnewyear[0]
    threadnewline = yearnewyear[1]
    thread = str(threadnewline.rstrip('\n'))
    ##For shapefile expression, fields are double quoted (") and text values are single quoted (')
    output = "select_%s_%s" %(year, thread)
    command = '"YEAR" = %s AND "THREAD_NUM" = %s' %(year, thread)
    intersect = '%s_%s_intersect.shp' %(year,thread)
    newname = 'intersect_%s_%s' %(year,thread)
    outLocation = "f:/landcover/analysis5/analysis5.gdb/test"
##    if gp.exists(outLocation+'/'+newname):
##        pass
##    else:

    
    try:
    # Process: Find all stream crossings (points)
##        gp.select_analysis("NR_MT_003_0", output,  command)
##        gp.Intersect_analysis(output, intersect, "#", '#', "input")
##        print intersect
##            gp.FeatureClassToFeatureClass_conversion(intersect, outLocation, newname, '#', '#', '#')
        gp.TableToTable_conversion(outLocation+'/'+newname, "f:/landcover/analysis5/tables", newname)

    except:
        # If an error occurred while running a tool, print the messages.
        print gp.GetMessages()



##    db = dbf.Dbf('c:/workspace/landcover/CA_CA_002_0/tables/intersect_%s_%s.dbf' %(year,thread))
##
##    for rec in db:
##        ##print rec[1], ',', rec[7],',', rec[8]
##        apple = str(rec[3])+','+str(rec[8])+','+ str(rec[16])
##        res.append(apple)
##
##
##newfile = open('c:/workspace/landcover/CA_CA_002_0/tables/ResultsII.txt', 'w')
##newfile.write('Thread,'+'Year,'+'sqMeters\n')
##orange = set(res) #uniqify list
##print orange
##for item in orange:
##    newfile.write(item)
##    newfile.write('\n')
##firefile.close()
##newfile.close()











