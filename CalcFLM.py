#------------------------------------------------------------------------------
#           Name: CalcFLM.py
#         Author: Jason Herynk
#  Last Modified: 03/09/2009
#    Description: This Python script asks the user for duff, FWD, CWD, and Litter measurements in kg m^2 and outputs a FLM value.
#                 
#------------------------------------------------------------------------------
import os,re

# read the data file in as a list

duff = float(raw_input('enter duff: '))
FWD = float(raw_input('enter FWD: '))
CWD = float(raw_input('enter CWD: '))
Litter = float(raw_input('enter LITTER: '))

if (duff == 0 and FWD < .53 and Litter >= 0 and CWD >= 0):
    print 'FLM011, Light FWD, light to no duff, Effects Group 1, Wispy Cool Sparse'        
elif (duff == 0 and FWD >= .53 and Litter < .21 and CWD >= 0):
    print 'FLM012 Moderate FWD, light litter, Effects Group 1, Wispy Cool Sparse'
elif (duff == 0 and FWD >= .53 and Litter >= .21 and CWD >= 0):
    print 'FLM041 Moderate FWD, light to moderate litter, Effects Group 4, Wispy Very Hot Light'
elif (duff >= .01 and duff <= .42 and FWD < .53 and Litter >= 0 and CWD >= 0):
    print 'FLM011'
elif (duff >= .01 and duff <= .42 and FWD >= .53 and Litter < .21 and CWD >= 0):
    print 'FLM012'
elif (duff >= .01 and duff <= .42 and FWD >= .53 and Litter >= .21 and CWD >= 0):
    print 'FLM013'
elif (duff >= .43 and duff <= 1.10 and FWD >= 0 and Litter >= 0 and CWD < 2.27):
    print 'FLM021'
elif (duff >= .43 and duff <= 1.10 and FWD >= 0 and Litter >= 0 and CWD >= 2.27 and CWD <= 6.34):
    print 'FLM061'
elif (duff >= .43 and duff <= 1.10 and FWD >= 0 and Litter >= 0 and CWD >= 6.35):
    print 'FLM081'
elif (duff >= 1.11 and duff <= 2.29 and FWD >= 0 and Litter < 2.43 and CWD < 1.83):
    print 'FLM031'
elif (duff >= 1.11 and duff <= 2.29 and FWD >= 0 and Litter >= 2.43 and CWD < 1.83):
    print 'FLM102'
elif (duff >= 1.11 and duff <= 2.29 and FWD >= 0 and Litter >= 0 and CWD >= 1.83 and CWD <= 3.56):
    print 'FLM071'
elif (duff >= 1.11 and duff <= 2.29 and FWD >= 0 and Litter >= 0 and CWD >= 3.57 and CWD <= 7.87):
    print 'FLM083'
elif (duff >= 1.11 and duff <= 2.29 and FWD >= 0 and Litter >= 0 and CWD >= 7.88):
    print 'FLM092'
elif (duff >= 2.3 and duff <= 2.98 and FWD >= 0 and Litter < 2.43 and CWD < 1.83):
    print 'FLM031'
elif (duff >= 2.3 and duff <= 2.98 and FWD >= 0 and Litter >= 2.43 and CWD < 1.83):
    print 'FLM102'
elif (duff >= 2.3 and duff <= 2.98 and FWD >= 0 and Litter >= 0 and CWD >= 1.83 and CWD <= 3.56):
    print 'FLM071'
elif (duff >= 2.3 and duff <= 2.98 and FWD >= 0 and Litter >= 0 and CWD >= 3.57 and CWD <= 7.87):
    print 'FLM083'
elif (duff >= 2.3 and duff <= 2.98 and FWD >= 0 and Litter >= 0 and CWD >= 7.88):
    print 'FLM092'
elif (duff >= 2.99 and duff <= 4.22 and FWD >= 0 and Litter < .62 and CWD < 1.01):
    print 'FLM051'
elif (duff >= 2.99 and duff <= 4.22 and FWD >= 0 and Litter < .62 and CWD >= 1.01 and CWD <= 3.56):
    print 'FLM063'
