import re,os,sets,time,sys, Queue
from rpy import *
set_default_mode(NO_CONVERSION)
r.library("randomForest")
from _RFTree import *
from _Proc_Data import *

Zone="55"
working_dir="C:/temp/1045"#z%s"%(Zone)

MAT_filename="%s/z%s_1450_sclass.csv"%(working_dir,Zone) #The file containing assignments to plots
root="%s/z%s_1450_sclass"%(working_dir,Zone) #the root name of the classifications - output root

#The predictor files
geotable="%s/Z%s_Geo.csv"%(working_dir,Zone)
gradtable="%s/Z%s_Gradients.csv"%(working_dir,Zone)
imagetable="%s/Z%s_Imagery.csv"%(working_dir,Zone)
vegtable="%s/Z%s_Veg.csv"%(working_dir,Zone)  #changme!
species_comp_filename="%s/Z%s_Species_Comp.csv"%(working_dir,Zone)
exotics_filename="%s/z%s_Exotics.csv"%(working_dir,Zone)#not used here, but required as an input to one of the functions
xf_presence_filename="%s/z%s_presence_XF.csv"%(working_dir,Zone) #not used here, but required as an input to one of the functions

def rev_val_srt(a,b):
    return -cmp(a[1],b[1])

###Z12 predictor list
# independents=['f_glshi', 'offb9', 'dem', 'VEG_evt', 'pari', 'g_glshi', 'swavgfdi', 'onb9', 'wxsradi', 'tmini', 'f_ppfdi', 'f_peti', 'g_peti', 'relhumi', 'f_tsoili', 'g_tsoili', 'ddayi', 'sprb9', 'f_dsri', 'g_transi', 'tnighti', 'f_evapi', 'offtc3', 'sprb2', 'tdayi', 'vpdi', 'offtc2', 'offb5', 'tpi2000', 'g_dsri', 'tavei', 'g_eti', 'f_vmci', 'tmaxi', 'sprb1', 'g_evapi', 'g_vmci', 'g_ppfdi', 'g_soilwi', 'ontc2']

# independents.extend(['VEG_esp','VEG_evt','VEG_evc'])
# independents.extend(['ESP_Discard','EVT_Discard']) #include these for filtering plots
independents=['dem','slpp','asp_cl8','mxdepth','tpi150','tpi300','tpi2000','d2coast1k','d2coast1k','ycoord_2k','hli','lae']

######Gradients
independents.extend(['ddayi','pari','ppti','relhumi','swavgfdi','tavei','tdayi','tmaxi','tmini','tnighti',
                     'vpdi','wxsradi','f_cwdci','f_dsri','f_eti','f_evapi','f_gcshi','f_glshi','f_gppi','f_gswsi',
                     'f_mxlaii','f_mxpsii','f_nindexi','f_nppi','f_outflowi','f_peti','f_ppfdi','f_psii',
                     'f_rautoi','f_rheti','f_snowwi','f_soilci','f_soilwi','f_transi','f_tsoili',
                     'f_vmci','g_dsri','g_eti','g_evapi','g_gcshi','g_glshi','g_gppi','g_gswsi','g_mxlaii',
                     'g_mxpsii','g_nindexi','g_nppi','g_outflowi','g_peti','g_ppfdi','g_psii','g_rautoi','g_rheti',
                     'g_snowwi','g_soilci','g_soilwi','g_transi','g_tsoili','g_vmci'])
#####Imagery
independents.extend(['onb1','onb2','onb3','onb4','onb5','onb6','onb9','ontc1','ontc2','ontc3',
                     'offb1','offb2','offb3','offb4','offb5','offb6','offb9','offtc1','offtc2','offtc3',
                     'sprb1','sprb2','sprb3','sprb4','sprb5','sprb6','sprb9','sprtc1','sprtc2','sprtc3'])

independents=['g_evapi', 'f_nindexi', 'onb3', 'offb9', 'g_gppi', 'dem', 'g_mxpsii', 'sprb9', 'ontc2', 'g_outflowi', 'offb3', 'tavei', 'g_glshi', 'g_transi', 'g_mxlaii', 'tmaxi', 'onb9', 'g_tsoili', 'f_cwdci', 'f_psii', 'swavgfdi', 'ontc3', 'offb6', 'f_eti', 'g_nppi', 'pari', 'g_rautoi', 'offb4', 'g_rheti', 'tpi300', 'f_soilwi', 'f_transi', 'onb6', 'f_evapi', 'ontc1', 'f_gswsi', 'g_psii', 'wxsradi', 'g_eti', 'onb2']

