# import modules and create geoprocessor
import arcgisscripting
gp = arcgisscripting.create()

# set workspace containing atlas and mtbs shapefiles
gp.Workspace = "c:/aaronwilson/NR_fire/shapefiles"

## select features from the Northern Rockies Atlas
#Set initial fire year
n = 1984

#Cycle through years
while n < 2004:
    
    year = str(n)
    inFC = "nr_atlas_poly.shp"
    inLyr = str("nr_atlas_%s"%(year))
    outFC = str("atlas_%s.shp"%(year))
    #Create expression with attribute to use in selection
    exp ='"FIRE_YEAR"' + " = " + year
    gp.MakeFeatureLayer_management(inFC, inLyr)

    gp.SelectLayerByAttribute_management(inLyr, "NEW_SELECTION", exp)
    gp.SelectLayerByLocation_management(inLyr, "INTERSECT", "recording_area.shp", "", "SUBSET_SELECTION")

    gp.CopyFeatures_management(inLyr, outFC)
    n = n + 1

del year, n, inFC, inLyr, outFC

## select features from mtbs data that intersect with the Atlas recording area
# Set initial fire year
n = 1984

#Cycle through years
while n < 2004:

    year = str(n)
    inFC = str("mtbs_%s.shp"%(year))
    inLyr = str("mtbs_lyr_%s"%(year))
    outFC = str("nr_mtbs_%s.shp"%(year))

    gp.MakeFeatureLayer_management(inFC, inLyr)

    gp.SelectLayerByLocation_management(inLyr, "INTERSECT", "recording_area.shp", "", "NEW_SELECTION")

    gp.Dissolve_management(inLyr, outFC, "Fire_ID")
    n = n + 1

del year, n, inFC, inLyr, outFC


##  Run union process to find intersect of Atlas and MTBS
# set workspace and add tool
gp.Workspace = "C:\\aaronwilson\\NR_fire\\shapefiles"
gp.AddToolbox("C:/Program Files/ArcGIS/ArcToolbox/Toolboxes/Analysis Tools.tbx")
wrksp = gp.Workspace

# set initial fire year
n = 1984

#Cycle through each year
while n < 2004:
    
    year = str(n)
    fcList = gp.ListFeatureClasses()
    fc = fcList.Next()
    vtab = gp.CreateObject("ValueTable")
    while fc:
        if fc == str("atlas_%s.shp"%(year)):
            print fc
            vtab.AddRow(fc)
        if fc == str("nr_mtbs_%s.shp"%(year)):
            print fc
            ##Change projection of MTBS data to match Atlas
            mtbsProj = str("nr_mtbs_%s_proj.shp"%(year))
            #define the projection file
            cs = "NAD_83_albers.prj"
            gp.project_management(fc, mtbsProj, cs) 
            vtab.AddRow(mtbsProj)
            print mtbsProj
        fc = fcList.Next()
    outFC = str("union_%s.shp"%(year))
    gp.Union_analysis(vtab, outFC, "ALL", "", "GAPS")
    del vtab
    n = n + 1
    
del n, year, fc, outFC, mtbsProj, cs, fcList

##Update Intersect Area field, and dissolve features based in Union_ID
#Set workspace containing shapefiles created above and out workspace for new shapefiles (can be the same)
gp.Workspace = "c:/aaronwilson/NR_fire/shapefiles"
outWksp = "c:/aaronwilson/NR_fires/shapefiles"

