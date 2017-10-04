import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
#import mpl_toolkits.mplot3d.axes3d as axes3d
import pandas as pd


def interpolating_func(params,x,V):
    aE=  params[0]  
    aB=  params[1]  
    aP=  params[2]
    aV=  params[3]  
    bE0= params[4]  
    bB0= params[5]      
    bP0= params[6]      
    bV0= params[7]   
    return ((aE*x)/(bE0+x)) + (((aB*x)/(bB0+x))*V/((aP*x)/(bP0+x)))*(((((aV*x)/(bV0+x))/V)**
((aP*x)/(bP0+x)))/(((aP*x)/(bP0+x))-1)+1) - ((aV*x)/(bV0+x))*((aB*x)/(bB0+x))/((aP*x)/(bP0+x)-1)


#fig = plt.figure(dpi=100)
#ax = fig.add_subplot(111)#, projection='3d')

# interpolation called
col = cmx.get_cmap('afmhot')
coeffs = pd.read_csv('Result_table.csv')

# actual calculated data scatter
p = pd.read_csv('Rdata.csv')
fx = p['kpts']
fy = p['volume']
fz = p['energy']


#error data
#zerror = p['Errorbars']
#ze_max = max(abs(p['Errorbars']))

kpts_list = np.unique(fx)

print ('read till here fine')

#plot points
#ax.plot(fx, fy, fz, linestyle ="None", marker="o")

#plot individual EV curves at each k

fzp = interpolating_func(list(coeffs['Extrapolate']),fx,fy)
p['predict_energy'] = fzp
p['predict_error'] = p['predict_energy'] - p['energy']

#WORKS
#for k in kpts_list:
#   kpt_select = p[p['kpts']==k]
#   fz_k = list(kpt_select['energy'])
#   fzpe_k = list(kpt_select['predict_error'])
#   fy_k = list(kpt_select['volume'])
#   fx_k = list(kpt_select['kpts'])
#   ax.plot(fx_k, fy_k, fzpe_k, marker = '*', color='red')
   #ax.scatter(fx_k, fy_k, fzp_k, marker='*',color='orange')
   #ax.plot(fx_k, fy_k, fzp_k, color='blue')

# plot errorbars
#for i in np.arange(0, len(fx)):
#    ax.plot([fx[i], fx[i]], [fy[i], fy[i]], [fz[i]+zerror[i], fz[i]-zerror[i]], color=col(abs(zerror[i]/ze_max)),
#marker="_")

# plot surface interpolation 
x = np.linspace(min(fx),max(fx),500)
V = np.linspace(min(fy), max(fy),500)

X,Y = np.meshgrid(x,V)

Z = interpolating_func(list(coeffs['Extrapolate']),X,Y)
#surf = ax.contour(X, Y, Z, cmap=cmx.coolwarm,
#                       linewidth=0, antialiased=False)
# colorbar
#fig.colorbar(surf, shrink=0.5, aspect=5)

#configure axes
#ax.set_xlim3d(10000, 300000)
#ax.set_xscale('log')
#ax.set_ylim3d(0.2, 0.5)
#ax.set_zlim3d(-0.001, 0.001)

#calculate the fitting error predicted at x,V - calculated at x,V
fX, fY = np.meshgrid(fx,fy)

fzp = interpolating_func(list(coeffs['Extrapolate']), fX,fY)

fzp_xy = interpolating_func(list(coeffs['Extrapolate']),fx,fy)

print( (fzp_xy - fz)/fz * 100)

#print (np.shape(fzp))
#print (np.shape(fz))
#print (fzp-fz) 
#print (np.shape(fzp),np.shape(fz))
#print (fzp, np.meshgrid(fz,fz))
fzg = np.meshgrid(fz,fz)
fP = ((fzp-fzg[0])/fzg[0])*100
print (np.shape(fzp), np.shape(fzg[0]))
print (fP)
#print (np.shape(fzp),np.shape(fzg), np.shape(fz))
#fX,fY = np.meshgrid(fx,fy)
#fY = np.meshgrid(fy)

#print (np.shape(fP), np.shape(fX), np.shape(fP))
#v = np.linspace(0.00001, 1.0, 15, endpoint=True)

plt.contour(fx,fy,(fzp_xy - fz)/fz * 100,100, cmap=cmx.coolwarm)

#plt.contourf(fX,fY,fP,100,cmap=cmx.coolwarm)

#plt.pcolor(fX,fY,fP,cmap=cmx.coolwarm, vmin=0.00001, vmax=0.001,
#                       linewidth=0, antialiased=False)

plt.xscale('log')

plt.colorbar()

plt.show()
#p['fit_error_energy'] = fzp - fz

#p.to_csv('Predict_Energy.csv',index=False)

#plt.show()
