# ipython of pretty printing latex table

from math import floor, log10
import pandas as pd
import yaml 
dataset_table1 = pd.read_csv('LDA_VASP_fit_weighted_birch_pade_table_data.csv')

#dataset_cohesives = yaml.load(open('PBE_isos.yaml'))

#E0_formatted = []
#v0_formatted = []
#B_formatted = []
#dB_formatted = []

E0 = list(dataset_table1['E0'])
E0_err = list(dataset_table1['E0_err'])

v0 = list(dataset_table1['V0'])
v0_err = list(dataset_table1['V0_err'])

B = list(dataset_table1['B'])
B_err = list(dataset_table1['B_err'])

BP = list(dataset_table1['BP'])
BP_err = list(dataset_table1['BP_err'])

precs = [2 for x in E0]

def un2str(x, xe, precision=2):
         """
         pretty print nominal value and uncertainty

         x  - nominal value
         xe - uncertainty
         precision - number of significant digits in uncertainty
         returns shortest string representation of `x +- xe` either as
         x.xx(ee)e+xx
         or as
         xxx.xx(ee)"""

         # base 10 exponents
         x_exp = int(floor(log10(abs(x))))
         xe_exp = int(floor(log10(abs(xe))))
         # uncertainty
         un_exp = xe_exp-precision+1
         un_int = round(xe*10**(-un_exp))

         # nominal value
         no_exp = un_exp
         no_int = round(x*10**(-no_exp))

         # format - nom(unc)exp
         fieldw = x_exp - no_exp
         fmt = '%%.%df' % fieldw
         result1 = (fmt + '(%.0f)e%d') % (no_int*10**(-fieldw), un_int, x_exp)
         # format - nom(unc)
         fieldw = max(0, -no_exp)
         fmt = '%%.%df' % fieldw
         result2 = (fmt + '(%.0f)') % (no_int*10**no_exp, un_int*10**max(0, un_exp))
         # return shortest representation
         if len(result2) <= len(result1):
             return result2
         else:
             return result1

el = list(dataset_table1['element'])
st = list(dataset_table1['structure'])
#for (e,x,xe,prec) in zip(el,E0,E0_err,precs):
#        print (e)
E0_coh = [] 

for n,e in enumerate(el): 
#    if e in list(dataset_cohesives.keys()):
#          E0_coh.append(E0[n])
#    else:
     E0_coh.append(E0[n])

#E0_coh  = [ dataset_cohesives[e] - E0[n] for n,e in enumerate(el)]

#E0_formatted = ['%s' % (un2str(x, xe, prec)) for x, xe,prec in zip(E0_coh,E0_err,precs)]

#v0_formatted = ['%s' % (un2str(x, xe, prec)) for x, xe,prec in zip(v0,v0_err,precs)]

#B_formatted = ['%s' % (un2str(x, xe, prec)) for x, xe,prec in zip(B,B_err,precs)] 

#dB_formatted = ['%s' % (un2str(x, xe, prec)) for x, xe,prec in zip(BP,BP_err,precs)]

new_frame = {'Element': el,
             'Structure':st,
             'E0': ['%s' % (un2str(x, xe, prec)) for x, xe,prec in zip(E0_coh,E0_err,precs)],
             'v0': ['%s' % (un2str(x, xe, prec)) for x, xe,prec in zip(v0,v0_err,precs)],
             'B' : ['%s' % (un2str(x, xe, prec)) for x, xe,prec in zip(B,B_err,precs)],
             'dB': ['%s' % (un2str(x, xe, prec)) for x, xe,prec in zip(BP,BP_err,precs)] }

pd.DataFrame(new_frame).to_csv('Paper2_Table_VASP_LDA.csv', index=False)


#        elif pr=='dB':
#            dB_formatted.append('%s' % (un2str(x, xe, prec)))
#        elif pr=='v0':
#            v0_formatted.append('%s' % (un2str(x, xe, prec)))
#        elif pr=='E0':
#            E0_formatted.append('%s' % (un2str(x, xe, prec)))
