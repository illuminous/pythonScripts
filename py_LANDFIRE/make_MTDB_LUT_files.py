##""********************************************************************************************************************
##AUTHOR: Brendan C. Ward, Marc H. Weber
##UPDATED: 9/1/2007
##VARIABLES TO SET AND LINE #():    Zone (24)
##                                  root (26)
##                                  veg_dir (28)
##                                  popeye (29)
##                                  inputs_dir(30)
##                                  working_dir(31)
##                                  Metadata(33)
##DATA SOURCES:
##  MTDB and VDDT mdb files (usually on network)
##  input file (*.in) templates in National Data folder on network
##
##SCRIPT DEPENDENCIES:  
##SCRIPT OUTPUTS: LANDSUM input files for zone, miscelaneous lookup tables for zone
##SCRIPT DESCRIPTION:   This script create the input files necessary to run LANDSUM
##*********************************************************************************************************************"""

import win32com.client,os,re,sets,shutil,sys
import time
#sys.path.append("k:/fe/landfire/dat3/firereg/core_scripts/shared")
sys.path.append("f:/core_scripts/shared")

#import functions from shared folder on network:
from _LANDSUM_functions import SClassID, reclass_FRI, Outcome, Disturbance
from Compare_VDDT_MTDB import *

Zone='16'
# specify folder locations:
root="k:/fe/landfire/dat3/firereg"
#veg_dir="%s/z%s/dat/current_veg_models"%(root,Zone)
veg_dir = "k:/fe/landfire/z%s/z%s_fire_regimes/dat/current_veg_models"%(Zone,Zone) # location of MTDB and VDDT

popeye = "//Pcibkqpcxx2/landsum" #change me depending on which drive on popeye is being used
#popeye = "c:/landsum"
inputs_dir = "%s/z%s/inputs"%(popeye,Zone) # where to write Landsum input files
#inputs_dir = popeye
working_dir="%s/z%s/dat/working_data"%(root,Zone)    
#working_dir=popeye

Metadata="This file was created %s\n"%(time.ctime(time.time())) #written to the top of LANDSUM input files

compare_vddt_mtdb(Zone,veg_dir) #this will create the file "VDDT_MTDB_mismatches.csv" in working_dir

VDDT_DB="%s/%sVDDT.mdb"%(veg_dir,Zone)
MTDB="%s/%sMTDB.mdb"%(veg_dir,Zone)


#misc look-up files to be stored on network and used in subsequent processes:
lutfilename="%s/BpS_SClass_LUT.csv"%(working_dir)
Pred_Dist_lutfilename="%s/BPS_SClass_Distribution.csv"%(working_dir)
FRI_lutfilename="%s/BPS_Fire_Params.csv"%(working_dir)
class_lutfilename="%s/MTDB_BpS_SClass_LUT.csv"%(working_dir)

connection=win32com.client.Dispatch(r'ADODB.Connection')
result=win32com.client.Dispatch(r'ADODB.Recordset')      

def area_sort(a,b):
    return -cmp(a[1],b[1])
def prob_sort(a,b):
    return cmp(a[1],b[1])

BpS_LUT=dict()
source="PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE=%s"%(MTDB)
connection.Open(source)

#read SClass definitions from MTDB
sclass_labels=dict()
sclass_dist=dict()
query="""SELECT AllModels.PVG_Code, AllModels.ClassAPercent, AllModels.ClassACover, AllModels.ClassAStruct,
AllModels.ClassBPercent, AllModels.ClassBCover, AllModels.ClassBStruct,
AllModels.ClassCPercent, AllModels.ClassCCover, AllModels.ClassCStruct,
AllModels.ClassDPercent, AllModels.ClassDCover, AllModels.ClassDStruct,
AllModels.ClassEPercent, AllModels.ClassECover, AllModels.ClassEStruct
FROM AllModels;"""
result.Open(query,connection,1,3)
while not result.EOF:
    bps=result.Fields.Item(0).Value
