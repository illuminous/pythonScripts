#!/usr/bin/env python

import sys
import ftplib
import os
import time


server = "10.80.0.2"
user = "mrlclerk"
password = "Power1"
source = ""
destination = "V:/accounting/Scale Tickets"
interval = 0.05

ftp = ftplib.FTP(server)
ftp.login(user, password)


def downloadFiles(path, destination):
    
##    try:
##        ftp.cwd(path)       
##        os.chdir(destination)
##        mkdir_p(destination[0:len(destination)-1] + path)
##        print "Created: " + destination[0:len(destination)-1] + path
##    except OSError:     
##        pass
##    except ftplib.error_perm:       
##        print "Error: could not change to " + path
##        sys.exit("Ending Application")
    
    filelist=ftp.nlst()
    print destination
    for file in filelist:
        time.sleep(interval)
        try:            
            ftp.cwd(path + file + "/")          
            downloadFiles(path + file + "/", destination)
        except ftplib.error_perm:
            os.chdir(destination[0:len(destination)-1] + path)
            
            try:
                checkfile = path + file + "/"
                if os.path.isfile(checkpath) == false:
                    ftp.retrbinary("RETR " + file, open(os.path.join(destination + path, file),"wb").write)
                print "Downloaded: " + file
            except:
                print "Error: File could not be downloaded " + file
    return
    
def mkdir_p(path):
    try:
        os.makedirs(path)
    except: pass
##    except OSError as exc:
##        if exc.errno == errno.EEXIST and os.path.isdir(path):
##            pass
##        else:
##            raise

downloadFiles(source, destination)
