import pandas as pd

orig = pd.read_csv('bcc_bcc_reruns_data.csv')
#print (list(orig['k-point'].index))
orig_vol_list =[[float(o) for o in l.replace('[','').replace(']','').split(',')] for l in list(orig['volume'])]

orig_energy_list =[[float(o) for o in l.replace('[','').replace(']','').split(',')] for l in list(orig['energy'])]

keys = list(orig.columns)
new_frame = {key: [] for key in keys}
keys.remove('energy')
keys.remove('volume')
for n in list(orig['k-point'].index):
   for m,v in enumerate(orig_vol_list[n]):
      new_frame['volume'].append(v)
      new_frame['energy'].append(orig_energy_list[n][m])
      for k in keys:
          new_frame[k].append(orig[k][n])

print ([(k,len(new_frame[k])) for k in list(new_frame.keys())])

print (len(orig_vol_list), len(orig_energy_list))

new_data_frame = pd.DataFrame(new_frame)
new_data_frame.to_csv('fcc_missings.csv', index=False)

