import profile
def fidYear(inputfile):
    perimeterfile = {}
    global perimeterfile
    poly = open(inputfile, 'r')
    FID = -1 #start counter at -1 because of header
    """analyse the polygon perimeter file and store the FID and associated year
    in a dictionary"""
    for polyline in poly.readlines():    
        polysplit = polyline.split(',')
        year = polysplit[7]
        perimeterfile[FID]=year
        FID+=1

    print '###############'
    poly.close()

def overlap(inputfile, outfile):
    """open the biogeography tools outfile and store the results in a dictionary
    where the key is the FID and the values are the overlapping polygons stored as
    an FID"""
    intersectfile = {}
    global intersectfile
    f = open(inputfile, 'r')
    for line in f.readlines():
        lineclean = line.rstrip('\n')
        splitter =lineclean.split(':')
        polyID = splitter[0]
        splitter2 = splitter[1:]
        for item in splitter2:
            newitem = item.split(',')
            try:
                intersectfile[int(polyID)] = newitem
            except:pass

    print '###############'
    f.close()

    """start iterating through the itnersectfile dictionary and swap out FIDs for year values"""
    FIDYEAR={}
    for k, v in intersectfile.iteritems(): # for the polygon FID in the intersectfile
        try:
            if perimeterfile.has_key(int(k)):
                apple = [perimeterfile.get(int(k))]
            orangelist = []
            for item in v:           
                orange = perimeterfile.get(int(item))         
                orangelist.append(str(orange))           
                FIDYEAR[perimeterfile.get(int(k))]=orangelist
                
            else:
                pass
        except:
            pass


    """if the year intersect with it's year, write it out"""
    results = open(outfile, 'w')
    for k, v in FIDYEAR.iteritems():
        if k in v:      
            results.write(k)
            results.write('\n')

        
    else:
        pass
    results.close()    

def main():    
    fidYear('f:/landcover/analysis5/NR_ID_001_0_perimeter.txt')
    overlap('f:/landcover/analysis5/NR_ID_001_0_out.txt', 'f:/landcover/analysis5/NR_ID_001_0_YearResults.csv')


if __name__ == "__main__":
    profile.run('main()')
