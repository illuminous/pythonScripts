import csv
import shutil
import glob
with open('C:/Temp/diff/round2/ComparisonRecopy.csv') as csvfile:
    fileread = csv.reader(csvfile, quotechar='|')
    dst = 'C:/temp/mFilesImports'
    for row in fileread:
        try:
            print row
            shutil.copy2('V:/contractadministration/Real Estate/'+row[0], dst)
        except:
            print 'does not exist' + str(row[0])
            pass


