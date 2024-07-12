"""
Plotting a comparison plot for different kinematics runs.

Input the directories of the GALNAME_kinematics.txt files, the number of GH moments,
whether of not MC simulations were done (mc = True or False), and the names of each
kinematics run.
"""

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.io import ascii

def comp_plotter(txtdir_A, txtdir_B, gh_mom_num, mc, set1_name, set2_name):
    setA = ascii.read(txtdir_A)
    setB = ascii.read(txtdir_B)
    if mc == True:
        cols_to_remove = ['col' + str(x) for x in np.arange(6, 6 + (gh_mom_num * 3), 3)]
        setA.remove_columns(cols_to_remove)
        setB.remove_columns(cols_to_remove)

    setA_nested = []
    setB_nested = []
    setA_err = []
    setB_err = []

    i = 7
    no_mc = 6
    if mc == True:
        k = 8
        while i < 7 + (gh_mom_num*3):
            # subtract off median for odd GH moments
            if i in np.arange(7, 7 + gh_mom_num*3, 6):
                setA_nested.append(setA['col' + str(i)] - np.median(setA['col' + str(i)]))
                setB_nested.append(setB['col' + str(i)] - np.median(setB['col' + str(i)]))
            else:
                setA_nested.append(setA['col' + str(i)])
                setB_nested.append(setB['col' + str(i)])
            
            
            setA_err.append(setA['col' + str(k)])
            setB_err.append(setB['col' + str(k)])
            i += 3
            k += 3
    else:
        while no_mc < 6 + gh_mom_num:
            if i in np.arange(6, 6 + gh_mom_num, 2):
                setA_nested.append(setA['col' + str(no_mc)] - np.median(setA['col' + str(no_mc)]))
                setB_nested.append(setB['col' + str(no_mc)] - np.median(setB['col' + str(no_mc)]))
            else:
                setA_nested.append(setA['col' + str(no_mc)])
                setB_nested.append(setB['col' + str(no_mc)])
            no_mc += 1
    
    gh_mom = ['V (km/s)', '$\sigma$ (km/s)', '$h_{3}$', '$h_{4}$', '$h_{5}$', '$h_{6}$', '$h_{7}$', '$h_{8}$', '$h_{9}$', '$h_{10}$',
              '$h_{11}$', '$h_{12}$', '$h_{13}$', '$h_{14}$', '$h_{15}$', '$h_{16}$', '$h_{17}$', '$h_{18}$', '$h_{19}$', '$h_{20}$',
              '$h_{21}$', '$h_{22}$', '$h_{23}$', '$h_{24}$']

    nrows = 2
    ncols = int(gh_mom_num/2)

    j = 0
    r = 0

    fig, axs = plt.subplots(nrows, ncols)

    while r < nrows:
        c = 0
        while c < ncols:
            ax = axs[r, c]
            if mc == True:
                mark, bar, cap = ax.errorbar(setA_nested[j], setB_nested[j], xerr = setA_err[j], yerr = setB_err[j], fmt = '.', c = '#13294b',
                            ecolor = 'k', elinewidth = 0.75, capsize = 1.0)
                
                [b.set_alpha(0.2) for b in bar]
                [c.set_alpha(0.2) for c in cap]
            else:
                ax.errorbar(setA_nested[j], setB_nested[j], fmt = '.', c = '#13294b')

            lims = [np.min([ax.get_xlim(), ax.get_ylim()]),  np.max([ax.get_xlim(), ax.get_ylim()])]
            ax.errorbar(lims, lims, fmt = '--', c='#e84a27', alpha=0.5, zorder=0)
            ax.set_xlim(lims)
            ax.set_ylim(lims)
            ax.set_xlabel(set1_name + ' %s' %gh_mom[j])
            ax.set_ylabel(set2_name + ' %s' %gh_mom[j])

            ax.set_aspect('equal')
            c += 1
            j += 1
        r += 1

    fig.set_size_inches(gh_mom_num*2 + 1, 8)
    plt.tight_layout()
    return fig, axs


