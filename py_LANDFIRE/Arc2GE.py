import os  
from sys import argv  
  
class KML_File:  
   def __init__(self):  
       pass  

   def open(self, filename): #open file and add header  
       "adds the kml header to a file (includes a default style)"  
        self.filename=filename  
        self.kmlfile = open(filename,"w")  
        self.kmlfile.write("""<?xml version="1.0" encoding="UTF-8"?>  
        <kml xmlns="http://earth.google.com/kml/2.0">  
        <Document>""")  
 
    def close(self): #add tail  
        self.kmlfile.write("</Document>\n</kml>\n")  
        self.kmlfile.close()  
 
    def add_placemark(self,pmname="FireLab-Outback",pmlat=46.92597564568973,pmlon=-114.0951456205846,pmrange=7000.0,pmtilt=0.0,pmhead=0.0):  
        "adds the point to a kml file"  
        data="""  
        <Placemark>  
          <description>Current Placemark</description>  
          <name>%s</name>  
          <!--  
          <LookAt>  
            <longitude>%.14f</longitude>  
            <latitude>%.14f</latitude>  
            <range>%.14f</range>  
             <tilt>%.14f</tilt>  
             <heading>%.14f</heading>  
           </LookAt>  
           -->  
           <visibility>1</visibility>  
           <Style>  
             <IconStyle>  
               <Icon>  
                 <href>root://icons/palette-3.png</href>  
                 <x>96</x>  
                 <y>160</y>  
                 <w>32</w>  
                 <h>32</h>  
               </Icon>  
             </IconStyle>  
           </Style>  
           <Point>  
             <extrude>0</extrude>  
             <altitudeMode>clampToGround</altitudeMode>  
             <coordinates>%.14f,%.14f,0</coordinates>  
           </Point>  
         </Placemark>  
         """%(pmname,pmlon,pmlat,pmrange,pmtilt,pmhead,pmlon,pmlat)  
         self.kmlfile.write(data)  
  
     def add_polygon(self,xmin,xmax,ymin,ymax):  
         data="""  
         <Placemark>  
         <name>ArcMap_View</name>  
         <Style>  
         <PolyStyle>  
         <fill>0</fill>  
         </PolyStyle>  
         </Style>  
         <Polygon>  
         <extrude>0</extrude>  
         <altitudeMode>clampToGround</altitudeMode>  
         <tessellate>1</tessellate>  
         <outerBoundaryIs>  
         <LinearRing>  
         <coordinates>  
         %s,%s,0  
         %s,%s,0  
         %s,%s,0  
         %s,%s,0  
         %s,%s,0  
         </coordinates>  
         </LinearRing>  
         </outerBoundaryIs>  
         </Polygon>  
         </Placemark>  
         """%(xmin,ymin,xmin,ymax,xmax,ymax,xmax,ymin,xmin,ymin)  
         self.kmlfile.write(data)  
          
     def execute(self):  
         os.startfile(self.filename)  
  
  
 if __name__=="__main__":  
     #point info  
     lat=float(argv[1])  
     lon=float(argv[2])  
     #extent polygon info  
     xmin=float(argv[3])  
     xmax=float(argv[4])  
     ymin=float(argv[5])  
     ymax=float(argv[6])  
  
     outfilename="c:/temp/arc2ge.kml"  
     kmlfile=KML_File()  
     kmlfile.open(outfilename)  
     kmlfile.add_placemark("",lat,lon,10000,0)  
     kmlfile.add_polygon(xmin,xmax,ymin,ymax)  
     kmlfile.close()  
     kmlfile.execute()  
 

