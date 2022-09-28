import csv
import difflib

def find_key(input_dict, value):
    return {k for k, v in input_dict.items() if v == value}


f = open('C:/Users/jherynk/OneDrive - Washington Corporations/M-Files Data Mapping/QAQC/Diff/M-FilesvsSharepointDocsReport_pt5.txt', 'w')
with open('C:/Users/jherynk/OneDrive - Washington Corporations/M-Files Data Mapping/QAQC/Diff/M-FilesvsSharepointDocs.txt') as csvfile:
    print 'Processing....'
    fileread=csv.reader(csvfile, delimiter = '\t')
    mFilesDocs = {}
    spDocs = {}
    output = ()

##    """Improvements to be made: 1. Speed enhancement - Write output into memory and then out to the file at the end of the loops.  """

    
    for row in fileread: #build dictionary using the address number (key) and the company name (value)

        mFilesDocs[row[0]]=row[0]
        
        spDocs[row[1]]=row[1]

        
        
    for key in mFilesDocs.iterkeys(): # Iterate over the Address number ('727218') keys
        res = difflib.get_close_matches(mFilesDocs.get(key), spDocs.values(), cutoff = .5) #use difflib to find closely matched company names
        if len(res) > 0:
            pass
##            score = difflib.SequenceMatcher(None, key,res).ratio()
##            f.write(mFilesDocs.get(key)+'\t'+'Exists'+'\t'+'\t'+str(score)+"\n") #write output
        else:
            score = difflib.SequenceMatcher(None, key,res).ratio()
            f.write(mFilesDocs.get(key)+'\t'+'Does Not Exist'+'\t'+'\t'+str(score)+"\n") #write output


f.close() #close the output
