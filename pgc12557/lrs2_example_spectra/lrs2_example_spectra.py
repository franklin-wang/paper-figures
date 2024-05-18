base_dir = '/Users/zfwang2/Documents/Research/bh_group/lrs2_kin/binning_saved/pgc12557/FIDUCIAL/apoly0_mpoly4_bias0.2_gh6_sn59_cut3_miles_cat_0.8555_0.8935_eachbin/binned_spectra_results/bestfit/'

# inner bin, bin 1 of fiducial
inner = ascii.read(base_dir + 'ppxf_bestfit_bias0.2_bin_1_all.txt')
inner_r = 0.25
inner_wave = np.array(inner['col1'])
inner_obsF = np.array(inner['col2'])
inner_flux = np.array(inner['col3'])

# intermediate bin, bin 51 of fiducial
intermediate = ascii.read(base_dir + 'ppxf_bestfit_bias0.2_bin_51_all.txt')
intermediate_r = 1.487
intermediate_wave = np.array(intermediate['col1'])
intermediate_obsF = np.array(intermediate['col2'])
intermediate_flux = np.array(intermediate['col3'])

# outer bin, bin 83 of fiducial
outer = ascii.read(base_dir + 'ppxf_bestfit_bias0.2_bin_83_all.txt')
outer_r = 3.999
outer_wave = np.array(outer['col1'])
outer_obsF = np.array(outer['col2'])
outer_flux = np.array(outer['col3'])

fig, axs = plt.subplots(3, 1, sharex=True)
ax1 = axs[0]
ax1.step(inner_wave, inner_obsF, color = 'k')
ax1.errorbar(inner_wave, inner_flux, c = 'r')
ax1.errorbar(inner_wave, (inner_obsF - inner_flux)+0.77, c = 'green', fmt = 'd', markersize = 0.5)
ax1.text(8450, 1.05, 'r = '+str(inner_r)+'"', fontsize = 14)

ax2 = axs[1]
ax2.step(intermediate_wave, intermediate_obsF, color = 'k')
ax2.errorbar(intermediate_wave, intermediate_flux, c = 'r')
ax2.errorbar(intermediate_wave, (intermediate_obsF - intermediate_flux)+0.77, c = 'green', fmt = 'd', markersize = 0.5)
ax2.text(8450, 1.05, 'r = '+str(intermediate_r)+'"', fontsize = 14)
ax2.set_ylabel(r'Relative Flux (f$_\lambda$)', fontsize = 14)

ax3 = axs[2]
ax3.step(outer_wave, outer_obsF, color = 'k')
ax3.errorbar(outer_wave, outer_flux, c = 'r')
ax3.errorbar(outer_wave, (outer_obsF - outer_flux)+0.77, c = 'green', fmt = 'd', markersize = 0.5)
ax3.text(8450, 1.05, 'r = '+str(outer_r)+'"', fontsize = 14)
ax3.set_xlabel(r'Rest Wavelength (Å)', fontsize = 14)

for ax in axs:
    ax.set_xlim(8420, 8780)
    ax.set_ylim(0.71, 1.13)
    ax.minorticks_on()
    ax.tick_params(axis='both', which='both', direction='in', labelsize = 14)
    ax.tick_params(axis='both', which='major', length=6)
    ax.tick_params(axis='both', which='minor', length=3)
    ax.xaxis.set_ticks_position('both')
    ax.yaxis.set_ticks_position('both')

plt.subplots_adjust(hspace = 0)
fig.set_size_inches(8, 10)
plt.savefig('/Users/zfwang2/Desktop/lrs2_spectra.pdf', bbox_inches = 'tight')
