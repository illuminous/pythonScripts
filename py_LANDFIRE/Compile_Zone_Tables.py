##""********************************************************************************************************************
##AUTHOR: Brendan C. Ward
##DATE UPDATED: 11/14/2007
##VARIABLES TO SET AND LINE #():    Zone (31)
##                                  working_dir (32)
##                                  net_dir (33)
##                                  SSURGO_DB (34)
##                                  rescale_LUT_filename (35)
##                                  arc (36)
##DATA SOURCES: SSURGO_DB: column names are extracted from tables in here
##              composited tables in .../tabular/composite folder
##SCRIPT DEPENDENCIES:  win32com.client
##SCRIPT OUTPUTS: 3 ArcInfo tables: zXX_muaggatt (base information at map unit level), zXX_component (categorical component data for dominant component in map unit),
##                  and zXX_derived (horizon level data aggregated up to map units)
##                  ZXX_SSURGO_Report.htm (provides links to ecosite reports on web for each eco site)
##SCRIPT DESCRIPTION: This script processes the compiled SSURGO CSV files for a Zone into an appropriate form for mapping.  This involves reading in several files,
##                      retrieving field names from the SSURGO database, and aggregating individual horizon- and component-level data up to a map unit.  Soil horizon
##                      data (such as sandtotal_r) are first aggregated to the component level using depth-weighted averaging.  Component-level attributes (such as aggregated horizon data)
##                      are then aggregated to the map unit using area-weighted averaging, using the proportional area recorded for each component.  Categorical attributes at
##                      the component level are passed upward to the map unit only for the dominant component, since no meaningful average can be calculated.
##
##*********************************************************************************************************************"""

import os, re, win32com.client, sets, shutil
from zipfile import ZipFile, ZIP_DEFLATED
from urllib2 import *

########################################################################
### User defined variables below this point ############################
########################################################################
Zone="59"
working_dir="g:/ssurgo/z%s_ssurgo/tabular"%(Zone) #base directory of ssurgo data
net_dir="k:/fe/landfire/ssurgo_z/z%s_ssurgo"%(Zone) #location of input zip files on network
SSURGO_DB="g:/ssurgo/soildb_US_2002.mdb" #this is just an empty template database to get the column names and positions
rescale_LUT_filename="g:/horizon_rescale_LUT.csv" #the location of the horizon rescale file
arc='C:/arcgis/arcexe9x/bin/arc.exe' #physical location of Arc executable - this should be generic for all standard-FS image machines
########################################################################
### User defined variables above this point ############################
########################################################################


NODATA=255 #standard 8-bit nodata
tablenames=["muaggatt","component","coeplants","chorizon","coecoclass","corestrictions"] #raw tables that need to be read



########################################################################
### Function for rescaling on [1,255] and [1,65535] scales (0 is NULL) #
########################################################################
def stretch_it(curval,minval,maxval,base): #function to rescale numbers to 8/16 bits
    if base==8: #valid range is 0-254
        basemax=254.0
    else:  #base = 16, valid range is 0-65534
        basemax=65534.0
    curpct=(float(curval)-float(minval))/(float(maxval)-float(minval)) #where is this value in the range of values
    newval=int(round(basemax * curpct,0))
    return newval

def area_weighted_average(pairs): #function that takes pairs of relative proportions and their associated values, and renormalizes based on removing the proportions of the missing data
    total=0
    new_pairs=[]
    for pair in pairs:
        if pair[1] or pair[1]==0: #is 0 valid?
            total+=pair[0]
            new_pairs.append(pair)
    if new_pairs and total<>0:
        aw_avg=0
        for pair in new_pairs:
            aw_avg+=(float(pair[0])/float(total))*float(pair[1])
    else:
        aw_avg=""
    return aw_avg

def classify_pH(pH):
    pH_class=255
    if pH<=4:
        pH_class=101
    elif pH<=6.5:
        pH_class=102
    elif pH<=7.5:
        pH_class=103
    else:
        pH_class=104
    return pH_class


########################################################################
### Build Composite Raw Text Files #####################################
### This is out of date 11/21/07 ###########
########################################################################
##if not os.access("%s/compiled"%(working_dir),os.F_OK):
##    ssas = [] #soil survey areas
##    for entry in os.listdir(working_dir): #subdirectories of state directory - these are the mapping chunks
##        if os.path.isdir("%s/%s"%(working_dir,entry)) and entry.count("soil_"):
##            ssas.append(entry)
##
##    if ssas:
##        #retrieve list of files from first map chunk, assume that all map chunks have the same list of tables
##        filenames=[]
##        for entry in os.listdir("%s/%s/tabular"%(working_dir,ssas[0])): #ignore the sdv tables, they don't compile this way
##            if re.search(".txt",entry) and not re.search("sdv",entry):
##                filenames.append(entry)
##
##        comp_dir="%s/compiled"%(working_dir) #compiled data directory
##        if not os.access(comp_dir,os.F_OK):
##            os.mkdir(comp_dir)
##
##        outfiles=dict() #dictionary of output file pointers, indexed by name of file
##        for filename in filenames:
##            #now open the files
##            outfiles[filename]=open("%s/%s"%(comp_dir,filename),'w')
##
##        #now iterate over every ssa
##        for ssa in ssas:
##            print "Processing Soil Survey Area:",ssa
##            for filename in filenames:
##                if os.access("%s/%s/tabular/%s"%(working_dir,ssa,filename),os.F_OK): #need to make sure it exists!
##                    infile=open("%s/%s/tabular/%s"%(working_dir,ssa,filename),'r')
##                    data=infile.read()
##                    infile.close()
##                    outfiles[filename].write(data)
##
##        #now close all the files
##        for filename in filenames: 
##            outfiles[filename].close()


