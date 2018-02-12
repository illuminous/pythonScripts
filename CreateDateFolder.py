"""CreateDateFolder.py creates folders within a specified Root Directory.
Created by Jason M. Herynk Systems for Environmental Management 20100722."""

import os

Date = ['20100722', '20100723', '20100724']

Root = 'G:/Working/AirTanker/DailyGACC'

Folders = ['AICC', 'EACC', 'EBCC', 'IncidentTeams', 'NRCC', 'NWCC', 'ONCC', 'OSCC', 
           'RMCC', 'SACC', 'SWCC', 'WBCC']

for d in Date:
    for x in Folders:
        try:
            os.makedirs(Root + '/'+ x + '/' + d)
        except:
            print 'folder exists'

