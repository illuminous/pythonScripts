

import glob, os, shutil, csv

with open('C:/Temp/diff/M-FilesvsSharepointDocsReport.csv') as csvfile:
    fileread = csv.reader(csvfile, quotechar='|')
    dst = 'C:/temp/mFilesImports'


        
    for x in glob.glob('C:/'):
        ##filetocopy = 'V:/contractadministration/Real Estate/'+row[0]
        print x
        ##shutil.copy2(filetocopy, dst)


##.doc, .htm, .jpg, .msg, .oft, .pdf, .png, .rtf, .tif, .txt, .xls, .docx, .html, .jpeg, .xlsx
