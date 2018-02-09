import win32com.client, os
from rpy import *

def extract_intervals(years,stats,filter_percent=10,min_samples=3,start_year=0,end_year=2050):
    fires=[]
    intervals=[]
    for entry in range(0,len(years)):
        fire=0
        if stats['percent_scarred'][entry]>=filter_percent and stats['num_recording_samples'][entry]>=min_samples:
            fire=1
        fires.append(fire)
    start=0
    for index in range(0,len(fires)):
        start+=1
        if fires[index]==1:
            break
    counter=0
    end=0
    for index in range(start,len(fires)):
        counter+=1
        if fires[index]==1:
            intervals.append(counter)
            counter=0
            end=index

    #now construct fire data for start year to end year
    print years[start],years[end]
    scarred=[]
    recording=[]
    plot_years=[]
    filter_samples=[]
    for index in range(start,end+1):
        scarred.append(stats['num_scarred'][index])
        recording.append(stats['num_recording_samples'][index])
        filter_samples.append((float(filter_percent)/100.0)*stats['num_recording_samples'][index])
##        if years[index]%10==0:
##            plot_years.append(years[index])
##        else:
##            plot_years.append("")
        plot_years.append(years[index])

        
    #now fires is the composite series    
    #print len(fires),sum(fires),intervals
    #result is a list of intervals
    

    r("library(MASS)")
    fit=r.fitdistr(intervals,"weibull")['estimate']
    scale=fit['scale']
    shape=fit['shape']
    print scale,shape


    #after this do the K-S test, and look at probability
    r("library(stats)")
    test=r.ks_test(intervals, fit)
    print test["p.value"]
    wmfi=scale * r.gamma(1+ 1/shape)
    #grab mean of intervals from R
    r("library(base)")
    mean=r.mean(intervals)
    #if p>0.05 then just simple MFI rather than WMPI
    if test["p.value"] > 0.05:
        MFI=mean
        print "Arithmetic Mean",MFI
    #to calculate the mean from weibull, will need to call R again using gamma function
    elif test["p.value"] < 0.05:
        MFI=wmfi
        print "WMPI", MFI
    
    #also look for outliers

    #some R snippets for composite chart:
##    r("library(graphics)")
    r.plot(plot_years,recording,main="",xlab="Year",ylab="Number of Trees",type="l",lwd=2,ylim=[0,max(recording)],las=2)
    #ticks=r.barplot(recording,names_arg=plot_years,las=2,cex_names=0.75,axis_lty=1,border="white")
    r.lines(plot_years,scarred,lwd=2,col='red')
    r.lines(plot_years,filter_samples,lty=3)
    #r.abline(h=min_samples,lty=3)
    
#global variables we control at top of program    
min_percent_trees=30


working_dir=os.getcwd()

datafile = open("%s/abm_all.fhx"%(working_dir),"r")
data= datafile.readlines()
i=0
for line in data:
    i+=1
    if line.count("FHX2 FORMAT"):
            break
rows_to_skip=int(data[i].split(" ")[2])+2
start=i+1+rows_to_skip

samples=[]
num_samples=int(data[i].split(" ")[1])
for col in range(0,num_samples):
	samples.append([])

min_samples=int(round(num_samples*(min_percent_trees/100.0),0))

years=[]
stats=dict()
stats['num_scarred']=[]
stats['num_recording_samples']=[]
stats['percent_scarred']=[]


outfile=open("%s/test_out.txt"%(working_dir),'w')

for line in data[start:]:
        line=line.replace("\n","").split(" ")
        samp_data=line[0]
        year=int(line[1])
        years.append(year)
        num_recording_samples=0
        num_scarred=0
        percent_scarred = 0

        outline=""
        
        for col in range(0,len(samp_data)):
            cur=samp_data[col]
            outline+="%s"%(cur)
            samples[col].append(cur)
            #nonrecording
            if cur==".":
                pass
            #is recording tree
            if cur =="|":
                num_recording_samples+=1

            #tree start     
            if (cur=="{" or cur=="["):
                pass
            #tree end
            if cur=="}" or "]":
                pass
            #scars
            if cur in ["A","D","E","L","M","U"]:
                num_recording_samples+=1
                num_scarred+=1
                        
        if num_scarred > 0:
            percent_scarred=100.0* num_scarred/num_recording_samples
        
        stats['num_scarred'].append(num_scarred)
        stats['num_recording_samples'].append(num_recording_samples)
        stats['percent_scarred'].append(percent_scarred)

        outline+="  %s  %s  %s  %s\n"%(year,num_scarred,num_recording_samples,percent_scarred)
        outfile.write(outline)
        
outfile.close()

extract_intervals(years,stats,10,min_samples,start_year=min(years),end_year=max(years))