### lookup table of tables in database to their names on disk
file_LUT=dict()
file_LUT["sacatalog"]="sacatlog.txt"
file_LUT["sainterp"]="sainterp.txt"
file_LUT["featdesc"]="featdesc.txt"
file_LUT["distmd"]="distmd.txt"
file_LUT["legend"]="legend.txt"
file_LUT["distinterpmd"]="distimd.txt"
file_LUT["distlegendmd"]="distlmd.txt"
file_LUT["laoverlap"]="lareao.txt"
file_LUT["legendtext"]="ltext.txt"
file_LUT["mapunit"]="mapunit.txt"
file_LUT["component"]="comp.txt"
file_LUT["muaggatt"]="muaggatt.txt"
file_LUT["muaoverlap"]="muareao.txt"
file_LUT["mucropyld"]="mucrpyd.txt"
file_LUT["mutext"]="mutext.txt"
file_LUT["chorizon"]="chorizon.txt"
file_LUT["cocanopycover"]="ccancov.txt"
file_LUT["cocropyld"]="ccrpyd.txt"
file_LUT["codiagfeatures"]="cdfeat.txt"
file_LUT["coecoclass"]="cecoclas.txt"
file_LUT["coerosionacc"]="cerosnac.txt"
file_LUT["coeplants"]="ceplants.txt"
file_LUT["coforprod"]="cfprod.txt"
file_LUT["cogeomordesc"]="cgeomord.txt"
file_LUT["cohydriccriteria"]="chydcrit.txt"
file_LUT["cointerp"]="cinterp.txt"
file_LUT["comonth"]="cmonth.txt"
file_LUT["copmgrp"]="cpmatgrp.txt"
file_LUT["copwindbreak"]="cpwndbrk.txt"
file_LUT["corestrictions"]="crstrcts.txt"
file_LUT["cosurffrags"]="csfrags.txt"
file_LUT["cotaxfmmin"]="ctxfmmin.txt"
file_LUT["cotxfmother"]="ctxfmoth.txt"
file_LUT["cotaxmoistcl"]="ctxmoicl.txt"
file_LUT["cotext"]="ctext.txt"
file_LUT["cotreestomng"]="ctreestm.txt"
file_LUT["chaashto"]="chaashto.txt"
file_LUT["chconsistence"]="chconsis.txt"
file_LUT["chdesgnsuffix"]="chdsuffx.txt"
file_LUT["chfrags"]="chfrags.txt"
file_LUT["chpores"]="chpores.txt"
file_LUT["chstructgrp"]="chstrgrp.txt"
file_LUT["chtext"]="chtext.txt"
file_LUT["chtexturegrp"]="chtexgrp.txt"
file_LUT["chunified"]="chunifie.txt"
file_LUT["coforprodo"]="cfprodo.txt"
file_LUT["copm"]="cpmat.txt"
file_LUT["cosoilmoist"]="csmoist.txt"
file_LUT["cosoiltemp"]="cstemp.txt"
file_LUT["cosurfmorphgc"]="csmorgc.txt"
file_LUT["cosurfmorphhpp"]="csmorhpp.txt"
file_LUT["cosurfmorphmr"]="csmormr.txt"
file_LUT["cosurfmorphss"]="csmorss.txt"
file_LUT["chstruct"]="chstr.txt"
file_LUT["chtexture"]="chtextur.txt"
file_LUT["chtexturemod"]="chtexmod.txt"

#lookup table of data types to ArcInfo table specifications
types=dict()
types[2]=['i',8]
types[3]=['i',8]
types[4]=['f',8]
types[5]=['f',8]
types[14]=['f',8]
types[202]=['c',255] # max of 320 characters for INFO
types[203]=['c',255] # max of 320 characters for INFO

soil_orders=['Alfisols','Andisols','Aridisols','Entisols','Histosols','Inceptisols','Mollisols','Oxisols','Spodosols','Ultisols','Vertisols']









########################################################################
### Table Class for convenience ########################################
########################################################################
class Table:
    def __init__(self):
        #data structure
        self.cols=[] #ordered list exactly as in the DB and text files
        self.col_pos_LUT=dict()
        self.col_len_LUT=dict()
        self.col_type_LUT=dict()
        self.want_cols=[] #list of columns that we want
        self.rescale_LUT=dict()
    def add_col(self,colname,colpos,coltype):
        self.cols.append(colname)
        self.col_pos_LUT[colname]=colpos
        self.col_len_LUT[colname]=0 #initialize to 0
        self.col_type_LUT[colname]=types[coltype]
    #accessors
    def colPos(self,colname):
        return self.col_pos_LUT[colname]
    def colType(self,colname):
        return self.col_type_LUT[colname]
    def colLength(self,colname):
        return self.col_len_LUT[colname]
    def checkLength(self,colname,cursize):#check new record against existing lengths, and increase size if necessary - this is also where we'd hard-code limits if necessary
        if cursize>self.col_len_LUT[colname]:
            self.col_len_LUT[colname]=cursize
    def get_goodCols(self): #return list of columns that were populated
        temp=[]
        for col in self.cols:
            if self.col_len_LUT[col]>0:
                temp.append(col)
        return temp
    def set_wantCols(self,want_cols):
        if want_cols:
            self.want_cols=want_cols
        else:
            self.want_cols = self.cols
    def get_wantCols(self):
        return self.want_cols


########################################################################
### Horizon Class - stores finest level data ###########################
########################################################################
class Horizon:  #stores useful info for each horizon in each component
    def __init__(self,top,bottom):
        self.top=top
        self.bottom=bottom
        self.depth=bottom-top
        self.elements=dict() #these are the want_cols of data for this horizon
        self.derived=dict()
        
    def calc_derived_elements(self):
        #provided that we are populated correctly, go through elements and derive coarse, sand, silt, clay values
        #need to be robust to missing data
        coarse=0
        sand=0
        silt=0
        clay=0
        claytotal=0
        silttotal=0
        if self.elements['sieveno10_r']: #Bare minimum precondition
            sieve10=float(self.elements['sieveno10_r'])
            coarse=(100-sieve10)
            if coarse < 100: #if coarse is 100 then we don't care about the others
                if self.elements['sieveno200_r']:
                    sieve200=float(self.elements['sieveno200_r'])
                    sand=float(sieve10-sieve200)
                    if (coarse+sand)<100: #otherwise silt and clay must be 0
                        if self.elements['claytotal_r'] and self.elements['silttotal_r']:
                            claytotal=float(self.elements['claytotal_r'])
                            silttotal=float(self.elements['silttotal_r'])
                            if (claytotal+silttotal)>0:#otherwise we'll get a divide by 0
                ##                clay=(float(claytotal*sieve200)/100.0) #these two are from STATSGO SAS code, which does not seem right
                ##                silt=float(sieve200-clay)
                                silt=silttotal/(silttotal+claytotal)*(100-(coarse+sand))#calculate relative proportion and rescale in with coarse +sand
                                clay=claytotal/(silttotal+claytotal)*(100-(coarse+sand))
        total=coarse+sand+silt+clay
        if total>=99 and total<=101: #100+/-1 for rounding errors
            self.derived["coarse"]=coarse
            self.derived["sand"]=sand
            self.derived["silt"]=silt
            self.derived["clay"]=clay
            if (sand+silt+clay)>0:
                whc=self.calc_whc(sand,silt,clay)
                self.derived["whc"]=whc
            elif (sand+silt+clay)==0 and coarse>0:
                self.derived["whc"]=0
    def calc_whc(self,sand,silt,clay):
        #this calculation assumes that sand silt clay add to 100% - need to readjust to remove coarse percentage
        #code borrowed from biomeBGC (sitec_init.c, lines 101-104)
        #Based on Cosby et al. 1984
        sand=100.0*float(sand)/float(sand+silt+clay)
        silt=100.0*float(silt)/float(sand+silt+clay)
        clay=100.0*float(clay)/float(sand+silt+clay)
        
        b=-(3.10 + 0.157*clay-0.003*sand)
        vwc_sat=(50.5 - 0.142*sand - 0.037*clay)/100.0
        psi_sat=-pow(2.71828,(1.54-0.0095*sand+0.0063*silt))*9.85e-5
        whc=vwc_sat*pow((-0.015/psi_sat),(1.0/b)) #this is volumetric in m-cubed of water per m-cubed of soil
        return whc






