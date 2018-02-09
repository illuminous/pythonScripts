# Import system modules
#First Section creates mask for removing 3km buffer on grids
#Second Section copies all western grids off K, then removes buffer, then deletes original
#Third Section mosaics to new -GRID CANNOT EXIST, and IT WON'T OVERWRITE, and joinsitem at end

import arcgisscripting, os
# Create the Geoprocessor object
gp = arcgisscripting.create()
gp.CheckOutExtension("spatial")
amlfilename2 = "C:\\WorkSpace\\datalist\\grid_aml\\joinitem.aml"

w = ['01']#, '02', '03', '04', '05', '06', '07', '08', '09', '10', '12', '13', '14', '15', '16', '17', '18', '19', '20',
    #'21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '33', '34'] #these are western zones remapped by fuels
e = ['31', '32', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51',
    '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '98', '99']
a = ['67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '97', '77', '78']


zone = w
name = ['_asp']#['_prs', '_pls']#, '_mfri', '_dep', '_sclass', '_cbd', '_cbh', ,'_pls'
        #done '_frcc', '_frg', 'fbfm13', 'fbfm40', '_evt','_evc','_evh', '_pms', '_prs', '_bps', '_esp'

###First Section:  Creates zone mask
##for x in zone:    
##    InRaster = "C:\\Workspace\\mosaics_a\\lf_grid"
##    InWhereClause = "value = %s" % (x)
##    OutRaster = "C:\\Workspace\\mosaics_a\\z%s_mask" % (x)
##    kms = 'K:\\fe\\landfire\\z%s\\z%s_base\\gis\\z%s_3kgd' %(x, x, x)
##    print InWhereClause
##    Ras = gp.Describe(kms)
##    print Ras.Extent
##    if gp.exists (OutRaster):
##        print OutRaster + "exists"
##    else:
##        tempEnvironment7 = gp.extent
##        gp.extent = Ras.Extent
##        # Process: ExtractByAttribute
##        gp.ExtractByAttributes_sa(InRaster, InWhereClause, OutRaster)
##        print "next one"
##print "Masks all done"

#Second Section:  Copies grids from K, extracts by mask to remove 3km buffer, and deletes original
for x in zone:
    print x
    for i in name:
        print i
        InMask = "C:\\Workspace\\mosaics\\z%s_mask" % (x)
        LFRaster = 'K:\\fe\\landfire\\z%s\\fin_del\\gis\\z%s%s' %(x, x, i)
        OutRaster = "C:\\Workspace\\mosaics1\\z%s%s" % (x, i)
        OutRaster2 = "C:\\Workspace\\mosaics1\\z%s%s2" % (x, i)
        if gp.exists (OutRaster2):
            print OutRaster2 + "exists"
        else:
            #Process:  Copy Raster, using copy from aml
            gp.copy(LFRaster, OutRaster)
            #Process:  Extract by zone mask delet this....gp.AddToolbox("C:/Program Files/ArcGIS/ArcToolbox/Toolboxes/Spatial Analyst Tools.tbx")
            gp.ExtractByMask_sa(OutRaster, InMask, OutRaster2)
            gp.delete_management(OutRaster)

#Third Section:  Creates new mosaic, and performs joinitem at end
for x in name:
    print x
    gp.WorkSpace ='C:\\WorkSpace\\mosaics1\\' 
    OutWorkspace = 'C:\\WorkSpace\\mosaics_fin\\'
    tabs = 'C:\\WorkSpace\\datalist\\LANDFIRE_CSV\\tabs\\z%s.tab' %(x)
    OutRaster = 'C:\\WorkSpace\\mosaics_fin\\z%s'%(x) #needed for the input grid in the aml to run joinitem
    rasters = gp.ListRasters("*%s*"%(x), "GRID") 
    raster = rasters.next()
    namegrid = 'z%s'%(x)
    mystring=""
    while raster:
        mystring+=(raster) + "; "
        raster = rasters.next()
    else:
       mystring=mystring.rstrip("; ") # r meaning strip the ; on the right
       gp.MosaicToNewRaster_management(mystring, OutWorkspace, namegrid, "#", "#", "#", "#", "MAXIMUM", "#")
       print 'mosaic complete!'
       amldata = """
       &sv tabs = %s 
       &sv OutRaster = %s
       /*----join attributes to grids VAT---------------------
       joinitem %%OutRaster%%.vat %%tabs%% %%OutRaster%%.vat value
       &ty [quote Attributes successfully joined to %%OutRaster%%!]
       &workspace C:\\WorkSpace\\datalist\\grid_aml
       &end""" %(tabs, OutRaster)
       amlfile=open(amlfilename2,'w')
       #you are recreating the aml in python,
       #this is not running at this point, just revising, doesn't run until arc is opened
       #w means write, amlfilename could be an empty file, but the name needs to be there as a place holder
       amlfile.write(amldata) #points to variable amldata = above
       amlfile.close()
       #now run it!
       arc='C:/arcgis/arcexe9x/bin/arc.exe'
       args=['arc',"&r %s"%(amlfilename2)]
       os.spawnv(os.P_WAIT, arc, args)
       print 'next one!'


