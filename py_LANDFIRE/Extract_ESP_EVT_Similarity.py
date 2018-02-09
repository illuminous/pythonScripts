import win32com.client,os,re,sets
from rpy import *
set_default_mode(NO_CONVERSION)
r.library("cluster")
from _Load_LUTs import *
from _Word_Wrapper import *

Zone='08'
working_dir="C:/Documents and Settings/bward/My Documents/LANDFIRE/Vegetation Modeling/Zone%s"%(Zone)
LUT=LUT_type(Zone,[])
LFRDB="%s/z%s_LFRDB.mdb"%(working_dir,Zone)
source="PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE=%s"%(LFRDB)
connection=win32com.client.Dispatch(r'ADODB.Connection')
result=win32com.client.Dispatch(r'ADODB.Recordset')      


def make_matrix(triangle_vector, units):
    #take a vector representing the lower half of a dissimilarity matrix and use it to populate a symmetric, normalized dissimilarity matrix
    min_dis=min(triangle_vector)
    max_dis=max(triangle_vector)
    ret=dict()
    cur_index=0
    
    for unit1 in units:
        if not ret.has_key(unit1):
            ret[unit1]=dict()
        for unit2 in units:
            ret[unit1][unit2]=""
    for unit1 in units:
        if cur_index+1 < len(units):
            for unit2 in units[cur_index+1:]:
                value=triangle_vector.pop(0)
                #rescale
                value="%.0f"%(100-100.0*(value-min_dis)/(max_dis-min_dis))
                ret[unit1][unit2]=value
                ret[unit2][unit1]=value
        cur_index+=1
    return ret


ESP_plots=dict()
ESP_spps=dict()
all_spps=sets.Set()

connection.Open(source)
query="""SELECT Z%s_Map_Attributes.LF_ESPCode, Count(Z%s_Map_Attributes.Master_ID) AS CountOfMaster_ID
FROM Z%s_Map_Attributes INNER JOIN Z%s_Map_Attributes_QAQC ON Z%s_Map_Attributes.Master_ID = Z%s_Map_Attributes_QAQC.Master_ID
GROUP BY Z%s_Map_Attributes.LF_ESPCode, Z%s_Map_Attributes_QAQC.ESP_Discard
HAVING (((Z%s_Map_Attributes.LF_ESPCode)>0) AND ((Z%s_Map_Attributes_QAQC.ESP_Discard)=0))
ORDER BY Z%s_Map_Attributes.LF_ESPCode;"""%(Zone,Zone,Zone,Zone,Zone,Zone,Zone,Zone,Zone,Zone,Zone)
result.Open(query,connection,1,3)
while not result.EOF:
    ESP=int(result.Fields.Item(0).Value)
    plots=int(result.Fields.Item(1).Value)
    ESP_plots[ESP]=plots
    result.MoveNext()
result.Close()


try:
    connection.Execute("DROP TABLE Temp1;")
except:
    pass

query="""SELECT Z%s_Map_Attributes.Master_ID, Z%s_Map_Attributes_QAQC.ESP_Discard,
Z%s_Map_Attributes.LF_ESPCode, Z%s_Species_Comp.Scientific_Name, Z%s_Species_Comp.AC_or_ABA, Plots.totcov,
[AC_or_ABA]/[totcov] AS RC INTO Temp1
FROM ((Plots INNER JOIN Z%s_Map_Attributes ON Plots.Master_ID = Z%s_Map_Attributes.Master_ID)
INNER JOIN Z%s_Species_Comp ON Z%s_Map_Attributes.Master_ID = Z%s_Species_Comp.Master_ID)
INNER JOIN Z%s_Map_Attributes_QAQC ON (Z%s_Species_Comp.Master_ID = Z%s_Map_Attributes_QAQC.Master_ID)
AND (Z%s_Map_Attributes.Master_ID = Z%s_Map_Attributes_QAQC.Master_ID)
WHERE (((Z%s_Map_Attributes_QAQC.ESP_Discard)=0) AND ((Z%s_Map_Attributes.LF_ESPCode)>0))
ORDER BY Z%s_Map_Attributes.LF_ESPCode, Z%s_Species_Comp.Scientific_Name;"""%(Zone,Zone,Zone,Zone,Zone,Zone,Zone,Zone,Zone,Zone,Zone,Zone,Zone,Zone,Zone,Zone,Zone,Zone,Zone)
connection.Execute(query)