plot_species=read_plot_data(species_comp_filename,exotics_filename)#LUT of species data per plot
plots=dict()#LUT of dep and indep plot data
predictors=read_indep_data(plots,independents,vegtable,geotable,gradtable,imagetable) #Read in predictors
predictors=list(predictors)
for bad_predictor in ['ESP_Discard','EVT_Discard']: #keep these predictors from being used in the classification trees, only used for QA/QC
    if bad_predictor in predictors:
        predictors.remove(bad_predictor)
predictors.sort()

var_LUT=dict() #LUT of predictor variable to its ID
i=0
for predictor in predictors:
    var_LUT[predictor]=i
    i+=1

#set tree-building parameters
numTrees=100
numVars=40

PlotIDs=[]
classes=dict()
infile=open(MAT_filename,'r')
infile.readline()
data=infile.readlines()
infile.close()
for line in data:
    line=line.split(',')
    plot=int(line[0]) #Plot ID
    if plots.has_key(plot): #and not plots[plot]['indep']["EVT_Discard"]: #if this is a valid plot and we haven't thrown it out
        sclass=int(line[1])
        PlotIDs.append(plot)
        plots[plot]['dep']=[sclass]
        classes[sclass]=sclass




##################################################
# Mask Cross-Validation ##########################
##################################################
report=open("%s_mask.report"%(root),'w')
CV_groups=make_CV_groups(plots)  #partition plots into 10 CV groups
rf_cv=dict()
cmd="xf~" + str(predictors).replace("]",'').replace("[",'').replace(",","+").replace("'",'')
for CV_group in range(0,10):   
    #stratify plots into training & validation subsets
    print "Fold",CV_group+1
    training_plots=[]
    cv_plots=[]
    for plot in PlotIDs:
        if CV_groups[plot]==CV_group: #withold
            cv_plots.append(plot)
        else:
            training_plots.append(plot)

    rfvarsfilename="%s_mask.vars"%(root)    
    rfdatafilename=root+"_mask_training_data.csv"
    rfdatafile=open(rfdatafilename,'w')
    header=""
    for predictor in predictors:
        header+="%s,"%(predictor)
    header+="xf\n"
    rfdatafile.write(header)
    for plot in training_plots:
        line=""
        for predictor in predictors:
            line+="%s,"%(plots[plot]['indep'][predictor])
        xf=plots[plot]['dep'][0]
        line+="%s\n"%(xf)
        rfdatafile.write(line)
    rfdatafile.close()

    varfile=open(rfvarsfilename,'w')
    i=0
    for predictor in predictors:
        line="%i %s\n"%(i,predictor)
        varfile.write(line)
        i+=1
    varfile.close()
    
    print "Running Random Forest"
    rf=r("""
    data=read.csv("%s",header=T)
    data$xf = as.factor(data$xf)
    randomForest(%s,data=data,ntree=%i)
    """%(rfdatafilename,cmd,numTrees))
    class_LUT=classes.keys()
    class_LUT.sort()
    write_RFTree("C",rf,numTrees,"%s_mask"%(root),class_LUT)
rftrees=read_RFTree("%s_mask"%(root))

#use the trees to classify the hold-out plots
for plot in cv_plots:
    assign_xf=plots[plot]['dep'][0]
    if not rf_cv.has_key(assign_xf):
        rf_cv[assign_xf]=dict()
    case=[]
    for predictor in predictors:
        case.append(int(plots[plot]['indep'][predictor]))
    pred_class=predict_RFTree("C",rftrees,case)
    if not rf_cv[assign_xf].has_key(pred_class):
        rf_cv[assign_xf][pred_class]=0
    rf_cv[assign_xf][pred_class]+=1

#create the crosstabs
report.write("\n\n10-Fold Cross-Validation:\n")
line="Class"
for xf in classes:
    line+="\t%s"%(xf)
line+="\tError\n"
report.write(line)
col_totals=dict()
row_totals=dict()
total_correct=0
total=0

for xf1 in classes:
    line="%s"%(xf1)
    err=1.0
    row_correct=0
    row_total=0
    for xf2 in classes:
        if not col_totals.has_key(xf2):
            col_totals[xf2]=0
        plot_count=""
        if rf_cv.has_key(xf1) and rf_cv[xf1].has_key(xf2):
            plot_count=rf_cv[xf1][xf2]            
            if xf1==xf2:
                row_correct+=plot_count
            col_totals[xf2]+=plot_count
            row_total+=plot_count
        line+="\t%s"%(plot_count)
    if row_total:
        err=1.0-float(row_correct)/float(row_total)
    else:
        err=0.0
    row_totals[xf1]=row_total
    total_correct+=row_correct
    total+=row_total
    line+="\t%.3f\n"%(err)
    report.write(line)
