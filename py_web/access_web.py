
from urllib import urlopen
doc = urlopen("https://fpa.nwcg.gov/FPA/jsps/login/FPALogin.jsf").read()
print doc
