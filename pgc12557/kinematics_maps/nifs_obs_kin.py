kin_data = ascii.read('/Users/zfwang2/Desktop/kin_data_nifspt.dat')
bin_info = ascii.read('/Users/zfwang2/Desktop/voronoi_2d_binning_bininfo_nifs.txt')

velocity = np.array(kin_data['col2'])
sigma = np.array(kin_data['col4'])
h3 = np.array(kin_data['col7'])
h4 = np.array(kin_data['col9'])
h5 = np.array(kin_data['col11'])
h6 = np.array(kin_data['col13'])
gh_nested = [velocity, sigma, h3, h4, h5, h6]
gh_names = [r'$V$', r'$\sigma$', r'$h_3$', r'$h_4$', r'$h_5$', r'$h_6$']

from plotbin import display_bins

bin_num = ascii.read('/Users/zfwang2/Desktop/voronoi_2d_binning_binnum_nifs.txt')
x = np.array(bin_num['col1'])
y = np.array(bin_num['col2'])
bin_num = np.array(bin_num['col3']-1) # subtract 1 to match Python indexing

nrows = 2
ncols = 3
fig = plt.figure(figsize = (8.5,5))
for i in np.arange(1, 7, 1):
    ax = plt.subplot(nrows, ncols, i)
    ax.set_title(gh_names[i-1])
    if i <= 2:
        ax.set_title(gh_names[i-1] + r' (km s$^{-1}$)')
        display_bins.display_bins(x, y, bin_num, gh_nested[i-1], colorbar=True, cmap = 'Spectral_r')
    else:
        display_bins.display_bins(x, y, bin_num, gh_nested[i-1], colorbar=True, cmap = 'Spectral_r')

    ax.minorticks_on()
    ax.tick_params(axis='both', which='both', direction='in')
    ax.tick_params(axis='both', which='major', length=3)
    ax.tick_params(axis='both', which='minor', length=1.5)
    ax.xaxis.set_ticks_position('both')
    ax.yaxis.set_ticks_position('both')
    ax.set_xlabel('x (")')
    ax.set_ylabel('y (")')

plt.tight_layout()
plt.savefig('/Users/zfwang2/Desktop/obs_kin.pdf')
