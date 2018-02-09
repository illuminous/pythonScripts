import win32com.client,os,re,sets,codecs,shutil
connection=win32com.client.Dispatch(r'ADODB.Connection')
result=win32com.client.Dispatch(r'ADODB.Recordset')

Zones=['18','19','23','24','28','03','06','08','09','10','12','13','14','15','16','17']
#Zones=['10']
redo_Zones=['12','15','16','17','18','23','24','28']
working_dir="e:/landsum/BpS_issues"

bps_areas=dict() #tally area in each BpS in each Zone
zone_areas=dict()
total_area=0 #total area across all Zones
BpS_fire=dict()
for Zone in Zones:
    print "Zone %s: Extracting BpS Areas"%(Zone)
    #extract
    if os.access("k:/fe/landfire/dat4/veg/z%s/bps/gis_fin/z%s_bps"%(Zone,Zone),os.F_OK):
        if not os.access("%s/z%s_bps.csv"%(working_dir,Zone),os.F_OK):
            bps_dir="k:/fe/landfire/dat4/veg/z%s/bps/gis_fin/"%(Zone)
            amlfilename="c:/temp/Extract_BpS_Areas.aml"

            amldata="""
            &sv zone = %s
            &sv working_dir = %s
            w %%working_dir%%

            /*write the header line
            listoutput z%%zone%%_bps_report_for_sagebrush_issue.csv init
            listoutput note Value,Count,BpS,Zone,Model,Name,R,G,B,Red,Green,Blue
            listoutput screen

            /*export the attribute table
            tables
            select z%%zone%%_bps.vat
            unload z%%zone%%_bps_report_for_sagebrush_issue.csv
            &echo &off
            q
            """%(Zone,bps_dir)
            amlfile=open(amlfilename,'w')
            amlfile.write(amldata)
            amlfile.close()
            #now run it!
            arc='C:/arcgis/arcexe9x/bin/arc.exe'
            args=['arc',"&r %s"%(amlfilename)]
            os.spawnv(os.P_WAIT,arc,args)

            shutil.move("k:/fe/landfire/dat4/veg/z%s/bps/gis_fin/z%s_bps_report_for_sagebrush_issue.csv"%(Zone,Zone),"%s/z%s_bps.csv"%(working_dir,Zone))
        infile=open("%s/z%s_bps.csv"%(working_dir,Zone),'r')
        infile.readline()
        data=infile.readlines()
        infile.close()

        zone_areas[Zone]=0
        for line in data:
            line=line.split(",")
            BpS=int(line[2])
            pixels=int(line[1])
            #acres=int(round(float(pixels)*0.09*2.471/1000,0))  #convert pixels to hectares to thousands of acres
            if not bps_areas.has_key(BpS):
                bps_areas[BpS]=dict()
            bps_areas[BpS][Zone]=pixels
            total_area+=pixels #this is gonna be one freakin' ginormous number
            zone_areas[Zone]+=pixels


    print "Zone %s: Extracting MTDB Reports"%(Zone)
    MTDB="K:/fe/landfire/dat3/firereg/Z%s/dat/Current_Veg_Models/%sMTDB.mdb"%(Zone,Zone)

    #create reports subdirectory
    cur_dir=os.getcwd()
    report_dir="K:/fe/landfire/dat3/firereg/Z%s/dat/Current_Veg_Models/FRI_reports"%(Zone)
    if not os.access(report_dir,os.F_OK):
        os.mkdir(report_dir)


    source="PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE=%s"%(MTDB)
    #query the MTDB for this Zone
    query="""SELECT AllModels.PVG_Code, AllModels.PVG_Name, AllModels.Modeler1, AllModels.Modeler2, AllModels.Modeler3,
    AllModels.DisturbanceDescription, AllModels.ScaleDescription, AllModels.AdjIdentConcerns, AllModels.[Issues/Problems],
    AllModels.Comments, AllModels.ReplaceAveFreq, AllModels.MixedSevAveFreq, AllModels.SurfaceSevAveFreq, AllModels.FRGroup,
    AllModels.ModelSourceLit, AllModels.ModelSourceLocal, AllModels.ModelSourceExpert,
    AllModels.[FireRegSrc-Lit], AllModels.[FireRegSrc-LocalData], AllModels.[FireRegSrc-ExpEst]
    FROM AllModels;"""

    connection.Open(source)
    result.Open(query,connection,1,3)

    while not result.EOF:
        BpSID=result.fields.Item(0).Value
        bps_area=0 #stored in pixels
        hectares=0
        acres=0
        BpS=int(re.search("(?<=\d\d)\d\d\d\d\d",BpSID).group())
        if bps_areas.has_key(BpS) and bps_areas[BpS].has_key(Zone):
            bps_area=bps_areas[BpS][Zone]
        hectares=bps_area*0.09/10000.0
        acres=hectares*2.471
        percent_zone=0.000
        if zone_areas.has_key(Zone):
            percent_zone=100.0*float(bps_area)/float(zone_areas[Zone])
        
        outfilename="%s/%s_Report.htm"%(report_dir,BpSID)
        outfile=codecs.open(outfilename,'w','UTF-16')
        outfile.write("<HTML><HEAD><Title>MTDB Report for Model %s</Title></HEAD><BODY>\n"%(BpSID))

        outfile.write("<p align=CENTER><span style='font-size:20.0pt'><b>%s<br>%s</b></span></p>\n"%(result.fields.Item(0).Value,result.fields.Item(1).Value))
        outfile.write("<p><b>Bps Area:</b><br>%.0f thousand hectares (%.0f thousand acres)<br>Percent of Zone:  %.3f</p>\n"%(hectares,acres,percent_zone))
        outfile.write("<p><b>Modeler1:</b><br>%s</p>\n"%(result.fields.Item(2).Value))
        outfile.write("<p><b>Modeler2:</b><br>%s</p>\n"%(result.fields.Item(3).Value))
        outfile.write("<p><b>Modeler3:</b><br>%s</p>\n"%(result.fields.Item(4).Value))
        outfile.write("<p><b>Disturbance Description:</b><br>%s</p>\n"%(result.fields.Item(5).Value))
        outfile.write("<p><b>Adjacency/Identification Concerns:</b><br>%s</p>\n"%(result.fields.Item(7).Value))
        outfile.write("<p><b>Scale Description:</b><br>%s</p>\n"%(result.fields.Item(6).Value))
        outfile.write("<p><b>Issues/Problems:</b><br>%s</p>\n"%(result.fields.Item(8).Value))
        outfile.write("<p><b>Comments:</b><br>%s</p>\n"%(result.fields.Item(9).Value))
        outfile.write("<p><b>Fire Regime Group:</b><br>%s</p>\n"%(result.fields.Item(13).Value))


        if not BpS_fire.has_key(BpSID):
            BpS_fire[BpS]=dict()
        #retrieve fire parameters, if not given, default frequency is a million years
        RFreq=result.fields.Item(10).Value
        if RFreq:
            RFreq=int(RFreq)
        else:
            RFreq=1000000
        MFreq=result.fields.Item(11).Value
        if MFreq:
            MFreq=int(MFreq)
        else:
            MFreq=1000000    
        SFreq=result.fields.Item(12).Value
        if SFreq:
            SFreq=int(SFreq)
        else:
            SFreq=1000000    
        TotalProb=(1.0/float(RFreq))+(1.0/float(MFreq))+(1.0/float(SFreq))
        TotalFreq=int(round(1.0/TotalProb,0))
        if TotalFreq:
            PR=100.0*((1.0/float(RFreq))/TotalProb)
            PM=100.0*((1.0/float(MFreq))/TotalProb)
            PS=100.0*((1.0/float(SFreq))/TotalProb)
            outfile.write("<p><br></p><p><table width=350><b><tr><td></td><td>Avg Frequency</td><td>Percent</td></tr></b>\n")
            for sev in [["Replacement",RFreq,PR],["Mixed",MFreq,PM],["Low",SFreq,PS]]:
                if not sev[1]==1000000:  #if it wasn't defined in MTDB, leave it blank here
                    outfile.write("<tr><td><b>%s</b></td><td>%s</td><td>%.0f</td></tr>\n"%(sev[0],sev[1],sev[2]))
            #write total
            outfile.write("<tr><b><td>All Fires</td><td>%s</td><td></td></b></tr>\n"%(TotalFreq))
            outfile.write("</table></p>\n")

            #store fire parameters for later use, and keep pixel count
            BpS_fire[BpS][Zone]=[RFreq,PR,MFreq,PM,SFreq,PS,TotalFreq,bps_area]      

            
        ModelSrc1=result.fields.Item(14).Value #literature
        ModelSrc2=result.fields.Item(15).Value #local data
        ModelSrc3=result.fields.Item(16).Value #expert opinion

        outfile.write("<p><b>Model Source:</b><br>\n")
        for src in [["Literature",ModelSrc1],["Local Data",ModelSrc2],["Expert Opinion",ModelSrc3]]:
            if src[1]:
                outfile.write("%s<br>"%(src[0]))
        outfile.write("</p>\n")
                              
        FRSrc1=result.fields.Item(17).Value
        FRSrc2=result.fields.Item(18).Value
        FRSrc3=result.fields.Item(19).Value

        outfile.write("<p><b>Fire Regime Source:</b><br>\n")
        for src in [["Literature",FRSrc1],["Local Data",FRSrc2],["Expert Opinion",FRSrc3]]:
            if src[1]:
                outfile.write("%s<br>"%(src[0]))
        outfile.write("</p>\n")
        
        outfile.write("</BODY></HTML>\n")
        outfile.close()
        result.MoveNext()

    result.Close()
    connection.Close()