#Set initial fire year
n = 1984
#cycle through years
while n < 2004:
    year = str(n)
    inFC = str("union_%s.shp"%(year))
    fldUnion = gp.ValidateFieldName("Union_ID", outWksp)
    fldList = gp.ListFields(inFC, "Union_ID")
    if fldList.Next() == None:
        gp.AddField_management(inFC, fldUnion, "TEXT")
    else:
        print "Field exists"

    cur = gp.UpdateCursor(inFC)
    row = cur.Next()
    while row:
        atlas_id = row.GetValue("POLY_")
        mtbs_id = row.GetValue("FID_nr_mtb")
        row.Union_ID = "%s %s"%(atlas_id,mtbs_id)
        row.Intersect = 0
        cur.UpdateRow(row)
        row = cur.Next()
    unionLyr = str("union_lyr%s"%(year))
    outDslv = str("union_%s_dslv.shp"%(year))
    gp.MakeFeatureLayer_management(inFC, unionLyr)
    gp.Dissolve_management(unionLyr, outDslv, "Union_ID")

    fldAtlasNew = gp.ValidateFieldName("Atlas_ID", outWksp)
    fldMtbsNew = gp.ValidateFieldName("MTBS_ID", outWksp)
    fldList2 = gp.ListFields(outDslv, "Atlas_ID")
    if fldList2.Next() == None:
        gp.AddField_management(outDslv, fldAtlasNew, "TEXT")
        gp.AddField_management(outDslv, fldMtbsNew, "TEXT")
##        testList = gp.ListFields(outDslv)
##        print testList
    else:
        print fldList2
    fldName = gp.ValidateFieldName("Intersect", outWksp)    
    fldList3 = gp.ListFields(outDslv, "Intersect")
    if fldList3.Next() == None:
        gp.AddField_management(outDslv, fldName, "DOUBLE")
    else:
        print fldList3

    cur2 = gp.UpdateCursor(outDslv)
    row2 = cur2.Next()
    while row2:
        geo = row2.GetValue("Shape")
        area = geo.Area
        print area
        row2.Intersect = area
        fld_id = row2.GetValue("Union_ID")
        id_list = fld_id.split(" ")
        print id_list
        atlasIDnew = str(id_list[0])
        mtbsIDnew = str(id_list[1])
        row2.Atlas_ID = atlasIDnew
        row2.MTBS_ID = mtbsIDnew
        cur2.UpdateRow(row2)
        row2 = cur2.Next()
    n = n + 1
del year, n, inFC, fldUnion, fldList, cur, cur2, row, row2, unionLyr, outDslv, fldAtlasNew, fldMtbsNew, fldList2, fldName, fldList3

##Import the DBF Reader Script to read shapefile data table
###### DBF Reader Utility Function ########
def dbfreader(f):
    import struct, datetime, itertools
    """Returns an iterator over records in a Xbase DBF file.
    The first row returned contains the field names.
    The second row contains field specs: (type, size, decimal places).
    Subsequent rows contain the data records.
    If a record is marked as deleted, it is skipped.
    File should be opened for binary reads.
    """
    # See DBF format spec at:
    #     http://www.pgts.com.au/download/public/xbase.htm#DBF_STRUCT
    numrec, lenheader = struct.unpack('<xxxxLH22x', f.read(32))    
    numfields = (lenheader - 33) // 32

    fields = []
    for fieldno in xrange(numfields):
        name, typ, size, deci = struct.unpack('<11sc4xBB14x', f.read(32))
        name = name.replace('\0', '')       # eliminate NULs from string   
        fields.append((name, typ, size, deci))
    yield [field[0] for field in fields]
    yield [tuple(field[1:]) for field in fields]

    terminator = f.read(1)
    assert terminator == '\r'

    fields.insert(0, ('DeletionFlag', 'C', 1, 0))
    fmt = ''.join(['%ds' % fieldinfo[2] for fieldinfo in fields])
    fmtsiz = struct.calcsize(fmt)
    for i in xrange(numrec):
        record = struct.unpack(fmt, f.read(fmtsiz))
        if record[0] != ' ':
            continue                        # deleted record
        result = []
        for (name, typ, size, deci), value in itertools.izip(fields, record):
            if name == 'DeletionFlag':
                continue
            if typ == "N":
                value = value.replace('\0', '').lstrip()
                if value == '':
                    value = 0
                elif deci:
                    value = float(value)
                else:
                    value = int(value)
            elif typ == 'D':
                y, m, d = int(value[:4]), int(value[4:6]), int(value[6:8])
                value = datetime.date(y, m, d)
            elif typ == 'L':
                value = (value in 'YyTt' and 'T') or (value in 'NnFf' and 'F') or '?'
            result.append(value)
        yield result


