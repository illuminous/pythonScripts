import os
root1 = 'c:/tmp/outfiles/'
root2 = os.listdir('c:/tmp/outfiles')
res = []
for grid in root2:
    filenames = root1+grid
    res.append(filenames)
print filenames
content = ''
for f in res:
    print f
    content = content + '\n' + open(f).read()
open('c:/tmp/outfiles/joined_file.txt','wb').write(content)
