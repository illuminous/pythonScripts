import os,datetime,shutil
import arcpy
from arcpy import env
from arcpy.sa import *

####################################################
#functions
def checkPath(path):
    try: os.makedirs(path)
    except: pass

def checkPathRm(path):
    try: shutil.rmtree(path)
    except: pass
    try: os.makedirs(path)
    except: pass    

def checkDelete(indata):
    if arcpy.Exists(indata):
        arcpy.Delete_management(indata)
        print "%s deleted" % (indata)

def translateIDs(in_lookup,out_lookup):
    # read in the original file, translate characters to upper case,
    # and write the new file
    out = open(out_lookup, "w")
    for line in open(in_lookup).readlines()[1:]:
        newline = line.upper()
        out.write(newline)
    out.close()

def translateImageSummary(in_lookup,out_lookup):
    # read in the original file, translate IDs to upper case,
    # and write just "ID,delta_post" the new file
    out = open(out_lookup, "w")
    for line in open(in_lookup).readlines()[1:]:
        record = line.replace("\n","").split(",")
        fireid = record[0].upper()
        delta_post = record[2]
        newline = "%s,%s\n" % (fireid,delta_post)
        out.write(newline)
    out.close()

####################################################

# set up ArcGIS environment settings
env.outputCoordinateSystem = "E:/firesev/base/nad83_albersUSGS.prj"
env.cellSize = 30
env.pyramid = "NONE"
env.overwriteOutput = True
arcpy.CheckOutExtension("Spatial")

# Set up file for recording output messages (stdout)...
base_dir = "E:/firesev/mtbs"
today = datetime.datetime.now().strftime("%m.%d.%y")
stdout_file = "%s/mosaics/mtbs_mosaic_log9-15_%s.txt" % (base_dir,today)
stdout = open(stdout_file, "a")