############################################################################################################
### Component Class - stores component level data, and contains horizon data in data structure  ############
############################################################################################################     
class Component: #stores useful info for each component
    def __init__(self,percent):
        self.percent=percent #representative percent
        self.compdata=dict()
        self.horizons=dict() #dictionary of Horizon objects
        self.max_depth=0
        self.ecosite=[]#triad of type, ID, name
        self.restrictive_layer=[]#pair of kind and depth
        self.soil_order=""
        self.derived_horizon_avg=dict()#depth weighted average of derived variables
        self.raw_horizon_avg=dict()#depth weighted average of the raw variables
        self.valid_horizons=[]#this tracks the ones that have the minimum data fields populated


    def Add_Horizon(self,hokey,top,bottom):
        self.horizons[hokey]=Horizon(top,bottom)
        if bottom>=self.max_depth:
            self.max_depth=bottom

    def Avg_Horizons(self):
        #first calculate the derived values
        for horizon in self.horizons:
            self.horizons[horizon].calc_derived_elements()
            #now make sure we have valid horizons
            if self.horizons[horizon].derived.has_key("coarse"):
                self.valid_horizons.append(horizon)

        #depth-weighted average of raw data
        pairs=dict()
        for horizon in self.valid_horizons:
            depth=self.horizons[horizon].depth
            if depth:
                for element in self.horizons[horizon].elements:
                    if self.horizons[horizon].elements[element] or self.horizons[horizon].elements[element]==0:
                        if not pairs.has_key(element):
                            pairs[element]=[]
                        pairs[element].append([depth,self.horizons[horizon].elements[element]])
        for element in pairs:
            avg=area_weighted_average(pairs[element]) #this is calling the area-weighted averaging function at the top of the code, but in this case area=depth
            if str(avg):
                self.raw_horizon_avg[element]=avg

        #average derived elements 
        for element in ["coarse","sand","silt","clay","whc"]: #the derived data
            pairs = []
            for horizon in self.valid_horizons:
                depth=self.horizons[horizon].depth
                if depth and self.horizons[horizon].derived.has_key(element):
                    pairs.append([depth, self.horizons[horizon].derived[element]])
            avg=area_weighted_average(pairs) #this is calling the area-weighted averaging function at the top of the code, but in this case area=depth

            if str(avg):                
                self.derived_horizon_avg[element]=avg


