# This code counts the number of files within a finished grid to ensure that everything is present.
# Also helpful for checking Grace and local hard drive to make sure that files copied over okay.
import numpy as np
import os

main_dir = '/Volumes/Frank_HD_1/dynamical_modeling/pgc12557/main_nfwdm_kinpa_mypsf_modeldust/'

#### NO EDITING PAST THIS POINT ###

main_list = os.listdir(main_dir)
print('---')

# count number of b*/ directories (= # of models)
bstar = [x for x in main_list if x[0] == 'b']
print('number of b* directories: %s' %(int(len(bstar))))
print('---')

# count number of files in b*/datfil/ directories (= # of models)
datfil_dir = [main_dir + x + '/' + 'datfil/' for x in bstar]

# count number of files in datfil/
df_filenames = ['begin.dat', 'orblibbox.dat', 'beginbox.dat', 'orblibbox.dat.tmp', 'mass_aper.dat', 'orblibbox.dat_orbclass.out', 
                'mass_qgrid.dat', 'orblibbox.log', 'mass_radmass.dat', 'orbstart.dat', 'orblib.dat', 'orbstart.log', 'orblib.dat.tmp',
                'triaxmass.log', 'orblib.dat_orbclass.out', 'triaxmassbin.log', 'orblib.log']

for x in df_filenames:
    counter = 0
    for y in datfil_dir:
        z = os.listdir(y)
        for i in z:
            if x in i and len(x) == len(i):
                counter += 1
    print('number of ' + x + ' files: ' + str(counter))

print('---')

# count number of files in ml*/
bstar_dir = [main_dir + x + '/' for x in bstar]
mldirs = []
for x in bstar_dir:
    foo = os.listdir(x)
    i = 0
    while i < len(foo):
        if 'ml' in foo[i]:
            mldirs.append(x + foo[i] + '/')
            i += 1
        else:
            i += 1

ml_filenames = ['.in', '.log', '_aphist.out', '_con.out', '_intrinsic_moments.out', '_kinem.out', '_nnls.out', '_orb.out']
for x in ml_filenames:
    counter = 0
    for y in mldirs:
        for z in os.listdir(y):
            if x in z:
                counter += 1
    print('number of *' + x + ' files: ' + str(counter))

print('---')

# count number of fort30 and interpolgrid files
for x in ['fort.30', 'interpolgrid']:
    counter = 0
    for y in bstar_dir:
        if x in os.listdir(y):
            counter += 1
    print('number of ' + x + ' files: ' + str(counter))
