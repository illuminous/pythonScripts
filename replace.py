from tempfile import mkstemp
from shutil import move
from os import remove, close

def replace(file, pattern, subst):
    #Create temp file
    fh, abs_path = mkstemp()
    new_file = open(abs_path,'w')
    old_file = open(file)
    for line in old_file:
        new_file.write(line.replace(pattern, subst))
    #close temp file
    new_file.close()
    close(fh)
    old_file.close()
    #Remove original file
    remove(file)
    #Move new file
    move(abs_path, file)

def createOutgrids(root):
    outputfile = open(root + '/' + 'z23_dm_00test.out', 'r')
    combofile =(root + '/' + 'comboevt_scratch.asc')
    
    for item in outputfile:
        pixelkey = []    
        linelist = item.split()
        pixelkey.append(linelist[0:2])   
        for pixel in pixelkey:
            pixelID = str(pixel[0])
            spreadrate = str(pixel[1])            
            try:
                replace(combofile, pixelID, spreadrate)
            except:
                pass

def trysomethingelse(root):
    combofile =open(root + '/' + 'comboevt_scratch.asc', 'r')
    for line in combofile:
        print line[0]
        print len(line[0])

trysomethingelse('J:/event_fireharm/z23/outfiles')
##createOutgrids('J:/event_fireharm/z23/outfiles')
##replace('j:/event_fireharm/z23/outfiles/combotest.out', 'x', '55')