#############################################################################################################
### Map Unit Class - stores map unit level data, and contains component data in data stucture ###############
#############################################################################################################      
class MU: #stores useful info for each map unit
    def __init__(self):
        self.aggdata=dict()#data from aggregate table
        self.components=dict()
        self.dom_component=""#key of dominant component
        self.soil_orders=dict()
        self.raw_horizon_avg=dict()#area and depth weighted average of raw horizon-level data
        self.derived_horizon_avg=dict()#area and depth weighted average of derived horizon-level data
    
    def addComponent(self,cokey,percent):#cols is the list of column names of data at the component level to add to this component
        cur_pct=0 #default is always 0
        if percent:
            cur_pct=int(percent)
        self.components[cokey]=Component(cur_pct)
        if not self.dom_component: #no dominant component defined yet, percent doesn't matter
            self.dom_component=cokey
        elif cur_pct: 
            old_pct=self.components[self.dom_component].percent
            if cur_pct>old_pct:
                self.dom_component=cokey
        #else null or 0, neither of which qualify this one any more than the one already dominant              
            
    def getComponent(self,cokey):
        return self.components[cokey] #is this by reference?

    def getDomComponent(self):
        if self.dom_component:
            return self.components[self.dom_component]
        else:
            print "ERROR - no dominant component defined!!"

    def Avg_Components(self):
        #first - make the components depth-weight average their horizons
        for cokey in self.components:
            self.components[cokey].Avg_Horizons()

        #next - area-weight by representative percent        
        #raw horizon info
        pairs=dict()
        for cokey in self.components:
            percent=self.components[cokey].percent
            for element in self.components[cokey].raw_horizon_avg:
                if self.components[cokey].raw_horizon_avg[element] or self.components[cokey].raw_horizon_avg[element]==0:
                    if not pairs.has_key(element):
                        pairs[element]=[]
                    pairs[element].append([percent,self.components[cokey].raw_horizon_avg[element]])
        for element in pairs:
            avg=area_weighted_average(pairs[element])#this is calling the area-weighted averaging function at the top of the code
            if str(avg):
                self.raw_horizon_avg[element]=avg
        #derived info
        for element in ["coarse","sand","silt","clay","whc"]:         
            pairs = []
            for cokey in self.components:
                percent=self.components[cokey].percent
                if percent and self.components[cokey].derived_horizon_avg.has_key(element):
                    pairs.append([percent, self.components[cokey].derived_horizon_avg[element]])
            avg=area_weighted_average(pairs)#this is calling the area-weighted averaging function at the top of the code
            if str(avg):
                self.derived_horizon_avg[element]=avg

        # max depth
        pairs=[]
        for cokey in self.components:
            percent=self.components[cokey].percent
            max_depth=self.components[cokey].max_depth
            pairs.append([percent,max_depth])
        avg=area_weighted_average(pairs)#this is calling the area-weighted averaging function at the top of the code
        if str(avg):
            self.derived_horizon_avg["mxdepth"]=avg

        #restrictive depth
        pairs=[]
        for cokey in self.components:
            percent=self.components[cokey].percent
            if self.components[cokey].restrictive_layer:
                restrictive_depth=self.components[cokey].restrictive_layer[1]
                pairs.append([percent,restrictive_depth])
        avg=area_weighted_average(pairs)#this is calling the area-weighted averaging function at the top of the code
        if str(avg):
            self.derived_horizon_avg["resdepth"]=avg
                

    def Calc_Soil_Orders(self): #iterate through components and determine the percentage of each soil order in this map unit
        soil_order_percents=dict()
        for cokey in self.components:
            order=self.components[cokey].soil_order
            percent=self.components[cokey].percent
            if order and percent:
                if not soil_order_percents.has_key(order):
                    soil_order_percents[order]=0
                soil_order_percents[order]+=percent
        #now normalize to 100%
        total=float(sum(soil_order_percents.values()))
        for order in soil_order_percents:
            soil_order_percents[order]=100.0*(soil_order_percents[order]/total)    
        return soil_order_percents

    def Calc_Drainage_Classes(self):#iterate through components and determine the percentage of each drainage class in this map unit
        drainclass_LUT=dict()
        drainclass_LUT['Excessively drained']='dc_ex'
        drainclass_LUT['Somewhat excessively drained']='dc_sex'
        drainclass_LUT['Moderately well drained']='dc_mod'
        drainclass_LUT['Well drained']='dc_well'
        drainclass_LUT['Somewhat poorly drained']='dc_spoor'
        drainclass_LUT['Poorly drained']='dc_poor'
        drainclass_LUT['Very poorly drained']='dc_vpoor'
        
        drainclass_percents=dict()
        for cokey in self.components:
            drainclass=self.components[cokey].compdata['drainagecl']
            percent=self.components[cokey].percent
            if drainclass and percent:
                drainclass_label=drainclass_LUT[drainclass]
                if not drainclass_percents.has_key(drainclass_label):
                    drainclass_percents[drainclass_label]=0
                drainclass_percents[drainclass_label]+=percent
        #now normalize to 100%
        total=float(sum(drainclass_percents.values()))
        for drainclass_label in drainclass_percents:
            drainclass_percents[drainclass_label]=100.0*(drainclass_percents[drainclass_label]/total)    
        return drainclass_percents


################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
### Main program below HERE ####################################################################################################################
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################ 


########################################################################
### Download the data  - only retrieve the tables we actually need #####
########################################################################
if not os.access("%s/compiled"%(working_dir),os.F_OK):
    os.makedirs("%s/compiled"%(working_dir))

want_files=[]
for entry in tablenames:
    want_files.append(file_LUT[entry])

    
zipfilename="%s/z%s_compiled.zip"%(net_dir,Zone)
print "Extracting:",zipfilename
if not os.access(zipfilename,os.F_OK):
    raise Exception("Input file is missing:  %s"%(zipfilename))
inzip=ZipFile(zipfilename,'r',ZIP_DEFLATED)
for entry in inzip.namelist():
    if entry.count(".txt") and entry.split("/").pop() in want_files: #if a text file and in the list of tables we want 
        outfilename="%s/compiled/%s"%(working_dir,entry.split("/").pop())
        if not os.access(outfilename,os.F_OK):
            data=inzip.read(entry)
            outfile=open(outfilename,'w')
            outfile.write(data)
            outfile.close()
inzip.close()




########################################################################
### Get Column Names and Locations #####################################
########################################################################
tables=dict()
connection=win32com.client.Dispatch(r'ADODB.Connection')
result=win32com.client.Dispatch(r'ADODB.Recordset')      
source="PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE=%s"%(SSURGO_DB)
connection.Open(source)
for tablename in tablenames:  #tablenames is set all the way at the top - these are the tables we care about
    tables[tablename]=Table() #build a data structure to contain its metadata
    curTable=tables[tablename] #retrieve current table by reference (this is not a copy!!!)
    query="SELECT * FROM %s;"%(tablename)
    result.Open(query,connection,1,3)
    for colpos in range(0,len(result.Fields)):
        colname=str(result.Fields.Item(colpos).name) #must be less than 16 characters
        coltype=result.Fields.Item(colpos).type
        curTable.add_col(colname,colpos,coltype)
    result.Close()
connection.Close()


#Set the columns we want
tables["muaggatt"].set_wantCols(['musym', 'muname', 'brockdepmin', 'wtdepannmin', 'wtdepaprjunmin', 'flodfreqdcd', 'flodfreqmax', 'pondfreqprs',
                                 'aws025wta', 'aws050wta', 'aws0100wta', 'aws0150wta', 'drclassdcd', 'drclasswettest', 'hydgrpdcd', 'hydclprs'])
tables["component"].set_wantCols(['comppct_l', 'comppct_r', 'comppct_h', 'compname', 'compkind', 'majcompflag', 'localphase', 'runoff', 'tfact',
                                  'hydricon', 'hydricrating', 'drainagecl', 'constreeshrubgrp', 'wlgrain', 'wlgrass', 'wlherbaceous', 'wlshrub',
                                  'wlconiferous', 'wlhardwood', 'wlwetplant', 'wlshallowwat', 'wlrangeland', 'wlopenland', 'wlwoodland', 'wlwetland',
                                  'hydgrp', 'taxclname', 'taxorder', 'taxsuborder', 'taxgrtgroup', 'taxsubgrp', 'taxpartsize', 'taxpartsizemod',
                                  'taxceactcl', 'taxreaction', 'taxtempcl', 'taxmoistscl', 'taxtempregime', 'soiltaxedition', 'indraingrp',
                                  'innitrateleachi', 'vasoimgtgrp', 'mukey', 'cokey'])
