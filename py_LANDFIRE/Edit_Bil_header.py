# IMPORT MODULES
import re
import sys
exit_code = 0
#####  OPEN THE INPUT TEXT FILE WITH NAMES OF ALL FILES ######
#####  Input file MUST be comma delimated For example:
#####  I:,z18,Gradients,z18f_av_cwdci.hdr

infile   = "I:\\z18\\z18_headers.txt"
infil    = open(infile,"r")

#####  DIRECTORY TO STORE THE NEW HEADER FILES - should be a csv list of all .hdr files you want to change ######
#####  DANGER - The outdir MUST have a \\ at the end of it!!!

outdir   = "I:\\z18\\new_headers\\"
files = infil.readlines()

#####  DIRECTORY WHERE ALL THE HEADER FILES ARE STORED ######
#####  DANGER - The indir MUST have a \\ at the end of it!!!
indir = "I:\\z18\\Gradients\\"


##### Name and directory of the king .BLW file ######
##### example:  E:\\Fuels_Mapping\\NATIONAL\\z18\\rectified\\Z18_BPS3RF.blw
king_blw_name = "E:\\Fuels_Mapping\\NATIONAL\\z18\\rectified\\Z18_BPS3RF.blw"

print len(files)
print "start new"
for i in range(1,len(files)):	#The number of loops is = to the # of lines in files.
    ##### "Zero the text out so the names dont get too big" ######
    in_header_file = ""
    outfile = ""
    fullpath  = files[i]
    print fullpath
    line_list  = files[i].split(',')#split into a list using slash as delimiter 
    num = len(line_list)
    file_place = num - 1
    file = line_list[file_place]
    print file

    ##### DEFINE IN AND OUTPUT HEADER FILES ######
    in_header_file += str("%s%s"%(indir, file))
    outfile += str("%s%s"%(outdir, file))
    new_outfilename = outfile.replace("\n",'')
    new_filename = in_header_file.replace("\n",'')
    ##### OPEN IN AND OUTPUT HEADER FILES ######
    in_header_fil = open(new_filename, "r")
    outfil    = open(new_outfilename,"w")
    inblw    = open(king_blw_name,"r")
    
    ##### READ THE FIRST 8 LINES OF EACH HEADER #####
    for i in range(1,9):
        content = in_header_fil.readline()
        outfil.write(content)
    outfil.write("BANDGAPBYTES         0")
    #blwcontent = inblw.readlines()
  
    ##### CLOSE THE HEADER I/O FILES ######
    outfil.close()
    in_header_fil.close()
   # outfile = ""
    #outfile += str("%s%s"%(outdir, file))
    
infil.close()      
            
            
    