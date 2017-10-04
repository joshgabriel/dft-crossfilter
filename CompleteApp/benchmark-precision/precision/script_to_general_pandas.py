from mpinterfaces.utils import jobs_from_file
from pymatgen.io.vasp.inputs import Kpoints
from pymatgen.io.vasp.outputs import Vasprun
from scipy.optimize import curve_fit
import numpy as np 

import os
from glob import glob

import pandas as pd


def diagnose_cur_dir():
    datasets = []
    good_vaspruns = []
    relax_only = []
    not_goods = []
    totl = len(os.listdir('.'))
    for n,f in enumerate(os.listdir('.')):
        data = {'energy':[],'volume':[],'kpts':[]}
        try:
           #v = Vasprun(f+os.sep+'vasprun.xml')
           if 'POS' in os.listdir(f):
              try:
                 for r in os.listdir(f+os.sep+'POS'):
                    v = Vasprun(f+os.sep+'POS'+os.sep+r+os.sep+'vasprun.xml')
                    struct = v.structures[0]
                    data['energy'].append(v.final_energy/len(struct))
                    data['volume'].append(v.structures[0].volume/len(struct))
                    kpt_list = v.kpoints.as_dict()['kpoints'][0]
                    kpts = kpt_list[0]*kpt_list[1]*kpt_list[2] / len(struct)
                    data['kpts'].append(kpts)
                 good_vaspruns.append(f)
              except:
                 relax_only.append(f)
           else:
               v = Vasprun(f+os.sep+'vasprun.xml')
               relax_only.append(f)
        except:
           not_goods.append(f)
        dframe = pd.DataFrame(data)
        datasets.append({f:dframe})
        print ('FINISHED {0} of {1}'.format(n,totl))
    return good_vaspruns, relax_only, not_goods, len(os.listdir('.')), datasets


def check_correction(tag):
    el, struct = tag.split('_')[0], tag.split('_')[2]
    corr = pd.read_csv('check_combine/{}'.format(tag))
    if struct == 'BCC':
        s = 'bcc'
    elif struct == 'FCC':
        s = 'fcc'
    elif struct == 'HCP':
        s = 'hcp'
    orig = pd.read_csv('{0}_PBE_{1}_VASP.csv'.format(el,s))
    orig.dropna(inplace=False)
    kpts_corr = [k for k in np.unique(corr['kpts']) if k not in np.unique(orig['kpts'])]
    printnew = False
    for n,k in enumerate(kpts_corr):
        print (corr[corr['kpts']==k])
        response = input('Enter 1 if good: ')
        if response:
            orig = pd.concat([orig,corr[corr['kpts']==k]])
            print ('Adding {0}, {1} out of {2}'.format(k,n+1,len(kpts_corr)))
            printnew = True
        else:
            print ('User says {} is not good to add'.format(k))
    if printnew:
        orig.to_csv('buffer_Alex/{0}_PBE_{1}_VASP.csv'.format(el,s),index=False)


def check_kpts(filename):
    print ('checking {}'.format(filename))
    cfilt_file =pd.read_csv(filename)
    dropna_file = cfilt_file.dropna()
    troublemakers = {'Name':[],'Kpt': [], 'NumKpts':[], 'Reason':[]}
    def parabola(x,a,b,c):
        return a + b*x + c*x**2
    numkpts_afterdrop = [(k,dropna_file[dropna_file['kpts']==k]) for k in np.unique(dropna_file['kpts'])]
    print (len(np.unique(dropna_file['kpts'])), max(dropna_file['kpts']))
    for n in numkpts_afterdrop:
        parabola_guess = [min(n[1]['energy']), 1, 1]
        try:
           popt, pcov = curve_fit(parabola, n[1]['volume'], n[1]['energy'], parabola_guess)
           parabola_parameters = popt
           # Here I just make sure the minimum is bracketed by the volumes
           # this if for the solver
           minvol = min(n[1]['volume'])
           maxvol = max(n[1]['volume'])

           # the minimum of the parabola is at dE/dV = 0, or 2 * c V +b =0
           c = parabola_parameters[2]
           b = parabola_parameters[1]
           a = parabola_parameters[0]
           parabola_vmin = -b / 2 / c
           #print (n[0], parabola_vmin)

           Reasons = []
           if not minvol < parabola_vmin and parabola_vmin < maxvol:
             print ('{} has minima issues'.format(n[0]) )
             troublemakers['Name'].append(filename)
             troublemakers['Kpt'].append(n[0])
             troublemakers['NumKpts'].append(len(n[1]))
             troublemakers['Reason'].append('MinimaIssue')

           elif len(n[1])!=11:
             troublemakers['Name'].append(filename)
             troublemakers['Kpt'].append(n[0])
             troublemakers['NumKpts'].append(len(n[1]))
             troublemakers['Reason'].append('Not11Kpoints')

        except:
            print ('Exception caught for {0} at {1}'.format(filename,n[0]))
            troublemakers['Name'].append(filename)
            troublemakers['Kpt'].append(n[0])
            troublemakers['NumKpts'].append(len(n[1]))
            troublemakers['Reason'].append('Exception')

    return troublemakers