tables["coeplants"].set_wantCols([])
tables["coecoclass"].set_wantCols([])
tables["chorizon"].set_wantCols(['fraggt10_r', 'frag3to10_r', 'sieveno4_r', 'sieveno10_r', 'sieveno40_r', 'sieveno200_r', 'sandtotal_r', 'sandvc_r',
            'sandco_r','sandmed_r', 'sandfine_r', 'sandvf_r', 'silttotal_r', 'claytotal_r', 'dbthirdbar_r', 'ksat_r', 'awc_r', 'wtenthbar_r',
            'wthirdbar_r','wfifteenbar_r', 'lep_r', 'll_r', 'pi_r', 'ec_r', 'sumbases_r', 'ph1to1h2o_r'])
tables["corestrictions"].set_wantCols([]) #['reskind','resdept_r'] #not used




#Main data storage variable
mudata=dict()

########################################################################
### Read component data ################################################
########################################################################
print "Reading Component Data"
curTable=tables["component"]
infile=open("%s/compiled/%s"%(working_dir,file_LUT["component"]),'r')
indata=infile.readlines()
infile.close()
for line in indata:
    line=line.replace("\n",'').replace('"','').replace("\r",'').replace(",",";").split('|')
    mukey=int(line[curTable.colPos('mukey')])
    cokey=line[curTable.colPos('cokey')]
    percent=line[curTable.colPos('comppct_r')]
    if not mudata.has_key(mukey):
        mudata[mukey]=MU()
    mudata[mukey].addComponent(cokey,percent)  
    curCmp=mudata[mukey].getComponent(cokey)
    #there are two ways to hit an individual component:
    # long way mudata[mukey].components[cokey]
    #short way is to retrive pointer directly
    #curCmp=mudata[mukey].getComponent(cokey)
    
    curCmp.soil_order=line[curTable.colPos('taxorder')] #set soil order

    for col in curTable.cols:
        pos=curTable.colPos(col)
        value=line[pos]
        curCmp.compdata[col]=value
        curTable.checkLength(col,len(value))


########################################################################
### Read aggregate data ################################################
########################################################################
print "Reading Aggregate Data"
curTable=tables["muaggatt"] #retrieve current table by reference (this is not a copy!!!)
infile=open("%s/compiled/%s"%(working_dir,file_LUT["muaggatt"]),'r')
indata=infile.readlines()
infile.close()
for line in indata:
    line=line.replace("\n",'').replace('"','').replace("\r",'').replace(",",";").split('|')
    mukey=int(line[curTable.colPos('mukey')])
    for col in curTable.cols:
        pos=curTable.colPos(col)
        value=line[pos]
        if not mudata.has_key(mukey):
            mudata[mukey]=MU()
        mudata[mukey].aggdata[col]=value
        curTable.checkLength(col,len(value))

mukeys=mudata.keys()
mukeys.sort()



########################################################################
### Create ARCINFO workspace and cut tabular stuff to INFO tables ######
########################################################################
arc_workspace="%s/info_tables"%(working_dir)

##need to create workspace before dropping the files there
if not os.access(arc_workspace,os.F_OK):
    amlfile=open("c:/temp/junk.aml",'w')
    amlfile.write("cw %s"%(arc_workspace))
    amlfile.close()
    args=['arc',"&r %s"%("c:/temp/junk.aml")]
    os.spawnv(os.P_WAIT,arc,args)

########################################################################
### Write aggregate data ###############################################
########################################################################
print "Writing Aggregate Table"
tablename="z%s_muaggatt"%(Zone)
curTable=tables["muaggatt"]
outfilename="%s/%s_info.csv"%(arc_workspace,tablename)
outfile=open(outfilename,'w')
for mukey in mukeys:
    line="%i"%(mukey)
    for col in curTable.get_wantCols(): #the columns we specified above
        value=''       
        if mudata[mukey].aggdata.has_key(col):
            value=mudata[mukey].aggdata[col]
        arc_type=curTable.colType(col)[0]
        if arc_type=="c":
            if len(value)>curTable.colLength(col):
                value="%s"%(value[0:curTable.colLength(col)])
            value='"%s"'%(value)
        line+=",%s"%(value)
    line+="\n"
    outfile.write(line)
outfile.close()

#Write table define - this needs to be run manually in arc
amlfile=open("%s/define_%s_info.aml"%(arc_workspace,tablename),'w')
amlfile.write("&echo &on\nw %s\n&if [exists %s -info] &then killinfo %s\ntables\ndefine %s\n"%(arc_workspace,tablename,tablename,tablename))
line = "Value 8 8 i\n"
amlfile.write(line)
for col in curTable.get_wantCols():
    curtype=curTable.colType(col)
    if curtype[0]=="i":
        arc_type,arc_width=curtype
        line = "%s %s %s %s\n"%(col, arc_width, arc_width,arc_type)
    elif curtype[0]=="f":
        arc_type,arc_width=curtype
        decimals=2
        line = "%s %s %s %s %s\n"%(col, arc_width, arc_width,arc_type,decimals)        
    else:
        arc_type=curtype[0]
        arc_width=min(255,curTable.colLength(col)+1)
        line = "%s %s %s %s\n"%(col, arc_width, arc_width,arc_type)
    amlfile.write(line)
amlfile.write("~\n")
amldata="""
select %s
add Value %s from %s
select
indexitem %s Value
q
"""%(tablename,str(curTable.get_wantCols()).replace("[",'').replace("]",'').replace("'",'').replace('"','').replace(",",''),outfilename.split("/").pop(), tablename)
amlfile.write(amldata)
amlfile.close()

#run arc
args=['arc',"&r %s"%("%s/define_%s_info.aml"%(arc_workspace,tablename))]
os.spawnv(os.P_WAIT,arc,args)








########################################################################
### Ecological Site Tables #############################################
########################################################################
print "Reading Ecological Site Data"
curTable=tables["coecoclass"]
infile=open("%s/compiled/%s"%(working_dir,file_LUT["coecoclass"]),'r')
indata=infile.readlines()
infile.close()
for line in indata:
    line=line.replace("\n",'').replace('"','').replace("\r",'').replace(",",";").split('|')
    cokey=line[curTable.colPos("cokey")] #component key - used to join back to components
    mukey=int(cokey.split(":").pop(0))
    if not mudata[mukey].components[cokey].ecosite: #only grab the first one
        ecosite_type=line[curTable.colPos("ecoclasstypename")]
        ecosite_ID=line[curTable.colPos("ecoclassid")]
        ecosite_name=line[curTable.colPos("ecoclassname")]
        mudata[mukey].components[cokey].ecosite=[ecosite_type,ecosite_ID,ecosite_name]
        curTable.checkLength("ecoclasstypename",len(ecosite_type))
        curTable.checkLength("ecoclassid",len(ecosite_ID))
        curTable.checkLength("ecoclassname",len(ecosite_name))



