infile = open("c:/aaronwilson/NR_fire/test/export_test.csv",'r')
infile.readline()
data=infile.readlines()
infile.close()
fire_polygons = dict()
for line in data:
    line=line.split(",")
    atlas_area = float(line[1])
    atlas_poly = int(line[3])
    mtbs_poly = int(line[7])
    mtbs_area = float(line[8])
    intersect = float(line[18])
    if not fire_polygons.has_key(atlas_poly):
        fire_polygons[atlas_poly]=dict()
    if not fire_polygons[atlas_poly].has_key(mtbs_poly):
        fire_polygons[atlas_poly][mtbs_poly]=dict()
    if fire_polygons[atlas_poly] <> 0 and fire_polygons[atlas_poly][mtbs_poly] <> -1:
        fire_polygons[atlas_poly][mtbs_poly] = []
        fire_polygons[atlas_poly][mtbs_poly].append(intersect)
        fire_polygons[atlas_poly][mtbs_poly].append(atlas_area)
        fire_polygons[atlas_poly][mtbs_poly].append(mtbs_area)
            
outfile=open('c:/aaronwilson/NR_fire/test_out.csv','w')
outfile.write("Atlas_poly,MTBS_poly,Intersect,Atlas_Only,MTBS_Only,Orig_Atlas,Orig_MTBS\n")#,Atlas_Only,MTBS_Only,All_Atlas,All_MTBS
polyList = []
for poly in fire_polygons.keys():
    for x in fire_polygons[poly].keys():
        if x <> -1 and poly > 0:
        	polyList.append(poly)
##    print polyList
for poly in fire_polygons.keys():
        print poly
##	print fire_polygons[poly].keys()
##	print polyList
	for x in fire_polygons[poly].keys():
            print x
            mtbsList = fire_polygons[poly].keys()
            if x <> -1 and poly > 0:
                print x
                mtbs_id = x
                area = fire_polygons[poly][x][0]
                atlas_out = fire_polygons[poly][-1][0]
                mtbs_out = fire_polygons[0][x][0]
                atlas_old = fire_polygons[poly][x][1]
                mtbs_old = fire_polygons[poly][x][2]
                outfile.write("%s,%s,%s,%s,%s,%s,%s\n"%(poly,mtbs_id,area,atlas_out,mtbs_out,atlas_old,mtbs_old))
                print mtbs_id
##                print area
            elif x == -1:
                for z in mtbsList:
                    if z <> -1:
                        exists = 1
                        break
                    else:
                        exists = 0
                if exists == 0:
##                    print mtbsList[0]
                    mtbs_id = x
                    area = 0
                    atlas_out = 0
                    mtbs_out = 0
                    atlas_old = fire_polygons[poly][x][1]
                    mtbs_old = 0
                    outfile.write("%s,%s,%s,%s,%s,%s,%s\n"%(poly,mtbs_id,area,atlas_out,mtbs_out,atlas_old,mtbs_old))
##                    print mtbs_id
##                    print atlas_old
            elif poly == 0:
                for y in polyList:
                    if fire_polygons[y].has_key(x):
                        exists = 1
                        break
                    else:
                        exists = 0
                if exists == 0:
                    mtbs_id = x
                    area = 0
                    atlas_out = 0
                    mtbs_out = 0
                    atlas_old = 0
                    mtbs_old = fire_polygons[poly][x][2]
                    outfile.write("%s,%s,%s,%s,%s,%s,%s\n"%(poly,mtbs_id,area,atlas_out,mtbs_out,atlas_old,mtbs_old))
                
##                print mtbs_id
##                print mtbs_old
outfile.close()
