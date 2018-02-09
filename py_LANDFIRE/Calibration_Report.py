# Make_Landsum_Calibration_FRI_Maps
import win32com.client,sys,os,re,shutil,sets
from rpy import *
set_default_mode(NO_CONVERSION)
#import functions
from _DBF_Reader import *
from _Word_Wrapper import *
from _Compare_VDDT_LS import *
connection=win32com.client.Dispatch(r'ADODB.Connection')
result=win32com.client.Dispatch(r'ADODB.Recordset')
GP=win32com.client.Dispatch("esriGeoprocessing.GpDispatch.1")
GP.CheckOutExtension("Spatial")
GP.AddToolbox("C:/Program Files/ArcGIS/ArcToolbox/Toolboxes/Spatial Analyst Tools.tbx")



##############################################
### Inputs  ##################################
##############################################
Zone="06"
#root = "c:/z%s"%(Zone)
root = "u:/z%s"%(Zone)
working_dir="c:/z%s/calibration"%(Zone)#LOCATION OF OUTPUTS
num_BpS_to_highlight=5 #the number of BpS units to highlight in terms of highest error





##############################################
### Other Inputs  ############################
### These shouldn't need to be set manually ##
##############################################
MTDB="K:/fe/landfire/dat3/firereg/Z%s/dat/Current_Veg_Models/%sMTDB.mdb"%(Zone,Zone)
chunk_grid="%s/gis_data/z%s_chunks"%(root,Zone)
bps="%s/gis_data/z%s_lsbps"%(root,Zone)
FRIfilename="k:/fe/landfire/dat3/firereg/z%s/dat/working_data/BpS_Fire_Params.csv"%(Zone)
RCfilename="k:/fe/landfire/dat3/firereg/z%s/dat/working_data/BPS_SClass_Distribution.csv"%(Zone)
SClassLabfilename="k:/fe/landfire/dat3/firereg/z%s/dat/working_data/MTDB_BpS_SClass_LUT.csv"%(Zone)
outmaps_dir="%s/outmaps"%(working_dir)
analysis_dir="%s/analysis"%(working_dir)
##if not os.access(outmaps_dir,os.F_OK):
##    os.mkdir(outmaps_dir)
##if not os.access(analysis_dir,os.F_OK):
##    os.mkdir(analysis_dir)
##
##
##Utility conversion and lookup-tables
##def val_srt(a,b):
##    return -cmp(a[1],b[1])
##
##    
##def reclass_FRI(FRI):
##    if FRI<=0:
##        FRI=0
##    elif FRI>0 and FRI <=5:
##        FRI=1
##    elif FRI>5 and FRI <=10:
##        FRI=2
##    elif FRI>10 and FRI<=15:
##        FRI=3
##    elif FRI>15 and FRI<=20:
##        FRI=4
##    elif FRI>20 and FRI<=25:
##        FRI=5
##    elif FRI>25 and FRI<=30:
##        FRI=6
##    elif FRI>30 and FRI<=35:
##        FRI=7
##    elif FRI>35 and FRI<=40:
##        FRI=8
##    elif FRI>40 and FRI<=45:
##        FRI=9
##    elif FRI>45 and FRI<=50:
##        FRI=10
##    elif FRI>50 and FRI<=60:
##        FRI=11
##    elif FRI>60 and FRI<=70:
##        FRI=12
##    elif FRI>70 and FRI<=80:
##        FRI=13
##    elif FRI>80 and FRI<=90:
##        FRI=14
##    elif FRI>90 and FRI<=100:
##        FRI=15
##    elif FRI>100 and FRI<=125:
##        FRI=16
##    elif FRI>125 and FRI<=150:
##        FRI=17
##    elif FRI>150 and FRI<=200:
##        FRI=18
##    elif FRI>200 and FRI<=300:
##        FRI=19
##    elif FRI>300 and FRI<=500:
##        FRI=20
##    elif FRI>500 and FRI<=1000:
##        FRI=21
##    elif FRI>1000:
##        FRI=22
##    else:
##        FRI=-9999
##    return FRI
##
##def FRG(TotalFreq, PR):
##    if TotalFreq >= 200:
##        LF_FRG=5
##    elif TotalFreq < 35:
##        if PR < 66:
##            LF_FRG=1
##        else:
##            LF_FRG=2
##    elif TotalFreq < 100:
##        if PR < 80:
##            LF_FRG=3
##        else:
##            LF_FRG=4
##    elif TotalFreq < 200:
##        if PR < 66:
##            LF_FRG=3
##        else:
##            LF_FRG=4
##    return LF_FRG
##
##
##FRI_label_LUT=dict()
##FRI_label_LUT[0]='0'
##FRI_label_LUT[1]='0-5'
##FRI_label_LUT[2]='5-10'
##FRI_label_LUT[3]='10-15'
##FRI_label_LUT[4]='15-20'
##FRI_label_LUT[5]='20-25'
##FRI_label_LUT[6]='25-30'
##FRI_label_LUT[7]='30-35'
##FRI_label_LUT[8]='35-40'
##FRI_label_LUT[9]='40-45'
##FRI_label_LUT[10]='45-50'
##FRI_label_LUT[11]='50-60'
##FRI_label_LUT[12]='60-70'
##FRI_label_LUT[13]='70-80'
##FRI_label_LUT[14]='80-90'
##FRI_label_LUT[15]='90-100'
##FRI_label_LUT[16]='100-125'
##FRI_label_LUT[17]='125-150'
##FRI_label_LUT[18]='150-200'
##FRI_label_LUT[19]='200-300'
##FRI_label_LUT[20]='300-500'
##FRI_label_LUT[21]='500-1000'
##FRI_label_LUT[22]='>1000'