########################################################################
### Restrictive Layer ##################################################
########################################################################
print "Reading Restrictive Layer Data"
curTable=tables["corestrictions"]
infile=open("%s/compiled/%s"%(working_dir,file_LUT["corestrictions"]),'r')
indata=infile.readlines()
infile.close()
for line in indata:
    line=line.replace("\n",'').replace('"','').replace("\r",'').replace(",",";").split('|')
    cokey=line[curTable.colPos("cokey")] #component key - used to join back to components
    mukey=int(cokey.split(":").pop(0))
    if not mudata[mukey].components[cokey].restrictive_layer: #only grab the first one
        kind=line[curTable.colPos("reskind")]
        depth=line[curTable.colPos("resdept_r")]
        if kind and depth:
            mudata[mukey].components[cokey].restrictive_layer=[kind,float(depth)]
            curTable.checkLength("reskind",len(kind))
            curTable.checkLength("resdept_r",len(depth))


########################################################################
### Component Tables ###################################################
########################################################################
print "Writing Component Table"
ecofile=open("%s/z%s_ecosite_LUT.csv"%(arc_workspace,Zone),'w')
ecofile.write("Value,ecoclassid,ecoclassname\n")
tablename="z%s_component"%(Zone)
curTable=tables["component"]
outfilename="%s/%s_info.csv"%(arc_workspace,tablename)
outfile=open(outfilename,'w')
for mukey in mukeys:
    line="%i"%(mukey)
    if mudata[mukey].components:
        dom_component=mudata[mukey].getDomComponent()#do this just for dominant component
        if dom_component.ecosite:
            ecoline="%i,%s,%s\n"%(mukey,dom_component.ecosite[1],dom_component.ecosite[2])
            ecofile.write(ecoline)
        for col in curTable.get_wantCols():
            value=''       
            if dom_component.compdata.has_key(col):
                value=dom_component.compdata[col]
            arc_type=curTable.colType(col)[0]
            if arc_type=="c":
                if len(value)>curTable.colLength(col):
                    value="%s"%(value[0:curTable.colLength(col)]) #truncate to max length
                value='"%s"'%(value)
            line+=",%s"%(value)
        if dom_component.ecosite:
            line+=',"%s","%s"'%(dom_component.ecosite[1],dom_component.ecosite[2])
        else:
            line+=',"",""'
        line+="\n"
    outfile.write(line)
outfile.close()
ecofile.close()


#Write table define - this needs to be run manually in arc
amlfile=open("%s/define_%s_info.aml"%(arc_workspace,tablename),'w')
amlfile.write("&echo &on\nw %s\n&if [exists %s -info] &then killinfo %s\ntables\ndefine %s\n"%(arc_workspace,tablename,tablename,tablename))
line = "Value 8 8 i\n"
amlfile.write(line)
for col in curTable.get_wantCols():
    curtype=curTable.colType(col)
    if curtype[0]=="i":
        arc_type,arc_width=curtype
        line = "%s %s %s %s\n"%(col, arc_width, arc_width,arc_type)
    elif curtype[0]=="f":
        arc_type,arc_width=curtype
        decimals=2
        line = "%s %s %s %s %s\n"%(col, arc_width, arc_width,arc_type,decimals)        
    else:
        arc_type=curtype[0]
        arc_width=min(255,curTable.colLength(col)+1)
        line = "%s %s %s %s\n"%(col, arc_width, arc_width,arc_type)
    amlfile.write(line)

#ecosite level stuff
for ecosite_col in ["ecoclassid","ecoclassname"]:
    arc_type=tables["coecoclass"].colType(ecosite_col)[0]
    arc_width=min(255,tables["coecoclass"].colLength(ecosite_col)+1)
    line = "%s %s %s %s\n"%(ecosite_col, arc_width, arc_width,arc_type)
    amlfile.write(line)    
amlfile.write("~\n")
amldata="""
select %s
add Value %s ecoclassid ecoclassname from %s
select
indexitem %s Value
q
"""%(tablename,str(curTable.get_wantCols()).replace("[",'').replace("]",'').replace("'",'').replace('"','').replace(",",''),outfilename.split("/").pop(), tablename)
amlfile.write(amldata)
amlfile.close()

##run arc
args=['arc',"&r %s"%("%s/define_%s_info.aml"%(arc_workspace,tablename))]
os.spawnv(os.P_WAIT,arc,args)







########################################################################
### Soil horizon tables ################################################
########################################################################
#read the horizon table now
print "Reading Horizon Data"
tablename="horizon"
curTable=tables["chorizon"]

#retrieve the rescaling LUT defined for at least some columns in this table
if os.access(rescale_LUT_filename,os.F_OK):
    infile=open(rescale_LUT_filename,'r')
    infile.readline()
    data=infile.readlines()
    infile.close()
    for line in data:
        line=line.split(",")
        col=line[0]
        abs_min=float(line[3])
        abs_max=float(line[4])
        gain=float(line[6])
        offset=float(line[7])
        curTable.rescale_LUT[col]=[gain,offset,abs_min,abs_max]

col_tally=dict()

infile=open("%s/compiled/%s"%(working_dir,file_LUT["chorizon"]),'r')
data=infile.readlines()
infile.close()
for line in data:
    line=line.replace("\n",'').replace('"','').replace("\r",'').replace(",",";").split('|')
    cokey=line[curTable.colPos("cokey")] #component key - used to join back to components
    mukey=int(cokey.split(":").pop(0))
    if mudata[mukey].components.has_key(cokey):
        hokey=line[curTable.colPos("chkey")] #horizon key
        if line[curTable.colPos("hzdept_r")] and line[curTable.colPos("hzdepb_r")]:
            top=int(round(float(line[curTable.colPos("hzdept_r")]),0))
            bottom=int(round(float(line[curTable.colPos("hzdepb_r")]),0))
            mudata[mukey].components[cokey].Add_Horizon(hokey,top,bottom)
            #this loop will add all the raw horizon level data to the data structures
            for col in curTable.get_wantCols():
                value = line[curTable.colPos(col)]
                mudata[mukey].components[cokey].horizons[hokey].elements[col]=value
                if value:
                    if not col_tally.has_key(col):
                        col_tally[col]=0
                    col_tally[col]+=1
                    
