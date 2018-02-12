"""FLM_stageIV.py
goal: export all the rows in a table or featureclass to a csv file or text file
Created by Samuel B on 2009/04/23, last changed 2009/06/24, modified to work on
FLM directory structure by Jason M. Herynk
url : http://gissolved.blogspot.com/2009/04/table-to-csv.html
command to run: export_csvfiles()
"""

__author__ = "Jason M. Herynk"
__copyright__ = "Copyright 2011, SEM Systems for Environmental Management"
__credits__ = [""]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Jason M. Herynk"
__email__ = "jherynk.sem@gmail.com"
__status__ = "Prototype"

import sys, traceback, os
import arcgisscripting
import FLM_stageIII 

gp = arcgisscripting.create()

table = 'combo' ## table or feature class from wich the attributes should be exported
csvseparator = ',' ## column separator field
ignorefields = [] ##list with fields to ignore

"""call the buildDirectories def from copy_landfire.py"""

##FLM_stageIII.buildDirectories(1,100)
directories = FLM_stageIII.directories

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


export_csvfiles()