########################################################
### For each scenario, convert maps to grid and clip ###
### mosaic using pure edge-joining #####################
########################################################
print "Performing GIS Operations"
#this loop creates a list of calibration files to operate on
cals=[]
##for entry in os.listdir(working_dir):
##    if entry.count("cal") and not entry.count(".tar.gz"):
##        scenario=entry
##        cal=int(re.findall("\d+",entry)[0])
##        cals.append(cal)
##        if not GP.exists("%s/%s/freq"%(outmaps_dir,scenario)): #only do this if it hasn't already been processed
##            print "Processing",scenario
##            if not os.access("%s/%s"%(outmaps_dir,scenario),os.F_OK):
##                os.mkdir("%s/%s"%(outmaps_dir,scenario)) #create the directory and subdirectory for the scenario
##            
##            #Build list of maps to process
##            total_chunks=0
##            num_done=0
##            #create empty dictionary (frimaps) to populate in following loop
##            frimaps=[]
##            for chunk in os.listdir("%s/%s"%(working_dir,scenario)):
##                if re.search("chunk",chunk):
##                    total_chunks+=1 #increment counter by 1?
##                    outmap_path="%s/%s/%s/outmaps"%(working_dir,scenario,chunk)
##                    if os.listdir(outmap_path):
##                        num_done+=1 #again, counter increment?
##                        # assign result of regular expression search to variable 'map'
##                        # all files that meet criteria of search get added to frimaps dictionary
##                        for map in os.listdir(outmap_path):
##                            if re.search(".asc",map): 
##                                if re.search("freq",map):
##                                    frimaps.append("%s/%s/%s/outmaps/%s"%(working_dir,scenario,chunk,map))
##            #process maps
##            workdir="%s/%s"%(outmaps_dir,scenario)
##            GP.Workspace=workdir
##            for map in frimaps:
##                #not quite sure about this re.search operation...looks like replace '.' before
##                #extension name w/ underscore character
##                outmap=re.search("\S+(?=.asc)",map.split("/").pop()).group().replace('.','_')
##                outmap_clip=outmap.replace("fire","clip")
##                #find everything w/ 'd' in first position and result of outmap search as following characters?
##                ChunkID=re.findall("\d+",outmap)[0]
##                if not os.access("%s/%s"%(workdir,outmap_clip),os.F_OK) and not os.access("%s/%s"%(workdir,outmap),os.F_OK):
##                    print outmap
##                    #take results of re.search operations and convert to grid
##                    GP.asciitoraster(map,outmap,"INTEGER")
##                    print outmap_clip
##                    
##                    GP.con_sa("%s"%(chunk_grid),outmap,outmap_clip,"","VALUE = %s"%(ChunkID))
##                #pick up the ones that fell through
##                if not os.access("%s/%s"%(workdir,outmap_clip),os.F_OK) and os.access("%s/%s"%(workdir,outmap),os.F_OK):
##                    print outmap_clip
##                    GP.con_sa("%s"%(chunk_grid),outmap,outmap_clip,"","VALUE = %s"%(ChunkID))
##             
##            freq_list=""
##            for entry in os.listdir(workdir):
##                if re.search("clip",entry) and re.search("freq",entry) and (not re.search(".aux",entry)):     
##                    freq_list+=entry+"; "
##            try:        
##                GP.mosaictonewraster(freq_list,"%s/%s"%(outmaps_dir,scenario),"freq")                
##            except:
##                print GP.getmessages()    