def process_to_dataframe(identifiers, metadata = ['energy','volume','kpoints'], chkfiles=glob('*.json'),job_dirs=None):
    """
    utility function that processes data from a list of checkpoints
    or directories into a pandas dataframe

    identifiers: Creates file names for the dataframes
                 1. dict type: job directory concatenation
                example: {0:(('_',0),('/',1)),1:('__',1),'JoinBy':'_','OtherNames':'PBE'}
                         will split the job_dirs elements by
                         '_' and take position 0 followed by a split by '__' take
                         position 1

    """
    if chkfiles:
       #
       chk_jobs = sum([jobs_from_file(c) for c in chkfiles],[])
       jobs = [j for j in chk_jobs if j.final_energy]
       #
       if type(identifiers)==dict:

           def rec_split(string, split_rule):
               #print ('Split rule', split_rule)
               for s in split_rule:
                   #print ('element in split rule', s)
                   string = string.split(s[0])[s[1]]
                   #print (string)
               return string

           dir_splits = []

           for j in jobs:

             single_name = {k:None for k in list(identifiers.keys()) if type(k)==int}
             #
             num_a = len(j.vis.poscar.structure)
             kpt_list = Kpoints.from_file(j.job_dir+os.sep+'KPOINTS').as_dict()['kpoints'][0]
             kpts = kpt_list[0]*kpt_list[1]*kpt_list[2]
             data = pd.DataFrame({'energy':[j.final_energy/num_a],\
                     'volume':[j.vis.poscar.structure.volume/num_a],\
                     'kpts':[kpts/num_a]})
             #
             for k in list(identifiers.keys()):
               if type(identifiers[k])==tuple:
                   single_name.update({k:rec_split(j.job_dir,identifiers[k])})
               else:
                   if k != 'JoinBy':
                      single_name.update({k:identifiers[k]})
             dir_splits.append({identifiers['JoinBy'].join(list(single_name.values())):data})
             print ('finished {}'.format(j.job_dir))

           sorted_dict = {list(d.keys())[0]:[] for d in dir_splits}
           for d in dir_splits:
              sorted_dict[list(d.keys())[0]].append(list(d.values())[0])

           complete_frames = {k:pd.concat(sorted_dict[k]) for k in list(sorted_dict.keys())}
           write_outs = [complete_frames[k].to_csv(k,index=False) \
                         for k in list(complete_frames.keys())]

    elif jobdirs:

       if type(identifiers)==dict:

           def rec_split(string, split_rule):
               #print ('Split rule', split_rule)
               for s in split_rule:
                   #print ('element in split rule', s)
                   string = string.split(s[0])[s[1]]
                   #print (string)
               return string

           dir_splits = []

           for j in jobdirs:
             # simple read whole vasprun
             try:
                 v = Vasprun(j+os.sep+'vasprun.xml')
                 single_name = {k:None for k in list(identifiers.keys()) if type(k)==int}
                 #
                 num_a = len(v.vis.poscar.structure)
                 kpt_list = Kpoints.from_file(j.job_dir+os.sep+'KPOINTS').as_dict()['kpoints'][0]
                 kpts = kpt_list[0]*kpt_list[1]*kpt_list[2]
                 data = pd.DataFrame({'energy':[j.final_energy/num_a],\
                         'volume':[j.vis.poscar.structure.volume/num_a],\
                         'kpts':[kpts/num_a]})
                 #
                 for k in list(identifiers.keys()):
                   if type(identifiers[k])==tuple:
                       single_name.update({k:rec_split(j.job_dir,identifiers[k])})
                   else:
                       if k != 'JoinBy':
                          single_name.update({k:identifiers[k]})
                 dir_splits.append({identifiers['JoinBy'].join(list(single_name.values())):data})
                 print ('finished {}'.format(j.job_dir))
             except:
                 print ('Vaspruns issues')

             sorted_dict = {list(d.keys())[0]:[] for d in dir_splits}
             for d in dir_splits:
                  sorted_dict[list(d.keys())[0]].append(list(d.values())[0])

             complete_frames = {k:pd.concat(sorted_dict[k]) for k in list(sorted_dict.keys())}
             write_outs = [complete_frames[k].to_csv(k,index=False) \
                             for k in list(complete_frames.keys())]



if __name__ == '__main__':
    crossfilts_VASP = [pd.DataFrame(check_kpts(filename=f)) for f in glob('AutoCrossfilts_LDA_VASP/*VASP.csv')]
    pd.concat(crossfilts_VASP).to_csv('LDA_Report.csv',index=False)
    #process_to_dataframe(identifiers={0:(('__',0),('_',0)),1:'PBE',2:(('__',0),('_',1)),\
    #                                    'JoinBy':'_','3':'VASP.csv'}, chkfiles=glob('*Relaxed*.json'))
