import os

##Set the file directory
txtfileRoot = 'G:/Working/EMDS/DAYMET/daymet_outfiles/z06/outfiles'

def getLines(txtfileRoot):
    allFileNames = os.listdir(txtfileRoot)
    for txtfile in allFileNames:
        outfiles = txtfileRoot + '/' + txtfile
        if outfiles[-4:] == '.out':  ##logic for .outfiles
            num_lines = sum(1 for line in open(txtfileRoot + '/' + txtfile)) - 26 ##Subtract 26 lines because of the header file in the outfiles
            print txtfile, num_lines
        else:                       ##logic for .infiles
            num_lines2 = sum(1 for line in open(txtfileRoot + '/' + txtfile)) -2 ##Subtract 2 lines because of the header file in the infiles
            print txtfile, num_lines2