##            #write Zonal stats file
##            out_zonal_stat_file="%s/analysis/freq_%s.dbf"%(working_dir,scenario)
##            if not os.access(out_zonal_stat_file,os.F_OK):
##                GP.ZonalStatisticsAsTable_sa(bps,'Value', "%s/%s/freq"%(outmaps_dir,scenario),out_zonal_stat_file)
##
##            if total_chunks and 100.0*(float(num_done)/float(total_chunks))<100:
##                print "=====> %.2f Percent Done"%(100.0*(float(num_done)/float(total_chunks)))

#Reclassify into LANDFIRE standard FRI classes
if not GP.exists("%s/fri%s_cl"%(outmaps_dir,cal)):
    try:
        GP.Reclassify_sa("%s/%s/freq"%(outmaps_dir,scenario), "Value", "0 0;0 5 1;5 10 2;10 15 3;15 20 4;20 25 5;25 30 6;30 35 7;35 40 8;40 45 9;45 50 10;50 60 11;60 70 12;70 80 13;80 90 14;90 100 15;100 125 16;125 150 17;150 200 18;200 300 19;300 500 20;500 1000 21;1000 100000 22", "%s/fri%s_cl"%(outmaps_dir,cal), "DATA")
    except:
        print GP.getmessages()

#Combine with BpS for summary histograms
if not GP.exists("%s/cfri%s"%(outmaps_dir,cal)):
    try:
        GP.Combine_sa("%s;%s/fri%s_cl"%(bps,outmaps_dir,cal), "%s/cfri%s"%(outmaps_dir,cal))
    except:
        print GP.getmessages()            

#Run a stupid AML to get the VAT into a csv, and join the classified fri with color definitions while we're at it
outfile=open("c:/temp/temp.aml",'w')
outfile.write("w %s\njoinitem fri%s_cl.vat k:/fe/landfire/dat3/firereg/core_amls/luts/fri_label_lut fri%s_cl.vat value\ntables\nsel cfri%s.vat\nunload cfri%s.csv\nq\nq"%(outmaps_dir,cal,cal,cal,cal))
outfile.close()
arc='C:/arcgis/arcexe9x/bin/arc.exe'
args=['arc',"&r %s"%("c:/temp/temp.aml")]
os.spawnv(os.P_WAIT,arc,args)