# dbfreader.py
#
# based on dbf.py version 0.2 1999/11/12
# with addition of little endian
# geared to returning data for given variable names (fields)
#
# original author Michal Spalinski (mspal@curie.harvard.edu)
# additions: Luc Anselin (anselin@uiuc.edu), Luis Galvis (galvis@uiuc.edu)
#
# latest version 2005/9/26 LA
#

"""
dbfreader is a module for reading dbf files and returning the data.

Takes care of endian issue. Has methods to return a list of lists
of values or a dictionary of lists of values, based on field names.
Takes care of repeated field names (shape file issue).

Includes the missint and missfloat functions to deal with missing
values (LA).

Usage:
	import dbfreader
	db = dbfreader.dbf('mydata.dbf')
Attributes:
	db.fname          : file name
	db.nrecs          : number of records
	db.hlen           : header length in bytes
	db.rlen           : record length in bytes
	db.fields         : a list of tuples with fieldname, 
	                    numeric/character, field width, precision
	db.fieldName      : a list of field names, with duplicates indicated
	db.numfieldName   : a list of field names for numeric variables
	db.open()         : read contents
	db[i]             : return record i as a tuple of strings
	db.status()       : summary characteristics of file
	db.close()        : close file
	rec = db.listrecords( )     : returns list of formatted records
	rec = db.safe_listrecords() : returns list of formatted records, checking 
	                              for missing values (set to None)
	rec = db.listfields()       : returns a list of lists of observations
	                              by field
	                              optional arguments: a list of variable
	                              names or a list of variable index numbers
	rec = db.dictfields()       : returns a dictionary with variable name
	                              as key and observations as a list
	                              optional arguments: a list of variable
	                              names
Helper functions: missint, missfloat turn string into int or float, or
	return None for missing value (empty string)
	
"""

import struct

def missint(item):
	try:
		item1=int(item)
	except ValueError:
		return
	else:
	    return item1
	
def missfloat(item):
	try:
		item1=float(item)
	except ValueError:
		return
	else:
	    return item1

