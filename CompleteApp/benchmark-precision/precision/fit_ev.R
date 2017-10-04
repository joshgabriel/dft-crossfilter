library(minpack.lm)

init_data = read.csv("Init_fit.csv")  # Read CSV data file
V<-mydata$Volume
E<-mydata$Energy


m<- nlsLM( E ~ ((aE*x)/(bE0+x)) + (((aB*x)/(bB0+x))*V/((aP*x)/(bP0+x)))*(((((aV*x)/(bV0+x))/V)**
((aP*x)/(bP0+x)))/(((aP*x)/(bP0+x))-1)+1) - ((aV*x)/(bV0+x))*((aB*x)/(bB0+x))/((aP*x)/(bP0+x)-1), start = list(aE=aE,aB=aB,aP=aP,aV=aV, bE0=1, bB0=1, bP0=1, bV0=1), weights = x^3)

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
#zp  = matrix(predict(m),nrow=length(predict(m))/11,ncol=11)
#par(new=TRUE)

#persp3D(x=unique(x),y=V[1:11],zp,xlab='k-points density',ylab='volume',zlab='energy', ticktype='detailed')
#zp
#z
#predict(m)
#E
#errorbars = c(predict(m)-E[1:length(predict(m))])
#pred_values = c(predict(m))

#plots = data.frame(Kpoints=x, Volumes=V, Errorbars=errorbars, predict_energy=pred_values, Energy=E)

write.csv(output, 'Result_table.csv')
#write.csv(plots, 'Full_table.csv')
