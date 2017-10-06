"""
complete Pade analysis workflow
from E-V fitted data to
the precision data, plots and
histograms
GOAL: to be the one script that is used by
the database web app to be activated in part
on sensibly crossfiltered data
and also on the a complete new set of data
in an object oriented way.
"""
# must be executed within
# an anaconda shell with R-3.3.1
# this script will command the required R scripts
# 1. first crossfilter according to the project
# 2. perform the Pade analysis on each of the crossfiltered parts
# 3. calculate the precisions and create the database ready data with precisions
# 4. perform analysis on the precision relationship between properties
# 5. describe the analysis with histograms

import os
import pandas as pd
import numpy as np
from glob import glob
import matplotlib
#print (matplotlib.rcParams.keys())
matplotlib.rcParams.update({'font.size': 16, 'font.family':'Times New Roman', 'legend.fontsize':12, 'lines.markersize': 12})
#from mpinterfaces.utils import get_logger

import matplotlib.pyplot as plt
import sys
from matplotlib.ticker import FuncFormatter
from matplotlib.mlab import griddata
from scipy.interpolate import griddata as sci_grid
from scipy.ndimage import zoom
from scipy.odr import *
from math import sqrt
from sklearn.metrics import mean_squared_error
try:
   from ase.eos import EquationOfState
except:
   print ('Warning: import ase fail')
#from mpinterfaces.utils import print_exception

#logger = get_logger('Warnings')

code = 'LDA_DMol3'

