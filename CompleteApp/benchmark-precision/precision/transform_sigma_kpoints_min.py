# change sigma precs to sigma_E_kmin precs

import matplotlib
#matplotlib.rcParams.update({'font.size': 18,'legend.fontsize':18, 'lines.markersize': 14})
matplotlib.rcParams.update({'font.size': 18, 'font.family':'Times New Roman', 'legend.fontsize':12, 'lines.markersize': 12})
matplotlib.rcParams['figure.figsize'] = 7.5, 5

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

import yaml
import numpy as np
import os
import sys

def to_percent(y, position):
        # Ignore the passed in position. This has the effect of scaling the default
        # tick locations.
        s = str(int(100 * y))

        # The percent symbol needs escaping in latex
        #if matplotlib.rcParams['text.usetex'] is True:
        #    return s + r'$\%$'
        #else:
        #    return s + '%'
        return s

def crossfilter_el(data,el,st):
    # first element
    el_data  = data[data['element']==el]
    st_el_data = el_data[el_data['structure']==st]
    #structs = np.unique(el_data['structure'])
    # perform crossfilter on first structure entry available, list others as well
    #print (structs)
    #st_el_data = el_data[el_data['structure']==structs[0]]
    # finally on property
    kpoints_atom = list(st_el_data['k'])
    #kpoints_atom = [k**3 for k in kpoints]
    #print (el,st,p,kpoints_atom, list(p_st_el_data['perc_precisions']))
    E0,v0,B,BP = list(st_el_data['sE0k']), list(st_el_data['sV0k']), \
                 list(st_el_data['sBk']), list(st_el_data['sBPk'])
    return kpoints_atom, E0,v0,B,BP

if __name__=='__main__':
   """
   extract transforms
   """
   code = 'DMol3'
   mydata = pd.read_csv('{}_fit_weighted_birch_precision_data_frames.csv'.format(code)) 
   sigma_Ps = {}
   kpoints_choices = []  
   st_el = [] 
   print ('finished sorted clean up.. crossfiltering..')
   transformed_set = {'element': [], 'structure': [], 'kpts_density': [], 'sigma_P_kmin':[]}
   prop_colors = { 'E0':'darkgreen', 'v0':'black', 'B':'blue', 'BP':'red' }
   prop_labels = { 'E0':'$\sigma_{E_0}kmin$', 'v0': '$\sigma_{V_0}kmin$', 'B': '$\sigma_Bkmin$', 'BP': "$\sigma_B'kmin$" }
   prop_markers = {'BP':'D','B':'s','v0':'x','E0':'*'}
   for el in np.unique(mydata['element']):
      el_mydata  = mydata[mydata['element']==el]
      for st in np.unique(el_mydata['structure']):
         st_el_mydata = el_mydata[el_mydata['structure']==st]
         kpts, E0,v0,B,BP = crossfilter_el(mydata, el, st)
         for s,p in [('v0',v0),('B',B),('BP',BP), ('E0',E0)]: 
            sigma_P_kmin = [ max( [abs(i) for i in p][n:] ) for n, k in enumerate(kpts) ]
            print (s, sigma_P_kmin)
            #print (len(sigma_P_kmin),len(kpts))
            if st == 'Tetra' and el == 'Cr':
                 print ('Here?')
                 name = 'bcc_Cr'
            elif st == 'Tetra' and el == 'Al':
                 print ('Here Al?')
                 name = 'fcc_Al'
            else:
                 name = '_'.join([st,el]) 

            plt.scatter(kpts,sigma_P_kmin, label=prop_labels[s], color=prop_colors[s], marker=prop_markers[s]) 
            plt.plot(kpts,sigma_P_kmin, label=None, color=prop_colors[s], marker=prop_markers[s])
            print (st,el,s)
            sigma_Ps[s] = {'Sigma':sigma_P_kmin, 'Kpts':kpts} 

#         for n,k in enumerate(kpts):
#               transformed_set['element'].append(el)
#               transformed_set['structure'].append(st)
#               transformed_set['kpts_density'].append(k)
                #print (k,sigma_P_kmin[n])
#               transformed_set['sigma_E_kmin'].append(sigma_Ps['E0']['Sigma'][n])
#               transformed_set['sigma_V_kmin'].append(sigma_Ps['v0']['Sigma'][n])
#               transformed_set['sigma_B_kmin'].append(sigma_Ps['B']['Sigma'][n])
#               transformed_set['sigma_BP_kmin'].append(sigma_Ps['BP']['Sigma'][n])
             #trans_set = transformed_set
             #pd.DataFrame(trans_set).to_csv('trans{}set.csv'.format(i))

         plt.yscale('log') 
         plt.xscale('log') 
         plt.ylim(min(sigma_P_kmin),10.0) 
         plt.ylabel('Max $\sigma$ % for $k-$points choice')
         plt.xlabel('$k-$points density per atom')
         #plt.legend()
         #plt.tight_layout()
         print (name)
         plt.savefig('{}_sigma_kmin_'.format(code)+name+'.pdf')
         plt.close()
         print (el,st)
         for k in sigma_Ps.keys():
            sigma_indices = [n for n,s in enumerate(sigma_Ps[k]['Sigma']) if abs(float(s))<1.0]
            if sigma_indices:
               sigma_Ps[k].update( {'min_index':min(sigma_indices)} )
            else:
               sigma_Ps[k].update( {'min_index':1} )
               print ('Non precise warning for {0} {1}'.format(st, el))
         #if (el,st)!=('Al','bcc'): 
         kpt_index = max([sigma_Ps[k]['min_index'] for k in sigma_Ps.keys()])
         print (np.log10(sigma_Ps['E0']['Kpts'][kpt_index]))
         kpoints_choices.append(np.log10(sigma_Ps['E0']['Kpts'][kpt_index]))
         st_el.append('_'.join([el,st]))
        
            
         #print (sigma_Ps)

         sigma_Ps = {}

         # k-points choices 
         #prop_sigmas  = [ n for n,s in enumerate(p[0]) for p in sigma_Ps if abs(float(s)) < 1.0 ]
         #kpt_sigmas = [ p[1] for p in sigma_Ps ]
#counter = counter + i
   print ('got the records for the new table..')
   #transformed = pd.DataFrame(transformed_set)
   print ('made the dataframe and saving... finished. ')
   #transformed.to_csv('v6_transformed_sigmas.csv')
   plt.close()
   pd.DataFrame({'Material':st_el, 'Kpoints_Density':kpoints_choices}).to_csv('DMol3_Kpoints_Choices.csv')
   formatter = FuncFormatter(to_percent) 
   my_weights = np.ones_like(kpoints_choices)/float(len(kpoints_choices))
   plt.hist(kpoints_choices,weights=my_weights)
   ax = plt.gca()
   plt.gca().yaxis.set_major_formatter(formatter)
   plt.title('DMol3')
   plt.xlim(1,5)
   ax.set_xlabel('$k-$points density per atom')
   ax.set_xticklabels(['$10^{}$'.format(a) for a in [int(s) for s in ax.get_xticks()]])#range( int(min(kpoints_choices))-1,int(max(kpoints_choices))+2 )] )
   ax.set_ylabel('% of Elements')
   plt.savefig('DMol3_Kpoints_Choices_histogram_logs.pdf')
   