#data structures
#create an empty dictionary for each variable?        
SClass_label_LUT=dict()
pred_FRI=dict()
pred_FRG=dict()
pred_RC=dict()
sim_FRI=dict()
FRI_LUT=dict() #from combine of ls_bps and classified FRI
sim_RC=dict()
BpS_name=dict()
BpS_area=dict()
BpS_percent=dict()
FRI_GOF=dict()
BpSs=sets.Set()
FRI_err=dict() #per-bps FRI error
total_FRI_err=dict() #per-scenario FRI error
RC_err=dict() #per-bps RC error
total_RC_err=dict()
bps_rc_errors=[]#used for sorting BpS units by their average errors across scenarios
bps_fri_errors=[]
high_fri_errors=[]
high_rc_errors=[]


########################################################
### Extract RC & FRI data from MTDB  ###################
########################################################
print "Extracting Data from MTDB"
source="PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE=%s"%(MTDB)
#query the MTDB for this Zone
query="""SELECT AllModels.PVG_Code, AllModels.PVG_Name, AllModels.ReplaceAveFreq, AllModels.MixedSevAveFreq, AllModels.SurfaceSevAveFreq, AllModels.ClassAPercent,
AllModels.ClassBPercent, AllModels.ClassCPercent, AllModels.ClassDPercent, AllModels.ClassEPercent FROM AllModels;"""
connection.Open(source)
result.Open(query,connection,1,3)
while not result.EOF:
    BpS=int(re.search("(?<=\d\d)\d\d\d\d\d",result.fields.Item(0).Value).group())
    Name=result.fields.Item(1).Value
    BpS_name[BpS]=Name
    #retrieve fire parameters, if not given, default frequency is a million years
    RFreq=result.fields.Item(2).Value
    if RFreq:
        RFreq=int(RFreq)
    else:
        RFreq=1000000
    MFreq=result.fields.Item(3).Value
    if MFreq:
        MFreq=int(MFreq)
    else:
        MFreq=1000000    
    SFreq=result.fields.Item(4).Value
    if SFreq:
        SFreq=int(SFreq)
    else:
        SFreq=1000000    
    TotalProb=(1.0/float(RFreq))+(1.0/float(MFreq))+(1.0/float(SFreq))
    TotalFreq=int(round(1.0/TotalProb,0))
    LF_FRG=0
    if TotalFreq:
        PR=100.0*((1.0/float(RFreq))/TotalProb)
        PM=100.0*((1.0/float(MFreq))/TotalProb)
        PS=100.0*((1.0/float(SFreq))/TotalProb)
        LF_FRG=FRG(TotalFreq,PR)
    pred_FRG[BpS]=LF_FRG
    pred_FRI[BpS]=TotalFreq
    pred_RC[BpS]=dict()
    A_percent=int(result.fields.Item(5).Value)
    if A_percent:
        pred_RC[BpS]['A']=A_percent
    B_percent=int(result.fields.Item(6).Value)
    if B_percent:
        pred_RC[BpS]['B']=B_percent
    C_percent=int(result.fields.Item(7).Value)
    if C_percent:
        pred_RC[BpS]['C']=C_percent
    D_percent=int(result.fields.Item(8).Value)
    if D_percent:
        pred_RC[BpS]['D']=D_percent
    E_percent=int(result.fields.Item(9).Value)
    if E_percent:
        pred_RC[BpS]['E']=E_percent
    result.MoveNext()
result.Close()
connection.Close()

#Load the SClass label LUT
infile=open(SClassLabfilename,'r')
infile.readline()
data=infile.readlines()
infile.close()
for line in data:
    line=line.split(',')
    BpS=int(line[0])
    label=line[1]
    SClass=int(line[2])
    if not SClass_label_LUT.has_key(BpS):
        SClass_label_LUT[BpS]=dict()
    SClass_label_LUT[BpS][SClass]=label


