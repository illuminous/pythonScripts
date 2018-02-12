################################################
setwd("G:\\Working\\Treelists_2012_update\\NE\\data_analysis\\")
canopyFuel<- read.table("NE_Canopy_Fuel_NoNull.csv",header = TRUE, sep = ",", row.names= 1)

A <- boxplot(canopyFuel$dia)
sink("NE_BoxPlot2.txt", append=T)
mytable <- A$stats
rownames(mytable)<-c('min','lower quartile','median','upper quartile','max')
colnames(mytable)<-A$names
mytable 
print("diameter")
print("")

B <- boxplot(canopyFuel$hgt)
mytable <- B$stats
rownames(mytable)<-c('min','lower quartile','median','upper quartile','max')
colnames(mytable)<-B$names
mytable 
print("height")
print("")

C <- boxplot(canopyFuel$c.hbc)
mytable <- C$stats
rownames(mytable)<-c('min','lower quartile','median','upper quartile','max')
colnames(mytable)<-C$names
mytable 
print("hbc")
print("")

D <- boxplot(canopyFuel$tpa)
mytable <- D$stats
rownames(mytable)<-c('min','lower quartile','median','upper quartile','max')
colnames(mytable)<-D$names
mytable 
print("tpa")
print("")

E <- boxplot(canopyFuel$barkthickn)
mytable <- E$stats
rownames(mytable)<-c('min','lower quartile','median','upper quartile','max')
colnames(mytable)<-E$names
mytable 
print("barkthickness")
print("")

sink()