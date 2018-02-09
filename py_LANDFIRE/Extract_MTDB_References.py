import win32com.client,re,sets,os
connection=win32com.client.Dispatch(r'ADODB.Connection')
result=win32com.client.Dispatch(r'ADODB.Recordset')    

working_dir="C:/Documents and Settings/bward/My Documents/LANDFIRE/Vegetation Modeling"
Zones=[10,19,13,14,12,15,16,17,18,23,24,28]


ref_dict=dict()
total=0 #counts total number of references (not unique) - compare to len(ref_dict), which is all the "unique" referenes
for Zone in Zones:
    query="SELECT AllModels.PVG_Code, AllModels.PVG_Name, AllModels.References FROM AllModels ORDER BY AllModels.PVG_Code;"
    MTDB="%s/Zone%i/%iMTDB.mdb"%(working_dir,Zone,Zone)
    source="PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE=%s"%(MTDB)
    connection.Open(source)
    result.Open(query,connection,1,3)
    while not result.EOF:
        bps=int(re.search("(?<=\d\d)\d\d\d\d\d",result.Fields.Item(0).Value).group())
        name=result.Fields.Item(1).Value
        references=result.Fields.Item(2).Value
        if references:
            references=references.split("\r\n\r")
            for ref in references:
                if ref:
                    ref=ref.replace("\n"," ")
                    #convert to string data the hard way
                    z=""
                    flag=0
                    for entry in ref:
                        try:
                            temp=str(entry)
                            z+=temp
                        except:
                            flag=1
                            pass
                    ref=z.strip()
                    if not ref_dict.has_key(ref):
                        #set up the data structure - placeholders for National and RA data
                        ref_dict[ref]=dict()
                        ref_dict[ref]["Zone"]=sets.Set()
                        ref_dict[ref]["BpS"]=sets.Set()
                        ref_dict[ref]["Flag"]=flag
                        ref_dict[ref]["PNVG"]=sets.Set()
                        ref_dict[ref]["RAZone"]=sets.Set()
                    #since this is just National data, only add Zone & BpS
                    ref_dict[ref]["Zone"].add(Zone)
                    ref_dict[ref]["BpS"].add(bps)
                    total+=1
        result.MoveNext()
    result.Close()
    connection.Close()

for modelset in ['RAwest','RAeast']:
    query="SELECT AllModels.PVG_Code, AllModels.PVG_Name, AllModels.References, AllModels.Alaska, AllModels.California, AllModels.GreatBasin, AllModels.GreatLakes, AllModels.Northeast, AllModels.NorthernPlains, AllModels.NorthernRockies, AllModels.PacificNorthwest, AllModels.SouthCentral, AllModels.Southeast, AllModels.SouthernAppalations, AllModels.Southwest FROM AllModels ORDER BY AllModels.PVG_Code;"
    MTDB="%s/RapidAssessment/MTDB_%s_Final.mdb"%(working_dir,modelset)
    source="PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE=%s"%(MTDB)
    connection.Open(source)
    result.Open(query,connection,1,3)
    while not result.EOF:
        #bps=int(re.search("(?<=\d\d)\d\d\d\d\d",result.Fields.Item(0).Value).group())
        pnvg=str(result.Fields.Item(0).Value)
        name=result.Fields.Item(1).Value
        references=result.Fields.Item(2).Value
        ak=result.Fields.Item(3).Value
        ca=result.Fields.Item(4).Value
        gb=result.Fields.Item(5).Value
        gl=result.Fields.Item(6).Value
        ne=result.Fields.Item(7).Value
        np=result.Fields.Item(8).Value
        nr=result.Fields.Item(9).Value
        pnw=result.Fields.Item(10).Value
        sc=result.Fields.Item(11).Value
        se=result.Fields.Item(12).Value
        sa=result.Fields.Item(13).Value
        sw=result.Fields.Item(14).Value

        #parse the checkboxes for region (above) into text regions
        RAZones=[]
        if ak:
            RAZones.append("Alaska")
        if ca:
            RAZones.append("California")
        if gb:
            RAZones.append("Great Basin")
        if gl:
            RAZones.append("Great Lakes")
        if ne:
            RAZones.append("Northeast")
        if np:
            RAZones.append("Northern Plains")
        if nr:
            RAZones.append("Northern Rockies")
        if pnw:
            RAZones.append("Pacific Northwest")
        if sc:
            RAZones.append("South Central")
        if se:
            RAZones.append("Southeast")
        if sa:
            RAZones.append("Southern Appalachia")
        if sw:
            RAZones.append("Southwest")
        
        if references:
            references=references.split("\r\n\r")
            for ref in references:
                if ref:
                    ref=ref.replace("\n"," ")
                    #convert to string data the hard way
                    z=""
                    flag=0
                    for entry in ref:
                        try:
                            temp=str(entry)
                            z+=temp
                        except:
                            flag=1
                            pass
                    ref=z.strip()
                    if not ref_dict.has_key(ref):
                        ref_dict[ref]=dict()
                        ref_dict[ref]=dict()
                        ref_dict[ref]["Zone"]=sets.Set()
                        ref_dict[ref]["BpS"]=sets.Set()
                        ref_dict[ref]["Flag"]=flag
                        ref_dict[ref]["PNVG"]=sets.Set()
                        ref_dict[ref]["RAZone"]=sets.Set()
                    for RAZone in RAZones:
                        ref_dict[ref]["RAZone"].add(RAZone)
                    ref_dict[ref]["PNVG"].add(pnvg)
                    total+=1
        result.MoveNext()
    result.Close()
    connection.Close()
    

outfile=open("%s/Model_Citations.csv"%(working_dir),'w')
outfile.write("Citation,Zones,Models,RA_Zones,RA_PNVGs,Parse_Error\n")
refs=ref_dict.keys()
refs.sort()
for ref in refs:
    zones=list(ref_dict[ref]["Zone"])
    bps=list(ref_dict[ref]["BpS"])
    razones=list(ref_dict[ref]["RAZone"])
    pnvgs=list(ref_dict[ref]["PNVG"])
    error=""
    if ref_dict[ref]["Flag"]:
        error="Error"
    zones.sort()
    bps.sort()
    razones.sort()
    pnvgs.sort()
    
    zones=str(zones).replace('[','').replace(']','')
    if zones:
        zones='"%s"'%(zones)
    bps=str(bps).replace('[','').replace(']','')
    if bps:
        bps='"%s"'%(bps)
    razones=str(razones).replace('[','').replace(']','')
    if razones:
        razones='"%s"'%(razones)
    pnvgs=str(pnvgs).replace('[','').replace(']','')
    if pnvgs:
        pnvgs='"%s"'%(pnvgs)
    outfile.write(u'"%s",%s,%s,%s,%s,%s\n'%(ref,zones,bps,razones,pnvgs,error))

outfile.close()
