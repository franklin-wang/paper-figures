"""
Once the grid is on the external hard drive, we should copy over some of the essential files from
the external hard drive to your personal laptop so we're not doing the corner plot stuff on the HD.
The following files from the external HD need to be copied to local:

(within the grid directory)
- infil/
- template/
- griddata/
- log/
- b*/ml*/ 
- b*/infil

When copying b*/... (the last two), we see same issue that forced us to use rsync when copying over
the files from Grace - directory structure is not preserved. Strangley, rsync -R does not work here,
I received a 'skipped directory' message when I tried, and nothing was copied.

As such, this code:
    1. Creates directory structures (b*/ml* and b*/infil) on local laptop.
    2. Copies files from HD to local laptop.
"""

import os
import shutil

src_dir = '/Volumes/Frank_HD_1/dynamical_modeling/pgc12557/main_nfwdm_kinpa_mypsf_modeldust/'
dest_dir = '/Users/zfwang2/Documents/Research/bh_group/schwarzschild_model/output/hello_world_200/'

### no need to edit from here ###

# creating directory structure in output directory #
bstar_dir = [src_dir + x for x in os.listdir(src_dir) if x[0] == 'b']
mlstar_dirs = []
for x in bstar_dir:
    y = os.listdir(x)
    for z in y:
        if z[:2] == 'ml':
            mlstar_dirs.append(x + '/' + str(z))

mlstar_dirs_clean = [x[len(src_dir):] + '/' for x in mlstar_dirs]
for i in mlstar_dirs_clean:
    if os.path.exists(dest_dir + i) == False:
        os.makedirs(dest_dir + i)

# copy files from hard drive to destination #
for x in mlstar_dirs_clean:
    y = os.listdir(src_dir + x)
    for z in y:
        shutil.copyfile(src_dir + x + '/' + z, dest_dir + x + '/' + z)


# same thing but for infil/ files
bstar_dir_dest = [dest_dir + x[len(src_dir):] + '/' for x in bstar_dir]
for x in bstar_dir_dest:
    if os.path.exists(x + 'infil/') == False:
        os.makedirs(x + 'infil/')

i = 0
while i < len(bstar_dir):
    src = bstar_dir[i] + '/infil/'
    dst = bstar_dir_dest[i] + 'infil/'
    y = os.listdir(src)
    for z in y:
        shutil.copyfile(src + z, dst + z)
    i += 1