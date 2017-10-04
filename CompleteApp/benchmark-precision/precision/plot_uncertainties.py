import pandas as pd
import numpy as np

import matplotlib 
matplotlib.rcParams['figure.figsize'] = 7.5, 5
matplotlib.rcParams['font.size'] = 16
matplotlib.rcParams['lines.markersize'] = 12
matplotlib.rcParams['font.family'] = 'Times New Roman'

import matplotlib.pyplot as plt

code = 'LDA_VASP'
prec_data = pd.read_csv('{}_fit_weighted_birch_precision_data_frames.csv'.format(code))

def calculate_property_uncertainty(p):
         median = []
         percentile90 = []
         percentile10 = []

         for k in np.unique(prec_data['k']):
             k_prec = prec_data[prec_data['k']==k]
             percentile10.append(k_prec['s{}k'.format(p)].quantile(0.1))
             percentile90.append(k_prec['s{}k'.format(p)].quantile(0.9))
             median.append(k_prec['s{}k'.format(p)].median())
         return (percentile10, median, percentile90)

plt.xscale('log')

colors = {'E0':'green', 'V0':'black','B':'blue','BP':'red'}
markers = {'E0':'*', 'V0':'+','B':'^','BP':'v'}
kpts = np.unique(prec_data['k'])
for p in ['E0','V0','B','BP']:
   percentile10, median, percentile90= calculate_property_uncertainty(p)
   #plt.fill_between(kpts, percentile10, percentile90, color='white'
   plt.plot(kpts, percentile10, color=colors[p], linestyle='--',linewidth=0.2)
   plt.plot(kpts, percentile90, color=colors[p], linestyle='-.',linewidth=0.8)
   plt.plot(kpts, median, color=colors[p],linewidth=0.4)
   #plt.fill_between(kpts, percentile10, percentile90, color='#d3d3d3')

plt.ylim(-10.0,10.0)
plt.savefig('Percentile_Uncertainties_{}.pdf'.format(code))

