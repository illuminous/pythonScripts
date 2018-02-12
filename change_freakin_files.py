

#Import system modules
#First Section creates mask for removing 3km buffer on grids
#Second Section copies all western grids off K, then removes buffer, then deletes original
#Third Section mosaics to new -GRID CANNOT EXIST, and IT WON'T OVERWRITE, and joinsitem at end

import glob, arcgisscripting, os
# Create the Geoprocessor object
gp = arcgisscripting.create()
gp.CheckOutExtension("spatial")
gp.AddToolBox
gp.toolbox = "management"


w = ['NR_MT']#, '22', '21']#, '22']#, '02', '03', '04', '05', '06', '07', '08', '09', '10', '12', '13', '14', '15', '16', '17', '18', '19', '20',
    #'21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '33', '34'] #these are western zones remapped by fuels
#e = ['31', '32', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51',
    #'52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '98', '99']
#a = ['67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '97', '77', '78']


zone = w
name = ['_002']#, '_002', '_003', '_004', '_005', '_006', '_007', '_008', '_009', '_010']#_bps', '_cbd', '_ch', '_cbh', '_cc', '_clay', '_dem', '_evt','_fb40','_flm', '_sand', '_sdep', '_silt']
        #done '_bps', '_cbd', '_cbh', '_cc', '_clay', '_dem', '_evt'
oldname = ['_STANDARD0_burnprob.asc', '_STANDARD0_burnprob.asc_FLP.txt', '_STANDARD0_burnprob.asc_MeanIntensity.asc', '_STANDARD0_burnprob.asc_FireSizeList.txt']
newname = ['_SB.asc', '_FLP.txt', '_MI.asc', '_FSL.txt']
directory = 'C:\\working\\FPA\\MT_20090608\\test\\'

#First Section: Rename the FPA files into a consistent format




                
for x in zone:
    print x
    for i in name:
        print x+i
        for h in newname:
            print x + i + h
            for j in oldname:
                print x + i + j
                newfilename = 'C:\\working\\FPA\\MT_20090608\\test\\' '%s%s%s' %(x, i, h)
                oldfilename = 'C:\\working\\FPA\\MT_20090608\\test\\' '%s%s%s' %(x, i, j)
                for file in os.listdir(directory):
                    if '%s%s%s' %(x, i, j) in file:
                        os.rename(oldfilename, newfilename)
##                if os.path.exists(oldfilename):
##                     os.rename(oldfilename, newfilename)

