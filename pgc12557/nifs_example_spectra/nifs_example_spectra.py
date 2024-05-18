base_dir = '/Users/zfwang2/Documents/Research/bh_group/nifs_kin/kinematics_saved/pgc12557/grace_kinematics/fiducial/apoly0_mpoly4_bias0.2_gh6_sn44_cut4_wingegnirs_2.2541_2.4198_eachbin/binned_spectra_results/bestfit/'

# inner bin, bin 0 of fiducial
inner = ascii.read(base_dir + 'ppxf_bestfit_bias0.2_bin_0_all.txt')
inner_r = 0.050
inner_wave = np.array(inner['col1'])/10000
inner_obsF = np.array(inner['col2'])
inner_flux = np.array(inner['col3'])

# intermediate bin, bin 25 of fiducial
intermediate = ascii.read(base_dir + 'ppxf_bestfit_bias0.2_bin_25_all.txt')
intermediate_r = 0.512
intermediate_wave = np.array(intermediate['col1'])/10000
intermediate_obsF = np.array(intermediate['col2'])
intermediate_flux = np.array(intermediate['col3'])

# outer bin, bin 35 of fiducial
outer = ascii.read(base_dir + 'ppxf_bestfit_bias0.2_bin_35_all.txt')
outer_r = 1.044
outer_wave = np.array(outer['col1'])/10000
outer_obsF = np.array(outer['col2'])
outer_flux = np.array(outer['col3'])

fig, axs = plt.subplots(3, 1, sharex=True)
ax1 = axs[0]
ax1.step(inner_wave, inner_obsF, color = 'k')
ax1.errorbar(inner_wave, inner_flux, c = 'r')
ax1.errorbar(inner_wave, (inner_obsF - inner_flux)+0.6, c = 'green', fmt = 'd', markersize = 0.5)
ax1.text(2.3500, 1.2, 'r = '+str(inner_r)+'"', fontsize = 14)

ax2 = axs[1]
ax2.step(intermediate_wave, intermediate_obsF, color = 'k')
ax2.errorbar(intermediate_wave, intermediate_flux, c = 'r')
ax2.errorbar(intermediate_wave, (intermediate_obsF - intermediate_flux)+0.6, c = 'green', fmt = 'd', markersize = 0.5)
ax2.text(2.3500, 1.2, 'r = '+str(intermediate_r)+'"', fontsize = 14)
ax2.set_ylabel(r'Relative Flux (f$_\lambda$)', fontsize = 14)

ax3 = axs[2]
ax3.step(outer_wave, outer_obsF, color = 'k')
ax3.errorbar(outer_wave, outer_flux, c = 'r')
ax3.errorbar(outer_wave, (outer_obsF - outer_flux)+0.6, c = 'green', fmt = 'd', markersize = 0.5)
ax3.text(2.3500, 1.2, 'r = '+str(outer_r)+'"', fontsize = 14)
ax3.set_xlabel(r'Rest Wavelength ($\mu$m)', fontsize = 14)

for ax in axs:
    ax.set_xlim(2.2201, 2.3799)
    ax.set_ylim(0.41, 1.39)
    ax.axvspan(2.2550, 2.2745, color = 'k', alpha = 0.1)
    ax.minorticks_on()
    ax.tick_params(axis='both', which='both', direction='in', labelsize = 14)
    ax.tick_params(axis='both', which='major', length=6)
    ax.tick_params(axis='both', which='minor', length=3)
    ax.xaxis.set_ticks_position('both')
    ax.yaxis.set_ticks_position('both')

plt.subplots_adjust(hspace = 0)
fig.set_size_inches(8, 10)
plt.savefig('/Users/zfwang2/Desktop/nifs_spectra.pdf', bbox_inches = 'tight')
