"""TL_stage3-export-csv-.py exports csv files from an esri raster grid attribute table"""

__author__ = "Jason M. Herynk"
__copyright__ = "Copyright 2012, SEM llc"
__credits__ = [""]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Jason M. Herynk"
__email__ = "jherynk.sem@gmail.com"
__status__ = "Prototype"

import sys, traceback, os
import arcgisscripting


gp = arcgisscripting.create()

table = 'combo' ## table or feature class from wich the attributes should be exported
csvseparator = ',' ## column separator field
ignorefields = [] ##list with fields to ignore
geoarea = ['PNW','PSW','NC','NE','SC','SE','SW']
res = []
directories = []
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
                
def print_exception():
    tb = sys.exc_info()[2]
    l = traceback.format_tb(tb)
    l.reverse()
    tbinfo = "".join(l)
    pymsg = "ERROR:\nTraceback Info:\n" + tbinfo + "Error Info:\n    " +  str(sys.exc_type)+ ": " + str(sys.exc_value) + ""
    print pymsg

def get_fieldnames(fields, ignorefields=[]):
    fields_output = []
    for field in iter(fields.next, None):
        if not field.name in ignorefields:
            fields_output.append(field.name)
    return fields_output

def export_csvfiles():
    for d in directories:
        if os.path.exists(d):
            try:
                gp.workspace = d
                outputpath = d +'combo.csv'
                fields = gp.listfields(table)
                fieldnames = get_fieldnames(fields, ignorefields)
                print fieldnames
                rows = gp.searchcursor(table)

                output = []
                output.append(csvseparator.join(fieldnames))
                
                for row in iter(rows.next, None):
                    outputrow = []
                    for fieldname in fieldnames:
                        outputrow.append(str(row.getvalue(fieldname)))
                    outputrow = csvseparator.join(outputrow)
                    output.append(outputrow)
                print 'found', str(len(output)), 'rows'
                f = open(outputpath, 'w')
                f.write('\n'.join(output))
                f.close()
            except:
                print_exception()
                print gp.getmessages(2)
        else:pass
buildDirectories(1,100)
export_csvfiles()
