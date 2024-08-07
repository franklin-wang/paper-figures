import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.io import ascii
import os
import sys
from scipy import ndimage
from astropy.table import Table
from plotbin import display_bins

dir_tools_py = '/Users/zfwang2/documents/research/bh_group/github_repos/NIFS_LP_kinematics/python_tools/'
dir_comp_plot = '/Users/zfwang2/Documents/Research/bh_group/python_notebooks/lrs2/frank_pytools/'
sys.path.append(dir_tools_py)
sys.path.append(dir_comp_plot)

# first function (model_kinematics_binnum) returns a table with:
# 1). Index of X and Y pixels (0,0), (0,1), ...
# 2). X and Y pixel locations, in arcsec. 
# 3). Bin number corresponding to pixel locations.
# This table will have 'bad' pixels (those not included in kinematics) filtered out
# 
# Input:
# bin_dir = Where the input bins_INSTRUMENT.dat file is located. The original version of this file
#           has two lines at the top of it, a comment and the # of bins. Delete those lines first.
# dimX/Y = # of pixels on the X/Y side of the instrument. Can be found in aperture_*.dat file (line 4).
# x/yarc0 = bottom left arcsec value of bottom left pixel. Can be found in aperture_*.dat file (line 1).
# x/yarcdim = size of each dimension in arcsecs. Can be found in aperture_*.dat file (line 2).
#
# Returns: 
# binnum_table = table of 'good' pixels (X, Y locations and bin numbers)
# Xarc = X in arcsec, BEFORE filtering bad pixels (for troubleshooting)
# Yarc = Y in arcsec, BEFORE filtering bad pixels (for troubleshooting)

def model_kinematics_binnum(bin_dir, dimx, dimy, xarc0, yarc0, xarcdim, yarcdim):
    bin_data = open(bin_dir)
    bin_str = bin_data.read()
    cleaned_str = bin_str.replace('\n', '')
    bin_nums = [int(x) for x in cleaned_str.split()]
    
    assert len(bin_nums) == dimx * dimy, "input bins_INSTRUMENT.dat file not cleaned correctly"

    # Setting up table of (X, Y) and their corresponding bin numbers in PIXELS
    # How this works: set up an empty list called nested_bininfo. This will contain a series of lists, formatted by [Xpix, Ypix, Bin number]
    # The bin_nums list provides bin numbers as: [x0y0, x1y0, ... , x(dimx-1)y0, x(dimx)y0, x0y1, x1y1, ... , x(dimx-1)y1, x(dimx)y1, x0y2, ...]
    # So Y will first be set to 0, and then we loop through all Xs. Once we loop through an entire set of Xs, we reset X to 0
    # and add 1 to Y. For every single pixel, we will be adding 1 to a counter: this counter is going through and indexing bin_nums, as each of
    # the elements in that list corresponds to a single pixel.
    nested_bininfo = []
    counter = 0
    Y = 0
    while Y < dimy:
        X = 0
        while X < dimx:
            
            nested_bininfo.append([X, Y, bin_nums[counter]])
            X += 1
            counter += 1
        Y += 1
    
    # now set up arrays for Xpix, Ypix, and bin number:
    pixX = np.array([x[0] for x in nested_bininfo])
    pixY = np.array([y[1] for y in nested_bininfo])
    bins = np.array([bn[2] for bn in nested_bininfo])

    # At this point, we can now go from pixel numbers to arcseconds.
    # First defining the pixel size / dimension:
    xarcD = xarcdim/dimx
    yarcD = yarcdim/dimy

    # Generating two lists of arcseconds, going from X0 -> X(dimx) and Y0 -> Y(dimy)
    Xarclist = np.arange(xarc0, xarc0 + (dimx * xarcD), xarcD)
    Yarclist = np.arange(yarc0, yarc0 + (dimy * yarcD), yarcD)

    # We're going to make something like the bin_num.txt files found after running our binning wrapper code,
    # this requires us two arrays that map to bin numbers. This can be done in a similar way to the (X, Y) in
    # pixels, except we don't need to map it to a bin number this time.
    nested_arc = []
    yidx = 0
    while yidx < len(Yarclist):
        xidx = 0
        while xidx < len(Xarclist):
            nested_arc.append([Xarclist[xidx], Yarclist[yidx]])
            xidx += 1
        yidx += 1
    
    # set up arrays for Xarc, Yarc, the same dimension as Xpix, Ypix
    # also add half a pixel to each X and Y to shift the arcsec position to center,
    # current setup has Xarc and Yarc in bottom left of pixel
    Xarc = np.array([x[0] for x in nested_arc]) + xarcD/2
    Yarc = np.array([y[1] for y in nested_arc]) + yarcD/2

    # Make a table for the coordinates and bin numbers we mapped.
    binnum_table = Table()
    binnum_table['Xpix'] = pixX
    binnum_table['Ypix'] = pixY
    binnum_table['Xarc'] = Xarc
    binnum_table['Yarc'] = Yarc
    binnum_table['bin_num'] = bins

    # the input file has spaxels listed in bin 0 when it is not assigned to a bin. Remvoing those from our final table.
    binnum_table = binnum_table[binnum_table['bin_num'] > 0]

    return binnum_table, Xarc, Yarc

