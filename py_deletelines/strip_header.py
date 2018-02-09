import os

zones = ['z29']
names = ['_event_1.out', '_event_2.out', '_event_3.out', '_event_4.out', '_event_5.out', '_event_6.out', '_event_7.out', '_event_8.out', '_event_9.out',\
         '_event_10.out', '_event_11.out','_event_12.out', '_event_13.out', '_event_14.out', '_event_15.out', '_event_16.out', '_event_17.out',\
         '_event_18.out', '_event_19.out', '_event_20.out']

for zone in zones:
    for name in names:
        print zone+name
        input = open('E:/emds/event_outfiles/%s%s' %(zone, name), 'r') 
        s = input.readlines()
        del s[:26]
        output = open('E:/emds/event_outfiles/test/fin/%s%s' %(zone, name), 'w')
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