##    if BpS_LUT.has_key(bps):
##        BpS=int(BpS_LUT[bps])

    BpS=int(re.search("(?<=%s)\d\d\d\d\d"%(Zone),bps).group())
    BpS_LUT[bps]=BpS
    
    if not sclass_dist.has_key(BpS):
        sclass_dist[BpS]=dict()
    Apercent=int(result.Fields.Item(1).Value)
    Acov=result.Fields.Item(2).Value
    Astruct=result.Fields.Item(3).Value
    A_SClass=SClassID(Acov,Astruct)
    Bpercent=int(result.Fields.Item(4).Value)
    Bcov=result.Fields.Item(5).Value
    Bstruct=result.Fields.Item(6).Value
    if Bcov and Bstruct:
        B_SClass=SClassID(Bcov,Bstruct)
    else:
        B_SClass=0
    Cpercent=int(result.Fields.Item(7).Value)
    Ccov=result.Fields.Item(8).Value
    Cstruct=result.Fields.Item(9).Value
    if Ccov and Cstruct:
        C_SClass=SClassID(Ccov,Cstruct)
    else:
        C_SClass=0
    Dpercent=int(result.Fields.Item(10).Value)
    Dcov=result.Fields.Item(11).Value
    Dstruct=result.Fields.Item(12).Value
    if Dcov and Dstruct:
        D_SClass=SClassID(Dcov,Dstruct)
    else:
        D_SClass=0
    Epercent=int(result.Fields.Item(13).Value)
    Ecov=result.Fields.Item(14).Value
    Estruct=result.Fields.Item(15).Value
    if Ecov and Estruct:
        E_SClass=SClassID(Ecov,Estruct)
    else:
        E_SClass=0

    sclass_labels[BpS]=dict()
    sclass_labels[BpS][int(A_SClass)]='A'
    sclass_dist[BpS][A_SClass]=Apercent
    sclass_labels[BpS][int(B_SClass)]='B'
    sclass_dist[BpS][B_SClass]=Bpercent
    if Cpercent:
        sclass_labels[BpS][int(C_SClass)]='C'
        sclass_dist[BpS][C_SClass]=Cpercent
    if Dpercent:
        sclass_labels[BpS][int(D_SClass)]='D'
        sclass_dist[BpS][D_SClass]=Dpercent
    if Epercent:
        sclass_labels[BpS][int(E_SClass)]='E'
        sclass_dist[BpS][E_SClass]=Epercent

    result.MoveNext()
result.Close()