class DatabaseData:
    """
    a class that contains all the attributes of
    the DatabaseData and builds the database
    to a complete set of its endpoints
    """
    def __init__(self,dataframe):
        """
        constructor function that builds from original data
        of values of the different properties. simply constructs
        data from a k-point, value attribute csv file with pandas
        """
        self.dataframe = dataframe

    def create_crossfilts(self,tags,db):
        """
        function to create crossfilters by a specified tag
        this function can serve further as a
        generalized query to the mongoDB
        """
        #print (db.columns, db['code'], tags['code'])
        tag1_database = db[db['code']==tags['code']]
        tag2_database = tag1_database[tag1_database['exchange']==tags['exchange']]
        tag3_database = tag2_database[tag2_database['element']==tags['element']]
        tag4_database = tag3_database[tag3_database['structure']==tags['structure']]
        #tag5_database = tag4_database[tag4_database['property']==tags['property']]

        return tag4_database

    def fit_ev(self,energy, volume, eos_name,return_rms=False, return_params=False):
            """
            fit an energy volume curve
            handles three cases :
            1. fit ev for the high k-point data for the initial values for the power fit
            2. fit eos for each k-point, general eos fit for an energy volume set
            3. calculate and return rms error of the eos fit
            """
            try:
              Eos = EquationOfState(volume, energy, eos='birch')
              E0, E0_err, V0, V0_err,\
               B, B_err, BP , BP_err,y_pred = Eos.fit()
              if return_params:
                  # case when ev fit required for each k-point
                 #print ('Returning individual k')
                 return (E0, E0_err, V0, V0_err, B, B_err, BP, BP_err)
            except:
              #logger.warn('Exception eos')
              #print (print_exception())
              if return_rms:
                 return ('xxx')
              else:
                 return (None, None, None, None, None, None, None, None)

            if not return_rms and not return_params:
               # for high k- points initial fit values return
               #print ('High K!')
               pd.DataFrame({'E0':[E0],'V0':[V0],'B':[B],'BP':[BP]}).to_csv('./Rdata_init.csv', index=False)
               #print (E0,V0,B,BP)
            else:
               # calculate rms error of fit
               rms = sqrt(mean_squared_error(energy, y_pred))
               return (rms)

    def get_avg_rms_fit_error(self,data,name,eos_name):
            """
            takes the whole file and fits EOS for each
            kpts density, calculates the RMS error of fit
            and returns the average across all kpts for that element
            combination name
            """
            for k in np.unique(data['kpts']):
               kpt_data = data[data['kpts']==k]
               self.fit_rms_set['_'.join([name,'kpt',str(k)])] = self.fit_ev(kpt_data['energy'],kpt_data['volume'], eos_name=eos_name,return_rms=True)


    def read_crossfilts(self, filename):
            """
            file reader for crossfilts
            """
            self.crossfilt = pd.read_csv(filename)

    def pade_precision(self,coeff,vals,kpts):
            """
            return the precision by property, element and structure
            """
            try:
              #kpts = [k for k in np.linspace(100,int(list(coeff['nKptMax'])[0]),100)]
              #print (len(kpts))
              #sys.exit(0)
              E0 = float(list(coeff['E0'])[0])
              V0 = float(list(coeff['V0'])[0])
              B = float(list(coeff['B'])[0])
              BP = float(list(coeff['BP'])[0])
              bE0 = float(list(coeff['bE0'])[0])
              bV0 = float(list(coeff['bV0'])[0])
              bB = float(list(coeff['bB'])[0])
              bBP = float(list(coeff['bBP'])[0])
              E0_err = float(list(coeff['E0_err'])[0])
              V0_err = float(list(coeff['V0_err'])[0])
              B_err = float(list(coeff['B_err'])[0])
              BP_err = float(list(coeff['BP_err'])[0])

              return [list(vals['E0k'])[n] for n,k in enumerate(kpts)],\
                     [ (list(vals['E0k'])[n] - E0 )/ E0 * 100 for n,k in enumerate(kpts) ],\
                     [ np.sqrt( (list(vals['E0k_err'])[n])**2 + (E0_err)**2 ) for n,k in enumerate(kpts) ],\
                     [list(vals['V0k'])[n] for n,k in enumerate(kpts)],\
                     [ (list(vals['V0k'])[n] - V0 )/ V0 * 100 for n,k in enumerate(kpts) ],\
                     [ np.sqrt( (list(vals['V0k_err'])[n])**2 + (V0_err)**2 ) for n,k in enumerate(kpts) ],\
                     [list(vals['Bk'])[n] for n,k in enumerate(kpts)],\
                     [ (list(vals['Bk'])[n] - B )/ B * 100 for n,k in enumerate(kpts) ],\
                     [ np.sqrt( (list(vals['Bk_err'])[n])**2 + (B_err)**2 ) for n,k in enumerate(kpts) ],\
                     [list(vals['BPk'])[n] for n,k in enumerate(kpts)],\
                     [ (list(vals['BPk'])[n] - BP )/ BP * 100 for n,k in enumerate(kpts) ],\
                     [ np.sqrt( (list(vals['BPk_err'])[n])**2 + (BP_err)**2 ) for n,k in enumerate(kpts) ],\

            except:
              #logger.warn('precision EXCEPTIONS')
              return None, None, None, None, None, None, None, None#[None for k in range(1,4)], [None for k in range(1,4)], [None for k in range(1,4)], [None for k in range(1,4)], [None for k in range(1,4)], [None for k in range(1,4)], [None for k in range(1,4)], [None for k in range(1,4)], [None for k in range(1,4)]

    def interpolating_func(self,k,V,params,eos='birch'):
            """
            general interpolating function for the contour plots
            """
            print ('makes into interpol', params)
            aE=  params['E0']
            aB=  params['B']*(6.241509125883258e+21/1.e24)
            aP=  params['BP']
            aV=  params['V0']
            print ('here half')
            bE0= params['bE0']
            bB0= params['bB']
            bP0= params['bBP']
            bV0= params['bV0']

            print ('makes past params')

            if eos=='murnaghan':
               #print ('Here')
               return ((aE*k)/(bE0+k)) + (((aB*k)/(bB0+k))*V/((aP*k)/(bP0+k)))*(((((aV*k)/(bV0+k))/V)**((aP*k)/(bP0+k)))/(((aP*k)/(bP0+k))-1)+1) - ((aV*k)/(bV0+k))*((aB*k)/(bB0+k))/((aP*k)/(bP0+k)-1)

            elif eos=='birch':
               #print ([type(Vi) for Vi in V])
               return ((aE*k)/(bE0+k)) + \
    9.0 / 8.0 * ((aB*k)/(bB0+k)) * ((aV*k)/(bV0+k)) * (( (aV*k)/(bV0+k) / V)**(2.0 / 3.0) - 1.0)**2.0 + 9.0 / 16.0 * ((aB*k)/(bB0+k)) * ((aV*k)/(bV0+k)) * ( (aP*k)/(bP0+k) - 4.0) * (( (aV*k)/(bV0+k) / V)**(2.0 / 3.0) - 1.0)**3.0

            elif eos=='pouriertarantola':
               return (aE*k)/(bE0+k) + (aB*k)/(bB0+k) * (aV*k)/(bV0+k) * (-3 * log((V / (aV*k)/(bV0+k) )**(1 / 3)))**2 / 6 * (3 + (-3 * log((V / (aV*k)/(bV0+k) )**(1 / 3))) * ((aP*k)/(bP0+k) - 2))

            elif eos=='birchmurnaghan':
               return (aE*k)/(bE0+k) + 9 * ((aB*k)/(bB0+k)) * ((aV*k)/(bV0)) / 16 * ((((aV*k)/(bV0+k)*V)**(1/3))**2 - 1)**2 * (6 + ((aP*k)/(aP+k)) * ((((aV*k)/(bV0+k)*V)**(1/3))**2 - 1) - 4 * (((aV*k)/(bV0+k)*V)**(1/3))**2)
               pass

            elif eos=='vinet':
               print ('with vinet')
               return ((aE*k)/(bE0+k) + 2 * (aB*k)/(bB0+k) * (aV*k)/(bV0+k) / ((aP*k)/(bP0+k) -1)**2 * (2-(5 + 3 * (aE*k)/(bE0+k) * ( (V / (aV*k)/(bV0+k))**(1 / 3) - 1) - 3 * (V / (aV*k)/(bV0+k))**(1 / 3) ) * exp(-3 * ((aP*k)/(bP0+k) - 1) * ( (V / (aV*k)/(bV0+k))**(1 / 3) - 1) / 2)))

    def run_pade_through_R(self, rscript, plot_contours=False,get_inits_ev=False, get_fit_rms=False):
        """
        Runs the Pade analysis through a supplied R script
        runs the Pade through a python subprocess call to nls.R
        on the input crossfilt
        - copies the input to Rdata.csv for input to nls.R
        - retrieves the output of nls.R that is pasted out into csv file
          that can be read back into pandas
          .. element, structure, exchange, code, property, extrapolate, fit error
          which can serve as another reference collection for calculation of
          the precision from the main database.
        """
        self.records = []
        self.ev_fit_records = []
        self.incomps = {}
        self.result = {}
        ###############
        run_R_data = self.dataframe
        kpt_list = []
        kpt_drops = []
        fcc_bcc_nlist = []
        hcp_nlist = []
        for k in np.unique(run_R_data['kpoints']):
            k_crossfilt = run_R_data[run_R_data['kpoints']==k]
            if len(k_crossfilt['energy'])<11:
               #logger.info('k-point less than 11 points'.format(k))
               kpt_drops.append(k_crossfilt)
               kpt_list.append(k)
               #logger.info('appended to drop {}'.format(k))

        if kpt_drops:
            kpt_drop_cf = pd.concat(kpt_drops)
            fit_data=run_R_data.drop(run_R_data.index[list(kpt_drop_cf.index)])
            #logger.info('dropped something {}'.format(kpt_drops))
        else:
            fit_data = run_R_data


        if list(fit_data['energy']):
           fit_data.to_csv('./Rdata.csv', index=False)

           # for first inits?
           if get_inits_ev:
             kpt_max = max(np.unique(list(run_R_data['kpoints'])))
             end_kpt_data = run_R_data[run_R_data['kpoints']==kpt_max]
             print ('fitting init')
             self.fit_ev(list(end_kpt_data['energy']), list(end_kpt_data['volume']),rscript)

           if get_fit_rms:
               self.fit_rms_set = {}
               self.get_avg_rms_fit_error(data=run_R_data,name=NAME,eos_name=rscript)

           self.result['element'] = str(np.unique(list(self.dataframe['element']))[0])
           self.result['exchange'] = str(np.unique(list(self.dataframe['exchange']))[0])
           self.result['code'] = str(np.unique(list(self.dataframe['code']))[0])
           self.result['structure'] = str(np.unique(list(self.dataframe['structure']))[0])
           # for calculating the precisions?
           for k in np.unique(list(run_R_data['kpoints'])):
              end_kpt_data = run_R_data[run_R_data['kpoints']==k]
              E0, E0_err, V0, V0_err, B, B_err, BP, BP_err = \
              self.fit_ev(list(end_kpt_data['energy']),\
                      list(end_kpt_data['volume']),rscript, return_params=True)
              #print ('E0 value: {}'.format(E0))
              if E0 and E0!='Warn':
                 self.ev_fits = {'E0_eos':E0,'E0_eos_err': E0_err,
                              'V0_eos':V0, 'V0_eos_err':V0_err,
                              'B_eos':B, 'B_eos_err': B_err,
                              'BP_eos':BP, 'BP_eos_err':BP_err,
                              'k':k,
                              'element': self.result['element'],
                              'exchange':self.result['exchange'],
                              'structure':self.result['structure'],
                              'code':self.result['code']
                              }

                 self.ev_fit_records.append(self.ev_fits)
                 #print (self.ev_fits)
              elif E0 == 'Warn':
                 #logger.warn('Warning found at {0} {1} {2}'.format(k, len(end_kpt_data['energy']), NAME))
                 self.ev_fits = {'E0_eos':E0,'E0_eos_err': E0_err,
                              'V0_eos':V0, 'V0_eos_err':V0_err,
                              'B_eos':B, 'B_eos_err': B_err,
                              'BP_eos':BP, 'BP_eos_err':BP_err,
                              'k':k,'element': self.result['element'],
                              'exchange':self.result['exchange'],
                              'structure':self.result['structure'],
                              'code':self.result['code']
                              }

           if get_fit_rms:
              avg_rms = list(filter(lambda a:a!='xxx', list(self.fit_rms_set.values())))
              print ('RMS error of fit for {0} is {1}'.format(rscript,np.mean(avg_rms) ) )


        try:
            run_R_data.to_csv('Rdata.csv',index=False)
            os.system('Rscript {}_nls.R'.format(rscript))
            print ('R executed')
            R_result = pd.read_csv('Result_table.csv')

            #key = list(R_result['Error']).index(min(list(R_result['Error'])))
            self.result['E0'] = list(R_result['Extrapolate'])[0]
            self.result['E0_err'] = list(R_result['Error'])[0]
            self.result['B'] = list(R_result['Extrapolate'])[1] * (1.e24/6.241509125883258e+21)
            self.result['B_err'] = list(R_result['Error'])[1] * (1.e24/6.241509125883258e+21)
            self.result['BP'] = list(R_result['Extrapolate'])[2]
            self.result['BP_err'] = list(R_result['Error'])[2]
            self.result['V0'] = list(R_result['Extrapolate'])[3]
            self.result['V0_err'] = list(R_result['Error'])[3]
            self.result['bE0'] = list(R_result['Extrapolate'])[4]
            self.result['bB'] = list(R_result['Extrapolate'])[5]
            self.result['bBP'] = list(R_result['Extrapolate'])[6]
            self.result['bV0'] = list(R_result['Extrapolate'])[7]
            self.result['nKpoints'] = len(np.unique(run_R_data['kpoints']))
            #print (max(np.unique(run_R_data['kpts'])))
            self.result['maxKpoints'] = max(np.unique(run_R_data['kpoints']))
            print ("R success")
            #nam = '_'.join([NAME, 'maxK',str(self.result['maxKpoints']),'nK',str(self.result['nKpoints'])])
            #if plot_contours:
            #   print ('Here', self.result)
            #   plot_evk = self.plot_contour_evk(coeffs=self.result,fx=fit_data['kpts'],fy=fit_data['volume'], fz=fit_data['energy'],eos=rscript,name=nam)
            #   return plot_evk

        except:
            print ("R failure")
            self.result['E0'] = 'xxx'
            self.result['E0_err'] = 'xxx'
            self.result['B'] = 'xxx'
            self.result['B_err'] = 'xxx'
            self.result['BP'] = 'xxx'
            self.result['BP_err'] = 'xxx'
            self.result['V0'] = 'xxx'
            self.result['V0_err'] = 'xxx'
            self.result['bE0'] = 'xxx'
            self.result['bB'] = 'xxx'
            self.result['bBP'] = 'xxx'
            self.result['bV0'] = 'xxx'
            self.result['nKpoints'] = 'xxx'
            self.result['maxKpoints'] = 'xxx'

        self.records.append(self.result)
        # self for everything is redundant refer all plot parameters simply from pade analysis table
        self.pade_analysis_table =\
             pd.DataFrame({'element': [r['element'] for r in self.records],
                          'structure': [r['structure'] for r in self.records],
                          'exchange': [r['exchange'] for r in self.records],
                          'code': [r['code'] for r in self.records],
                          'E0': [r['E0'] for r in self.records],
                          'E0_err': [r['E0_err'] for r in self.records],
                          'V0': [r['V0'] for r in self.records],
                          'V0_err': [r['V0_err'] for r in self.records],
                          'B': [r['B'] for r in self.records],
                          'B_err': [r['B_err'] for r in self.records],
                          'BP': [r['BP'] for r in self.records],
                          'BP_err': [r['BP_err'] for r in self.records],
                          'bE0': [r['bE0'] for r in self.records],
                          'bB': [r['bB'] for r in self.records],
                          'bBP': [r['bBP'] for r in self.records],
                          'bV0': [r['bV0'] for r in self.records],
                          'nKpts': [r['nKpoints'] for r in self.records],
                          'nKptMax': [r['maxKpoints'] for r in self.records]
                         })

        self.ev_fit_table =\
             pd.DataFrame({'element': [r['element'] for r in self.ev_fit_records],
                          'structure': [r['structure'] for r in self.ev_fit_records],
                          'exchange': [r['exchange'] for r in self.ev_fit_records],
                          'code': [r['code'] for r in self.ev_fit_records],
                          'E0k': [r['E0_eos'] for r in self.ev_fit_records],
                          'E0k_err': [r['E0_eos_err'] for r in self.ev_fit_records],
                          'V0k': [r['V0_eos'] for r in self.ev_fit_records],
                          'V0k_err': [r['V0_eos_err'] for r in self.ev_fit_records],
                          'Bk': [(1.e24/6.241509125883258e+21)*r['B_eos'] for r in self.ev_fit_records],
                          'Bk_err': [(1.e24/6.241509125883258e+21)*r['B_eos_err'] for r in self.ev_fit_records],
                          'BPk': [r['BP_eos'] for r in self.ev_fit_records],
                          'BPk_err': [r['BP_eos_err'] for r in self.ev_fit_records],
                          'k':[r['k'] for r in self.ev_fit_records]
                         })

    def extract_pade_curve(self):
        """
        extracts the pade curve over a continuous range of available
        kpoints to plot a smooth curve
        """
        print ('extracting pade curve')
        #print (self.pade_analysis_table)
        self.pade_frames = []
        for c in np.unique(self.pade_analysis_table['code']):
            code = self.pade_analysis_table[self.pade_analysis_table['code']==c]
            for e in np.unique(code['exchange']):
                exch = code[code['exchange']==e]
                for el in np.unique(exch['element']):
                    elem = exch[exch['element']==el]
                    for st in np.unique(elem['structure']):
                        struct = elem[elem['structure']==st]
                        tags = {'code': str(c),
                            'exchange': str(e),
                            'element': str(el),
                            'structure': str(st)}
                        #print (self.ev_fit_table)
                        coeff = self.create_crossfilts(tags,self.pade_analysis_table)
                        vals = self.create_crossfilts(tags,self.ev_fit_table)
                        kpts = list(vals['k'])
                        try:

                              kpt_space = np.linspace(min(kpts),max(kpts))

                              E0 = float(list(coeff['E0'])[0])
                              V0 = float(list(coeff['V0'])[0])
                              B = float(list(coeff['B'])[0])
                              BP = float(list(coeff['BP'])[0])
                              bE0 = float(list(coeff['bE0'])[0])
                              bV0 = float(list(coeff['bV0'])[0])
                              bB = float(list(coeff['bB'])[0])
                              bBP = float(list(coeff['bBP'])[0])
                              E0_err = float(list(coeff['E0_err'])[0])
                              V0_err = float(list(coeff['V0_err'])[0])
                              B_err = float(list(coeff['B_err'])[0])
                              BP_err = float(list(coeff['BP_err'])[0])

                              self.pade_curve = pd.DataFrame(\
                                        {\
                                       'E0p': [ E0*k/(bE0 + k) for k in kpt_space],\
                                       'V0p': [ V0*k/(bV0 + k) for k in kpt_space],\
                                       'Bp': [ B*k/(bB + k) for k in kpt_space],\
                                       'BPp': [ BP*k/(bBP + k) for k in kpt_space],\
                                       'k': kpt_space,\
                                       'code': [c for k in kpt_space],\
                                       'exchange': [e for k in kpt_space],\
                                       'element': [el for k in kpt_space],\
                                       'structure': [st for k in kpt_space]})

                              #print (self.pade_curve)
                              self.E0p = E0
                              self.V0p = V0
                              self.Bp = B
                              self.BPp = BP

                        except:
                              #logger.warn('precision EXCEPTIONS')

                              self.pade_curve = pd.DataFrame(\
                                        {\
                                       'E0p': [ None for k in kpt_space],\
                                       'V0p': [ None for k in kpt_space],\
                                       'Bp': [ None for k in kpt_space],\
                                       'BPp': [ None for k in kpt_space],\
                                       'k': kpt_space,\
                                       'code': [c for k in kpt_space],\
                                       'exchange': [e for k in kpt_space],\
                                       'element': [el for k in kpt_space],\
                                       'structure': [st for k in kpt_space]})#[st for b in sBPk_err] } )

                        self.pade_frames.append(self.pade_curve)
                                                   #print (self.prec_result)
        self.pade_curve_table = pd.concat(self.pade_frames)


    def create_precisions(self):
        """
        works with create_crossfilts and the Pade analysis table to
        calculate the precisions and returns plottables to do linear regression
        with
        """
        #print (self.ev_fit_table, self.pade_analysis_table)
        print ('calling create precisions')
        #print (self.pade_analysis_table)
        self.frames = []
        for c in np.unique(self.pade_analysis_table['code']):
            code = self.pade_analysis_table[self.pade_analysis_table['code']==c]
            for e in np.unique(code['exchange']):
                exch = code[code['exchange']==e]
                for el in np.unique(exch['element']):
                    elem = exch[exch['element']==el]
                    #print ('at el')
                    for st in np.unique(elem['structure']):
                        struct = elem[elem['structure']==st]
                        tags = {'code': str(c),
                            'exchange': str(e),
                            'element': str(el),
                            'structure': str(st)}
                        #print (self.ev_fit_table)
                        coeff = self.create_crossfilts(tags,self.pade_analysis_table)
                        vals = self.create_crossfilts(tags,self.ev_fit_table)
                        kpts = list(vals['k'])
                        #print (kpts)
                        #print (vals)
                        E0k, sE0k, sE0k_err, V0k, sV0k, sV0k_err, Bk, sBk, sBk_err, BPk, sBPk, sBPk_err =self.pade_precision(coeff,vals,kpts)
                        #Ek, vk, Bk, BPk = self.pade_precision(coeff, vals)

                        if sBPk_err:
                           #print ('LENGTH of precs', len(sE0k),len(sE0k_err),len(sV0k),len(sV0k_err))
                           self.prec_result = pd.DataFrame(\
                                        {\
                                       'E0k': E0k,
                                       'sE0k':sE0k,
                                       'sE0k_err':sE0k_err,
                                       'V0k': V0k,
                                       'sV0k': sV0k,
                                       'sV0k_err':sV0k_err,
                                       'Bk': Bk,
                                       'sBk': sBk,
                                       'sBk_err':sBk_err,
                                       'BPk': BPk,
                                       'sBPk': sBPk,
                                       'sBPk_err': sBPk_err,
                                       'k': kpts,
                                       'code': c,#[c for b in sBPk_err],
                                       'exchange': e,#[e for b in sBPk_err],
                                       'element': el,#[el for b in sBPk_err],
                                       'structure': st})#[st for b in sBPk_err] } )
                           self.frames.append(self.prec_result)
                           #print (self.prec_result)
        self.prec_table = pd.concat(self.frames)

    def plot_contour_evk(self,coeffs,fx,fy,fz,eos,name):
        """
        kpoint volume contour
        """
        #print ('calls')
        n_fx = np.array([float(x) for x in list(fx)]) #kpoints
        n_fy = np.array(list(fy))
        n_fz = np.array(list(fz))
        #print (len(n_fx),len(n_fy),len(n_fz))
        numcols, numrows = 720, 720
        xi = np.logspace(min(np.log10(n_fx)), max(np.log10(n_fx)), numcols)
        pd.DataFrame({'xi':xi}).to_csv('check_me_xi.csv', index=False)
        yi = np.linspace(min(n_fy), max(n_fy), numrows)
        xi, yi = np.meshgrid(xi, yi)

        xi_p = np.logspace(min(np.log10(n_fx)), max(np.log10(n_fx)), 300)
        yi_p = np.linspace(min(n_fy), max(n_fy), 300)
        xi_pm, yi_pm = np.meshgrid(xi_p, yi_p)
        n_fz_p = self.interpolating_func(xi_pm,yi_pm, coeffs, eos)
        #print (np.shape(n_fz_p))

        #print ('makes meshgrid')
        #-- Interpolate at the points in xi, yi
        x,  y,  z,  zp = n_fx,  n_fy,  n_fz,  n_fz_p
        #print ('makes x,y,z s')
        #print ( np.shape( np.transpose(np.array([x,y])) ),np.shape(z),np.shape((xi,yi)))
        #zi = griddata(x,y,z,xi,yi,interp='linear')
        zi = sci_grid((x,y), z,(xi,yi),method='nearest')
        #print ('makes all grids')
        #print (len(xi_p),len(yi_p),len(zp),len(z),len(x),len(y))

        for a,b,cz,n in [(xi,yi,zi,'raw'),(xi_p,yi_p,zp,eos)]:
           #-- Display the results
           fig, ax = plt.subplots()
           lev = np.linspace(min(z), max(z),500)
           #print ('before tricontourf')
           #print (cz)
           #plt.imshow(zi.T, extent=(min(n_fx),max(n_fx),min(n_fy),max(n_fy)), origin='lower')
           im = ax.contourf(a,b,cz,levels=lev,cmap=plt.cm.jet,zorder=-20)
           #print ('finishes contourf')
           #im = ax.contourf(xi_p, yi_p, zp, levels=lev,cmap=plt.cm.jet)
           #im = ax.contourf(xi, yi, zi, levels=lev,cmap=plt.cm.jet)
           for i in im.collections:
              i.set_edgecolor("face")
           ax.scatter(n_fx, n_fy, c=n_fz, s=10, lw=0.8,edgecolor='black',\
           vmin=n_fz.min(), vmax=n_fz.max(),cmap=plt.cm.jet)

           minz= cz.min()
           maxz= cz.max()
           print (minz, maxz, (maxz - minz) * 1000)
           step = (maxz - minz)/4 # no. of equal changes by 4
           zticks = ["{:.3f}".format(minz) +' eV']+['+'+str(int(n*step*1000)) for n in list(range(1,5))]
           ticks=[minz+n*step for n in list(range(0,5))]
           #ticks=[minz+n for n in list(range(0,n_steps))]
           print (ticks,zticks)
           cbar = fig.colorbar(im, ticks=[minz+n*step for n in list(range(0,5))])
           #[minz, minz+step, minz+2*step, minz+3*step, minz+4*step])
           #print (len(cbar.ticks))
           #print (len(cbar))
           cbar.set_ticklabels(zticks)
           cbar.set_label('Calculated DFT Energy')
           #ax.contourf(data,zorder=-20)
           ax.set_rasterization_zorder(-10)
           plt.xscale('log')
           plt.ylim(min(n_fy),max(n_fy))
           plt.xlim(min(n_fx),max(n_fx))
           plt.xlabel('$k-$point density per atom')
           plt.ylabel('Volume per atom in $\AA^3$')
           #print ('past plotting {}'.format('_'.join([n,name])+'.pdf'))
           #plt.title(' '.join([eos,name.replace('.csv','')]))

           return plt

           plt.savefig('Raw_data/'+'_'.join([name,n])+'.pdf')
           plt.savefig('_'.join([name,n])+'.png')
           print ('past plotting {}'.format('_'.join([name,n])+'.pdf'))
           plt.close()
           #fig.close()

    def create_pade_bokeh_compat(self,properties):
        """
        plots an P(k) semi-log plot with error bars
        on the raw data from the EOS fit
        and Pade from the E(V,k) fit

        Returns:
           bokeh plottables
        """
        eos_source = self.ev_fit_table
        x_eos_kpts = list(eos_source['k'])
        y_eos = eos_source['{}k'.format(properties)]
        y_eos_err = eos_source['{}k_err'.format(properties)]

        pade_source = self.pade_curve_table
        x_pade_kpts = list(pade_source['k'])
        y_pade = pade_source['{}p'.format(properties)]

        xs_err = []
        ys_err = []
        for x, y, yerr in zip(x_eos_kpts, y_eos, y_eos_err):
            xs_err.append((x, x))
            ys_err.append((y - yerr, y + yerr))
        return x_eos_kpts, y_eos, xs_err, ys_err, x_pade_kpts, y_pade

    def create_precision_bokeh_compat(self,prop_data,energy_data,properties):
        """
        Returns data for the log-log plot of precision
        """
        dframe = pd.DataFrame({'X':energy_data, 'Y':prop_data})
        dframe.to_csv('Rdata_linear.csv', index=False)
        try:
           os.system('Rscript {}'.format('./regression_linear_model.R'))
        except:
           print (name, 'warnings')

        try:
           params = pd.read_csv('params.csv')
           preds = pd.read_csv('predicts.csv')
           pred_x = preds['x']
           pred_f = preds['f']
        except:
           params = pd.DataFrame( {'C':[np.nan],'M':[np.nan],'C_err':[np.nan],'M_err':[np.nan]} )

        return prop_data, energy_data, params['M'][0], params['C'][0], pred_x, pred_f


    def fit_tls_regression(self, name, X, X_err, Y, Y_err, rscript='regression_linear_model.R'):
        """
        fits total least squares non linear regression with scipy
        """
        def f(B, x):
           '''Linear function y = mx + c'''
           # B is a vector of the parameters.
           # x is an array of the current x values.
           # x is in the same format as the x passed to Data or RealData.
           #
           # Return an array in the same format as y passed to Data or RealData.
           return pow(np.e,B[0]*np.log(x) + B[1])

        dframe = pd.DataFrame({'X':X, 'Y':Y})
        dframe.to_csv('Rdata_linear.csv', index=False)
        try:
           os.system('Rscript {}'.format(rscript))
           params = pd.read_csv('params.csv')
        except:
           print ('something wrong with params')

        loglog = Model(f)
        mydata = RealData(X,Y,sx=X_err,sy=Y_err)
        myodr = ODR(mydata,loglog,beta0=[params['M'][0],params['C'][0]])
        pd.DataFrame({'Name':[name for n in X], 'X':X, 'X_err':X_err, 'Y':Y,'Y_err':Y_err}).to_csv(name+'.csv', index=False)
        plt.scatter(X,Y,c='black')
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('$\sigma_{E0}$')
        plt.ylabel('$\sigma_{P}$')
        #print (type(X_err),type(Y_err))
        # print (X_err)
        plt.errorbar(X,Y,xerr=X_err,yerr=Y_err, linestyle='')
        try:
            output = myodr.run()
            output.pprint()
            plt.plot(X,output.y,color='red')
            print ('Value at 0.1 perc 1 meV convergence is {}'.format(f(output.beta,0.1)))
            print ('successful tls',name)
        except:
            print ('failed tls',name)
        plt.savefig('_'.join(['TLS',name,'.png']))
        plt.close()
        return output.beta


    def fit_linear_regression_power_law(self,name, X,Y,X_err,Y_err,rscript='regression_linear_model.R'):
        """
        fits with R the variable X and Y according to
        the model provided by the script
        """
        #y = [y for y in Y if abs(y)<0.1]
        #n = [num for num,y in enumerate(Y) if abs(y)<0.1]
        #x = [X[num] for num in n]
        #print (len(x), len(y), len(X), len(Y), max(X), max(Y), min(X), min(Y))
        dframe = pd.DataFrame({'X':X, 'Y':Y})
        dframe.to_csv('Rdata_linear.csv', index=False)
        try:
           os.system('Rscript {}'.format(rscript))
        except:
           print (name, 'warnings')

        try:
           params = pd.read_csv('params.csv')
           preds = pd.read_csv('predicts.csv')
           plt.scatter(preds['x'], preds['y'])
           ax = plt.gca()
           ax.set_xscale('log')
           ax.set_yscale('log')
           plt.plot(preds['x'], preds['f'], color='red')
           plt.errorbar(preds['x'],preds['y'],xerr=X_err,yerr=Y_err, linestyle='')
           print ('saving {}'.format(name))
           plt.title(name)
           plt.savefig(name)
           plt.close()

        except:
           params = pd.DataFrame( {'C':[np.nan],'M':[np.nan],'C_err':[np.nan],'M_err':[np.nan]} )

        #logger.info('{0},{1},{2},{3},{4}'.format(name.split('_')[:-2], params['C'][0], params['C_err'][0], params['M'][0], params['M_err'][0]))
        return name, params['C'][0], params['C_err'][0], params['M'][0], params['M_err'][0], preds

    def plot_kpts_precision(self,dataK):
        """
        fig 2.
        """
        markers = {'BP':'D','B':'s','V0':'x','E0':'*'}
        colors = {'BP':'red','B':'blue','V0':'black','E0':'green'}
        labels = {'BP':"$B'$", 'B':"$B$", 'E0': "$E_{0}$", 'V0': "$V_{0}$"}

        for k in ['E0','V0','B','BP']:
           if k != 'name':
             dframe = dataK[k]
             plt.scatter(dframe['K'],dframe['Y'], label=labels[k],marker=markers[k],color=colors[k])
             plt.errorbar(dframe['K'],dframe['Y'],yerr=dframe['Y_err'],label=None, color=colors[k],linestyle='')
             plt.xscale('log')

        plt.xlabel('$k-$points density per atom')
        plt.ylabel("$\sigma_{E_0}$ in 10 meV\n$\sigma_{V_0}$, $\sigma_{B}$,$\sigma_{B'}$ in %")
        plt.ylim(-1.0,1.0)
        #plt.legend()
        print ('saving {}'.format('PrecKpoints_'+dataK['name']+'.pdf'))
        plt.savefig('PrecKpoints_{}_'.format(code)+dataK['name']+'.pdf')
        plt.savefig('PrecKpoints_{}_'.format(code)+dataK['name']+'.png')
        plt.close()


    def plot_linear_together(self,data,rscript='regression_linear_model.R'):
        """
        fit and plot all together
        """
        markers = {'BP':'D','B':'s','V0':'x','E0':'*'}
        colors = {'BP':'red','B':'blue','V0':'black','E0':'green'}
        labels = {'BP':"$B'$", 'B':"$B$", 'E0': "$E_{0}$", 'V0': "$V_{0}$"}

        for k in ['V0','B','BP']:
           if k != 'name':
             fitframe = pd.DataFrame(data[k])
             fitframe.to_csv('Rdata_linear.csv', index=False)

             dframe = data[k]
             print (dframe.keys())
             plt.scatter(dframe['X'],dframe['Y'], label=labels[k], marker=markers[k], color=colors[k])
             #plt.xlim(0.0001,1.0)
             plt.xscale('log')
             #plt.ylim(min(list(dframe['Y'])),10)
             plt.yscale('log')
             plt.xlabel('$\sigma_{E_0}$ in % or 10 meV per atom')
             plt.ylabel("$\sigma_{V_0}$, $\sigma_{B}$, $\sigma_{B'}$ in %")
             #plt.errorbar(list(dframe['X']),list(dframe['Y']),xerr=list(dframe['X_err']),yerr=list(dframe['Y_err']), linestyle='',color=colors[k],label=None)
             try:
               os.system('Rscript {}'.format(rscript))
               preds = pd.read_csv('predicts.csv')
               plt.plot(list(preds['x']), list(preds['f']),color=colors[k],label=None)
             except:
               print (data['name'], 'warnings')

        #plt.legend()
        plt.xlim(1e-06,1e-03)
        print ('saving {}'.format('InterProperty_{}_'.format(code)+data['name']+'.pdf'))
        plt.savefig('InterProperty_{}_'.format(code)+data['name']+'.pdf')
        plt.savefig('InterProperty_{}_'.format(code)+data['name']+'.png')
        plt.close()


    def to_percent(self,y, position):
        # Ignore the passed in position. This has the effect of scaling the default
        # tick locations.
        s = str(100 * y)

        # The percent symbol needs escaping in latex
        #if matplotlib.rcParams['text.usetex'] is True:
        #    return s + r'$\%$'
        #else:
        #    return s + '%'
        return s

    def myPowFunc(self,x,a,b):
        """
        return linear
        """
        return b*(x**a)

    def plot_histograms(self):
        """
        histogram plotter
        """
        print ('PLOTTING histograms')
        codes = 'VASP'
        exchs = 'PBE'
        corrected_plaws = self.plaws
        formatter = FuncFormatter(self.to_percent)

        my_hist_array = np.array([corrected_plaws['V0_M'], corrected_plaws['B_M'], corrected_plaws['BP_M']]).transpose()
        my_weights = np.ones_like(my_hist_array)/float(len(my_hist_array))
        n, bins, patches = plt.hist(my_hist_array,weights=my_weights)

        plt.setp(patches[0], color="black", label='$v_0$')
        plt.setp(patches[1], color="blue", label='$B$')
        plt.setp(patches[2], color="red", label="$B'$")

        plt.title("Sensitivity of Numerical Precision")
        print (max([max(corrected_plaws['V0_M']), max(corrected_plaws['B_M']), max(corrected_plaws['BP_M'])]))
        print (min([min(corrected_plaws['V0_M']), min(corrected_plaws['B_M']), min(corrected_plaws['BP_M'])]))
        plt.xlim(0.0, max([max(corrected_plaws['V0_M']), max(corrected_plaws['B_M']), max(corrected_plaws['BP_M'])]))
        plt.xlabel("Value of Slope $M$ (% per meV/atom)")
        plt.ylabel("% of Elements")
        #plt.legend()
        plt.gca().yaxis.set_major_formatter(formatter)
        plt.savefig('one_weighted_{0}_{1}_slopes.pdf'.format(codes, exchs))
        plt.savefig('one_weighted_{0}_{1}_slopes.png'.format(codes, exchs))
        print ('finished slopes')
        plt.close()
        ## Intercepts

        minx = min([min(corrected_plaws['V0_C']), min(corrected_plaws['B_C']), min(corrected_plaws['BP_C'])])
        maxx = max([max(corrected_plaws['V0_C']), max(corrected_plaws['B_C']), max(corrected_plaws['BP_C'])])

        my_hist_array = np.array([corrected_plaws['V0_C'], corrected_plaws['B_C'], corrected_plaws['BP_C']]).transpose()
        my_weights = np.ones_like(my_hist_array)/float(len(my_hist_array))
        n, bins, patches = plt.hist(my_hist_array,weights=my_weights,bins=np.logspace(np.log10(minx),np.log10(maxx),num=10), rwidth=0.7)


