import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

import matplotlib
#print (matplotlib.rcParams.keys())
matplotlib.rcParams['figure.figsize'] = 7.5, 5
matplotlib.rcParams['font.size'] = 16
matplotlib.rcParams['lines.markersize'] = 12
matplotlib.rcParams['font.family'] = 'Times New Roman'

def to_percent(y, position):
    # Ignore the passed in position. This has the effect of scaling the default
    # tick locations.
    s = str(100 * y)

    # The percent symbol needs escaping in latex
    #if matplotlib.rcParams['text.usetex'] is True:
    #    return s + r'$\%$'
    #else:
    #    return s + '%'
    return s

def myPowFunc(x,a,b):
    """
    return linear
    """
    print ('{0}*{1}^{2}'.format(b,x,a))
    return b*(x**a)

def plot_histograms():
    """
    histogram plotter
    """
    print ('PLOTTING histograms')
    codes = 'VASP'
    exchs = 'PBE'
    corrected_plaws = pd.read_csv('VASP_birch_plaws.csv')
    formatter = FuncFormatter(to_percent)

    my_hist_array = np.array([corrected_plaws['V0_M'], corrected_plaws['B_M'], corrected_plaws['BP_M']]).transpose()
    my_weights = np.ones_like(my_hist_array)/float(len(my_hist_array))
    n, bins, patches = plt.hist(my_hist_array,weights=my_weights)

    plt.setp(patches[0], color="black", label='$v_0$')
    plt.setp(patches[1], color="blue", label='$B$')
    plt.setp(patches[2], color="red", label="$B'$")

    plt.title("Sensitivity of Numerical Precision")
    print (max([max(corrected_plaws['V0_M']), max(corrected_plaws['B_M']), max(corrected_plaws['BP_M'])]))
    print (min([min(corrected_plaws['V0_M']), min(corrected_plaws['B_M']), min(corrected_plaws['BP_M'])]))
    plt.xlim(0.0, 1.0)#max([max(corrected_plaws['V0_M']), max(corrected_plaws['B_M']), max(corrected_plaws['BP_M'])]))
    plt.xlabel("Value of Slope $M$ (% per meV/atom)")
    plt.ylabel("% of Elements")
    #plt.legend()
    plt.gca().yaxis.set_major_formatter(formatter)
    plt.savefig('one_weighted_{0}_{1}_slopes.pdf'.format(codes, exchs))
    plt.savefig('one_weighted_{0}_{1}_slopes.png'.format(codes, exchs))
    print ('finished slopes')
    plt.close()
    ## Intercepts

    my_hist_array = np.array([corrected_plaws['V0_C'], corrected_plaws['B_C'], corrected_plaws['BP_C']]).transpose()
    print ([min(corrected_plaws['V0_C']), min(corrected_plaws['B_C']), min(corrected_plaws['BP_C'])])
    min_data = min([min(corrected_plaws['V0_C']), min(corrected_plaws['B_C']), min(corrected_plaws['BP_C'])])
    max_data = max([max(corrected_plaws['V0_C']), max(corrected_plaws['B_C']), max(corrected_plaws['BP_C'])])
    print ([max(corrected_plaws['V0_C']), max(corrected_plaws['B_C']), max(corrected_plaws['BP_C'])])
    print ('Numerical intercepts min {0} max {1}'.format(min_data, max_data))
    my_weights = np.ones_like(my_hist_array)/float(len(my_hist_array))
    n, bins, patches = plt.hist(my_hist_array,weights=my_weights,bins=np.logspace(np.log10(min_data),np.log10(max_data),num=10), rwidth=0.7)