#Predicted FRI and other fire parameters by BpS
FRI_LUT=open(FRI_lutfilename,'w')
FRI_LUT.write("BpS,SRF_Freq,MIX_Freq,NLSF_Freq,All_Fire_Prob,All_Fire_Freq,FRI_Class,FRegimeGp,AvgSize_ha\n")
query="""SELECT AllModels.PVG_Code, AllModels.ReplaceAveFreq, AllModels.MixedSevAveFreq, AllModels.SurfaceSevAveFreq, AllModels.FRGroup, AllModels.AvgHistFireSize
FROM AllModels;"""
result.Open(query,connection,1,3)
while not result.EOF:
    bps=result.Fields.Item(0).Value
    if BpS_LUT.has_key(bps):
        BpS=int(BpS_LUT[bps])
        SRF=result.Fields.Item(1).Value
        MIX=result.Fields.Item(2).Value
        NLSF=result.Fields.Item(3).Value
        if SRF:
            SRF=float(SRF)
        else:
            SRF=1000000
        if MIX:
            MIX=float(MIX)
        else:
            MIX=1000000
        if NLSF:
            NLSF=float(NLSF)
        else:
            NLSF=1000000
        cumulative_prob=(1.0/SRF)+(1.0/MIX)+(1.0/NLSF)
        cumulative_freq=int(1.0/cumulative_prob)
        if cumulative_prob<0.000001:
            cumulative_prob=0.0
            cumulative_freq=0.0
        FRI_class=reclass_FRI(cumulative_freq)
        FReg=result.Fields.Item(4).Value
        AvgSize=result.Fields.Item(5).Value
        if not AvgSize:
            AvgSize=0.0
        AvgSize=float(AvgSize)*0.40469 #used as the source of one estimate of mean fire size for calibration
        FRI_LUT.write("%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%(BpS,SRF,MIX,NLSF,cumulative_prob,cumulative_freq,FRI_class,FReg,AvgSize))
    result.MoveNext()
result.Close()
FRI_LUT.close()
connection.Close()





print "Reading Disturbance Pathway Data"
dists=dict()
query="""SELECT Project.Name, CLng([StructuralStage]![StructuralStage]+[CoverType]![CoverType]) AS StateClassCode, ProbabilisticTransitionType.ProbabilisticTransitionType, ProbabilisticTransition.Probability, CLng([StructuralStage_1]![StructuralStage]+[CoverType_1]![CoverType]) AS StateClassCode1, ProbabilisticTransition.TSD, ProbabilisticTransition.RelativeAge, Region.RegionNumber
FROM Region INNER JOIN (ProbabilisticTransitionType INNER JOIN (CoverType AS CoverType_1 INNER JOIN (StructuralStage AS StructuralStage_1 INNER JOIN (((CoverType INNER JOIN ((Project INNER JOIN ProbabilisticTransition ON Project.PVTID = ProbabilisticTransition.PVTID) INNER JOIN StateClass AS StateClass_1 ON (StateClass_1.StateClassID = ProbabilisticTransition.ToStateClassID) AND (Project.ProjectID = StateClass_1.ProjectID)) ON CoverType.ProjectID = Project.ProjectID) INNER JOIN StateClass ON (StateClass.StateClassID = ProbabilisticTransition.StateClassID) AND (Project.ProjectID = StateClass.ProjectID) AND (CoverType.CoverTypeID = StateClass.CoverTypeID)) INNER JOIN StructuralStage ON (Project.ProjectID = StructuralStage.ProjectID) AND (StateClass.StructuralStageID = StructuralStage.StructuralStageID)) ON (Project.ProjectID = StructuralStage_1.ProjectID) AND (StructuralStage_1.StructuralStageID = StateClass_1.StructuralStageID)) ON (Project.ProjectID = CoverType_1.ProjectID) AND (CoverType_1.CoverTypeID = StateClass_1.CoverTypeID)) ON (Project.ProjectID = ProbabilisticTransitionType.ProjectID) AND (ProbabilisticTransitionType.ProbabilisticTransitionTypeID = ProbabilisticTransition.ProbabilisticTransitionTypeID)) ON (Project.RegionID = Region.RegionID) AND (Region.RegionID = ProbabilisticTransition.RegionID)
ORDER BY Project.Name, CLng([StructuralStage]![StructuralStage]+[CoverType]![CoverType]), ProbabilisticTransitionType.ProbabilisticTransitionType, ProbabilisticTransition.Probability, CLng([StructuralStage_1]![StructuralStage]+[CoverType_1]![CoverType]);"""
result.Open(query,connection,1,3)
while not result.EOF:
    bps=result.Fields.Item(0).Value
    if BpS_LUT.has_key(bps):
        BpS=int(BpS_LUT[bps])
        SClass=int(result.Fields.Item(1).value)
        Dist=int(result.Fields.Item(2).Value)
        Prob=float(result.Fields.Item(3).Value)
        SClassTo=int(result.Fields.Item(4).Value)
        TSD=int(result.Fields.Item(5).Value)
        RelAge=int(result.Fields.Item(6).Value)
        #print BpS,SClass,Dist,Prob,SClassTo,TSD,RelAge
        ToAgePair=ages[BpS][SClassTo]
        FromAgePair=ages[BpS][SClass]
        if not dists.has_key(BpS):
            dists[BpS]=dict()
        if not dists[BpS].has_key(SClass):
            dists[BpS][SClass]=dict()
        if TSD>0:  #AltSuccession w/ TSD - don't put in same slot as other AltSuccession
            if not Dist==2000:
                print "Error - AltSuccession DistID is not == 2000 ",BpS,SClass,Dist
            Dist=2100
        if not dists[BpS][SClass].has_key(Dist):
            dists[BpS][SClass][Dist]=Disturbance(SClass,Dist,TSD)
        #print bps,SClass,Dist,SClassTo,RelAge
        dists[BpS][SClass][Dist].AddOutcome(Prob,SClassTo,RelAge,FromAgePair,ToAgePair)
    result.MoveNext()
result.Close()

distfile=open(distfilename,'w')
distfile.write(Metadata)
distfile.write("Project \tZone\tBpS\tSClass\tDist\tSClass2\tProb\tAgeSet\tAgeInc\n")
scenfile=open(scenfilename,'w')
scenfile.write(Metadata)
scenfile.write("Project \tZone\tScenario\tBpS\tSClass\tDist\tProb\tCost\tBenefits\tTSD\n")
for BpS in BpSs:
    if dists.has_key(BpS):
        SClasses=dists[BpS].keys()
        SClasses.sort()
        for SClass in SClasses:
            Dists=dists[BpS][SClass].keys()
            Dists.sort()
            for Dist in Dists:
                scenline="LANDFIRE %s 1 %s %s\n"%(Zone,BpS,dists[BpS][SClass][Dist].ScenEntry())
                scenfile.write(scenline)
                #print BpS,SClass,Dist
                Outcomes=dists[BpS][SClass][Dist].DistEntry()
                for Outcome in Outcomes:
                    distline="LANDFIRE %s %s %s\n"%(Zone,BpS,Outcome)
                    distfile.write(distline)
    else:
        print "Missing BpS from Dist Table!",BpS
distfile.close()
scenfile.close()

#plan.in and vegfix.in
print "Preparing other LANDSUM input files"
planfile=open(planfilename,'w')
planfile.write(Metadata)
planfile.write("Project \tZone\tJunk\tScenario\tStartYear\tEndYear\n")
planfile.write("LANDFIRE %s 1 1 0 1000000\n"%(Zone))
planfile.close()
vegfixfile=open(vegfixfilename,'w')
vegfixfile.write(Metadata)
vegfixfile.write("Project \tZone\tBpS\tSClass\tToSClass\tProb\n")
vegfixfile.close()


#Following step creates lookup table with percent of each BpS in each Sclass (VDDT REFERENCE CONDITIONS)
#Then creates lookup table listing the highest percent occuring sclass in each BpS to initialize LANDSUM
print "Preparing Prediction Lookup Tables from VDDT (ref cons, dominant sclass)"
#Map BpS-SClass LUT   # What is this and why is it commented out?
query="""SELECT Project.Name, CLng([StructuralStage]![StructuralStage]+[CoverType]![CoverType]) AS Expr1, OutputEndingConditions.ECPercent, Region.RegionNumber
FROM ((CoverType INNER JOIN ((Project INNER JOIN OutputEndingConditions ON Project.ProjectID = OutputEndingConditions.ProjectID) INNER JOIN StateClass ON (StateClass.StateClassID = OutputEndingConditions.StateClassID) AND (Project.ProjectID = StateClass.ProjectID)) ON (Project.ProjectID = CoverType.ProjectID) AND (CoverType.CoverTypeID = StateClass.CoverTypeID)) INNER JOIN StructuralStage ON (StructuralStage.StructuralStageID = StateClass.StructuralStageID) AND (Project.ProjectID = StructuralStage.ProjectID)) INNER JOIN Region ON Project.RegionID = Region.RegionID
WHERE (((Region.RegionNumber)=1));"""
result.Open(query,connection,1,3)
while not result.EOF:
    bps=result.Fields.Item(0).Value
    if BpS_LUT.has_key(bps):
        BpS=int(BpS_LUT[bps])
        sclass=int(result.Fields.Item(1).Value)
        percent=int(round(float(result.Fields.Item(2).Value),0))
        if not sclass_dist.has_key(BpS):
            sclass_dist[BpS]=dict()
        sclass_dist[BpS][sclass]=percent
    result.MoveNext()
result.Close()
connection.Close()

pred_outfile=open(Pred_Dist_lutfilename,'w')
pred_outfile.write("BpS,SClass,Percent\n")
class_lutfile=open(class_lutfilename,'w')
class_lutfile.write("BpS,Model_SClass,Model_SClassID\n")
lutfile=open(lutfilename,'w')
for BpS in BpSs:
    sclass_list=sclass_dist[BpS].items()
    sclass_list.sort(area_sort)
    lutfile.write("%i,%i\n"%(BpS,sclass_list[0][0]))
    for sclass in sclass_list:
        pred_outfile.write("%i,%s,%s\n"%(BpS,sclass[0],sclass[1]))
        if sclass_labels[BpS].has_key(sclass[0]):
            class_lutfile.write("%i,%s,%s\n"%(BpS,sclass_labels[BpS][sclass[0]],sclass[0]))
        else:
            print "Missing Sclass Label!",BpS,sclass[0]
lutfile.close()
pred_outfile.close()
class_lutfile.close()


for bps in BpS_LUT.values():
   bps=int(bps)
   if not bps in BpSs:
       print "Error - missing required BpS",bps
       