query="""SELECT Temp1.LF_ESPCode, Temp1.Scientific_Name, Avg(Temp1.AC_or_ABA) AS AvgOfAC_or_ABA,
[RC]*100 AS Expr1, Count(Temp1.Master_ID) AS CountOfMaster_ID
FROM Temp1
GROUP BY Temp1.LF_ESPCode, Temp1.Scientific_Name, [RC]*100
HAVING ((([RC]*100)>1))
ORDER BY Temp1.LF_ESPCode, Temp1.Scientific_Name;"""
result.Open(query,connection,1,3)
while not result.EOF:
    ESP=int(result.Fields.Item(0).Value)
    if ESP>=1000:
        spp=str(result.Fields.Item(1).Value)
        all_spps.add(spp)
        avg_AC=float(result.Fields.Item(2).Value)
        RC=max(100.0,float(result.Fields.Item(3).Value))#cap at 100% cover
        Count=float(result.Fields.Item(4).Value)
        constancy=100.0*Count/float(ESP_plots[ESP])
        RIV=(RC+constancy)/2.0
        #RIV=constancy
        if not ESP_spps.has_key(ESP):
            ESP_spps[ESP]=dict()
        ESP_spps[ESP][spp]=RIV
    result.MoveNext()
result.Close()

try:
    connection.Execute("DROP TABLE Temp1;")
except:
    pass


EVT_plots=dict()
EVT_spps=dict()
all_spps=sets.Set()

query="""SELECT Z%s_Map_Attributes.LF_EVTCode, Count(Z%s_Map_Attributes.Master_ID) AS CountOfMaster_ID
FROM Z%s_Map_Attributes INNER JOIN Z%s_Map_Attributes_QAQC ON Z%s_Map_Attributes.Master_ID = Z%s_Map_Attributes_QAQC.Master_ID
GROUP BY Z%s_Map_Attributes.LF_EVTCode, Z%s_Map_Attributes_QAQC.EVT_Discard
HAVING (((Z%s_Map_Attributes.LF_EVTCode)>0) AND ((Z%s_Map_Attributes_QAQC.EVT_Discard)=0))
ORDER BY Z%s_Map_Attributes.LF_EVTCode;"""%(Zone,Zone,Zone,Zone,Zone,Zone,Zone,Zone,Zone,Zone,Zone)
result.Open(query,connection,1,3)
while not result.EOF:
    EVT=int(result.Fields.Item(0).Value)
    plots=int(result.Fields.Item(1).Value)
    EVT_plots[EVT]=plots
    result.MoveNext()
result.Close()


try:
    connection.Execute("DROP TABLE Temp1;")
except:
    pass

query="""SELECT Z%s_Map_Attributes.Master_ID, Z%s_Map_Attributes_QAQC.EVT_Discard,
Z%s_Map_Attributes.LF_EVTCode, Z%s_Species_Comp.Scientific_Name, Z%s_Species_Comp.AC_or_ABA, Plots.totcov,
[AC_or_ABA]/[totcov] AS RC INTO Temp1
FROM ((Plots INNER JOIN Z%s_Map_Attributes ON Plots.Master_ID = Z%s_Map_Attributes.Master_ID)
INNER JOIN Z%s_Species_Comp ON Z%s_Map_Attributes.Master_ID = Z%s_Species_Comp.Master_ID)
INNER JOIN Z%s_Map_Attributes_QAQC ON (Z%s_Species_Comp.Master_ID = Z%s_Map_Attributes_QAQC.Master_ID)
AND (Z%s_Map_Attributes.Master_ID = Z%s_Map_Attributes_QAQC.Master_ID)
WHERE (((Z%s_Map_Attributes_QAQC.EVT_Discard)=0) AND ((Z%s_Map_Attributes.LF_EVTCode)>0))
ORDER BY Z%s_Map_Attributes.LF_EVTCode, Z%s_Species_Comp.Scientific_Name;"""%(Zone,Zone,Zone,Zone,Zone,Zone,Zone,Zone,Zone,Zone,Zone,Zone,Zone,Zone,Zone,Zone,Zone,Zone,Zone)
connection.Execute(query)


