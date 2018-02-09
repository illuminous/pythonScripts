"""
goal: export all the rows in a table or featureclass to a csv file or text file
Created by Samuel B on 2009/04/23, last changed 2009/06/24

url : http://gissolved.blogspot.com/2009/04/table-to-csv.html
"""
import sys, traceback, os
import arcgisscripting

gp = arcgisscripting.create()

gp.workspace = r'c:/Temp' ## workspace of the table or feature class
table = 'z47_combo' ## table or feature class from wich the attributes should be exported

csvseparator = ',' ## column separator field
outputpath = r'c:/Temp/dog.csv' ## path to the file to wich the output should be written
ignorefields = [] ##list with fields to ignore

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

try:
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
