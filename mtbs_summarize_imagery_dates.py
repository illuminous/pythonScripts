"""
File name: mtbs_summarize_imagery_dates.py
Author: Greg Dillon
History: created Feb 25, 2010
Purpose:  To read information from MTBS metadata files and compile all info relavent
          to timing of imagery to a new output file.

Usage: Currently this script is set up to either run from IDLE (F5) or from command
       line with no arguments.  Input paths, filenames, and other variables will need
       to be checked and edited before running under conditions different from those for
       which the script was specifically written.
"""

import arcgisscripting, os, sys, shutil
from datetime import *

# useful functions...
def checkPath(path):
    try: os.makedirs(path)
    except: pass

# Setup inputs
base_dir = "H:/cbs/mtbs_sw"
out_dir = "%s/all" % (base_dir)
input_file = "%s/export_allfires_for_image_summary.csv" % (out_dir)
checkPath(out_dir)

# Set up the output CSV file that will be a lookup between BARC firenames and IDs
# go ahead and include min and max values for each class in the barc256 grid
outfile = "%s/imagery_summary.csv" % (out_dir)
out = open(outfile, "w")
print "Creating output file %s..." % (outfile)
# write the header line
out.write("master_id,mtbs_id,delta_pre,delta_post,delta_doy")
out.write(",fire_year,fire_month,fire_day,fire_doy,fire_ord")
out.write(",pre_year,pre_month,pre_day,pre_doy,pre_ord,pre_sensor,pre_scene")
out.write(",post_year,post_month,post_day,post_doy,post_ord,post_sensor,post_scene")
out.write(",offset,xshift,yshift\n")

# set up a simple dictionary of text month : numeric month
# this will be used below
months = {'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,'July':7,'August':8,
          'September':9,'October':10,'November':11,'December':12}

# process by year...
for year in range(1984,2007):    
    year_dir = "%s/mtbs_sw_%s" % (base_dir,year)
    newyear_dir = "%s/download/new_%s" % (base_dir,year)
    
    # read in the input file and loop through the fires in the list
    for line in open(input_file).readlines()[1:]:
        record = line.replace("\n","").split(",")
        master_id = int(record[0])
        mtbs_id = record[1].strip('"')
        fire_year = int(record[2])
        fire_month = int(record[3])
        fire_day = int(record[4])
        fire_doy = int(date(fire_year,fire_month,fire_day).strftime("%j")) #day of year
        fire_ord = date(fire_year,fire_month,fire_day).toordinal()  #python ordinal date
        # if the current fire is in the current year, then process the metadata...
        if fire_year == year:
            found = 0
            # try to find the metadata file in the mtbs_sw_<year> directory
            # ...if it's not there, try looking in the download/new_<year> directory
            metadata = "%s/%s_fgdc_metadata.txt" % (year_dir,mtbs_id)
            if os.access(metadata,os.F_OK):
                found = 1 
            else:
                metadata = "%s/%s_fgdc_metadata.txt" % (newyear_dir,mtbs_id)
                if os.access(metadata,os.F_OK):
                    found = 1

            # if the metadata file was found, then parse the pertinent info from it
            if found == 0:
                print "No metadata found for fire %s (master_id %s)!" % (mtbs_id,master_id)
                continue

            for line in open(metadata).readlines():
                # get pre-fire image information
                if line.count('Pre-Fire Landsat Date/Scene ID:'):
                    # clean up the line a little
                    line = line.strip("\n").replace(";",":").replace("/",":").replace(",","")
                    # split it into a list
                    record = line.split(":")
                    # get the information
                    pre_sensor = record[2]
                    pre_fulldate = record[3].strip(" ").split(" ") #list of strings: month day year
                    pre_month = months[pre_fulldate[0]]
                    pre_day = int(pre_fulldate[1])
                    pre_year = int(pre_fulldate[2])
                    pre_doy = int(date(pre_year,pre_month,pre_day).strftime("%j")) #day of year
                    pre_ord = date(pre_year,pre_month,pre_day).toordinal()  #python ordinal date
                    pre_scene = record[4].strip(" ")

                # get post-fire image information
                if line.count('Post-Fire Landsat Date/Scene ID:'):
                    # clean up the line a little
                    line = line.strip("\n").replace(";",":").replace("/",":").replace(",","")
                    # split it into a list
                    record = line.split(":")
                    # get the information
                    post_sensor = record[2]
                    post_fulldate = record[3].strip(" ").split(" ") #list of strings: month day year
                    post_month = months[post_fulldate[0]]
                    post_day = int(post_fulldate[1])
                    post_year = int(post_fulldate[2])
                    post_doy = int(date(post_year,post_month,post_day).strftime("%j")) #day of year
                    post_ord = date(post_year,post_month,post_day).toordinal()  #python ordinal date
                    post_scene = record[4].strip(" ")

                # get dNBR offset used in calculating RdNBR
                if line.count('dNBR offset value used to calculate RdNBR:'):
                    line = line.strip("\n")
                    record = line.split(":")
                    offset = int(record[1].strip(" "))

                # get X and Y shift used in registering pre-fire image to post-fire image
                if line.count('X-shift adjustment:'):
                    line = line.strip("\n")
                    record = line.split(":")
                    xshift = int(record[1].strip(" ").split(" ")[0])
                if line.count('Y-shift adjustment:'):
                    line = line.strip("\n")
                    record = line.split(":")
                    yshift = int(record[1].strip(" ").split(" ")[0])
                    
            # do some date calculations...
            # ...number of days between pre-fire image and fire
            delta_pre = fire_ord - pre_ord
            # ...number of days between fire and post-fire image
            delta_post = post_ord - fire_ord
            # ...in terms of day of year, the number of days between pre and post-fire images
            delta_doy = post_doy - pre_doy

            # now write the output file record for this fire
            out.write("%s,%s,%s,%s,%s" % (master_id,mtbs_id,delta_pre,delta_post,delta_doy))
            out.write(",%s,%s,%s,%s,%s" % (fire_year,fire_month,fire_day,fire_doy,fire_ord))
            out.write(",%s,%s,%s,%s,%s,%s,%s" % (pre_year,pre_month,pre_day,pre_doy,pre_ord,pre_sensor,pre_scene))
            out.write(",%s,%s,%s,%s,%s,%s,%s" % (post_year,post_month,post_day,post_doy,post_ord,post_sensor,post_scene))
            out.write(",%s,%s,%s\n" % (offset,xshift,yshift))
out.close()
print "Finished!"