####Code for reading data from CSVs instead of MTDB        
###Extract MTDB FRI
##predfile=open(FRIfilename,'r')
##predfile.readline()
##data=predfile.readlines()
##predfile.close()
##for line in data:
##    line=line.split(',')
##    BpS=int(line[0])
##    fri=float(line[5])
##    pred_FRI[BpS]=fri
##
##
###Load MTDB RC Values
##predfile=open(RCfilename,'r')
##predfile.readline()
##data=predfile.readlines()
##for line in data:
##    line=line.split(',')
##    BpS=int(line[0])
##    SClass=SClass_label_LUT[BpS][int(line[1])]
##    Percent=int(line[2])
##    if not pred_RC.has_key(BpS):
##        pred_RC[BpS]=dict()
##    pred_RC[BpS][SClass]=Percent
##predfile.close()
##


########################################################
### Now calculate FRI GOF statistics ###################
########################################################
print "Processing FRI Goodness-of-fit"
#Extract LS FRI Zonal Stats
for entry in os.listdir(analysis_dir):
    if entry.count("freq") and entry.count(".dbf") and not entry.count(".xml"):
        for cal in cals:
            if cal==int(re.findall("\d+",entry)[0]):
                infile=open("%s/%s"%(analysis_dir,entry),'rb')
                fri_data=list(dbfreader(infile))[2:]
                infile.close()
                total_area=0
                for line in fri_data:    
                    BpS=int(line[0])
                    BpSs.add(BpS)
                    Area=float(line[2])/10000.0 #convert sq. meters to ha
                    Mean=float(line[6])
                    total_area+=Area
                    if not sim_FRI.has_key(BpS):
                        sim_FRI[BpS]=dict()
                    sim_FRI[BpS][cal]=Mean
                    BpS_area[BpS]=Area
                for BpS in BpSs:
                    BpS_percent[BpS]=100.0*float(BpS_area[BpS])/float(total_area)
                    if not pred_FRI.has_key(BpS):
                        dev=0
                    elif not pred_FRI[BpS]:
                        dev=0
                    else:
                        dev=(10*(pred_FRI[BpS]-float(sim_FRI[BpS][cal]))/pred_FRI[BpS])**2 #sums of squares error
                    AWsum=dev * BpS_percent[BpS]/100.0 #area weighted sums of squares error
                    if not FRI_err.has_key(BpS):
                        FRI_err[BpS]=dict()
                    FRI_err[BpS][cal]=AWsum
                    if not total_FRI_err.has_key(cal):
                        total_FRI_err[cal]=0
                    total_FRI_err[cal]+=AWsum
                break #something! It'll make you feel better!

BpSs=list(BpSs)
BpSs.sort()
cals.sort()

#Write the FRI summary
outfile=open("%s/z%s_FRI_Calibration.csv"%(analysis_dir,Zone),'w')
header="BpS,Percent"
for cal in cals:
    header+=",cal_%s"%(cal)
header+="\n"
outfile.write(header)
for BpS in BpSs:
    line="%s,%.2f%%"%(BpS,BpS_percent[BpS])
    for cal in cals:
        line+=",%.2f"%(FRI_err[BpS][cal])
    line+="\n"
    outfile.write(line)
#write summary line
tail="Sum,100%"
for cal in cals:
    tail+=",%.2f"%(total_FRI_err[cal])
tail+="\n"
outfile.write(tail)
outfile.close()

#Create FRI error table
fri_table=[]
header='BpS\tPercent'
for cal in cals:
    header+="\tcal_%s"%(cal)
header+="\n"
fri_table.append(header)
for BpS in BpSs:
    percent=BpS_percent[BpS]
    if percent < 1:
        percent="<1%"
    else:
        percent="%.0f%%"%(percent)
    table_line='%s\t%s'%(BpS,percent)
    avg_fri_err=0
    for cal in cals:
        table_line+="\t%.2f"%(FRI_err[BpS][cal])
        avg_fri_err+=FRI_err[BpS][cal]
    avg_fri_err = avg_fri_err / float(len(cals))
    bps_fri_errors.append([BpS,avg_fri_err])
    table_line+="\n"
    fri_table.append(table_line)