query="""SELECT Temp1.LF_EVTCode, Temp1.Scientific_Name, Avg(Temp1.AC_or_ABA) AS AvgOfAC_or_ABA,
[RC]*100 AS Expr1, Count(Temp1.Master_ID) AS CountOfMaster_ID
FROM Temp1
GROUP BY Temp1.LF_EVTCode, Temp1.Scientific_Name, [RC]*100
HAVING ((([RC]*100)>1))
ORDER BY Temp1.LF_EVTCode, Temp1.Scientific_Name;"""
result.Open(query,connection,1,3)
while not result.EOF:
    EVT=int(result.Fields.Item(0).Value)
    if EVT > 2000:
        spp=str(result.Fields.Item(1).Value)
        all_spps.add(spp)
        avg_AC=float(result.Fields.Item(2).Value)
        RC=max(100.0,float(result.Fields.Item(3).Value))#cap at 100% cover
        Count=float(result.Fields.Item(4).Value)
        constancy=100.0*Count/float(EVT_plots[EVT])
        RIV=(RC+constancy)/2.0
        if not EVT_spps.has_key(EVT):
            EVT_spps[EVT]=dict()
        EVT_spps[EVT][spp]=RIV
    result.MoveNext()
result.Close()

try:
    connection.Execute("DROP TABLE Temp1;")
except:
    pass

connection.Close()


spps=list(all_spps)
spps.sort()
ESPs=ESP_spps.keys()
ESPs.sort()
rdata=dict()

for ESP in ESPs:
    for spp in spps:
        RIV=0
        if ESP_plots.has_key(ESP) and ESP_spps.has_key(ESP) and ESP_spps[ESP].has_key(spp):
            RIV =ESP_spps[ESP][spp]
        if not rdata.has_key(spp):
            rdata[spp]=[]
        rdata[spp].append(RIV)
rdata=r.data_frame(rdata)
r.assign("data",rdata)
r("row.names(data)=c(%s)"%(str(ESPs).replace('[','').replace(']','')))
esp_agnes=r('agnes(data,method="ward")')
esp_matrix=make_matrix(esp_agnes.as_py(BASIC_CONVERSION)['diss'],ESPs)

spps=list(all_spps)
spps.sort()
EVTs=EVT_spps.keys()
EVTs.sort()
rdata=dict()

for EVT in EVTs:
    for spp in spps:
        RIV=0
        if EVT_plots.has_key(EVT) and EVT_spps.has_key(EVT) and EVT_spps[EVT].has_key(spp):
            RIV =EVT_spps[EVT][spp]
        if not rdata.has_key(spp):
            rdata[spp]=[]
        rdata[spp].append(RIV)
rdata=r.data_frame(rdata)
r.assign("data",rdata)
r("row.names(data)=c(%s)"%(str(EVTs).replace('[','').replace(']','')))
evt_agnes=r('agnes(data,method="ward")')
evt_matrix=make_matrix(evt_agnes.as_py(BASIC_CONVERSION)['diss'],EVTs)




