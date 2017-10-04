import matplotlib.pyplot as plt
import pandas as pd

from glob import glob

import os
import numpy as np

def interpolating_func(params,x,V, eos):
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

if __name__=='__main__':
    eos = 'murnaghan'
    rscript = eos+'_nls.R'
    for NAME in glob('AutoCrossfilts/*PBE*.csv'):
       try:
           os.system('cp AutoCrossfilts_VASP/{} Rdata.csv'.format(NAME.split('/')[-1]))
           print ('copied {}'.format(NAME))
           run_R_data = pd.read_csv('Rdata.csv')
           run_R_data.dropna(inplace=True)
           run_R_data.to_csv('Rdata.csv', index=False)
           os.system('Rscript {}'.format(rscript))
           print ('R executed')

           coeffs = pd.read_csv('Result_table.csv')

           p = pd.read_csv('Rdata.csv')
           fx = p['kpts']
           fy = p['volume']
           fz = p['energy']

           n_fx = list(p['kpts'])
           n_fy = list(p['volume'])
           print (len(n_fy), len(n_fx))
           n_fz = list(p['energy'])
           n_fx_spl = np.array([ [x for x in n_fx[n:n+int(len(n_fy)/len(np.unique(n_fx)))] ] \
                   for n in range(0,int(len(n_fy)/len(np.unique(n_fx))) * len(np.unique(n_fx)), int(len(n_fy)/len(np.unique(n_fx))))  ])

           n_fy_spl = np.array([ [y for y in n_fy[n:n+int(len(n_fy)/len(np.unique(n_fx)))] ] \
                   for n in range(0,int(len(n_fy)/len(np.unique(n_fx))) * len(np.unique(n_fx)), int(len(n_fy)/len(np.unique(n_fx))))  ])

           n_fz_spl = np.array([ [z for z in n_fz[n:n+int(len(n_fy)/len(np.unique(n_fx)))] ] \
                   for n in range(0,int(len(n_fy)/len(np.unique(n_fx))) * len(np.unique(n_fx)), int(len(n_fy)/len(np.unique(n_fx))))  ])

           n_fz_p = interpolating_func(list(coeffs['Extrapolate']),n_fx_spl,n_fy_spl)
           print ( np.shape(n_fx_spl),np.shape(n_fy_spl),np.shape(n_fz_spl), np.shape((n_fz_p-n_fz_spl)/n_fz_spl * 100) )
           plt.contourf(n_fx_spl, n_fy_spl, n_fz_spl)
           #plt.contourf(n_fx_spl,n_fy_spl,((n_fz_p-n_fz_spl)/n_fz_spl)*100,cmap=plt.cm.coolwarm)
           plt.xscale('log')
           plt.xlabel('$k-$point density per atom')
           plt.ylabel('Volume per atom in $\AA^3$')
           plt.colorbar()
           plt.savefig(NAME.split('/')[-1]+'raw_evk_contour_E.png')
           plt.close()
       except:
           print ('some error', NAME)