#Add summary line
table_line="Sum\t100%"
for cal in cals:
    table_line+="\t%.0f"%(total_FRI_err[cal])
table_line+="\n"
fri_table.append(table_line)

#extract histogram of pixel counts of FRI by BpS
for cal in cals: 
    infile=open("%s/cfri%s.csv"%(outmaps_dir,cal),'r')
    data=infile.readlines()
    infile.close()
    for line in data:
        line=line.split(',')
        count=int(round(float(line[1])*0.09,0))
        BpS=int(line[2])
        FRI=int(line[3])
        if not FRI_LUT.has_key(BpS):
            FRI_LUT[BpS]=dict()
        if not FRI_LUT[BpS].has_key(cal):
            FRI_LUT[BpS][cal]=dict()
        FRI_LUT[BpS][cal][FRI]=count




########################################################
### Now calculate RC GOF statistics ####################
########################################################

print "Processing RC Goodness-of-fit"        
Compare_VDDT_LS(working_dir,analysis_dir,pred_RC)

#Read the LANDSUM RC summary - these are in in a separate file for each scenario

for entry in os.listdir(analysis_dir):
    if entry.count("BpS_AWSum_cal"):
        for cal in cals:
            if cal==int(re.findall("\d+",entry)[0]):
                infile=open("%s/%s"%(analysis_dir,entry),'r')
                infile.readline()
                data=infile.readlines()
                infile.close()
                for line in data:
                    line=line.split(",")
                    BpS=int(line[0])
                    AWsum=float(line[3])
                    if not RC_err.has_key(BpS):
                        RC_err[BpS]=dict()
                    RC_err[BpS][cal]=AWsum
                    if not total_RC_err.has_key(cal):
                        total_RC_err[cal]=0
                    total_RC_err[cal]+=AWsum
                break #break out of this for loop



#Create RC error table
rc_table=[]
header='BpS\tPercent'
for cal in cals:
    header+="\tcal_%s"%(cal)
header+="\n"
rc_table.append(header)
for BpS in BpSs:
    percent=BpS_percent[BpS]
    if percent < 1:
        percent="<1%"
    else:
        percent="%.0f%%"%(percent)
    table_line='%s\t%s'%(BpS,percent)
    avg_rc_err=0 #avg error across scenarios - used for highlighting high error BpS units
    for cal in cals:
        table_line+="\t%.2f"%(RC_err[BpS][cal])
        avg_rc_err+=RC_err[BpS][cal]
    avg_rc_err = avg_rc_err / float(len(cals))
    bps_rc_errors.append([BpS,avg_rc_err])
    table_line+="\n"
    rc_table.append(table_line)
#Add summary line
table_line="Sum\t100%"
for cal in cals:
    table_line+="\t%.0f"%(total_RC_err[cal])
table_line+="\n"
rc_table.append(table_line)



#sort fri and rc errors in descending order
bps_fri_errors.sort(val_srt)
for entry in bps_fri_errors[0:num_BpS_to_highlight]:
    high_fri_errors.append(entry[0])

high_rcerrors=[]
bps_rc_errors.sort(val_srt)
for entry in bps_rc_errors[0:num_BpS_to_highlight]:
    high_rc_errors.append(entry[0])

#Pick the select cal to plot and show an LS RC table for
index=int(round(float(len(cals)-1)/2.0,0))
select_cals=[cals[index]]


