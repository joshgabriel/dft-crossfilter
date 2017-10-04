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
    s = str(int(100 * y))

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
    #print ('{0}*{1}^{2}'.format(b,x,a))
    return b*(x**a)

def plot_histograms():
    """
    histogram plotter
    """
    print ('PLOTTING histograms')
    codes = 'VASP'
    exchs = 'LDA'
    corrected_plaws = pd.read_csv('LDA_VASP_birch_plaws.csv')
    formatter = FuncFormatter(to_percent)

    # first collect all the data

    V0_1_0 = corrected_plaws['V0_C']
    V0_0_1 = [myPowFunc(0.01,corrected_plaws['V0_M'][n],corrected_plaws['V0_C'][n]) for n in corrected_plaws['V0_C'].index]
    V0_0_01 = [myPowFunc(0.001,corrected_plaws['V0_M'][n],corrected_plaws['V0_C'][n]) for n in corrected_plaws['V0_C'].index]
    V0_M = corrected_plaws['V0_M']

    B_1_0 = corrected_plaws['B_C']
    B_0_1 = [myPowFunc(0.01,corrected_plaws['B_M'][n],corrected_plaws['B_C'][n]) for n in corrected_plaws['B_C'].index]
    B_0_01 = [myPowFunc(0.001,corrected_plaws['B_M'][n],corrected_plaws['B_C'][n]) for n in corrected_plaws['B_C'].index]
    B_M = corrected_plaws['B_M']

    BP_1_0 = corrected_plaws['BP_C']
    BP_0_1 = [myPowFunc(0.01,corrected_plaws['BP_M'][n],corrected_plaws['BP_C'][n]) for n in corrected_plaws['BP_C'].index]
    BP_0_01 = [myPowFunc(0.001,corrected_plaws['BP_M'][n],corrected_plaws['BP_C'][n]) for n in corrected_plaws['BP_C'].index]
    BP_M = corrected_plaws['BP_M']

    minx = min([min(x) for x in [V0_1_0,V0_0_1,V0_0_01,B_1_0,B_0_1,B_0_01,BP_1_0,BP_0_1,BP_0_01]])
    minx = min(V0_0_01)
    print ([min(x) for x in [V0_1_0,V0_0_1,V0_0_01,B_1_0,B_0_1,B_0_01,BP_1_0,BP_0_1,BP_0_01]])
    maxx = max([max(x) for x in [V0_1_0,V0_0_1,V0_0_01,B_1_0,B_0_1,B_0_01,BP_1_0,BP_0_1,BP_0_01]])
    print (minx, maxx)

    # first plot volume
    my_hist_array = np.array([V0_1_0, V0_0_1, V0_0_01]).transpose()
    my_weights = np.ones_like(my_hist_array)/float(len(my_hist_array))
    n, bins, patches = plt.hist(my_hist_array,weights=my_weights,bins=np.logspace(np.log10(minx),np.log10(maxx),num=20))
    plt.setp(patches[0], color="red", label='1 $meV$')
    plt.setp(patches[1], color="blue", label='0.1 $meV$')
    plt.setp(patches[2], color="black", label="0.01 $meV$")
    plt.xlim(minx,70)
    plt.xscale('log')
    plt.gca().yaxis.set_major_formatter(formatter)
    plt.savefig('VASP_LDA_birch_V0_histograms.pdf')
    plt.close()

    # second plot B
    my_hist_array = np.array([B_1_0, B_0_1, B_0_01]).transpose()
    my_weights = np.ones_like(my_hist_array)/float(len(my_hist_array))
    n, bins, patches = plt.hist(my_hist_array,weights=my_weights,bins=np.logspace(np.log10(minx),np.log10(maxx),num=20))
    plt.setp(patches[0], color="red", label='1 $meV$')
    plt.setp(patches[1], color="blue", label='0.1 $meV$')
    plt.setp(patches[2], color="black", label="0.01 $meV$")
    plt.xlim(minx,70)
    plt.xscale('log')
    plt.gca().yaxis.set_major_formatter(formatter)
    plt.savefig('VASP_LDA_birch_B_histograms.pdf')
    plt.close()

    # third plot BP
    my_hist_array = np.array([BP_1_0, BP_0_1, BP_0_01]).transpose()
    my_weights = np.ones_like(my_hist_array)/float(len(my_hist_array))
    n, bins, patches = plt.hist(my_hist_array,weights=my_weights,bins=np.logspace(np.log10(minx),np.log10(maxx),num=20))
    plt.setp(patches[0], color="red", label='1 $meV$')
    plt.setp(patches[1], color="blue", label='0.1 $meV$')
    plt.setp(patches[2], color="black", label="0.01 $meV$")
    plt.xlim(minx,70)
    plt.xscale('log')
    plt.gca().yaxis.set_major_formatter(formatter)
    plt.savefig('VASP_LDA_birch_BP_histograms.pdf')
    plt.close()

    # plot the slopes now
    minM = min([min(x) for x in [V0_M,B_M,BP_M]])
    maxM = max([max(x) for x in [V0_M,B_M,BP_M]])
    # 0,1 works well usually

    my_hist_array = np.array(V0_M)
    my_weights = np.ones_like(my_hist_array)/float(len(my_hist_array))
    plt.hist(my_hist_array,weights=my_weights,bins=np.linspace(minM,maxM,num=20),color='brown')
    #plt.setp(patches[0], color="brown")
    plt.xlim(minM,maxM)
    plt.gca().yaxis.set_major_formatter(formatter)
    plt.xlabel("Value of Slope $M$ (% per meV/atom)")
    plt.ylabel("% of Elements")
    plt.savefig('VASP_LDA_birch_M_V0_histograms.pdf')
    plt.close()

    my_hist_array = np.array(B_M)
    my_weights = np.ones_like(my_hist_array)/float(len(my_hist_array))
    plt.hist(my_hist_array,weights=my_weights,bins=np.linspace(minM,maxM,num=20),color='brown')
    #plt.setp(patches[0], color="brown")
    plt.xlim(minM,maxM)
    plt.xlabel("Value of Slope $M$ (% per meV/atom)")
    plt.ylabel("% of Elements")
    plt.gca().yaxis.set_major_formatter(formatter)
    plt.savefig('VASP_LDA_birch_M_B_histograms.pdf')
    plt.close()

    my_hist_array = np.array(BP_M)
    my_weights = np.ones_like(my_hist_array)/float(len(my_hist_array))
    n, bins, patches = plt.hist(my_hist_array,weights=my_weights,bins=np.linspace(minM,maxM,num=20),color='brown')
    #plt.setp(patches[0], color="brown")
    plt.xlabel("Value of Slope $M$ (% per meV/atom)")
    plt.ylabel("% of Elements")
    plt.xlim(minM,maxM)
    plt.gca().yaxis.set_major_formatter(formatter)
    plt.savefig('VASP_LDA_birch_M_BP_histograms.pdf')
    plt.close()



if __name__ == '__main__':
    plot_histograms()