#   n, bins, patches = plt.hist(np.array([corrected_plaws['V0_C'], corrected_plaws['B_C'], corrected_plaws['BP_C']]).transpose())

    plt.setp(patches[0], color="black")
    plt.setp(patches[1], color="blue")
    plt.setp(patches[2], color="red")
    plt.title("Numerical Precision at 1 meV/atom")
    minx = min([min(corrected_plaws['V0_C']), min(corrected_plaws['B_C']), min(corrected_plaws['BP_C'])])
    maxx = max([max(corrected_plaws['V0_C']), max(corrected_plaws['B_C']), max(corrected_plaws['BP_C'])])
    print('Numerical intercepts min {0} max {1}'.format(minx, maxx))
    #labels  = ['$10^{'+str(s)+'}$' for s in [x for x in range(int(np.log10(minx)),int(np.log10(maxx))+1)]]
    #print (labels)
    ax = plt.gca()
    #ax.set_xticklabels(labels)
    plt.xlim(minx,70)
    #plt.xlim(int(np.log10(minx))-1,int(np.log10(maxx))+1)
    plt.xscale('log')
    plt.xlabel("Value of Intercept $C$ (%)")
    plt.ylabel("% of Elements")
    plt.gca().yaxis.set_major_formatter(formatter)
    #plt.show()
    #plt.tight_layout()
    plt.savefig('one_weighted_{0}_{1}_intercepts.pdf'.format(codes, exchs))
    plt.savefig('one_weighted_{0}_{1}_intercepts.png'.format(codes, exchs))
    plt.close()

    print('finished!')
    print ('open one_weighted_{0}_{1}_intercepts.pdf'.format(codes, exchs))

    meV = 0.001  # percent energy convergence
    E_intercept = meV

    V0_x = [myPowFunc(E_intercept,corrected_plaws['V0_M'][n],corrected_plaws['V0_C'][n]) for n in corrected_plaws['V0_C'].index]
    B_x = [myPowFunc(E_intercept,corrected_plaws['B_M'][n],corrected_plaws['B_C'][n]) for n in corrected_plaws['B_C'].index]
    BP_x = [myPowFunc(E_intercept,corrected_plaws['BP_M'][n],corrected_plaws['BP_C'][n]) for n in corrected_plaws['BP_C'].index]

    minx = min([min(V0_x),min(BP_x),min(B_x)])
    maxx = max([max(V0_x), max(B_x), max(BP_x)])
 
    my_hist_array = np.array([V0_x,B_x,BP_x]).transpose()
    my_weights = np.ones_like(my_hist_array)/float(len(my_hist_array))
    n, bins, patches = plt.hist(my_hist_array,weights=my_weights,bins=np.logspace(np.log10(minx),np.log10(maxx),num=10), rwidth=0.7)

    plt.setp(patches[0], color="black")
    plt.setp(patches[1], color="blue")
    plt.setp(patches[2], color="red")
    plt.title("Numerical Precision at {} meV/atom".format(str(10*meV)))
#    minx = min([min(V0_x),min(BP_x),min(B_x)])
#    maxx = max([max(V0_x), max(B_x), max(BP_x)])
    print(minx, maxx)
    #labels  = ['$10^{'+str(s)+'}$' for s in [-6+x for x in range(0,8)]]
    #print (labels)
    ax = plt.gca()
    #plt.xlim(-6,2)
    #ax.set_xticklabels(labels)
    #plt.xlim(int(minx),1.0)
    plt.xlim(minx,70)
    plt.xscale('log')
    plt.xlabel("Value of $\sigma_{V_0}, \sigma_{B_0}, \sigma_{B'}$ (%)")
    plt.ylabel("% of Elements")
    plt.gca().yaxis.set_major_formatter(formatter)
    #plt.show()
    print ('use saved {0}_{1}_intercepts_{2}.pdf'.format(codes, exchs, str(10*meV)))
    plt.savefig('one_weighted_{0}_{1}_intercepts_{2}_real.pdf'.format(codes, exchs, str(10*meV)))
    plt.savefig('one_weighted_{0}_{1}_intercepts_{2}_real.png'.format(codes, exchs, str(10*meV)))
    plt.close()


if __name__ == '__main__':
    plot_histograms()