#        n, bins, patches = plt.hist(np.array([corrected_plaws['V0_C'], corrected_plaws['B_C'], corrected_plaws['BP_C']]).transpose())

        plt.setp(patches[0], color="black")
        plt.setp(patches[1], color="blue")
        plt.setp(patches[2], color="red")
        plt.title("Numerical Precision at 1 meV/atom")
        print(minx, maxx)
        #print (labels)
        ax = plt.gca()
        #plt.xlim(int(minx),1.0)
        plt.xlim(minx,70)
        plt.xscale('log')
        plt.xlabel("Value of Intercept $C$ (%)")
        plt.ylabel("% of Elements")
        plt.gca().yaxis.set_major_formatter(formatter)
        #plt.show()
        plt.savefig('one_weighted_{0}_{1}_intercepts.pdf'.format(codes, exchs))
        plt.savefig('one_weighted_{0}_{1}_intercepts.pdf'.format(codes, exchs))
        plt.close()

        for m in [0.01,0.001]:
            meV = m  # percent energy convergence
            E_intercept = m

            V0_x = [self.myPowFunc(E_intercept,corrected_plaws['V0_M'][n],corrected_plaws['V0_C'][n]) for n in corrected_plaws['V0_C'].index]
            B_x = [self.myPowFunc(E_intercept,corrected_plaws['B_M'][n],corrected_plaws['B_C'][n]) for n in corrected_plaws['B_C'].index]
            BP_x = [self.myPowFunc(E_intercept,corrected_plaws['BP_M'][n],corrected_plaws['BP_C'][n]) for n in corrected_plaws['BP_C'].index]

            minx = min([min(V0_x),min(BP_x),min(B_x)])
            maxx = max([max(V0_x), max(B_x), max(BP_x)])

            my_hist_array = np.array([V0_x,B_x,BP_x]).transpose()
            my_weights = np.ones_like(my_hist_array)/float(len(my_hist_array))
            n, bins, patches = plt.hist(my_hist_array,weights=my_weights,bins=np.logspace(np.log10(minx),np.log10(maxx),num=10), rwidth=0.7)

            plt.setp(patches[0], color="black")
            plt.setp(patches[1], color="blue")
            plt.setp(patches[2], color="red")
            plt.title("Numerical Precision at {} meV/atom".format(str(10*meV)))
            #minx = min([min(corrected_plaws['V0_x']), min(corrected_plaws['B_x']), min(corrected_plaws['BP_x'])])
            #maxx = max([max(corrected_plaws['V0_x']), max(corrected_plaws['B_x']), max(corrected_plaws['BP_x'])])
            #print(minx, maxx)

            #print (labels)
            ax = plt.gca()
            plt.xlim(minx,70)

            #plt.xlim(int(minx),1.0)
            #plt.xlim(-8,2)
            plt.xlabel("Value of $\sigma_{V_0}, \sigma_{B_0}, \sigma_{B'}$ (%)")
            plt.ylabel("% of Elements")
            plt.gca().yaxis.set_major_formatter(formatter)
            #plt.show()
            plt.tight_layout()
            print ('use saved {0}_{1}_intercepts_{2}.pdf'.format(codes, exchs, str(10*meV)))
            plt.savefig('one_weighted_{0}_{1}_intercepts_{2}_real.pdf'.format(codes, exchs, str(10*meV)))
            plt.savefig('one_weighted_{0}_{1}_intercepts_{2}_real.png'.format(codes, exchs, str(10*meV)))
            plt.close()


        #n, bins, patches = plt.hist(np.array([np.log10(corrected_plaws['V0_dev']), np.log10(corrected_plaws['B_dev']), np.log10(corrected_plaws['BP_dev'])]).transpose())

        #print (corrected_plaws['V0_dev'], corrected_plaws['B_dev'], corrected_plaws['BP_dev'])
        #plt.setp(patches[0], color="black")
        #plt.setp(patches[1], color="blue")
        #plt.setp(patches[2], color="red")
        #plt.title("Mean Numerical Precision Deviations".format(str(meV)))
        #minx = min([min(corrected_plaws['V0_dev']), min(corrected_plaws['B_dev']), min(corrected_plaws['BP_dev'])])
        #maxx = max([max(corrected_plaws['V0_dev']), max(corrected_plaws['B_dev']), max(corrected_plaws['BP_dev'])])
        #print(minx, maxx)
        #labels  = ['$10^{'+str(s)+'}$' for s in [-4+x for x in range(0,6)]]
        #print (labels)
        #ax = plt.gca()
        #plt.xscale('log')
        #plt.xlim(-4,2)
        #ax.set_xticklabels(labels)
        #plt.xlim(int(minx),1.0)
        #plt.xlim(-8,2)
        #plt.xlabel("Value of $\sigma_{V_0}, \sigma_{B_0}, \sigma_{B'}$ (%)")
        #plt.ylabel("Number of Elements")

        #plt.show()
        #plt.tight_layout()
        #print ('use saved {0}_{1}_deviations.pdf'.format(codes, exchs))
        #plt.savefig('birch_{0}_{1}_deviations.pdf'.format(codes, exchs))
        plt.close()

        print('finished!')


    def inter_property_power_law_analysis(self):
        """
        commands the inter_property power law fits
        """
        BP_fits = { }
        V0_fits = { }
        B_fits = { }

        BP_fits_tls = {}
        V0_fits_tls = {}
        B_fits_tls = {}

        data = {}
        dataK = {}
        ## crossfilts implemented only to deal with VASP PBE now
        for el in np.unique(self.prec_table['element']):
           prec_el = self.prec_table[self.prec_table['element']==el]

           for st in np.unique(prec_el['structure']):
               st_prec_el = prec_el[prec_el['structure']==st]

               E_st_prec_el = st_prec_el['sE0k']  ## VASP
               E_err_st_prec_el = st_prec_el['sE0k_err']
               #print (E_st_prec_el, E_err_st_prec_el)
               V_st_prec_el = st_prec_el['sV0k']
               V_err_st_prec_el = st_prec_el['sV0k_err']
               B_st_prec_el = st_prec_el['sBk']
               B_err_st_prec_el = st_prec_el['sBk_err']
               BP_st_prec_el = st_prec_el['sBPk']
               BP_err_st_prec_el = st_prec_el['sBk_err']

               print (st,el)
               name = '_'.join([st,el])

               data['name'] = name
               dataK['name'] = name
               kpts = st_prec_el['k']

               X = list(abs(E_st_prec_el))
               X_err = list(abs(E_err_st_prec_el))
               print (len(X_err))
               Y = list(abs(BP_st_prec_el))
               Y_non_abs = list(BP_st_prec_el)
               Y_err = list(abs(BP_err_st_prec_el))
               names = '_'.join(['R_BP',name])
               params_powR = self.fit_linear_regression_power_law(names,X,Y,X_err,Y_err)
               #params = self.fit_tls_regression(names, X, X_err, Y, Y_err)

               #dframe = pd.DataFrame({'X':X,'Y':Y})
               #dframe.to_csv(name+'_LDA_BP_fits.csv', index=False)
               BP_fits['_'.join([st,el])]=params_powR
               #BP_fits_tls['_'.join([st,el])]=params

               data['BP'] = {'X':X, 'X_err':X_err, 'Y':Y, 'Y_err':Y_err}

               dataK['E0'] = {'K':kpts,'Y':X,'Y_err':X_err}
               dataK['BP'] = {'K':kpts,'Y':Y_non_abs,'Y_err':Y_err}

               Y = list(abs(V_st_prec_el))
               Y_non_abs = list(V_st_prec_el)
               Y_err = list(abs(V_err_st_prec_el))
               names = '_'.join(['R_V0',name])
               params_powR = self.fit_linear_regression_power_law(names, X,Y,X_err,Y_err)
               #params=self.fit_tls_regression(names, X,X_err,Y,Y_err)

               #dframe = pd.DataFrame({'X':X,'Y':Y})
               #dframe.to_csv(name+'_LDA_V0_fits.csv', index=False)
               V0_fits['_'.join([st,el])]=params_powR
               #V0_fits_tls['_'.join([st,el])]=params

               data['V0'] = {'X':X, 'X_err':X_err, 'Y':Y, 'Y_err': Y_err}
               dataK['V0'] = {'K':kpts,'Y':Y_non_abs,'Y_err':Y_err}

               name = '_'.join([st,el])

               Y = list(abs(B_st_prec_el))
               Y_non_abs = list(B_st_prec_el)
               Y_err = list(abs(B_err_st_prec_el))
               names = '_'.join(['R_B',name])
               params_powR = self.fit_linear_regression_power_law(names,X,Y,X_err,Y_err)
               #params=self.fit_tls_regression(names, X, X_err, Y, Y_err)
               #print (M,C)
               #dframe = pd.DataFrame({'X':X,'Y':Y})
               #dframe.to_csv(name+'_LDA_B_fits.csv', index=False)
               B_fits['_'.join([st,el])]=params_powR
               #B_fits_tls['_'.join([st,el])]=params

               data['B'] = {'X':X, 'X_err':X_err, 'Y':Y, 'Y_err': Y_err}
               dataK['B'] = {'K':kpts,'Y':Y_non_abs,'Y_err':Y_err}

               #self.plot_linear_together(data)
               #self.plot_kpts_precision(dataK)

        B_slope_m = [B_fits[k][3] for k in B_fits.keys()]#[ B_fits[k](1) - B_fits[k](0) for k in B_fits.keys() ]
        B_slope_m_err = [B_fits[k][4] for k in B_fits.keys()]
        #B_slope_eqn = [myLinFunc(B_fits[k][3], B_fits[k][1]) for k in B_fits.keys()]
        B_names = [B_fits[k][0] for k in B_fits.keys()]

        B_tls_slope_m = [B_fits_tls[k][0] for k in B_fits_tls.keys()]

        V0_slope_m = [V0_fits[k][3] for k in V0_fits.keys()] #[ a0_fits[k](1) - a0_fits[k](0) for k in a0_fits.keys() ]
        V0_slope_m_err = [V0_fits[k][4] for k in V0_fits.keys()]
        V0_names = [V0_fits[k][0] for k in V0_fits.keys()]

        V0_tls_slope_m = [V0_fits_tls[k][0] for k in V0_fits_tls.keys()]

        BP_slope_m = [BP_fits[k][3] for k in BP_fits.keys()]#[ BP_fits[k](1) - BP_fits[k](0) for k in BP_fits.keys() ]
        BP_slope_m_err = [BP_fits[k][4] for k in BP_fits.keys()]
        BP_names = [BP_fits[k][0] for k in BP_fits.keys()]

        BP_tls_slope_m = [BP_fits_tls[k][0] for k in BP_fits_tls.keys()]

        meV_intercept = 0.001
        E_intercept = np.log(meV_intercept)

        V0_intercept_c = [V0_fits[k][1] for k in V0_fits.keys()]
        print ('V0 intercepts', V0_intercept_c)
        V0_intercept_c = [V0_fits[k][1] for k in V0_fits.keys()]
        V0_intercept_c_err = [V0_fits[k][2] for k in V0_fits.keys()]
        V0_intercept_x = [self.myPowFunc(E_intercept, V0_fits[k][3], V0_fits[k][1]) for k in V0_fits.keys()]

        V0_tls_intercept_c = [V0_fits_tls[k][1] for k in V0_fits_tls.keys()]

        B_intercept_c = [B_fits[k][1] for k in B_fits.keys()]#[ B_fits[k](0) for k in B_fits.keys() ]
        B_intercept_c_err = [B_fits[k][2] for k in B_fits.keys()]
        B_intercept_x = [self.myPowFunc(E_intercept, B_fits[k][3], B_fits[k][1]) for k in B_fits.keys()]

        B_tls_intercept_c = [B_fits_tls[k][1] for k in B_fits_tls.keys()]

        BP_intercept_c = [BP_fits[k][1] for k in BP_fits.keys()]#[ BP_fts[k](0) for k in BP_fits.keys() ]
        BP_intercept_c_err = [BP_fits[k][2] for k in BP_fits.keys()]
        BP_intercept_x = [self.myPowFunc(E_intercept, BP_fits[k][3],BP_fits[k][1]) for k in BP_fits.keys()]

        BP_tls_intercept_c  = [BP_fits_tls[k][1] for k in BP_fits_tls.keys()]

        limits_compare = [len(B_slope_m), len(BP_slope_m), len(V0_slope_m),len(B_intercept_c),len(V0_intercept_c),
                          len(BP_intercept_c), len(V0_intercept_x),len(B_intercept_x),len(BP_intercept_x)]
        print (limits_compare, min(limits_compare))

        l = min(limits_compare)
        ## saving the data on the slopes and intercepts

        DataSet = {'V0_names': V0_names,#[:l],
                   'V0_M': V0_slope_m,#[:l],
                   'V0_M_err':V0_slope_m_err,#[:l],
                  # 'V0_M_tls':V0_tls_slope_m,#[:l],
                   'V0_C': V0_intercept_c,#[:l],
                   'V0_C_err': V0_intercept_c_err,#[:l],
                   'V0_x': V0_intercept_x,#[:l],
                  # 'V0_C_tls': V0_tls_intercept_c,#[:l],
                   'B_names': B_names,#[:l],
                   'B_M': B_slope_m,#[:l],
                  # 'B_M_tls': B_tls_slope_m,#[:l],
                   'B_M_err': B_slope_m_err,#[:l],
                   'B_C': B_intercept_c,#[:l],
                  # 'B_C_tls': B_tls_intercept_c,#[:l],
                   'B_C_err': B_intercept_c_err,#[:l],
                   'B_x': B_intercept_x,#[:l],
                   'BP_names': BP_names,#[:l],
                   'BP_M': BP_slope_m,#[:l],
                  # 'BP_M_tls': BP_tls_slope_m,#[:l],
                   'BP_M_err': BP_slope_m_err,#[:l],
                   'BP_C': BP_intercept_c[:l],#,
                  # 'BP_C_tls': BP_tls_intercept_c,#[:l],
                   'BP_C_err': BP_intercept_c_err,#[:l],
                   'BP_x': BP_intercept_x}#[:l]}

        #try:
        #  for e in list(B_fits.keys())[:l]:
        #    elem_set = e, V0_fits[e][-1], B_fits[e][-1], BP_fits[e][-1]
        #    plot_all_together(*elem_set)
        #except:
        #  for e in list(BP_fits.keys())[:l]:
        #    elem_set = e, V0_fits[e][-1], B_fits[e][-1], BP_fits[e][-1]
        #    plot_all_together(*elem_set)

        self.plaws = pd.DataFrame(DataSet)
        self.plaws.to_csv('{}_birch_plaws.csv'.format(code), index=False)
        #self.plot_histograms()


if __name__ == '__main__':
    """
    test
    """
    dataSet = DatabaseData()
    #dataSet.support_data = pd.read_csv('FT_data_EOS_numbers_pbe.csv')
    #dataSet.auto_crossfilter_reduced()
    dataSet.run_pade_through_R(rscript='birch', get_inits_ev=True, plot_contours=False,get_fit_rms=False)
    #print (dataSet.incomps)
    #dataSet.pade_analysis_table.to_csv('{}_fit_weighted_birch_pade_table_data.csv'.format(code), index=False)
    dataSet.create_precisions()
    dataSet.prec_table.to_csv('{}_fit_weighted_birch_precision_data_frames.csv'.format(code))
#    dataSet.inter_property_power_law_analysis()
#    print (dataSet.data)
