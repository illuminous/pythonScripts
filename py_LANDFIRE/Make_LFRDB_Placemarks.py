import sys, os
from zipfile import ZipFile,ZIP_DEFLATED
import osr #required for converting from LANDFIRE Albers NAD83 to Lat/Long

if len(sys.argv)>1:
    Zone=sys.argv[1]
else:
    Zone=raw_input("Enter Zone ID:  ")
photo_dir="K:/fe/landfire/dat4/ReferenceData/z%s/DigitalPhotos/Z%s_Plot_Photos"%(Zone,Zone)  #MFSL
#photo_dir="c:/temp/z%s_Plot_Photos"%(Zone) #NS
##photo_dir="K:/landfire2/Zone_Photos/Z%s_Plot_Photos"%(Zone) #SEM 
working_dir=os.getcwd() #this can be hard coded too



#The query to produce the data:
"""SELECT Z55_Map_Attributes.Master_ID, Z55_Map_Attributes.RegID, Z55_Map_Attributes.ProjID, Z55_Map_Attributes.Date, Z55_Map_Attributes.Albers_x, Z55_Map_Attributes.Albers_y, Z55_Map_Attributes.Photo_1, Z55_Map_Attributes.Photo_2, Z55_Map_Attributes.Photo_3, Z55_Map_Attributes.Photo_4, Z55_Map_Attributes.LF_EVTCode, Z55_Map_Attributes.LF_EVT, Z55_Map_Attributes.LF_ESPCode, Z55_Map_Attributes.LF_ESP, Z55_Map_Attributes.LF_Lifeform_GenKey, Z55_Map_Attributes.Orig_TreeC, Z55_Map_Attributes.Orig_ShrubC, Z55_Map_Attributes.Orig_HerbC, Z55_Map_Attributes.LF_TreeC, Z55_Map_Attributes.LF_ShrubC, Z55_Map_Attributes.LF_HerbC, Z55_Map_Attributes.DomSp, Z55_Map_Attributes.DomSp_Lifeform, Z55_Map_Attributes.DomSpC, Z55_Map_Attributes.CoDomSp, Z55_Map_Attributes.CoDomSp_Lifeform, Z55_Map_Attributes.CoDomSpC INTO Z55_GE_Inputs
FROM Z55_Map_Attributes;"""




def snip_srt(a,b):
    return cmp(a[3],b[3])

#the class that does the dirty work of creating a KML file.  Still kind of rudimentary.  The icons in particular are lame.
class KML_File:
    def __init__(self, filename): #open file and add header
        "adds the kml header to a file (includes a default style)"
        self.filename=filename
        self.kmlfile = open(filename,"w")
        self.kmlfile.write("""<?xml version="1.0" encoding="UTF-8"?>
        <kml xmlns="http://earth.google.com/kml/2.0">
        <Document>""")

    def close(self): #add tail
        self.kmlfile.write("</Document>\n</kml>\n")
        self.kmlfile.close()

    def add_placemark(self,pmname="FireLab-Outback",pmdesc="This is the Outback",snippet="",pmlat=46.92597564568973,pmlon=-114.0951456205846,pmrange=7000.0,pmtilt=0.0,pmhead=0.0):
        "adds the point to a kml file"
        data="""
        <Placemark>
          <name>%s</name>
          <description>%s</description>        
          <Snippet>%s</Snippet>
          <LookAt>
            <longitude>%.14f</longitude>
            <latitude>%.14f</latitude>
            <range>%.14f</range>
            <tilt>%.14f</tilt>
            <heading>%.14f</heading>
          </LookAt>
          <visibility>1</visibility>
          <Style>
            <IconStyle>
              <Icon>
                <href>root://icons/palette-4.png</href>
                <x>32</x>
                <y>128</y>
                <w>32</w>
                <h>32</h>
              </Icon>
            </IconStyle>
          </Style>
          <Point>
            <extrude>0</extrude>
            <altitude>0</altitude>
            <altitudeMode>clampToGround</altitudeMode>
            <coordinates>%.14f,%.14f,50</coordinates>
          </Point>
        </Placemark>
        """%(pmname,pmdesc,snippet,pmlon,pmlat,pmrange,pmtilt,pmhead,pmlon,pmlat)
        self.kmlfile.write(data)
    def add_placemark_folder(self,name,placemarks):
        self.kmlfile.write("<Folder>\n<open>0</open>\n<name>%s</name>\n"%(name))
        for placemark in placemarks:
            pmname,pmdesc,snippet,pmlat,pmlon,pmrange,pmtilt,pmhead=placemark
            self.add_placemark(pmname,pmdesc,snippet,pmlat,pmlon,pmrange,pmtilt,pmhead)
        self.kmlfile.write("</Folder>\n")
            