# Plots the model v. observed kinematics.
# Input:
# 1). bin_table: bin_table created by previous code.
# 2). kin_dir: file path to the nn_..._ghX_kinem.out file. First line in these files must be removed.
# 2a). If working with two instruments, make sure to split up this kinem.out file into bins for two instruments.
# 3). gh_num: # of GH moments in the model/observed kinematics.
# 4). size_tuple: (x, y) size that output plot is going to be.
# 5). Rotation of the kinematics. Refer to personal notes.

def model_kinematics_plotting(bin_table, kin_dir, gh_num, size_tuple, PA):
    kin_data = ascii.read(kin_dir)

    model = [np.array(kin_data['col'+str(x)]) for x in np.arange(4, gh_num*3+3, 3)]
    obs = [np.array(kin_data['col'+str(x)]) for x in np.arange(5, gh_num*3+3, 3)]

    gh_names = [r'$V$', r'$\sigma$', r'$h_3$', r'$h_4$', r'$h_5$', r'$h_6$']

    from plotbin import display_bins

    x = np.array(bin_table['Xarc'])
    y = np.array(bin_table['Yarc'])
    bin_num = np.array(bin_table['bin_num']-1) # subtract 1 to match Python indexing

    nrows = 2
    ncols = gh_num

    fig = plt.figure(figsize = size_tuple)
    for i in np.arange(1, gh_num+1, 1):
        ax = plt.subplot(nrows, ncols, i)
        ax.set_title(gh_names[i-1], fontsize = 14)
        if i <= 2:
            ax.set_title(gh_names[i-1] + r' (km s$^{-1}$)', fontsize = 14)
            display_bins.display_bins(x, y, bin_num, obs[i-1], colorbar=True, angle = PA)
        else:
            display_bins.display_bins(x, y, bin_num, obs[i-1], colorbar=True, angle = PA)

        ax.set_xticklabels([])
        if i >= 2:
            ax.set_yticklabels([])
        ax.minorticks_on()
        ax.tick_params(axis='both', which='both', direction='in')
        ax.tick_params(axis='both', which='major', length=3)
        ax.tick_params(axis='both', which='minor', length=1.5)
        ax.xaxis.set_ticks_position('both')
        ax.yaxis.set_ticks_position('both')
        #ax.set_ylabel('y (")')

    for i in np.arange(gh_num+1, (gh_num*2) + 1, 1):
        ax = plt.subplot(nrows, ncols, i)
        display_bins.display_bins(x, y, bin_num, model[i-(gh_num+1)], colorbar=True, angle = PA)

        if i >= gh_num+2:
            ax.set_yticklabels([])
        ax.minorticks_on()
        ax.tick_params(axis='both', which='both', direction='in')
        ax.tick_params(axis='both', which='major', length=3)
        ax.tick_params(axis='both', which='minor', length=1.5)
        ax.xaxis.set_ticks_position('both')
        ax.yaxis.set_ticks_position('both')
    
    fig.text(0.5, -0.01, 'X (")', ha = 'center', fontsize = 14)
    fig.text(-0.01, 0.5, 'Y (")', va = 'center', rotation = 'vertical', fontsize = 14)
    plt.tight_layout()
    return fig, model, obs