good_cols=[]
good_raw_cols=[]
for col in curTable.get_wantCols():
    if col_tally.has_key(col):
        good_cols.append(col)

print "Writing Derived Data"
tablename="z%s_derived"%(Zone)
#have to build this list ourselves
raw_cols=['fraggt10_r', 'frag3to10_r','sieveno4_r', 'sieveno10_r', 'sieveno40_r', 'sieveno200_r', 'sandtotal_r', 'sandvc_r',
            'sandco_r','sandmed_r', 'sandfine_r', 'sandvf_r', 'silttotal_r', 'claytotal_r','claysizedcarb_r',
           'om_r','dbtenthbar_r','dbthirdbar_r','dbfifteenbar_r','dbovendry_r','ksat_r','awc_r',
            'wtenthbar_r','wthirdbar_r','wfifteenbar_r','wsatiated_r','lep_r','ll_r','pi_r','caco3_r',
            'gypsum_r','sar_r','ec_r','cec7_r','ecec_r','sumbases_r']
for col in raw_cols:
    if col in good_cols:
        good_raw_cols.append(col)
        

want_cols=["mxdepth","coarse","sand","silt","clay","whc","resdepth","pH","pH_class",
           'P_Alfisols', 'P_Andisols', 'P_Aridisols', 'P_Entisols', 'P_Histosols',
           'P_Inceptisols', 'P_Mollisols', 'P_Oxisols', 'P_Spodosols', 'P_Ultisols', 'P_Vertisols',
           'dc_ex','dc_sex','dc_mod','dc_well','dc_spoor','dc_poor','dc_vpoor']#our derived stuff
want_cols.extend(good_raw_cols)



outfilename="%s/%s_info.csv"%(arc_workspace,tablename)
outfile=open(outfilename,'w')
for mukey in mudata:
    line="%i"%(mukey)
    mudata[mukey].Avg_Components() #this is going to call the averaging function we defined up in the MU class, so that we can spit these out later
    #this will do the depth and area weighted averages that we need, and calculate the derived stuff
    
    #maximum depth
    value=65535 #this is our default if no mxdepth is defined
    if mudata[mukey].derived_horizon_avg.has_key("mxdepth"):
         value="%.0f"%(round(mudata[mukey].derived_horizon_avg["mxdepth"]*2.54,0))#convert from inches, so maximum depth in cm
    line+=",%s"%(value)
    
    for element in ["coarse","sand","silt","clay"]: #think of each element as an attribute of this Map unit
        #these ones are on a 0-100% scale and don't need rescaling
        value=NODATA #this is the NODATA assigned at top of code
        if mudata[mukey].derived_horizon_avg.has_key(element):
            value="%.0f"%(round(mudata[mukey].derived_horizon_avg[element],0))
        line+=",%s"%(value)

    #need to rescale whc, assume it is natively on [0,0.5] (really seems to be about 0.002-0.4)
    value=NODATA
    if mudata[mukey].derived_horizon_avg.has_key("whc"):
        value=mudata[mukey].derived_horizon_avg["whc"]
        rescaled_value=stretch_it(value,0,0.5,8) #use the stretch_it function at top of code to inflate to 8 bit range
        value="%.0f"%(round(rescaled_value,0))
    line+=",%s"%(value)

    #restrictive depth stuff - default to mxdepth if not defined but mxdepth is
    value=65535
    if mudata[mukey].derived_horizon_avg.has_key("mxdepth"):
        value=round(mudata[mukey].derived_horizon_avg["mxdepth"]*2.54,0)
    if mudata[mukey].derived_horizon_avg.has_key("resdepth"):
         value="%.0f"%(round(mudata[mukey].derived_horizon_avg["resdepth"],0))
    line+=",%s"%(value)    

    #pH and pH_class
    pH=NODATA
    pH_class=NODATA
    if mudata[mukey].raw_horizon_avg.has_key('ph1to1h2o_r'):
        pH=mudata[mukey].raw_horizon_avg["ph1to1h2o_r"]
        if pH:
            pH_class=classify_pH(float(pH)) #call classify_pH above
            pH=int(round(10*float(pH),0)) #round pH to nearest integer, comes in as floating point
    line+=",%s,%s"%(pH,pH_class)

    #calculate % of soil orders
    soil_order_percents=mudata[mukey].Calc_Soil_Orders() #call the function in MU that determines % for each soil order
    for order in soil_orders:
        if (not soil_order_percents) or sum(soil_order_percents.values())==0:#never observed
            percent=255
        else:
            percent=0
            if soil_order_percents.has_key(order):
                percent=soil_order_percents[order]
        line+=",%.0f"%(round(percent,0))

    #calculate % of drainage classes
    drainclasses=['dc_ex','dc_sex','dc_mod','dc_well','dc_spoor','dc_poor','dc_vpoor']
    drainclass_percents=mudata[mukey].Calc_Drainage_Classes()
    for drainclass in drainclasses:
        if (not drainclass) or sum(drainclass_percents.values())==0:#never observed
            percent=255
        else:
            percent=0
            if drainclass_percents.has_key(drainclass):
                percent=drainclass_percents[drainclass]
        line+=",%.0f"%(round(percent,0))

    #raw values - these are the 'native' columns from the ssurgo horizon table aggregated up to map unit level
    for element in good_raw_cols:
        value=NODATA
        if mudata[mukey].raw_horizon_avg.has_key(element):
            value=mudata[mukey].raw_horizon_avg[element]
            if curTable.rescale_LUT.has_key(element):
                gain,offet,abs_min,abs_max=curTable.rescale_LUT[element] #determine rescaling from our LUT for this particular element (attribute)
                if value>(abs_max+1) or value<(abs_min-1):
                    print "Variable outside valid range for %s [%s,%s]: %s"%(element,abs_min,abs_max,value) #this is a warning if variable out of range - consider revising horizon_rescale_LUT if this gets triggered a lot
                    if value>(abs_max+1):
                        value=abs_max
                    else:
                        value=abs_min
                value=value/gain + offset
            #else we just integerize what we have
            value="%.0f"%(round(value,0))
        line+=",%s"%(value)

        
    line+=",1\n"
    outfile.write(line)
