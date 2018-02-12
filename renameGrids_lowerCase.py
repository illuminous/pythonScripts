import arcpy
from arcpy import env

yearStore = [] #store years from buildYears

def gridsLowercase(workspace, gridtype):
    env.workspace = workspace
    rasterList = arcpy.ListRasters("*", gridtype)
    for raster in rasterList:
        if raster[0].isupper() == True: #if the raster starts in uppercase
            try:
                outgrid = 'x'+raster.lower() #create an outgrid that is lower case with a leading x to trick the esri crap logic
                arcpy.Rename_management(raster, 'x'+raster.lower()) #rename the grid with a leading x
                arcpy.Rename_management(outgrid, outgrid[1:]) #rename it again by stripping the x
            except:
                pass

def buildYears(year_number_lower, year_number_upper):#enter start year, and stop year
    for year in range(year_number_lower, year_number_upper):
        yearStore.append(year)

def main():    
    buildYears(1984, 2009) #build a range of years
    for year in yearStore: #start looping through the years
        currentyear = str(year)
        print currentyear
        foldername = 'E:/firesev/mtbs/files/%s/imagery' %(year)
        gridsLowercase(foldername, 'TIF') #call the gridsLowercase def

if __name__ == "__main__":
    main()
