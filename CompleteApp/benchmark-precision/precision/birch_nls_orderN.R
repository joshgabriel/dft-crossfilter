library(minpack.lm)
#library(plot3D)
#library(plotly)          # Load the minpack.lm package
#library(webshot)
#library(rsm)

mydata = read.csv("Rdata.csv")  # Read CSV data file
x<-mydata$kpts         # Select the kpoints atom density
V<-mydata$volume
E<-mydata$energy

init_data = read.csv("Rdata_init.csv")
v0<-init_data$V0
E0<-init_data$E0
B<-init_data$B
BP<-init_data$BP

l = length(E0)

aE <- E0[l]
aP <- BP[l]
aV <- v0[l]
aB <- B[l]

m<- nlsLM( E ~ ((aE1*x + aE*x**2)/(bE0+x+x**2)) + 
    9 / 8 * ((aB1*x + aB*x**2)/(bB0+x+x**2)) * ((aV1*x + aV*x**2)/(bV0+x+x**2)) * (( (aV1*x+aV*x**2)/(bV0+x+x**2) / V)**(2 / 3) - 1)**2 + 
    9 / 16 * ((aB1*x+aB*x**2)/(bB0+x+x**2)) * ((aV1*x + aV*x**2)/(bV0+x+x**2)) * ( (aP*x)/(bP0+x) - 4) * (( (aV*x)/(bV0+x) / V)**(2 / 3) - 1)**3,
    start = list(aE=aE,aB=aB,aP=aP,aV=aV, bE0=1, bB0=1, bP0=1, bV0=1), weights=x^1)

m1=m
extrapol = coef(m)
errors = coef(summary(m))[1:8, "Std. Error"]
#plot(x,y, lty=2,col="black",lwd=3)
#lines(x[l1:l-l2],predict(m),lty=2,col="red",lwd=3)

#plot(x, y-extrapol, col="black", ylim=c(-0.5, 0.5)
#lines(x[l1:l-l2], predict(m)-extrapol, type="l", lty=2, col="red",lwd=3, log="")
#lines(x[l1:l-l2],abs(predict(m)-extrapol),lty=2,col="red",lwd=3)
#summary(m)                  # Report summary of fit, values and error bars

extrapol[1]
extrapol[2] * (1.e24/6.241509125883258e+21)
extrapol[3]
extrapol[4]

output  = data.frame(Extrapolate = extrapol, Error=errors)# Precisions = list(precs), Predicts=list(predicts))
#errorbars = c(predict(m)-E[1:length(predict(m))])
#pred_values = c(predict(m))

#plots = data.frame(Kpoints=x, Volumes=V, Errorbars=errorbars, predict_energy=pred_values, Energy=E)

write.csv(output, 'Result_table.csv')
#write.csv(plots, 'Full_table.csv')
