"""Stage4.py Creates the input files for fireharm and renames the ascii output files from Stage3.aml.  Created by Jason M.\n
Herynk 2010"""


import os, sys, shutil, tempfile
zone = 'z14'
root = 'F:/daymet_fireharm/'
emds = ''
infiles = 'infiles/'
outfiles = 'outfiles/'
mode = 'daymet'
workingdir =   infiles
workingdir2 =  outfiles
infiles = root + zone 

res = []
for chunk in range (1, 21):
    res.append(chunk)

for chunk in res:
    myfile = root + zone + '/' + zone+'_'+ mode + '%s' %(chunk)+'.in'
    infile = open(myfile, 'w')
    infile.write('FIREHARM Driver File: Filenames and general simulation input parameters\n')   
    infile.write(workingdir + zone +'poly%s.in\n' %(chunk))                       ##Name of input file that stores polygon values
    infile.write(workingdir + 'site.in\n')                                        ##Name of input file that stores site parameters
    infile.write(workingdir + 'NONE\n')                                       ##Name of input file that stores weather parms day of event (use NONE if temporal simulation)
    infile.write(workingdir + 'daymet/reference/quadreg.in\n')                  ##Name of input file that stores DAYMET Quad tiles
    infile.write(workingdir + 'daymet/maps/daymet_grid_pc.regimg\n')            ##Name of input map that stores DAYMET mask location values
    infile.write(workingdir + 'daymet/maps/daymet_master_index_pc.regimg\n')    ##Name of input map that stores DAYMET index values
    infile.write(workingdir + 'daymet/maps/daymet_us_dem_pc.regimg\n')          ##Name of input map that stores DAYMET dem elevation values
    infile.write(workingdir + 'nfdrsfuel.in\n')                                   ##Name of input file that stores NFDRS fuel parameters
    infile.write(workingdir + 'fbfmfuel40.in\n')                                  ##Name of input file that stores Fire behavior fuel parameters
    infile.write(workingdir + 'flmfuel.in\n')                                     ##Name of input file that stores Fuel Char Class fuel parameters
    infile.write(workingdir + 'tree_list.asc\n')                                  ##Name of input file that stores the tree list
    infile.write(workingdir + 'fofemspp.in\n')                                    ##Name of input file that stores FOFEM species information
    infile.write(workingdir2 + zone +'_dm_%s.out\n' %(chunk))                   ##Name of output file for FIREHARM results
    infile.write("""         1           Simulation option (1-simulate for entire wx record, 2-simulated for wx condition)
         0           Verbose flag (0-no intermediate messages, 1-some benchmark messages, 2-all messages)
         3          Lapse rate option: (1-use machine constants, 2-user-specified next, 3-daily dynamic computations)
    -0.003  0.0004   Starting and ending year for DAYMET weather in FIREHARM analysis
      1980    1997   Starting and ending year for DAYMET weather in FIREHARM analysis
      5.0      200   Wind speed (mph) and direction (azmiuth) for simulaiton
    Parameters for computing probabilities of a fire event assuming ignition
    Stat Begday Endday MinDays  Threshold   Name of the parameter (STAT=0-dont compute,1-ave,2-sum), Begday=beginning day, Endday=Ending Day, Minday=Minimum number days for computation, Threshold=minimum value for computation
       1    150    250      1      100.0   NFDRS KDBI
       1    150    250      1        6.0   NFDRS Spread Component SC
       1    150    250      1      400.0   NFDRS Energy Release Component ERC
       1    150    250      1        5.0   NFDRS Burning index BI
       1    150    250      1        0.01  NFDRS Ignition Component IC
       1    150    250      1       10.0   CFFWIS FFMC Fine fuel moisture code
       1    150    250      1      100.0   CFFWIS DMC Duff moisture code
       1    150    250      1       10.0   CFFWIS DC Drought code
       1    150    250      1        5.0   CFFWIS ISI Initial spread index
       1    150    250      1        5.0   CFFWIS FWI Fire Weather index
       1    150    250      1       10.0   Spread rate (km\hr)
       1    150    250      1      350.0   Fireline intensity (kw\m)
       1    150    250      1        2.0   Flame length (m)
       1    150    250      1     1000.0   Crown fire intensity (kw\m)
       1    150    250      1       50.0   Fuel consumption (%)
       1    150    250      1       35.0   Tree mortality (%)
       1    150    250      1       60.0   Soil heat at 2 cm
       1    150    250      1       10.0   PM2.5 smoke emissions (t\ac)
       1    150    250      1        5.0   Scorch height (m)
       1    150    250      1        2.0   Burn Severity""")
    infile.close()

##for chunk in res:
##    filename1 = root + emds+'/' + zone +'/'+zone + 'poly' + '%s' %(chunk)+'.asc'
##    print filename1
##    filename2 = root + zone + '/' + 'infiles' + '/'+zone + 'poly' + '%s' %(chunk)+'.in'
##    shutil.copy(filename1, filename2)
