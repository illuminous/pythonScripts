import csv
import difflib

def find_key(input_dict, value):
    return {k for k, v in input_dict.items() if v == value}


f = open('C:/Temp/diff/M-FilesvsSharepointDocsReport_pt6.txt', 'w')
with open('C:/Temp/diff/M-FilesvsSharepointDocs.txt') as csvfile:
    print 'Processing....'
    fileread=csv.reader(csvfile, delimiter = '\t')
    mFilesDocs = {}
    spDocs = {}
    output = ()

##    """Improvements to be made: 1. Speed enhancement - Write output into memory and then out to the file at the end of the loops.  """

    
    for row in fileread: #build dictionary using the address number (key) and the company name (value)

        mFilesDocs[row[0]]=row[0]
        
        spDocs[row[1]]=row[1]

        
        
    for key in spDocs.iterkeys(): # Iterate over the Address number ('727218') keys
        res = difflib.get_close_matches(spDocs.get(key), mFilesDocs.values(), cutoff = .6) #use difflib to find closely matched company names
        if len(res) > 0:
            pass
##            score = difflib.SequenceMatcher(None, key,res).ratio()
##            f.write(mFilesDocs.get(key)+'\t'+'Exists'+'\t'+'\t'+str(score)+"\n") #write output
        else:
            print spDocs.get(key)
            score = difflib.SequenceMatcher(None, key,res).ratio()
            f.write(spDocs.get(key)+'\t'+'Does Not Exist in M-Files'+'\t'+'\t'+str(score)+"\n") #write output


f.close() #close the output
