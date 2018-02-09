from zipfile import ZipFile,ZIP_DEFLATED
import os

def recursive_zip_add(zipfile,curdir): #pass in relative path location
    for entry in os.listdir(curdir):
        if os.path.isdir("%s/%s"%(curdir,entry)):
            recursive_zip_add(zipfile,"%s/%s"%(curdir,entry))
        else:
            zipfile.write("%s/%s"%(curdir,entry))

curdir="c:/temp"
zipfile_name="c:/temp.zip"
zipfile=ZipFile(zipfile_name,'w',ZIP_DEFLATED)
recursive_zip_add(zipfile,curdir)
