import re


hint6469 = 'NYPVTT'
dict = {"N":"B", "Y":"E", "P":"R","V":"L", "TT":"I"}
last97 = "OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
#alltext = line1+line2+line3+line4+line5+line6+line7+line8+line9+line10+line11+line12+line13+line14
count= 0
for i in last97:
    count+=1
    print i, count

##pattern = re.compile(last97)
##pattern.match(hint6469)
##print alltext
##
##trigger = []
##count= 0
##for letter in last97:
##    count +=1
##    print count, letter
##    if count >=64 and count<= 69:
##        print letter
##        trigger.append(letter)
##    else: pass

##line1 = 'NGHIJLMNQUVWXZKRYPTOSABCDEFGHIJL'
##line2 = 'OHIJLMNQUVWXZKRYPTOSABCDEFGHIJL'
##line3 = 'PIJLMNQUVWXZKRYPTOSABCDEFGHIJLM'
##line4 = 'QJLMNQUVWXZKRYPTOSABCDEFGHIJLMN'
##line5 = 'RLMNQUVWXZKRYPTOSABCDEFGHIJLMNQ'
##line6 = 'SMNQUVWXZKRYPTOSABCDEFGHIJLMNQU'
##line7 = 'TNQUVWXZKRYPTOSABCDEFGHIJLMNQUV'
##line8 = 'UQUVWXZKRYPTOSABCDEFGHIJLMNQUVW'
##line9 = 'VUVWXZKRYPTOSABCDEFGHIJLMNQUVWX'
##line10 = 'WVWXZKRYPTOSABCDEFGHIJLMNQUVWXZ'
##line11 = 'XWXZKRYPTOSABCDEFGHIJLMNQUVWXZK'
##line12 = 'YXZKRYPTOSABCDEFGHIJLMNQUVWXZKR'
##line13 = 'ZZKRYPTOSABCDEFGHIJLMNQUVWXZKRY'
##line14 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZABCD'