#Load LANDSUM RC Values for the select cal trial
for entry in os.listdir(analysis_dir):
    if entry.count("BpS_SClass_Year_cal"):
        for cal in select_cals:
            if cal==int(re.findall("\d+",entry)[0]):
                infile=open("%s/%s"%(analysis_dir,entry),'r')
                infile.readline()
                data=infile.readlines()
                for line in data:
                    line=line.split(",")
                    BpS=int(line[0])
                    SClass=SClass_label_LUT[BpS][int(line[1])]
                    Year=int(line[2])
                    Percent=int(line[3])
                    if not sim_RC.has_key(BpS):
                        sim_RC[BpS]=dict()
                    if not sim_RC[BpS].has_key(SClass):
                        sim_RC[BpS][SClass]=dict()
                    if not sim_RC[BpS][SClass].has_key(cal):
                        sim_RC[BpS][SClass][cal]=[]
                    sim_RC[BpS][SClass][cal].append(Percent)
                break


#Summarize LANDSUM results
for BpS in sim_RC:
    for SClass in sim_RC[BpS]:
        for cal in sim_RC[BpS][SClass]:
            rvals=r("c%s"%(str(sim_RC[BpS][SClass][cal]).replace('[','(').replace(']',')')))
            median=int(round(r.median(rvals).as_py(BASIC_CONVERSION),0))
            sim_RC[BpS][SClass][cal]=median


#Make the RC Tables
RC_tables=dict()
for BpS in sim_RC:
    #header
    RC_tables[BpS]=[]
    table_line="SClass\tMTDB"
    for cal in select_cals:
        table_line+="\tcal_%s"%(cal)
    table_line+="\n"
    RC_tables[BpS].append(table_line)
    #data
    SClasses=pred_RC[BpS].keys()
    SClasses.sort()
    for SClass in SClasses:
        table_line="%s\t%s"%(SClass,pred_RC[BpS][SClass])
        for cal in select_cals:
            if sim_RC[BpS][SClass].has_key(cal):
                median=sim_RC[BpS][SClass][cal]
            else:
                median=0
            table_line+="\t%s"%(median)
        table_line+="\n"
        RC_tables[BpS].append(table_line)





###########################################
### Create Word Report ####################
###########################################
print "Creating Word Report"
curDoc=Word("K:/fe/landfire/dat3/firereg/National_Data/Document_Templates/LANDSUM_Calibration_Report.doc")
curDoc.show()
curDoc.selectBookmark("Zone")
curDoc.addStyledPara("%s"%(Zone),'Heading 1')    

#Add summary information
curDoc.selectBookmark("fri_errors")
curDoc.addTable(fri_table,17)
for i in range(1,len(fri_table)-1):
    BpS=int(fri_table[i].split('\t')[0])
    row=i+1
    curDoc.wordDoc.Hyperlinks.Add(Anchor=curDoc.wordDoc.Tables(1).Rows(row).Range,Address="",SubAddress="bps%s"%(BpS))
    if BpS in high_fri_errors:
        curDoc.wordDoc.Tables(1).Rows(row).Range.Font.Color = c.wdColorRed
        curDoc.wordDoc.Tables(1).Rows(row).Range.Font.Bold = 1
curDoc.wordDoc.Tables(1).Rows(len(fri_table)).Range.Font.Bold = 1
curDoc.wordSel.InsertBreak(c.wdPageBreak)

curDoc.selectBookmark("rc_errors")
curDoc.addTable(rc_table,17)
for i in range(1,len(rc_table)-1):
    BpS=int(rc_table[i].split('\t')[0])
    row=i+1
    curDoc.wordDoc.Hyperlinks.Add(Anchor=curDoc.wordDoc.Tables(2).Rows(row).Range,Address="",SubAddress="bps%s"%(BpS))
    if BpS in high_rc_errors:           
        curDoc.wordDoc.Tables(2).Rows(row).Range.Font.Color = c.wdColorRed
        curDoc.wordDoc.Tables(2).Rows(row).Range.Font.Bold = 1
curDoc.wordDoc.Tables(1).Rows(len(rc_table)).Range.Font.Bold = 1

#BpS details
curDoc.wordSel.InsertBreak(c.wdPageBreak)
curDoc.selectBookmark("cal_details")