print "Creating Word Report"
curDoc=Word("K:/fe/landfire/dat3/firereg/National_Data/Document_Templates/ESP_EVT_Similarity.dot")
curDoc.show()
r.jpeg("c:/temp/ESP.jpg",quality=100,width=950,height=700)
r.par(omi=r("c%s"%(str([0,0,0,0]).replace('[','(').replace(']',')'))),mar=r("c%s"%(str([2,4,2,1]).replace('[','(').replace(']',')'))))
r.plot(esp_agnes,main="ESP Unit Similarity - Zone %s"%(Zone),xlab="",ylab="Dissimilarity",which_plots=2)
r.dev_off()
curDoc.addPicture("c:/temp/ESP.jpg")
curDoc.selectEnd()
##curDoc.wordSel.InsertBreak(c.wdPageBreak)
##curDoc.addStyledPara("ESP Similarity Matrix",'Heading 3')
##esp_table=["ESP\t%s\n"%(str(ESPs).replace('[','').replace(']','').replace(",",'\t'))]
##for ESP1 in ESPs:
##    line="%s"%(ESP1)
##    for ESP2 in ESPs:
##        line+="\t%s"%(esp_matrix[ESP1][ESP2])
##    line+="\n"
##    esp_table.append(line)
##curDoc.addTable(esp_table,17)
##curDoc.wordTable.Range.Font.Size = 8

outfile=open("%s/z%s_ESP_Similarity.csv"%(working_dir,Zone),'w')
outfile.write("ESP1,ESP2,Rel_Similarity\n")
for ESP1 in ESPs:
    for ESP2 in ESPs:
        if not ESP1==ESP2:
            outfile.write("%s,%s,%s\n"%(ESP1,ESP2,esp_matrix[ESP1][ESP2]))
outfile.close()


curDoc.addStyledPara("\nESP Names",'Heading 3')
for ESP in ESPs:
    name=""
    if LUT.ESP_names.has_key(ESP):
        name=LUT.ESP_names[ESP]
    else:
        print "Missing ESP from Westmaster",ESP
    curDoc.addStyledPara("%s: %s"%(ESP,name),'normal')

curDoc.wordSel.InsertBreak(c.wdPageBreak)
r.jpeg("c:/temp/EVT.jpg",quality=100,width=950,height=700)
r.par(omi=r("c%s"%(str([0,0,0,0]).replace('[','(').replace(']',')'))),mar=r("c%s"%(str([2,4,2,1]).replace('[','(').replace(']',')'))))
r.plot(evt_agnes,main="EVT Unit Similarity - Zone %s"%(Zone),xlab="",ylab="Dissimilarity",which_plots=2)
r.dev_off()
curDoc.addPicture("c:/temp/EVT.jpg")
curDoc.selectEnd()
##curDoc.wordSel.InsertBreak(c.wdPageBreak)
##curDoc.addStyledPara("EVT Similarity Matrix",'Heading 3')
##evt_table=["EVT\t%s\n"%(str(EVTs).replace('[','').replace(']','').replace(",",'\t'))]
##for EVT1 in EVTs:
##    line="%s"%(EVT1)
##    for EVT2 in EVTs:
##        line+="\t%s"%(evt_matrix[EVT1][EVT2])
##    line+="\n"
##    evt_table.append(line)
##curDoc.addTable(evt_table,17)
##curDoc.wordTable.Range.Font.Size = 8


outfile=open("%s/z%s_EVT_Similarity.csv"%(working_dir,Zone),'w')
outfile.write("EVT1,EVT2,Rel_Similarity\n")
for EVT1 in EVTs:
    for EVT2 in EVTs:
        if not EVT1==EVT2:
            outfile.write("%s,%s,%s\n"%(EVT1,EVT2,evt_matrix[EVT1][EVT2]))
outfile.close()




curDoc.addStyledPara("\nEVT Names",'Heading 3')
for EVT in EVTs:
    name=""
    if LUT.EVT_names.has_key(EVT):
        name=LUT.EVT_names[EVT]
    else:
        print "Missing EVT from Westmaster",EVT
    curDoc.addStyledPara("%s: %s"%(EVT,name),'normal')
