import pandas as pd
import numpy as np

import yaml
import matplotlib.pyplot as plt

def compare_datasets(tag, struct,my_data,reruns_Alex):
    for k in np.unique(my_data[tag]['kpts']):
        if k in reruns_Alex[struct][tag]:
                kpt_examine = my_data[tag][my_data[tag]==k]
                print (tag, struct, k, len(list(kpt_examine['energy'])), kpt_examine.columns)   
                plt.scatter(kpt_examine['volume'],kpt_examine['energy'])
                plt.show()
                plt.close()


if __name__ == '__main__':
   Alex_rerun = yaml.load(open('All_Problems/rerun_data.yaml'))

   # compare hcp's
   my_data_hcp = {e:pd.read_csv('AutoCrossfilts_VASP/{0}_PBE_{1}_VASP.csv'.\
               format(e.split('_')[0],e.split('_')[1])) for e in list(Alex_rerun['hcp'].keys())}

   for t in Alex_rerun['hcp']:
       compare_datasets(t,'hcp',my_data_hcp,Alex_rerun)

   # compare fcc's
   my_data_fcc = {e:pd.read_csv('AutoCrossfilts_VASP/{0}_PBE_{1}_VASP.csv'.\
               format(e.split('_')[0],e.split('_')[1])) for e in list(Alex_rerun['fcc'].keys())}
   for t in Alex_rerun['fcc']:
       compare_datasets(t,'fcc',my_data_fcc,Alex_rerun)

   # compare bcc's
   my_data_bcc = {e:pd.read_csv('AutoCrossfilts_VASP/{0}_PBE_{1}_VASP.csv'.\
               format(e.split('_')[0],e.split('_')[1])) for e in list(Alex_rerun['bcc'].keys())}

   for t in Alex_rerun['bcc']:
       compare_datasets(t,'bcc',my_data_bcc,Alex_rerun)