BpSs=BpS_fire.keys()
BpSs.sort()
#now write the detailed CSV report for Marc
outfile=open("%s/BpS_FRI_Detail_Report.csv"%(working_dir),'w')
outfile.write("BpS,Zone,Replacement_FI,Replacement_Percent,Mixed_FI,Mixed_Percent,Surface_FI,Surface_Percent,All_Fire_FI,BpS_Hectares,BpS_Acres,BpS_Percent_Zone,BpS_Percent_All_Zones,Redo?,Model_Contention\n")
for BpS in BpSs:
    cur_Zones=BpS_fire[BpS].keys()
    cur_Zones.sort()
    for Zone in cur_Zones:
        RFreq,PR,MFreq,PM,SFreq,PS,TotalFreq,bps_area=BpS_fire[BpS][Zone]
        #correct to remove the defaults
        if RFreq==1000000:
            RFreq=""
            PR=0.00
        if MFreq==1000000:
            MFreq=""
            PM=0.00
        if SFreq==1000000:
            SFreq=""
            PS=0.00          
        hectares=0
        acres=0
        if bps_areas.has_key(BpS) and bps_areas[BpS].has_key(Zone):
            bps_area=bps_areas[BpS][Zone]
        hectares=bps_area*0.09  #just raw hectares
        acres=hectares*2.471 #just raw acres
        percent_zone=0.000
        if zone_areas.has_key(Zone):
            percent_zone=100.0*float(bps_area)/float(zone_areas[Zone])
        percent_all_zones=100.0*float(bps_area)/float(total_area)
        redo=0 #just a binary response
        if Zone in redo_Zones:
            redo=1 #yep, we're gonna redo this one
        if TotalFreq:
            line="%s,%s,%s,%.2f,%s,%.2f,%s,%.2f,%.0f,%.0f,%s,%.3f,%.3f,%s,\n"%(BpS,Zone,RFreq,PR,MFreq,PM,SFreq,PS,TotalFreq,hectares,acres,percent_zone,percent_all_zones,redo)
            outfile.write(line)        
outfile.close()

