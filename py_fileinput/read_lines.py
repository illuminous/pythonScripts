#------------------------------------------------------------------------------
#           Name: read_lines.py
#         Author: Kevin Harris
#  Last Modified: 02/13/04
#    Description: This Python script demonstrates how to use fileinput to read
#                 each line of a given file.
#------------------------------------------------------------------------------

import fileinput

for line in fileinput.input( "C:/tmp/tlrg.aml" ):
    print line,

raw_input( '\n\nPress Enter to exit...' )
