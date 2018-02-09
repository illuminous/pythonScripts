import win32com.client

Zone="10"
working_dir="C:/Firereg/z%s"%(Zone)
RC_thresh=10 #need to figure out threshold

class Plot:
    def __init__(self,ESP):
        self.ESP=ESP
        self.spps=dict()
        self.Sclass=""
        
Plots=dict() 
#add in AC to query?
infile=open("C:/Firereg/z%s/z%s_plot_data.csv"%(Zone,Zone),'r')#need to set this to network
infile.readline()
data=infile.readlines()
infile.close()
for line in data:
    line=line.replace("\n",'').split(",")
    PlotID=int(line[0])
    if not Plots.has_key(PlotID):
        ESP=int(line[1])
        Plots[PlotID]=Plot(ESP)
    spp_code=str(line[2]).replace('"','')
    if line[3]: 
        RC=int(round(float(line[3]),0))
    else:
        RC=0
    Plots[PlotID].spps[spp_code]=RC

for PlotID in Plots:
    if Plots[PlotID].ESP==1045:
        if Plots[PlotID].spps.has_key("ABGR"):
            RC=Plots[PlotID].spps["ABGR"]
            if RC>RC_thresh:
                Plots[PlotID].Sclass=1
                

outfile=open("%s/z%s_plot_Sclass.csv"%(working_dir,Zone),'w')
outfile.write("Master_ID,Sclass\n")
for PlotID in Plots:
    Sclass=Plots[PlotID].Sclass #this can be dropped and used directly below   
    outfile.write("%s,%s\n"%(PlotID,Sclass))
outfile.close()
