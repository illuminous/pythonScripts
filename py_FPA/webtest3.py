import glob, urllib, zipfile, cStringIO, os



zones = ['CA_CA']#, 'CA_CA', 'SA_GA']#'EA_IL', 'EA_IN', 'NW_WA', 'SA_PR','CA_CA', 'EA_IA', 'EA_MI',/
        #'EA_MN', 'EA_MO', 'EA_NH', 'EA_NJ', 'EA_OH', 'EA_PA', 'EA_WI', 'EA_WV', 'GB_ID', 'GB_NV', /
        #'GB_UT', 'GB_WY', 'NR_ID','NR_MT', 'NR_ND', 'NW_OR', 'MW_WA', 'RM_CO', 'RM_KS', 'RM_NE', /
        #'RM_SD', 'RM_WY', 'SA_AL', 'SA_AR', 'SA_FL', 'SA_GA', 'SA_KY', 'SA_LA', 'SA_MD','SA_MS', /
        #'SA_NC', 'SA_OK', 'SA_SC', 'SA_TN', 'SA_TX', 'SA_VA', 'SW_AZ', 'SW_NM', 'SW_TX'] #these are FPUs



names = ['_002']#, '_003', '_004']#, '_005', '_006', '_007', '_008', '_009', '_010', '_011', '_012', '_013', '_014', '_015']

funky = [0-1000000000]
##oldnames = ['_STANDARD0_burnprob.asc_FLP.txt', '_STANDARD0_burnprob.asc', '_STANDARD0_burnprob.asc_MeanIntensity.asc', '_STANDARD0_burnprob.asc_FireSizeList.txt', '_TREATMENTS0_burnprob.asc', '_TREATMENTS0_burnprob.asc_FireSizeList.txt', '_TREATMENTS0_burnprob.asc_FLP.txt', '_TREATMENTS0_burnprob.asc_MeanIntensity.asc']


filename = 'c:/tmp'

for zone in zones:
    for name in names:
        for funk in funky:
            url = 'https://fpa.nwcg.gov/FPACommonREST/fpaservices/LF/SimRun/download/%s/%s%s/standard/%s' %(funk, zone, name, funk)
            zipwebfile = urllib.urlopen(url)
            buffer = cStringIO.StringIO(zipwebfile.read())
            zfile = zipfile.ZipFile(buffer)
            ##zfile.printdir()
            zfile.extractall(filename)
            zfile.close()


###First Section: Rename the FPA files into a consistent format
                
##for zone in zones:  
##    for name in names:       
##        for oldname in oldnames:                                                
##            oldfilename = 'C:\\Working\FPA\extracted\\simresults\\%s%s%s' %(zone, name, oldname)
##            newnames = dict()
##            newnames['_STANDARD0_burnprob.asc'] = '%s%s_SB.asc' %(zone, name)
##            newnames['_STANDARD0_burnprob.asc_FLP.txt'] = '%s%s_FLP.csv' %(zone, name)
##            newnames['_STANDARD0_burnprob.asc_MeanIntensity.asc'] = '%s%s_MI.asc' %(zone, name)
##            newnames['_STANDARD0_burnprob.asc_FireSizeList.txt'] = '%s%s_FSL.txt' %(zone, name)
##            newnames['_TREATMENTS0_burnprob.asc'] = '%s%s_TB.asc' %(zone, name)
##            newnames['_TREATMENTS0_burnprob.asc_FireSizeList.txt'] = '%s%s_TFSL.txt' %(zone, name)
##            newnames['_TREATMENTS0_burnprob.asc_FLP.txt'] = '%s%s_TFLP.csv' %(zone, name)
##            newnames['_TREATMENTS0_burnprob.asc_MeanIntensity.asc'] = '%s%s_TMI.asc' %(zone, name)
##            print 'oldfilename = ',oldfilename                
##            if os.access(oldfilename,os.F_OK):                
##                print 'renaming file...', oldfilename
##                newfilename = newnames[oldname]
##                os.rename(oldfilename, newfilename)
##            else:
##                print"file is not fixed or does not exist"
##
##



#####-------------------------------------------------------------------------------------------
##### Second Section: add x, y from files to create a layer
##### Set the spatial reference
##### NOTE: you must have the "Coordinate Systems" turned on
##### To do this click tools/options and check "Coordinate Systems"
##### in the General Tab
##print "Add x, y from files to create a layer"
##for zone in zones:
##    for name in names:
##        print name
##        try:
##            # Prepare the variables
##            in_Table = 'E:\\Working\\FPA\\renamed\\%s%s_FLP.csv' %(zone, name)
