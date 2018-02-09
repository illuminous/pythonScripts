#------------------------------------------------------------------------------
#           Name: deleteline.py
#         Author: Jason Herynk
#  Last Modified: 01/26/2009
#    Description: This Python script reads a file and prints selected lines.
#                 
#------------------------------------------------------------------------------
import os,re,win32com.client
connection=win32com.client.Dispatch(r'ADODB.Connection')
result=win32com.client.Dispatch(r'ADODB.Recordset')

# input = open("c:/tmp/z08poly1.asc", 'r')
# s = input.readlines()


#unique_lines = list(set(open('c:/tmp/z08poly1.asc', 'r').read().splitlines()))

#output = open("c:/tmp/z08poly2.asc", 'w')
#output.writelines
#output.close

f = open("c:/tmp/z08poly1.asc")
f2 = open("c:/tmp/z08poly2.asc", "w")
uniquelines = set(f.read().split("\n"))
f2.write("".join([line + "\n" for line in uniquelines]))
f2.close()
