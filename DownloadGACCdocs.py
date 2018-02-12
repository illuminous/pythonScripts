# Let's create a function that downloads a file, and saves it locally.
# This function accepts a file name, a read/write mode(binary or text),
# and the base url.
from urllib2 import Request, urlopen, URLError, HTTPError
import os, shutil
def stealStuff(file_name,file_mode,base_url):
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

# Set the range of images to 1-50.It says 51 because the
# range function never gets to the endpoint.
#image_range = range(1,51)
# Iterate over image range
#for index in image_range:

base_url = 'http://fire.ak.blm.gov/content/aicc/crews/type2crews.pdf'
#create file name based on known pattern
file_name =  ''
#file_name =  'G:/Working/AirTanker/DailyGACC/AICC/20100722/x.pdf'
# Now download the image. If these were text files,
# or other ascii types, just pass an empty string
# for the second param ala stealStuff(file_name,'',base_url)
stealStuff(file_name, '',base_url)
