"""Stage4.py Creates the input files for fireharm and renames the ascii output files from Stage3.aml.  Created by Jason M.\n
Herynk 2010"""


import os
import sys
import shutil
import tempfile

resrange = []
zones =[]
res = []



##############################################################


def chunkRange():
    for chunk in range (0, 16):
        if chunk < 10:
            item1 = '0%s' %(chunk)
            res.append(item1)
        else:
            res.append(chunk)


def createInFiles(zone, path0, path1, path2):
    for chunk in res:
        myfile = path0 + zone+'_'+ '%s' %(chunk)+'.in'
        infile = open(myfile, 'w')
        infile.write('FIREHARM Driver File: Filenames and general simulation input parameters\n')   
        infile.write(path2 +'infiles/%spoly%s.in\n' %(zone, chunk))                       ##Name of input file that stores polygon values
        infile.write(path1 + 'site.in\n')                                        ##Name of input file that stores site parameters
        infile.write(path1 + 'NONE\n')                                       ##Name of input file that stores weather parms day of event (use NONE if temporal simulation)
        infile.write(path1 + 'daymet/reference/quadreg.in\n')                  ##Name of input file that stores DAYMET Quad tiles
        infile.write(path1 + 'daymet/maps/daymet_grid_pc.regimg\n')            ##Name of input map that stores DAYMET mask location values
        infile.write(path1 + 'daymet/maps/daymet_master_index_pc.regimg\n')    ##Name of input map that stores DAYMET index values
        infile.write(path1 + 'daymet/maps/daymet_us_dem_pc.regimg\n')          ##Name of input map that stores DAYMET dem elevation values
        infile.write(path1 + 'nfdrsfuel.in\n')                                   ##Name of input file that stores NFDRS fuel parameters
        infile.write(path1 + 'fbfmfuel40.in\n')                                  ##Name of input file that stores Fire behavior fuel parameters
        infile.write(path1 + 'flmfuel.in\n')                                     ##Name of input file that stores Fuel Char Class fuel parameters
        infile.write(path1 + 'tree_list.asc\n')                                  ##Name of input file that stores the tree list
        infile.write(path1 + 'fofemspp.in\n')                                    ##Name of input file that stores FOFEM species information
        infile.write(path2 +'outfiles/%s_dm_%s.out\n' %(zone, chunk))                   ##Name of output file for FIREHARM results
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
           1    150    250      1       50.0   Tree mortality (%)
           1    150    250      1       60.0   Soil heat at 2 cm
           1    150    250      1       10.0   PM2.5 smoke emissions (t\ac)
           1    150    250      1        5.0   Scorch height (m)
           1    150    250      1        2.0   Burn Severity""")
        infile.close()

def createBashFile(zone, path0, path2):
    myfile = path0 + zone + '_' + 'fireharm' + '.bash'
    print myfile
    infile = open(myfile, 'w') 
    infile.write('#!/bin/bash' + '\n')
    infile.write('datadir='+ path2 + '\n')
    infile.write('cd ${datadir}\n')
    directions = """
qsub -cwd -S /bin/bash -l hostname=compute-0-** ./%s_00.bat
qsub -cwd -S /bin/bash -l hostname=compute-0-** ./%s_01.bat
qsub -cwd -S /bin/bash -l hostname=compute-0-** ./%s_02.bat
qsub -cwd -S /bin/bash -l hostname=compute-0-** ./%s_03.bat
qsub -cwd -S /bin/bash -l hostname=compute-0-** ./%s_04.bat
qsub -cwd -S /bin/bash -l hostname=compute-0-** ./%s_05.bat
qsub -cwd -S /bin/bash -l hostname=compute-0-** ./%s_06.bat
qsub -cwd -S /bin/bash -l hostname=compute-0-** ./%s_07.bat
qsub -cwd -S /bin/bash -l hostname=compute-0-** ./%s_08.bat
qsub -cwd -S /bin/bash -l hostname=compute-0-** ./%s_09.bat
qsub -cwd -S /bin/bash -l hostname=compute-0-** ./%s_10.bat
qsub -cwd -S /bin/bash -l hostname=compute-0-** ./%s_11.bat
qsub -cwd -S /bin/bash -l hostname=compute-0-** ./%s_12.bat
qsub -cwd -S /bin/bash -l hostname=compute-0-** ./%s_13.bat
qsub -cwd -S /bin/bash -l hostname=compute-0-** ./%s_14.bat
qsub -cwd -S /bin/bash -l hostname=compute-0-** ./%s_15.bat
""" %(zone, zone, zone, zone, zone, zone, zone, zone, zone, zone, zone,
      zone, zone, zone, zone, zone)
    infile.write(directions)
    infile.close()

def createBATS(zone, path0, path2, path3):
    for chunk in res:
        batfile = path0 + '%s_%s' %(zone, chunk) + '.bat'
        print batfile
        infile = open(batfile, 'w')
        infile.write(path3 + 'FIREHARM_v6/bin/fireharm6.0T' + ' ')
        infile.write(path2 + '%s_%s' %(zone,chunk) + '.in')
        infile.close()
                     
def copyASCII():
    for chunk in res:
        filename1 = prep +'/' + zone +'/'+'cleanFiles/'+zone + '_' + '%s' %(chunk)
        print filename1
        filename2 = root + zone + '/' + 'infiles' + '/'+zone + 'poly' + '%s' %(chunk)+'.in'
        print filename2
        shutil.copy(filename1, filename2)

def buildDirectories(zone_number_lower, zone_number_upper):
    for zone in range(zone_number_lower, zone_number_upper):
        resrange.append(zone)
        if zone < 10: #fix the formating if the zone number is less than 10
            path2 = 'z0%s' %(zone)
            zones.append(path2)
        else:
            path1 = 'z%s' %(zone)
            zones.append(path1)

##########Run Calls#####
def main():
    buildDirectories(32,36)
    for z in zones:
        try:
            path0 = 'N:/data/work/FH/d.daymet/%s/' %(z)
            path1 = '/share/jherynk/data/work/FH/d.infiles/'#/mnt/pvfs2/jherynk/' + zone + '/infiles/'
            path2 = '/share/jherynk/data/work/FH/d.daymet/%s/' %(z)
            path3 = '/share/jherynk/data/work/FH/'
            chunkRange()
            createInFiles(z, path0, path1, path2)
            createBashFile(z, path0, path2)
            createBATS(z, path0, path2, path3)
        except:
            pass

if __name__ == "__main__":
    main()



##copyASCII()
