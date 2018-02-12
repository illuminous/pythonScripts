from collections import defaultdict

"""make a dict of years and threads"""
d = defaultdict(list)
poly = open('f:/landcover/analysis5/NR_ID_001_0_perimeter.txt', 'r')
FID = -1 #start counter at -1 because of header
for polyline in poly.readlines():    
    try:
        polysplit = polyline.split(',')
        year = polysplit[7]
        thread = polysplit[2]
        ##d[int(year)].append(int(thread))
        d[year].append(thread)
    except:
        pass

"""from the years with overlaps, make a new file with year and thread"""

results =open('f:/landcover/analysis5/NR_ID_001_0_YearResults.csv', 'r')
finresults = open('f:/landcover/analysis5/NR_ID_001_0_FinResults.csv', 'w')
for overlap in results:
    stripoverlap = overlap.rstrip('\n')
    for item in d[stripoverlap]:
        finresults.write(str(stripoverlap)+','+str(item)+'\n')

results.close()
finresults.close()