for BpS in BpSs:
    curDoc.wordDoc.Bookmarks.Add(Range=curDoc.wordSel.Range,Name="bps%s"%(BpS))
    curDoc.addStyledPara("BpS %s - %s"%(BpS, BpS_name[BpS]),'Heading 1')
    
    percent=BpS_percent[BpS]
    if percent < 1:
        percent="<1%"
    else:
        percent="%.0f%%"%(percent)
    curDoc.addStyledPara("%s of Zone"%(percent),'Heading 3')
    curDoc.addStyledPara("\n",'normal')
    curDoc.addStyledPara("Reference Conditions",'Heading 2')
    curDoc.addTable(RC_tables[BpS],17)
    #format MTDB column
    cur = curDoc.wordTable.Columns(2)
    cur.Borders(c.wdBorderRight).LineStyle = c.wdLineStyleSingle
    cur.Borders(c.wdBorderRight).LineWidth=c.wdLineWidth150pt
    curDoc.addStyledPara("\n",'normal')
    curDoc.addStyledPara("Comments:",'Heading 2')
    curDoc.addStyledPara("\n\n\n",'normal')
    curDoc.wordSel.InsertBreak(c.wdColumnBreak)
    curDoc.addStyledPara("\n\n\n\n\n\n\n",'normal')
    r.jpeg("c:/temp/temp.jpg",quality=100,width=350,height=350)
    r.par(omi=r("c%s"%(str([0,0,0,0]).replace('[','(').replace(']',')'))),mar=r("c%s"%(str([7,4,5,1]).replace('[','(').replace(']',')'))))
    for cal in select_cals: #need to adjust r.par if this is >1 trial
        curDoc.addStyledPara("FRI Distribution (cal_%s)"%(cal),'Heading 2')
        counts=[]
        labels=[]
        min_fri=min(FRI_LUT[BpS][cal].keys())
        MTDB_FRI=reclass_FRI(pred_FRI[BpS])
        MTDB_offset=MTDB_FRI-min_fri #offset index for the MTDB fri on the axis
        max_fri=max(FRI_LUT[BpS][cal].keys())
        if MTDB_FRI > max_fri:
            max_fri=MTDB_FRI
        LS_FRI=reclass_FRI(sim_FRI[BpS][cal])
        LS_offset=LS_FRI-min_fri
        if LS_FRI > max_fri:
            max_fri=LS_FRI

        
        fri_vals=range(min_fri,max_fri+1)
        for fri in fri_vals:
            if FRI_LUT[BpS][cal].has_key(fri):
                counts.append(FRI_LUT[BpS][cal][fri])
            else:
                counts.append(0)
            labels.append(FRI_label_LUT[fri])
        rcounts=r("c%s"%(str(counts).replace('[','(').replace(']',')')))
        rlabs=r("c%s"%(str(labels).replace('[','(').replace(']',')')))

        ticks=r.barplot(rcounts,main="",xlab="",ylab="Hectares") #this function draws and returns the tick-mark locations
        r.box()#draw the box
        pyticks=list(ticks.as_py(BASIC_CONVERSION))
        r.axis(1,ticks,rlabs,las=2,cex_axis=0.85) #add the x axis with formatted labels
        r.mtext("FRI (Years)",1,5) #Add the x axis label               
        r.axis(3,pyticks[MTDB_offset][0],"MTDB",las=2)
        r.abline(v=pyticks[MTDB_offset][0],lwd=2,lty=2)
        r.axis(3,pyticks[LS_offset][0],"LS",las=2)
        r.abline(v=pyticks[LS_offset][0],lwd=2,lty=3,col='red')
        r.dev_off()
    curDoc.addPicture("c:/temp/temp.jpg")
    curDoc.wordSel.InsertAfter('\n')
    curDoc.selectEnd()
    if not BpS==BpSs[len(BpSs)-1]:
        curDoc.wordSel.InsertBreak(c.wdPageBreak)

