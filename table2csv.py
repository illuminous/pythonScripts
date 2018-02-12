"""
goal: export all the rows in a table or featureclass to a csv file or text file
Created by Samuel B on 2009/04/23, last changed 2009/06/24

url : http://gissolved.blogspot.com/2009/04/table-to-csv.html
"""
import sys, traceback, os
import arcgisscripting, copy_landfire
from copy_landfire import buildDirectories

gp = arcgisscripting.create()

##gp.workspace = r'g:/Working/FLM/FLM_Refreash/PNW/z01/z01' ## workspace of the table or feature class
table = 'combo' ## table or feature class from wich the attributes should be exported

csvseparator = ',' ## column separator field
##outputpath = r'g:/Working/FLM/FLM_Refreash/Temp/combo.csv' ## path to the file to wich the output should be written
ignorefields = [] ##list with fields to ignore

"""call the buildDirectories def from copy_landfire.py"""
copy_landfire.buildDirectories(1,20)

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
        try:
            gp.workspace = d
            outputpath = d +'/combo.csv'
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