# loop through regions
regions = range(1,18)
#regions = [14, 16, 17]
for regnum in regions:
    # **************************************************************************
    # set up inputs    
    models = ["rd", "ndvi"]  # needs to be a python list,usually [rd,ndvi]; maybe make it an arg?   
    work_dir = "%s/mosaics/reg%s" % (base_dir,regnum)        
    id_in = "E:/firesev/RoadMap/Step3/R%sFires.csv" % (regnum)
    id_lookup_in = "%s/mtbs_newid_lookup_05.25.11.csv" % (base_dir)
    id_lookup = id_lookup_in.replace(".csv","_nohead.csv")
    id_file = "%s/reg%s_ids_for_mosaic.csv"  % (work_dir,regnum)   
    extent_grid = "E:/firesev/RoadMap/Step2/regtile%sgd" % (regnum)
    tree_mask = "E:/firesev/RoadMap/VCT/VCT_ESP_EVC_masks/masks/rt%s_evcvct" % (regnum)
    # 1/9/12 - adding imagery summary input, so for rdnbr mosaics we
    #          can create separate mosaics for initial vs. extended assessments
    #          (based on post-fire image timing)
    image_summary_in = "%s/all/imagery_summary.csv" % (base_dir)
    image_summary = image_summary_in.replace(".csv","_nohead.csv")
    # set a switch to include image summary info or not
    #  -basically, set it to 1 if making a mosaic of RdNBR (or dNBR)
    #  -set it to zero if just doing NDVI
    include_image_timing = 1
    # **************************************************************************
    
    now = datetime.datetime.now().strftime("%m/%d/%y %I:%M:%S %p")
    print " "
    print "Starting region %s at %s..." % (regnum,now)
    stdout.write("\n")
    stdout.write("Starting region %s at %s...\n" % (regnum,now))

    # get into the working directory
    checkPath(work_dir)		    
    os.chdir(work_dir)
    env.workspace = work_dir

    # cleanup from earlier runs
    # (number is arbitrary; I'm assuming I won't ever have > 2000 temp grids)
    for g in range(1,2001):
        checkDelete("temp_%s" % (g))
        
    # format ID lookup file
    translateIDs(id_lookup_in,id_lookup)

    # format IDs in image summary (if needed)
    if include_image_timing == 1:
        translateImageSummary(image_summary_in,image_summary)

    # Create the ID file that will be used in the mosaic
    # For now, just do this with AML... could be rewritten into Python
    print "Making ID file..."
    stdout.write("Making ID file...\n")
    amlfilename = "make_id_file.aml"
    checkDelete(amlfilename)
    amlcode ="""
    &sv work_dir = %s
    &sv include_timing = %s
    &if ^ [exists %%work_dir%% -workspace] &then cw %%work_dir%%
    &workspace %%work_dir%%
    /* create a blank INFO file to add the ID lookup into
    &do t &list mtbs_id_lookup,reg_ids,reg_ids_reorder,image_timing
      &if [exists %%t%%.lut -info] &then killinfo %%t%%.lut
    &end

    tables
     define mtbs_id_lookup.lut
     master_id;5;5;i
     mtbs_id;100;100;c
     k_id;10;10;c
     k_year;4;4;i
     k_number;4;4;i;;
     
     /* add data from the CSV file
     select mtbs_id_lookup.lut
     add from %s

     /* set up a table to hold image timing info
     &sv image_summary = %s
     &if %%include_timing%% eq 1 &then
       &do
         define image_timing.lut
         mtbs_id;100;100;c
         delta_post;4;4;i;;
         /* add in data from CSV
         select image_timing.lut
         add from %%image_summary%%
       &end
     
     /* create another blank INFO file for the list of mtbs_ids for the current region
     define reg_ids.lut
     mtbs_id;100;100;c;;
     
     /* add in the list from the CSV file
     select reg_ids.lut
     add from %s 
    q

    /* join the two tables
    joinitem reg_ids.lut mtbs_id_lookup.lut reg_ids.lut mtbs_id

    /* create a copy with items in the correct order
    pullitems reg_ids.lut reg_ids_reorder.lut master_id mtbs_id k_id k_year k_number

    /* now join in the image timing information (delta_post attribute)
    &if %%include_timing%% eq 1 &then
      &do
        joinitem reg_ids_reorder.lut image_timing.lut reg_ids_reorder.lut mtbs_id
      &end

    /* go back into tables and unload the new file as a CSV
    tables
     /* open a CSV output file and write the header line
     &sv outfile = [open %s stat -write]
     &sv line = [subst [quote [listitem reg_ids_reorder.lut -info]] ' ' ',']
     &sv w = [write %%outfile%% %%line%%]
     &sv c = [close %%outfile%%]
     
     /* then unload all the data records into the CSV file
     sel reg_ids_reorder.lut
     unload %s
    q
    &return """ % (work_dir,include_image_timing,id_lookup,image_summary,id_in,id_file,id_file)
    amlfile = open(amlfilename, 'w')
    amlfile.write(amlcode)
    amlfile.close()

    # ...then set up the command line arguments to run the AML
    arc='C:/arcgis/arcexe10x/bin/arc.exe'
    args=['arc',"&r %s"%(amlfilename)]
    os.spawnv(os.P_WAIT,arc,args)

    ##################################################
    # iterate through models to mosaic and create annual mosaics
    for model in models:
        # do some set up for splitting out initial vs. extended assessment mosaics
        if model == "rd" and include_image_timing == 1:
            models_out = ["rdi","rde"]
        else:
            models_out = [model]
        
        # set up a loop for each output mosaic; start a timer
        for model_out in models_out:
            now = datetime.datetime.now().strftime("%m/%d/%y %I:%M:%S %p")
            print "Starting to process annual %s mosaics at %s..." % (model_out,now)
            stdout.write("Starting to process annual %s mosaics at %s...\n" % (model_out,now))

            # Create the yearly mosaics
            for year in range(1984,2011):#range(1984,2008):
                # set the source directory for grids from the current year
                year_dir = "%s/grids/%s/%s_clip" % (base_dir,year,model)
                # create a temp directory to use in the mosaic
                temp_dir = "%s/d_temp%s" % (work_dir,year)
                checkPathRm(temp_dir)
                # iterate through the ID file and add selected grids into a directory to mosaic   
                for line in open(id_file).readlines()[1:]:
                    record = line.replace("\n","").split(",")
                    master_id = int(record[0])
                    k_id = record[2].replace("'","")
                    id_year = int(record[3])
                    if include_image_timing == 1:
                        delta_post = int(record[5])

                    # check to see if id_year matches current year
                    # ...if so, copy it into the temp directory
                    if model_out == "rdi":
                        if id_year == year and delta_post <= 180 and delta_post > 0:
                            k_grid = "%s/%s_%s" % (year_dir,model,k_id)
                            out_grid = "%s/%s_%s" % (temp_dir,model,k_id)
                            print "Getting grid %s_%s, year = %s" % (model,k_id,year)
                            stdout.write("Getting grid %s_%s, year = %s\n" % (model,k_id,year))
                            arcpy.Copy_management(k_grid,out_grid)
                    elif model_out == "rde":
                        if id_year == year and delta_post > 180 and delta_post < 9999:
                            k_grid = "%s/%s_%s" % (year_dir,model,k_id)
                            out_grid = "%s/%s_%s" % (temp_dir,model,k_id)
                            print "Getting grid %s_%s, year = %s" % (model,k_id,year)
                            stdout.write("Getting grid %s_%s, year = %s\n" % (model,k_id,year))
                            arcpy.Copy_management(k_grid,out_grid)        
                    elif id_year == year:
                        k_grid = "%s/%s_%s" % (year_dir,model,k_id)
                        out_grid = "%s/%s_%s" % (temp_dir,model,k_id)
                        print "Getting grid %s_%s, year = %s" % (model,k_id,year)
                        stdout.write("Getting grid %s_%s, year = %s\n" % (model,k_id,year))
                        arcpy.Copy_management(k_grid,out_grid)
                    
                # once all grids are in the temp workspace, create a new empty raster
                # (only do this if there are grids for this year)
                env.workspace = temp_dir
                grids_to_merge = arcpy.ListRasters("*", "GRID")
                env.workspace = work_dir
                if len(grids_to_merge) > 0:
                    env.extent = extent_grid
                    env.mask = extent_grid
                    mosaic_dir = "%s/%s" % (work_dir,model)
                    checkPath(mosaic_dir)
                    mosaic_all = "%s/%s_%s" % (mosaic_dir,model_out,year)
                    print "Creating a new empty grid..."
                    stdout.write("Creating a new empty grid...\n")
                    outNewMosaic = SetNull(extent_grid,1)
                    outNewMosaic.save(mosaic_all)

                    # then mosaic all temp grids into the new rater
                    print "Creating a mosaic of all data for %s..." % (year)
                    stdout.write("Creating a mosaic of all data for %s...\n" % (year))
                    arcpy.WorkspaceToRasterDataset_management(temp_dir,mosaic_all)

                # finally, get rid of the temp directory with all the temp rasters
                # and reset the mask
                shutil.rmtree(temp_dir)
                env.mask = extent_grid
                now = datetime.datetime.now().strftime("%m/%d/%y %I:%M:%S %p")
                print "Finished %s mosaics for %s at %s" % (model_out,year,now)
                stdout.write("Finished %s mosaics for %s at %s\n" % (model_out,year,now))

    now = datetime.datetime.now().strftime("%m/%d/%y %I:%M:%S %p")
    print "Finished processing region %s mosaics at %s" % (regnum,now)
    stdout.write("Finished processing region %s mosaics at %s\n" % (regnum,now))

stdout.close() # close the output
