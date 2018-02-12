"""Download GACC docs from a url.  This script will download any specified file in the LookupRoot directory.
Created by Jason M. Herynk Systems for Environmental Management 20100723"""

from urllib2 import Request, urlopen, URLError, HTTPError
import os, shutil

def stealStuff(file_name, file_mode, base_url):
    #create the url and the request
    url = base_url 
    req = Request(url)
    # Open the url
    try:
            f = urlopen(req)
            print "downloading " + url

            # Open our local file for writing
            local_file = open(file_name, "w" + file_mode)
            #Write to our local file
            local_file.write(f.read())
            local_file.close()

    #handle errors
    except HTTPError, e:
            print "HTTP Error:",e.code , url
    except URLError, e:
            print "URL Error:",e.reason , url

###################################################################################
### Set the Date, Root, and Make the Folders labeled by Date
Date = ['20100921']

Root = 'G:/Working/AirTanker/DailyGACC'
LookupRoot = Root+'/LookupTables'
text = '.txt'
Folders = ['AICC', 'EACC', 'EBCC', 'IncidentTeams', 'NIFC','NRCC', 'NWCC', 'ONCC', 'OSCC', 
           'RMCC', 'SACC', 'SWCC', 'WBCC']

for day in Date:
    for item in Folders:
        try:
            os.makedirs(Root + '/'+ item + '/' + day)
            
        except:
            print 'folder exists'

### Create a list of lookup tables
for f in Folders:
    res = []
    LookupTables = LookupRoot + '/' + f + text
    res.append(LookupTables)
    print res

#### Point to the file with the http root directories and read a line one at a time
    for x in res:
        input = open(x, 'r')
        reports = input.readlines()
        print reports
        

        for day in Date:
            FinDest = Root + '/' + f+ '/' + day
            print FinDest
            for z in reports:
                if z != '\n':
                    url = z.strip()
                    print url 
                    base_url = url
                    urlsplit = base_url.split('/')
                    extension = urlsplit[-1]
                    storage =  FinDest + '/%s' %(extension)
                    file_name = storage.strip()
                    

                    # for the second param ala stealStuff(file_name,'',base_url) option is 'b' for binary
                    stealStuff(file_name, 'b',base_url)
                else:
                    print
                    print '*********************************************************************'
                    print 'Next File'
                    print 
                    print 


