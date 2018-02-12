from glob import iglob
import shutil
import os

PATH = 'C:/tmp'

destination = open('everything.txt', 'w')
for filename in iglob(os.path.join(PATH, '*.log')):
    print filename
    shutil.copyfileobj(open(filename, 'r'), destination)
destination.close()