elif (duff >= 2.99 and duff <= 4.22 and FWD >= 0 and Litter < .62 and CWD >= 3.57 and CWD <= 7.87):
    print 'FLM083'
elif (duff >= 2.99 and duff <= 4.22 and FWD >= 0 and Litter < .62 and CWD >= 7.88):
    print 'FLM092'
elif (duff >= 2.99 and duff <= 4.22 and FWD >= 0 and Litter >= .62 and CWD < 1.01):
    print 'FLM072'
elif (duff >= 2.99 and duff <= 4.22 and FWD >= 0 and Litter >= .62 and CWD >= 1.01 and CWD <= 3.56):
    print 'FLM082'
elif (duff >= 2.99 and duff <= 4.22 and FWD >= 0 and Litter >= .62 and CWD >= 3.57 and CWD <= 7.87):
    print 'FLM083'
elif (duff >= 2.99 and duff <= 4.22 and FWD >= 0 and Litter >= .62 and CWD >= 7.88):
    print 'FLM092'
elif (duff >= 4.23 and duff <= 4.86 and FWD >= 0 and Litter < .62 and CWD < 1.01):
    print 'FLM062'
elif (duff >= 4.23 and duff <= 4.86 and FWD >= 0 and Litter < .62 and CWD >= 1.01 and CWD <= 3.56):
    print 'FLM063'
elif (duff >= 4.23 and duff <= 4.86 and FWD >= 0 and Litter < .62 and CWD >= 3.57 and CWD <= 7.87):
    print 'FLM083'
elif (duff >= 4.23 and duff <= 4.86 and FWD >= 0 and Litter < .62 and CWD >= 7.88):
    print 'FLM092'
elif (duff >= 4.23 and duff <= 4.86 and FWD >= 0 and Litter >= .62 and CWD < 2.29):
    print 'FLM072'
elif (duff >= 4.23 and duff <= 4.86 and FWD >= 0 and Litter >= .62 and CWD >= 2.29 and CWD <= 3.56):
    print 'FLM082'
elif (duff >= 4.23 and duff <= 4.86 and FWD >= 0 and Litter >= .62 and CWD >= 3.57 and CWD <= 7.87):
    print 'FLM083'
elif (duff >= 4.23 and duff <= 4.86 and FWD >= 0 and Litter >= .62 and CWD >= 7.88):
    print 'FLM092'
elif (duff >= 4.87 and duff <= 5.89 and FWD >= 0 and Litter >= 0 and CWD < 3.57):
    print 'FLM064'
elif (duff >= 4.87 and duff <= 5.89 and FWD >= 0 and Litter >= 0 and CWD >= 3.57 and CWD <= 7.87):
    print 'FLM083'
elif (duff >= 4.87 and duff <= 5.89 and FWD >= 0 and Litter >= 0 and CWD >= 7.88):
    print 'FLM092'
elif (duff >= 5.9 and duff <= 8.44 and FWD >= 0 and Litter >= 0 and CWD < 3.57):
    print 'FLM064'
elif (duff >= 5.9 and duff <= 8.44 and FWD >= 0 and Litter >= 0 and CWD >= 3.57 and CWD <= 7.87):
    print 'FLM093'
elif (duff >= 5.9 and duff <= 8.44 and FWD >= 0 and Litter >= 0 and  CWD >= 7.88):
    print 'FLM092'
elif (duff >= 8.45 and duff <= 13.4 and FWD >= 0 and Litter >= 0 and CWD < 3.57):
    print 'FLM091'
elif (duff >= 8.45 and duff <= 13.4 and FWD >= 0 and Litter >= 0 and CWD >= 3.57 and CWD <= 7.87):
    print 'FLM093'
elif (duff >= 8.45 and duff <= 13.4 and FWD >= 0 and Litter >= 0 and CWD >= 7.88):
    print 'FLM092'
elif (duff >= 13.41 and FWD >= 0 and Litter >= 0 and CWD >= 0):
    print 'FLM101'
       
