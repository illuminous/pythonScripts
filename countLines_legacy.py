#!/bin/bash
import os

##Set the file directory
##txtfileRoot = '/home/jherynk/z44/infiles'
txtfileRoot = '/mnt/pvfs2/jherynk/z44/outfiles'
##txtfileRoot = '/home/jherynk/z36/outfiles/continuation'

def getLines(txtfileRoot):
    allFileNames = os.listdir(txtfileRoot)
    for txtfile in allFileNames:
        outfiles = txtfileRoot + '/' + txtfile
        if outfiles[-4:] == '.out':  ##logic for .outfiles
            num_lines = sum(1 for line in open(txtfileRoot + '/' + txtfile)) - 26 ##Subtract 26 lines because of the header file in the outfiles
            print txtfile, num_lines
        elif outfiles[-3:] == '.in':                       ##logic for .infiles
            num_lines2 = sum(1 for line in open(txtfileRoot + '/' + txtfile)) -2 ##Subtract 2 lines because of the header file in the infiles
            print txtfile, num_lines2
        else:
	     pass

getLines(txtfileRoot)