#### similar function for special H2 case, plotting code is just not nested twice:
def comp_plotter_h2(txtdir_A, txtdir_B, gh_mom_num, mc, set1_name, set2_name):
    setA = ascii.read(txtdir_A)
    setB = ascii.read(txtdir_B)
    if mc == True:
        cols_to_remove = ['col' + str(x) for x in np.arange(6, 6 + (gh_mom_num * 3), 3)]
        setA.remove_columns(cols_to_remove)
        setB.remove_columns(cols_to_remove)

    setA_nested = []
    setB_nested = []
    setA_err = []
    setB_err = []

    i = 7
    no_mc = 6
    if mc == True:
        k = 8
        while i < 7 + (gh_mom_num*3):
            # subtract off median for odd GH moments
            if i in np.arange(7, 7 + gh_mom_num*3, 6):
                setA_nested.append(setA['col' + str(i)] - np.median(setA['col' + str(i)]))
                setB_nested.append(setB['col' + str(i)] - np.median(setB['col' + str(i)]))
            else:
                setA_nested.append(setA['col' + str(i)])
                setB_nested.append(setB['col' + str(i)])
            
            
            setA_err.append(setA['col' + str(k)])
            setB_err.append(setB['col' + str(k)])
            i += 3
            k += 3
    else:
        while no_mc < 6 + gh_mom_num:
            if i in np.arange(6, 6 + gh_mom_num, 2):
                setA_nested.append(setA['col' + str(no_mc)] - np.median(setA['col' + str(no_mc)]))
                setB_nested.append(setB['col' + str(no_mc)] - np.median(setB['col' + str(no_mc)]))
            else:
                setA_nested.append(setA['col' + str(no_mc)])
                setB_nested.append(setB['col' + str(no_mc)])
            no_mc += 1
    
    gh_mom = ['V (km/s)', '$\sigma$ (km/s)', '$h_{3}$', '$h_{4}$', '$h_{5}$', '$h_{6}$', '$h_{7}$', '$h_{8}$', '$h_{9}$', '$h_{10}$',
              '$h_{11}$', '$h_{12}$', '$h_{13}$', '$h_{14}$', '$h_{15}$', '$h_{16}$', '$h_{17}$', '$h_{18}$', '$h_{19}$', '$h_{20}$',
              '$h_{21}$', '$h_{22}$', '$h_{23}$', '$h_{24}$']

    nrows = 2
    if gh_mom_num == 2:
        ncols = 1
    else:
        ncols = int(gh_mom_num/2)

    j = 0
    r = 0

    fig, axs = plt.subplots(ncols, nrows)

    while r < nrows:
        ax = axs[r]
        if mc == True:
            mark, bar, cap = ax.errorbar(setA_nested[j], setB_nested[j], xerr = setA_err[j], yerr = setB_err[j], fmt = '.', c = '#13294b',
                        ecolor = 'k', elinewidth = 0.75, capsize = 1.0)
            
            [b.set_alpha(0.2) for b in bar]
            [c.set_alpha(0.2) for c in cap]
        else:
            ax.errorbar(setA_nested[j], setB_nested[j], fmt = '.', c = '#13294b')

        lims = [np.min([ax.get_xlim(), ax.get_ylim()]),  np.max([ax.get_xlim(), ax.get_ylim()])]
        ax.errorbar(lims, lims, fmt = '--', c='#e84a27', alpha=0.5, zorder=0)
        ax.set_xlim(lims)
        ax.set_ylim(lims)
        ax.set_xlabel(set1_name + ' %s' %gh_mom[j])
        ax.set_ylabel(set2_name + ' %s' %gh_mom[j])

        ax.set_aspect('equal')

        j += 1
        r += 1

    fig.set_size_inches(8, gh_mom_num*2 + 1)
    plt.tight_layout()
    return fig, axs



# for the case where one .txt file has MC sims, and the other does not
def comp_plotter_MCdiff(txtdir_A, txtdir_B, gh_mom_num, mc, set1_name, set2_name):
    setA = ascii.read(txtdir_A)
    setB = ascii.read(txtdir_B)

    cols_to_remove = ['col' + str(x) for x in np.arange(7, 7 + (gh_mom_num * 3), 3)]
    setA.remove_columns(cols_to_remove)

    setA_nested = []
    setB_nested = []
    setA_err = []
    setB_err = []

    i = 6
    k = 8
    while i < 6 + (gh_mom_num*3):
        # subtract off median for odd GH moments
        if i in np.arange(6, 6 + gh_mom_num*3, 6):
            setA_nested.append(setA['col' + str(i)] - np.median(setA['col' + str(i)]))
        else:
            setA_nested.append(setA['col' + str(i)])
        
        setA_err.append(setA['col' + str(k)])
        i += 3
        k += 3
    
    no_mc = 6
    while no_mc < 6 + gh_mom_num:
        if no_mc in np.arange(6, 6 + gh_mom_num, 2):
            setB_nested.append(setB['col' + str(no_mc)] - np.median(setB['col' + str(no_mc)]))
        else:
            setB_nested.append(setB['col' + str(no_mc)])
        no_mc += 1
    
    gh_mom = ['V (km/s)', '$\sigma$ (km/s)', '$h_{3}$', '$h_{4}$', '$h_{5}$', '$h_{6}$', '$h_{7}$', '$h_{8}$', '$h_{9}$', '$h_{10}$',
              '$h_{11}$', '$h_{12}$', '$h_{13}$', '$h_{14}$', '$h_{15}$', '$h_{16}$', '$h_{17}$', '$h_{18}$', '$h_{19}$', '$h_{20}$',
              '$h_{21}$', '$h_{22}$', '$h_{23}$', '$h_{24}$']

    nrows = 2
    ncols = int(gh_mom_num/2)

    j = 0
    r = 0

    fig, axs = plt.subplots(nrows, ncols)

    while r < nrows:
        c = 0
        while c < ncols:
            ax = axs[r, c]
            if mc == True:
                mark, bar, cap = ax.errorbar(setA_nested[j], setB_nested[j], fmt = '.', c = '#13294b',
                            ecolor = 'k', elinewidth = 0.75, capsize = 1.0)
                
                [b.set_alpha(0.2) for b in bar]
                [c.set_alpha(0.2) for c in cap]
            else:
                ax.errorbar(setA_nested[j], setB_nested[j], fmt = '.', c = '#13294b')

            lims = [np.min([ax.get_xlim(), ax.get_ylim()]),  np.max([ax.get_xlim(), ax.get_ylim()])]
            ax.errorbar(lims, lims, fmt = '--', c='#e84a27', alpha=0.5, zorder=0)
            ax.set_xlim(lims)
            ax.set_ylim(lims)
            ax.set_xlabel(set1_name + ' %s' %gh_mom[j])
            ax.set_ylabel(set2_name + ' %s' %gh_mom[j])

            ax.set_aspect('equal')
            c += 1
            j += 1
        r += 1

    fig.set_size_inches(gh_mom_num*2 + 1, 8)
    plt.tight_layout()
    return fig, axs, setA_nested, setB_nested