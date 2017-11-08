#! /usr/bin/env Rscript
input <- file("stdin","r")
library("ggplot2")
X <- c()
Y <- c()
while(length(currentLine <- readLines(input,n=1)) > 0){
	fields <- unlist(strsplit(currentLine," "))
	x <- as.numeric(fields[3])
	y <- as.numeric(fields[4])
	X <- append(X,x)
	Y <- append(Y,y)
	}
data=data.frame(X,Y)
p <- ggplot(data,aes(X,Y))+geom_point()+stat_density2d(aes(fill=..density..),geom="raster",contour=FALSE)
print(p,stdout())
close(input)