observed_correct=float(total_correct)/float(total)
total_diag=0
total_matrix=0
for xf in classes:
    diag=0
    if row_totals.has_key(xf):
        if col_totals.has_key(xf):
            diag=row_totals[xf]*col_totals[xf]
        total_diag+=diag
        for xf2 in classes:
            cur=0
            if col_totals.has_key(xf2):
                cur=row_totals[xf]*col_totals[xf2]
            total_matrix+=cur
expected_correct=float(total_diag)/float(total_matrix)
kappa=(observed_correct-expected_correct)/(1-expected_correct)
report.write("Total Error: %.3f\n"%(1.0-observed_correct))
report.write("Accuracy: %.3f\n"%(100.0*observed_correct))
report.write("Kappa: %.3f"%(kappa))


####################################################
### Mask Classification  ###########################
####################################################
rfvarsfilename="%s_mask.vars"%(root)    
rfdatafilename=root+"_mask_training_data.csv"
rfdatafile=open(rfdatafilename,'w')
header=""
for predictor in predictors:
    header+="%s,"%(predictor)
header+="xf\n"
rfdatafile.write(header)
for plot in PlotIDs:
    line=""
    for predictor in predictors:
        line+="%s,"%(plots[plot]['indep'][predictor])
    xf=plots[plot]['dep'][0]
    line+="%s\n"%(xf)
    rfdatafile.write(line)
rfdatafile.close()

varfile=open(rfvarsfilename,'w')
i=0
for predictor in predictors:
    line="%i %s\n"%(i,predictor)
    varfile.write(line)
    i+=1
varfile.close()

print "Running Random Forest"
rf=r("""
data=read.csv("%s",header=T)
data$xf = as.factor(data$xf)
randomForest(%s,data=data,ntree=%i)
"""%(rfdatafilename,cmd,numTrees))

#extract RF importance matrix
imp_matrix=dict()
imp=r.importance(rf).as_py(BASIC_CONVERSION)
for i in range(0,len(predictors)):
    imp_matrix[predictors[i]]=imp[i][0]
#sort in decreasing importance
imp_list=imp_matrix.items()
imp_list.sort(rev_val_srt)
i=1
temp=[]
for entry in imp_list:
    if i<=numVars:
        temp.append(entry[0])
        i+=1
    else:
        break
predictors=temp


class_LUT=classes.keys()
class_LUT.sort()
write_RFTree("C",rf,numTrees,"%s_mask"%(root),class_LUT)
rftrees=read_RFTree("%s_mask"%(root))
#use the trees to classify the hold-out plots
rf_cv=dict()
for plot in PlotIDs:
    assign_xf=plots[plot]['dep'][0]
    if not rf_cv.has_key(assign_xf):
        rf_cv[assign_xf]=dict()
    case=[]
    for predictor in predictors:
        case.append(int(plots[plot]['indep'][predictor]))
    pred_class=predict_RFTree("C",rftrees,case)
    if not rf_cv[assign_xf].has_key(pred_class):
        rf_cv[assign_xf][pred_class]=0
    rf_cv[assign_xf][pred_class]+=1

###create the crosstabs
report.write("\n\nFull Training Dataset Cross-Validation:\n")
line="Class"
for xf in classes:
    line+="\t%s"%(xf)
line+="\tError\n"
report.write(line)
col_totals=dict()
row_totals=dict()
total_correct=0
total=0

for xf1 in classes:
    line="%s"%(xf1)
    err=1.0
    row_correct=0
    row_total=0
    for xf2 in classes:
        if not col_totals.has_key(xf2):
            col_totals[xf2]=0
        plot_count=""
        if rf_cv.has_key(xf1) and rf_cv[xf1].has_key(xf2):
            plot_count=rf_cv[xf1][xf2]            
            if xf1==xf2:
                row_correct+=plot_count
            col_totals[xf2]+=plot_count
            row_total+=plot_count
        line+="\t%s"%(plot_count)
    if row_total:
        err=1.0-float(row_correct)/float(row_total)
    else:
        err=0.0
    row_totals[xf1]=row_total
    total_correct+=row_correct
    total+=row_total
    line+="\t%.3f\n"%(err)
    report.write(line)
observed_correct=float(total_correct)/float(total)
total_diag=0
total_matrix=0
for xf in classes:
    diag=0
    if row_totals.has_key(xf):
        if col_totals.has_key(xf):
            diag=row_totals[xf]*col_totals[xf]
        total_diag+=diag
        for xf2 in classes:
            cur=0
            if col_totals.has_key(xf2):
                cur=row_totals[xf]*col_totals[xf2]
            total_matrix+=cur
expected_correct=float(total_diag)/float(total_matrix)
kappa=(observed_correct-expected_correct)/(1-expected_correct)
report.write("Total Error: %.3f\n"%(1.0-observed_correct))
report.write("Accuracy: %.3f\n"%(100.0*observed_correct))
report.write("Kappa: %.3f"%(kappa))
report.close()



