setwd("G:\\Working\\Treelists_2012_update\\SW\\data_analysis\\")
canopyFuel<- read.table("SW_Canopy_Fuel_NoNull.csv",header = TRUE, sep = ",", row.names= 1)

sink("SW_Canopy_Fuel_Summary.txt", append=T)
summary(canopyFuel)
sink()

#####################
pdf('SW.pdf')
fuelcomp <- par(mfrow=c(3,2))
hist(canopyFuel$dia,xlab="Diameter")
hist(canopyFuel$hgt,xlab="Height")
hist(canopyFuel$c.hbc,xlab="Canopy Base Height")
hist(canopyFuel$tpa,xlab="Trees Per Acre")
hist(canopyFuel$barkthickn,xlab="Barkthickness")
dev.off()
###############################################
clist <- c("PNW", "PSW", "NC", "SC", "SE", "NE")
for (i in 1:length(clist)){
	dir <- setwd("G:/Working/Treelists_2012_update/clist[i]/data_analysis/")
	print(dir)
}
	setwd(file.path(dir))
	canopyfueltbl <-paste(clist[i],"_Canopy_Fuel_NoNull.csv", sep=",")
}





