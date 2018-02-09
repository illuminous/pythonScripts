import os
def Split(inputFile,numParts,outputName):
    fileSize=os.stat(inputFile).st_size
    parts = '20'
    #parts=FileSizeParts(fileSize,numParts)
    openInputFile = open(inputFile, 'r')
    outPart=1
    for part in parts:
        if openInputFile.tell()<fileSize:
            fullOutputName=outputName+os.extsep+str(outPart)
            outPart+=1
            openOutputFile=open(fullOutputName,'w')
            openOutputFile.writelines(openInputFile.readlines(part))
            openOutputFile.close()
    openInputFile.close()
    return outPart-1

Split('J:/event_prep/z16/cleanFiles/outfileclean.txt', '20', 'bla')
