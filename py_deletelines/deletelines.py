#------------------------------------------------------------------------------
#           Name: deleteline.py
#         Author: Jason Herynk
#  Last Modified: 01/26/2009
#    Description: This Python script reads a file and prints selected lines.
#                 
#------------------------------------------------------------------------------

# read the data file in as a list
input = open("c:/tmp/z18_dm_4.out", 'r')
s = input.readlines()

# remove the first lines i.e. "the header"
del s[:26]

# write the changed data (list) to a file
output = open("c:/tmp/z18_dm_4a.out", 'w')
output.writelines(s)
output.close

    