#the following retrieves a projection from an Arc prj
#the standard LANDFIRE projection file
##infile=open("%s/LANDFIRE_Albers.prj"%(os.getcwd()),'r')
##prj_lines=infile.readlines()
##infile.close()
###src spatial ref    
##src_ref = osr.SpatialReference()
##src_ref.ImportFromESRI(prj_lines)
##k=src_ref.ExportToWkt()
##outfile=open("%s/wkt.txt"%(os.getcwd()),'w')
##outfile.write(k)
##outfile.close()

#the following takes the LANDFIRE projection in well known text format
src_ref = osr.SpatialReference()
LF_prj="""PROJCS["NAD_1983_Albers",GEOGCS["GCS_North_American_1983",DATUM["North_American_Datum_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers_Conic_Equal_Area"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["longitude_of_center",-96.0],PARAMETER["Standard_Parallel_1",29.5],PARAMETER["Standard_Parallel_2",45.5],PARAMETER["latitude_of_center",23.0],UNIT["Meter",1.0]]"""
src_ref.ImportFromWkt(LF_prj)


#sink spatial ref
sink_ref = osr.SpatialReference()
sink_ref.SetWellKnownGeogCS("WGS84")#this is the GoogleEarth Native projection

#coordinate transformation 
project = osr.CoordinateTransformation(src_ref,sink_ref)


infile=open("%s/z%s_ge_inputs.csv"%(working_dir,Zone),'r')
header=infile.readline()
data=infile.readlines()
infile.close()


data_LUT=dict()