class dbf:
    def __init__(self, fname, openit=1): 
        self.fname = fname
        if openit:
            self.open()

    def open(self):
        self.f = open(self.fname,'rb') 
        head = self.f.read(32)
        (self.nrecs, self.hlen, self.rlen) = struct.unpack('<4xihh20x', head) # LA added endian
        fdalen = (self.hlen - 33)/32 

        # read field descriptor array
        fda = [] 
        for k in range(fdalen): 
            fda.append(self.f.read(32)) 

        # interpret the field descriptors

        self.fields = []
        self.fieldName = []
        self.numfieldName = []
        for fd in fda:
            bytes = struct.unpack('<12c4xBb14x', fd)   # LA added little endian
            field = '' 
            for i in range(11): 
                if bytes[i] == '\000': 
                    break 
                field = field+bytes[i] 
            ftype = bytes[11] 
            length = bytes[12] 
            dec = bytes[13] 
            self.fields.append((field,ftype,length,dec))
            self.fieldName.append(field)
        for i in range(-1,-len(self.fieldName)+1,-1):
	        freqi = self.fieldName[:i].count(self.fieldName[i])
	        if freqi:
		        self.fieldName[i] = self.fieldName[i][:11] + "_" + str(freqi)
		        self.fields[i] = self.fieldName[i],self.fields[i][1],self.fields[i][2],self.fields[i][3]
        self.numfieldName = [ i[0] for i in self.fields if i[1] == 'N' ]

    # record numbers go from 0 to self.nrecs-1
    def _get(self, recno): 
        offs = self.hlen + recno*self.rlen 
        self.f.seek(offs,0) 
        return self.f.read(self.rlen) 
     
    def __getitem__(self, recno):
        if recno < 0 or recno >= self.nrecs:
            raise IndexError
        else:
            raw = self._get(recno) 
            res = [] 
            pos = 0 
            for field in self.fields: 
                end = pos+field[2] 
                item = raw[pos+1:end+1] 
                pos=end 
                res.append(item) 
            return tuple(res)

    # return contents as list of records
    def listrecords(self):
        """Returns db file contents as list of records, formatted.

        """
        db = []
        for i in range(self.nrecs):
	        db.append(self.__getitem__(i))
        fieldFormat = []
        reclist = []
        for j in self.fields:
            if j[1] == 'N':
                if j[3] == 0:
                    fieldFormat.append(int)
                else:
                    fieldFormat.append(float)
            else:
                fieldFormat.append(str)
        for rec in db:
            rec = [ i.strip() for i in rec ]
            reclist.append( [ i(j) for (i,j) in zip(fieldFormat,rec) ] )
        return reclist
            

    # return contents as list of records allowing for missing
    def safe_listrecords(self):
        """Returns db file contents as list of records, formatted.

        Allows for missing values.
        """
        db = []
        for i in range(self.nrecs):
	        db.append(self.__getitem__(i))
        fieldFormat = []
        reclist = []
        for j in self.fields:
            if j[1] == 'N':
                if j[3] == 0:
                    fieldFormat.append(missint)
                else:
                    fieldFormat.append(missfloat)
            else:
                fieldFormat.append(str)
        for rec in db:
            rec = [ i.strip() for i in rec ]
            reclist.append( [ i(j) for (i,j) in zip(fieldFormat,rec) ] )
        return reclist

    # return contents or selected variables as list of lists
    def listfields(self,varlist=[],numlist=[]):
        """Returns db file by variable as list of lists.

        varlist specifies a list of variable names (no duplicates)
        numlist specifies a list of variable index numbers starting at 0
        """

        reclist = []
        try:
	        reclist = self.listrecords()
        except ValueError:
            reclist = self.safe_listrecords()
        columlist = []
        if varlist:
            for i in varlist:
                try:
                    j = self.fieldName.index(i)
                except ValueError:
                    print "Error: variable %s is not in file %s" % (i,self.fname)
                    return
                else:
                    columlist.append(j)
        elif numlist:
            if max(numlist) > len(self.fieldName)-1:
                print "Error: index exceeds number of variables in file %s" % self.fname
                return
            columlist = numlist
        else:
            columlist = range(len(self.fieldName))
        table = []
        table = [ [ j[i] for j in reclist ] for i in columlist ]
        return table
		
    # return contents or selected variables as dictionary of lists
    def dictfields(self,varlist=[]):
        """Returns db file by variable as list of lists.

        varlist specifies a list of variable names (no duplicates)
        """

        reclist = []
        try:
	        reclist = self.listrecords()
        except ValueError:
            reclist = self.safe_listrecords()
        columlist = []
        if varlist:
            for i in varlist:
                try:
                    j = self.fieldName.index(i)
                except ValueError:
                    print "Error: variable %s is not in file %s" % (i,self.fname)
                    return
                else:
                    columlist.append(j)
        else:
            varlist = self.fieldName
            columlist=range(len(self.fieldName))
        table = {}
        for i in columlist:
            tab = []
            tab = [ j[i] for j in reclist ]
            table[self.fieldName[i]] = tab
        return table

    def status(self):
        print ''
        print 'File              :', self.fname
        print 'Header length     :', self.hlen
        print 'Record length     :', self.rlen
        print 'Number of fields  :', len(self.fields)
        print 'Number of records :',  self.nrecs
        print ''
        print '%-12s %-12s %-12s %-12s' % ('Field','Type','Length','Decimal')
        print '%-12s %-12s %-12s %-12s' % ('-----','----','------','-------')
        for k in self.fields:
            print '%-12s %-12s %-12s %-12s' % k
        
    def close(self):
        self.f.close()

##if __name__ == "__main__":
##	import time
##	time0 = time.time()
##	db = dbf("nat.dbf")
##	time1 = time.time()
##	print "time to read db for nat.dbf: %s" % str(time1-time0)
##	time3 = time.time()
##	dlist = db.listfields()
##	time4 = time.time()
##	print "time to read db into list: %s" % str(time4-time3)
##	time5 = time.time()
##	dd = db.dictfields()
##	time6 = time.time()
##	print "time to read db into dict: %s" % str(time6-time5)
##	db.close()


