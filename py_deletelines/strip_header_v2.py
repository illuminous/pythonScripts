import os

zones = ['z06']
root = 'C:/daymet_outfiles/%s/outfiles' %zones[0]
mode = '_dm_'
extension = '.out'
item = range(1, 21)

result=[]

for i in item:
    for z in zones:
        iterable = '%s' %(i)
        newfile = z + mode + iterable + extension 
        newlist = result.append(newfile)
    print result
    
for res in result:
    print res
    input = open(root + '//' + res, 'r') 
    s = input.readlines()
    del s[:26]
    output = open(root + '//' + res, 'w') 
    output.writelines(s)
    output.close


    
### let's create your data file from the string
##fout = open("MyData1.txt", "w")
##fout.write(data_str)
##fout.close()
## 
### read the data file in as a list
##fin = open( 'MyData1.txt', "r" )
##data_list = fin.readlines()
##fin.close()
### test it ...
##print data_list
## 
##print '-'*60
## 
### remove list items from index 3 to 5 (inclusive)
##del data_list[3:5+1]
### test it ...
##print data_list
## 
### write the changed data (list) to a file
##fout = open("MyData2.txt", "w")
##fout.writelines(data_list)
##fout.close()