for line in data:
    photo_names=[]
    dom_spps=[]#list of triads
    
    line=line.split(",")
    Master_ID=int(line[0])
    RegID=line[1]
    ProjID=line[2]
    Date=line[3].split(" ").pop(0)
    if line[4]:#plot must have xy
        x=float(line[4])
        y=float(line[5])
        if line[10]:
            EVT=int(line[10])
            EVT_name=line[11]
        else:
            EVT=""
            EVT_name=""
        if line[12]:
            ESP=int(line[12])
            ESP_name=line[13]
        else:
            ESP=""
            ESP_name=""


        #plot dominant lifeform and total cover categories
        LF_Lifeform_GenKey=""
        if line[14]:
            LF_Lifeform_GenKey=line[14]
        Orig_TreeC=0
        if line[15]:
            Orig_TreeC=int(round(float(line[15]),0))
        Orig_ShrubC=0
        if line[16]:
            Orig_ShrubC=int(round(float(line[16]),0))
        Orig_HerbC=0
        if line[17]:
            Orig_HerbC=int(round(float(line[17]),0))
        LF_TreeC=0
        if line[18]:
            LF_TreeC=int(round(float(line[18]),0))
        LF_ShrubC=0
        if line[19]:
            LF_ShrubC=int(round(float(line[19]),0))
        LF_HerbC=0
        if line[20]:
            LF_HerbC=int(round(float(line[20]),0))

        cov_table="<table border width='350' cellspacing='0' cellpadding='0'><tr><th> </th><th>Tree Cover</th><th>Shrub Cover</th><th>Herb Cover</th></tr>\n"
        cov_table+="<tr><td>Original</td><td>%s%%</td><td>%s%%</td><td>%s%%</td></tr>"%(Orig_TreeC,Orig_ShrubC,Orig_HerbC)
        cov_table+="<tr><td>LANDFIRE</td><td>%s%%</td><td>%s%%</td><td>%s%%</td></tr></table>"%(LF_TreeC,LF_ShrubC,LF_HerbC)

        #dominant / codominant species section
        for i in [21,24]:
            if line[i]:
                spp=line[i]
                lf=line[i+1]
                ac=line[i+2]
                dom_spps.append([spp,lf,ac])

        if dom_spps:
            dom_spp_table="<table border width='350' cellspacing='0' cellpadding='0'><tr><th>Dominant Species</th><th>Lifeform</th><th>AC</th></tr>\n"
            for entry in dom_spps:
                dom_spp_table+="<tr><td>%s</td><td>%s</td><td>%s</td></tr>\n"%(entry[0],entry[1],entry[2])
            dom_spp_table+="</table><br>\n"
        else:
            dom_spp_table=""


        #plot photo section
        for i in range(6,10):
            photo=line[i].replace(" ","").replace("\n","").replace("\r","")
            #if photo.count(".jpg") or photo.count(".JPG") or photo.count(".gif") or photo.count(".GIF") or photo.count(".png") or photo.count(".PNG"):#does not like TIFFs!
            if photo and not (photo.lower().count(".tif")):
                photo_names.append(photo)
        photos=""
        if photo_names:
            if len(photo_names)>1: #make a 2x2 table
                photos+="<table width='600' cellspacing='0' cellpadding='0'>"
                counter=1
                for photo in photo_names:
                    if counter in [1,3]:#beginning of table row
                        photos+="<tr>"
                    photo_loc="%s/%s"%(photo_dir,photo)
                    photos+="""<td><a href='%s'>
                    <img src='%s' alt='plot_photo' width='300'></a></td>\n"""%(photo_loc,photo_loc) #do a thumbnail image of plot photo, linked to the fullsize version
                    if counter in [1,3]:#end of table row
                        photos+="</tr>"
                    counter+=1
                photos+="</table>\n"
            else:
                photo_loc="%s/%s"%(photo_dir,photo_names[0])
                photos+="""<td><a href='%s'>
                <img src='%s' alt='plot_photo' width='300'></a></td>\n"""%(photo_loc,photo_loc) #do a thumbnail image of plot photo, linked to the fullsize version
            
        description="""<![CDATA[
        <p>Master_ID: %s</p>
        <p>ESP: %s %s<br>EVT: %s %s</p>
        <p>Plot Dominant Lifeform: %s</p>
        <p>%s</p>
        <p>%s</p>
        %s
        ]]>
        """%(Master_ID,ESP,ESP_name,EVT, EVT_name,LF_Lifeform_GenKey,cov_table,dom_spp_table,photos)

##        if photos:
        lon,lat,z= project.TransformPoint(x,y)  #transform points may be more efficient
        snippet="ESP: %s, EVT: %s"%(ESP,EVT)
        if not data_LUT.has_key(EVT):
            data_LUT[EVT]=[]
        data_LUT[EVT].append([lon,lat,description,snippet])

kmlfilename="%s/z%s_LFRDB_plots.kml"%(working_dir,Zone)
kmlfile=KML_File(kmlfilename)

EVTs=data_LUT.keys()
EVTs.sort()
for EVT in EVTs:
    data_LUT[EVT].sort(snip_srt)
    placemarks=[]
    for entry in data_LUT[EVT]:
        lon,lat,description,snippet=entry  
        placemarks.append([EVT,description,snippet,lat,lon,6000,0,0])
    kmlfile.add_placemark_folder(EVT,placemarks)
kmlfile.close()

#create kmz file
kmzfilename="%s/z%s_LFRDB_plots.kmz"%(working_dir,Zone)
kmzfile=ZipFile(kmzfilename,'w',ZIP_DEFLATED)
kmzfile.write("z%s_LFRDB_plots.kml"%(Zone))
kmzfile.close()