##Extract the union area data from shapefile dbf files:
#Set initial fire year
n = 1984
#Cycle through years, creating a dictionary storing atlas and mtbs polygon IDs and area
while n < 2004:
    year = str(n)
    import dbfreader
    ##Must have dbfreader scripts in script directory, or specify where they can be found
    db = dbfreader.dbf("c:/aaronwilson/NR_fire/shapefiles/union_%s_dslv.dbf"%(year))
    db.open()
    data = db.listrecords()
    db.close()
    fire_polygons = dict()
    for line in data:
##        line=line.split(", ")
        atlas_poly = int(line[1])
        mtbs_poly = int(line[2])
        intersect = float(line[3])
        if not fire_polygons.has_key(atlas_poly):
            fire_polygons[atlas_poly]=dict()
        if not fire_polygons[atlas_poly].has_key(mtbs_poly):
            fire_polygons[atlas_poly][mtbs_poly]=dict()
        if fire_polygons[atlas_poly] <> 0 and fire_polygons[atlas_poly][mtbs_poly] <> -1:
            fire_polygons[atlas_poly][mtbs_poly] = []
            fire_polygons[atlas_poly][mtbs_poly].append(intersect)

#Create the ouput file with unique ID for each polygon intersection, with corresponding areas                
    outfile=open('c:/aaronwilson/NR_fire/data_tables/union_%s_out.csv'%(year),'w')
    outfile.write("Year,Atlas_poly,MTBS_poly,Intersect,Atlas_Only,MTBS_Only,Orig_Atlas,Orig_MTBS\n")#,Atlas_Only,MTBS_Only,All_Atlas,All_MTBS
    polyList = []
    for poly in fire_polygons.keys():
        for x in fire_polygons[poly].keys():
            if x <> -1 and poly > 0:
                    polyList.append(poly)
    ##    print polyList
    for poly in fire_polygons.keys():
            print poly
    ##	print fire_polygons[poly].keys()
    ##	print polyList
            for x in fire_polygons[poly].keys():
                print x
                mtbsList = fire_polygons[poly].keys()
                if x <> -1 and poly > 0:
                    print x
                    mtbs_id = x
                    area = fire_polygons[poly][x][0]
                    if fire_polygons[poly].has_key(-1):
                        atlas_out = fire_polygons[poly][-1][0]
                    else:
                        atlas_out = fire_polygons[poly][x][0]
                    if fire_polygons[0].has_key(x):
                        mtbs_out = fire_polygons[0][x][0]
                    else:
                        mtbs_out = fire_polygons[poly][x][0]
                    atlas_old = area + atlas_out
                    mtbs_old = area + mtbs_out
                    outfile.write("%s,%s,%s,%s,%s,%s,%s,%s\n"%(year,poly,mtbs_id,area,atlas_out,mtbs_out,atlas_old,mtbs_old))
                    print mtbs_id
    ##                print area
                elif x == -1:
                    for z in mtbsList:
                        if z <> -1:
                            exists = 1
                            break
                        else:
                            exists = 0
                    if exists == 0:
    ##                    print mtbsList[0]
                        mtbs_id = x
                        area = 0
                        atlas_out = 0
                        mtbs_out = 0
                        atlas_old = fire_polygons[poly][x][0]
                        mtbs_old = 0
                        outfile.write("%s,%s,%s,%s,%s,%s,%s,%s\n"%(year,poly,mtbs_id,area,atlas_out,mtbs_out,atlas_old,mtbs_old))
    ##                    print mtbs_id
    ##                    print atlas_old
                elif poly == 0:
                    for y in polyList:
                        if fire_polygons[y].has_key(x):
                            exists = 1
                            break
                        else:
                            exists = 0
                    if exists == 0:
                        mtbs_id = x
                        area = 0
                        atlas_out = 0
                        mtbs_out = 0
                        atlas_old = 0
                        mtbs_old = fire_polygons[poly][x][0]
                        outfile.write("%s,%s,%s,%s,%s,%s,%s,%s\n"%(year,poly,mtbs_id,area,atlas_out,mtbs_out,atlas_old,mtbs_old))
                    
    ##                print mtbs_id
    ##                print mtbs_old
    outfile.close()
    n = n + 1
del n, year, polyList
