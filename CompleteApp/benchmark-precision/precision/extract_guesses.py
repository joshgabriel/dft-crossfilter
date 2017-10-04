import pandas as pd
from glob import glob
from ase.eos import EquationOfState

eos_name = 'birch'

for f in glob('AutoCrossfilts_VASP/*.csv'):
    dat = pd.read_csv(f)
    dat.dropna(inplace=True)
    #if dat:
    print (f)
    try:
      if max(dat['kpts']) > 100000:
        Eos = EquationOfState(dat['volume'], dat['energy'], eos=eos_name)
        E0, E0_err, V0, V0_err, B, B_err, BP, BP_err,y_pred = Eos.fit()
        pd.DataFrame({'E0':[E0],'V0':[V0],'B':[B],'BP':[BP]}).to_csv('Init_files/{}_Rdata_init.csv'.format(f.replace('.csv','').replace('AutoCrossfilts_VASP/','')), index=False)
    except:
       print ('Issue with {}'.format(f))



