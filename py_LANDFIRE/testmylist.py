import arcgisscripting
gp = arcgisscripting.create()

i=['_frcc', '_dep']
for x in i:
	
	gp.WorkSpace ='C:\\WorkSpace\\frcc_depm\\' 
	OutWorkspace = 'C:\\WorkSpace\\mosaics\\'
	rasters = gp.ListRasters("*%s*"%(x), "GRID") 
	raster = rasters.next()
	mystring = ""
	while raster:
		mystring = mystring +(raster) + "; "
		raster = rasters.next()
##	else:
##            gp.MosaicToNewRaster_management(mylist, OutWorkspace, x, "#", "#", "120", "#", "#", "#") 

            




##import arcgisscripting
##gp = arcgisscripting.create()
##
##i=['_frcc', '_dep']
##for x in i:
##	
##	gp.WorkSpace ='C:\\WorkSpace\\frcc_depm\\' 
##	OutWorkspace = 'C:\\WorkSpace\\mosaics\\'
##	rasters = gp.ListRasters("*%s*"%(x), "GRID") 
##	raster = rasters.next()
##	mylist = []
##	while raster:
##		mylist.append('%s;'%(raster))
##		raster = rasters.next()
##	else:
##            gp.MosaicToNewRaster_management(mylist, OutWorkspace, '%s_mos', "#", "#", "120", "#", "#", "#") %(x)
