mydata = read.csv('./Rdata_linear.csv')

#mydata

x = mydata$X
y = mydata$Y

power_law <-lm('log10(y)~log10(x)')

summary(power_law)

fit_values = 10**(coef(power_law)[1] + coef(power_law)[2] * log10(x))
dat = data.frame(x=x, y=y,f=fit_values)
write.csv(dat, 'predicts.csv')

C = 10**(coef(power_law)[1] + coef(power_law)[2] * log10(0.1)) #coef(power_law)[1]
C_err = 10**(coef(summary(power_law))[1, "Std. Error"] + coef(power_law)[2] * log10(0.1))  
M = coef(power_law)[2]
M_err = coef(summary(power_law))[2, "Std. Error"]

datp = data.frame(C=C, C_err=C_err, M=M, M_err=M_err)

Fit_Value0 =  10**(coef(power_law)[1] + coef(power_law)[2] * log10(0.1))
Fit_Value0

write.csv(datp, 'params.csv')
