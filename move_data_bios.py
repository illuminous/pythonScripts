import sys
import os
import zipfile



directories = []
res =[]
zoneres = []



"""Build a list of directories to copy grids from and to."""
def buildDirectories(zone_number_lower, zone_number_upper):
    for zone in range(zone_number_lower, zone_number_upper):
        res.append(zone)
        for area in geoarea:
            
            if zone < 10:
                path1 = 'G:/Working/Treelists_2012_update/
                path2 = '/z0%s/' %(zone)
                path = path1+path2
                directories.append(path)
            else:
                path1 = 'G:/Working/Treelists_2012_update/
                path2 = '/z%s/' %(zone)
                path = path1+path2
                directories.append(path)

    return directories



def main():
    products = ['clay', 'sand', 'silt', 'mxdepth']#['bps']#['evt08', 'bps']
    buildDirectories(1,100)
    for d in directories:
        for p in products:
            print d, p
        

        
        


if __name__ == '__main__':
    main()  