outfile.close()                
      
#Write table define
amlfile=open("%s/define_%s_info.aml"%(arc_workspace,tablename),'w')
amlfile.write("&echo &on\nw %s\n&if [exists %s -info] &then killinfo %s\ntables\ndefine %s\n"%(arc_workspace,tablename,tablename,tablename))
line = "Value 8 8 i\n"#make this unique!
amlfile.write(line)
for col in want_cols:
    line = "%s 8 8 i\n"%(col)
    amlfile.write(line)
amlfile.write("valid 8 8 i\n")
amlfile.write("~\n")
#make sure to set index at proper field to speed up joins!!
amldata="""
select %s
add Value %s valid from %s
select
indexitem %s Value
q
"""%(tablename,str(want_cols).replace("[",'').replace("]",'').replace("'",'').replace('"','').replace(",",''),outfilename.split("/").pop(), tablename)
amlfile.write(amldata)
amlfile.close()

##run arc
args=['arc',"&r %s"%("%s/define_%s_info.aml"%(arc_workspace,tablename))]
os.spawnv(os.P_WAIT,arc,args)



########################################################################
### Web report  ################################################
########################################################################
infile=open("%s/info_tables/z%s_ecosite_LUT.csv"%(working_dir,Zone),'r')
infile.readline()
data=infile.readlines()
infile.close()

#build LUT
ecosite_LUT=dict()
for line in data:
    line=line.replace("\n","").split(",")
    ecoID=line[1]
    ecosite=line[2]
    #Convert to 
    
    if not ecosite_LUT.has_key(ecosite):
        ecosite_LUT[ecosite]=dict()
    if not ecosite_LUT[ecosite].has_key(ecoID):
        ecosite_LUT[ecosite][ecoID]=[]

print "Building web report"
#now see if websites exists:
ecosites=ecosite_LUT.keys()
ecosites.sort()
for ecosite in ecosites:
    for ecoID in ecosite_LUT[ecosite]:
        print ecosite,ecoID
        state=ecoID[len(ecoID)-2:]
        web_page_url=""
        pdf_url=""
        #first see if pdf is available
        try:
            url = "http://efotg.nrcs.usda.gov/references/public/%s/%s_%s.pdf"%(state,ecoID,ecosite)
            pdf = urlopen(url)
            pdf.close()
            pdf_url = url
        except: #not found
            pass
        
        for approved in ['yes','no']:
            url="http://esis.sc.egov.usda.gov/esis_report/fsReportPrt.aspx?id=%s&rptLevel=all&approved=%s"%(ecoID,approved)
            try:
                page=urlopen(url)
                #check the size
                data=page.read(2000)
                page.close()
                if not re.search("""<span class="esdtag">Site Name:</span> <br />""",data):
                    #if site name is given, assume report is populated (name seems to be missing when report is empty)
                    web_page_url=url
                    break
            except: #not found
                pass

        ecosite_LUT[ecosite][ecoID]=[pdf_url,web_page_url]  



#build the report based on web sites we found + google links

outfilename="%s/z%s_SSURGO_Report.htm"%(working_dir,Zone)
outfile=open(outfilename,'w')
outfile.write("<HTML><HEAD><Title>SSURGO Ecological Site Descriptions for Zone %s</Title></HEAD><BODY>\n"%(Zone))
outfile.write("<p align=CENTER><span style='font-size:20.0pt'><b>Zone %s SSURGO Ecological Site Descriptions<br></b></span></p>\n"%(Zone))
#table of contents
outfile.write("<p>\n")
for ecosite in ecosites:
    outfile.write('<a href="#%s">%s</a><br>\n'%(ecosite,ecosite))
outfile.write("<br><br></p>\n")

for ecosite in ecosites:
    ecoIDs=ecosite_LUT[ecosite].keys()
    ecoIDs.sort()

    outfile.write('<p><a name="%s"></a><b>%s</b></p>'%(ecosite,ecosite))
    table="<table border cellpadding=4><tr><td><b>ECOSITE</b></td><td><b>Web Page Report</b></td><td><b>PDF Report</b></td><td><b>Google EcositeID</b></td><td><b>Google Name</b></td></tr>\n"
    
    for ecoID in ecoIDs:
        pdf_url,web_page_url=ecosite_LUT[ecosite][ecoID]
        if web_page_url:
            web='<a href="%s">Web Report</a>\n'%(web_page_url)
        else:
            web=""
        if pdf_url:
            pdf='<a href="%s">PDF Report</a>\n'%(pdf_url)
        else:
            pdf=""
        google_ID='<a href="http://www.google.com/search?q=%s">%s</a>\n'%(ecoID,ecoID)
        google_name='''<a href='http://www.google.com/search?q="%s"'>%s</a>\n'''%(ecosite,ecosite)
        table+="<tr><td><b>%s</b></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>\n"%(ecoID,web,pdf,google_ID,google_name)
            
    table+="</table><hr />\n"
    outfile.write(table)    
outfile.write("</BODY></HTML>\n")
outfile.close()



##############################################################################################################################
## Zip up package and post to network
##############################################################################################################################
def recursive_zip_add(zipfile,curdir): #pass in relative path location
    for entry in os.listdir(curdir):
        if os.path.isdir("%s/%s"%(curdir,entry)):
            recursive_zip_add(zipfile,"%s/%s"%(curdir,entry))
        else:
            zipfile.write("%s/%s"%(curdir,entry))

os.chdir(working_dir)
zipfile=ZipFile("%s/z%sw_info_tables.zip"%(working_dir,Zone),'w',ZIP_DEFLATED)
recursive_zip_add(zipfile,"info_tables")
zipfile.close()

if not os.access("%s/z%sw_info_tables.zip"%(net_dir,Zone),os.F_OK):
    print "Posting to network"
    shutil.copy("%s/z%sw_info_tables.zip"%(working_dir,Zone), "%s/z%sw_info_tables.zip"%(net_dir,Zone))

if not os.access("%s/z%s_SSURGO_Report.htm"%(net_dir,Zone),os.F_OK):
    shutil.copy("%s/z%s_SSURGO_Report.htm"%(working_dir,Zone),"%s/z%s_SSURGO_Report.htm"%(net_dir,Zone))
