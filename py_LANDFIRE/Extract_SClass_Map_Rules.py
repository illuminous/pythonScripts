import os,re,win32com.client

connection=win32com.client.Dispatch(r'ADODB.Connection')
result=win32com.client.Dispatch(r'ADODB.Recordset')      

Zone=16
working_dir="C:/Documents and Settings/bward/My Documents/LANDFIRE/Vegetation Modeling/Zone16"
BpS_lutfilename="%s/BpS_LUT.csv"%(working_dir)
Spp_outfile="%s/BpS_SClass_Dom_Spp.csv"%(working_dir)
Struct_outfile="%s/BpS_SClass_Struct.csv"%(working_dir)
MTDB="%s/%iMTDB.mdb"%(working_dir,Zone)
source="PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE=%s"%(MTDB)
connection.Open(source)

BpS_LUT=dict()
BpS_LUTfile=open(BpS_lutfilename,'r')
BpS_LUTfile.readline()
lines=BpS_LUTfile.readlines()
for line in lines:
    line=line.replace('\n','').split(",")
    MTDB_ID=line[0]
    Model_ID=line[1]
    Level4_ID=line[2]
    BpS_LUT[MTDB_ID]=Model_ID
BpS_LUTfile.close()

def SClassID(cov_code,struct_code):
    struct=0
    cov=0
    if re.search("All",struct_code) or re.search("PostRep",struct_code):
        struct=1
    elif re.search("Closed",struct_code):
        struct=2
    elif re.search("Open",struct_code):
        struct=3
    if re.search("Early",cov_code):
        if re.search("1",cov_code):
            cov=1001
        elif re.search("2",cov_code):
            cov=1002
        elif re.search("3",cov_code):
            cov=1003
    elif re.search("Mid",cov_code):
        if re.search("1",cov_code):
            cov=2001
        elif re.search("2",cov_code):
            cov=2002
        elif re.search("3",cov_code):
            cov=2003        
    elif re.search("Late",cov_code):
        if re.search("1",cov_code):
            cov=3001
        elif re.search("2",cov_code):
            cov=3002
        elif re.search("3",cov_code):
            cov=3003
    if struct and cov:
        return "%s%s"%(struct,cov)
    else:
        print "Error - unknown structure / cover",struct_code,cov_code
        return 0

map_rules=dict()

for Box in ['A','B','C','D','E']:
    query = """SELECT AllModels.PVG_Code, AllModels.Class%sCover,
    AllModels.Class%sStruct, AllModels.%sUpLayLifeHerb, AllModels.%sUpLayLifeShrub,
    AllModels.%sUpLayLifeTree, AllModels.%sUpLayMinCanClosure, AllModels.%sUpLayMaxCanClosure,
    AllModels.%sUpLayMinHt, AllModels.%sUpLayMaxHt, AllModels.Class%sDominSpec1, AllModels.Class%sDominSpec2,
    AllModels.Class%sDominSpec3, AllModels.Class%sDominSpec4
    FROM AllModels;"""%(Box,Box,Box,Box,Box,Box,Box,Box,Box,Box,Box,Box,Box)
    result.Open(query,connection,1,3)
    while not result.EOF:
        BpS=result.Fields.Item(0).Value
        if BpS_LUT.has_key(BpS):
            BpS=BpS_LUT[BpS]
        BpS=int(re.search("(?<=\d\d)\d\d\d\d",str(BpS)).group())
        if not map_rules.has_key(BpS):
            map_rules[BpS]=dict()
        Cov=result.Fields.Item(1).Value
        Struct=result.Fields.Item(2).Value
        SClass=SClassID(Cov,Struct)        
        Herb=result.Fields.Item(3).Value
        Shrub=result.Fields.Item(4).Value
        Tree=result.Fields.Item(5).Value        
        MinCover=result.Fields.Item(6).Value
        MaxCover=result.Fields.Item(7).Value        
        MinHt=result.Fields.Item(8).Value
        MaxHt=result.Fields.Item(9).Value        
        Dom1=result.Fields.Item(10).Value
        Dom2=result.Fields.Item(11).Value
        Dom3=result.Fields.Item(12).Value
        Dom4=result.Fields.Item(13).Value
        if Dom1:#only add valid SClasses
            map_rules[BpS][SClass]=dict()
            map_rules[BpS][SClass]['LF']=[Herb,Shrub,Tree]
            map_rules[BpS][SClass]['Cover']=[MinCover,MaxCover]
            map_rules[BpS][SClass]['Height']=[MinHt,MaxHt]
            map_rules[BpS][SClass]['Dom']=[Dom1,Dom2,Dom3,Dom4]
        result.MoveNext()
    result.Close()

connection.Close()

outfile=open(Spp_outfile,'w')
outfile.write("BpS,SClass,Dom1,Dom2,Dom3,Dom4\n")
BpSs=map_rules.keys()
BpSs.sort()
for BpS in BpSs:
    SClasses=map_rules[BpS].keys()
    SClasses.sort()
    for SClass in SClasses:
        line ="%s,%s"%(BpS,SClass)
        for Dom in map_rules[BpS][SClass]['Dom']:
            if Dom:
                line+=",%s"%(Dom)
        line+="\n"
        outfile.write(line)
outfile.close()

outfile=open(Struct_outfile,'w')
outfile.write("BpS,SClass,LifeForm,MinCover,MaxCover,MinHt,MaxHt\n")
BpSs=map_rules.keys()
BpSs.sort()
for BpS in BpSs:
    SClasses=map_rules[BpS].keys()
    SClasses.sort()
    for SClass in SClasses:
        line="%s,%s"%(BpS,SClass)
        if map_rules[BpS][SClass]['LF'][0]:
            LF="Herb"
        elif map_rules[BpS][SClass]['LF'][1]:
            LF="Shrub"
        elif map_rules[BpS][SClass]['LF'][2]:
            LF="Tree"
        line+=",%s,%s,%s,%s,%s\n"%(LF,map_rules[BpS][SClass]['Cover'][0],map_rules[BpS][SClass]['Cover'][1],map_rules[BpS][SClass]['Height'][0],map_rules[BpS][SClass]['Height'][1])
        outfile.write(line)
outfile.close()
