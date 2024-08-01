"""
A few files cannot be tarred from Grace because they have been corrupted while being tarred in the past.
These files are all in b*/datfil/, they are *.orbclass.out and orblib*.dat. As such, these need to be 
moved over to the external hard drive manually. 

We found that scp doesn't work: eveything copies over, but directory structure isn't preserved. Each file
is deleted by the next one that comes in, since they all have the same names.  
An alternative workaround is using rsync -R [user]@grace.tamu.edu:/scratch/.../*orbclass.out local_dir,
which copies everything over while preserving directory structure (i.e. *orbclass.out files are kept in
separate directories, so they don't overwrite each other).

This code takes the 'rysnc' directory (directory copied from Grace w/ correct directory structure) and
copies it over to the external hard drive. 
"""
import numpy as np
import os
import shutil

rsync_dir = '/Users/zfwang2/Desktop/scratch/user/zfwang2/LP_2016/frank_pgc12557_test/main_nfwdm_kinpa_mypsf_modeldust/'
main_dir = '/Volumes/Frank_HD_1/dynamical_modeling/pgc12557/main_nfwdm_kinpa_mypsf_modeldust/'

# no editing past this point #

rsync_datfil = [rsync_dir + x + '/' + 'datfil/' for x in os.listdir(rsync_dir)]
rsync_all = []
for rd in rsync_datfil:
    df = os.listdir(rd)
    for fn in df:
        rsync_all.append(rd + fn)

i = 0
for y in rsync_all:
    src = y
    des = main_dir + y[len(rsync_dir):] 
    shutil.copyfile(src, des)
    print(str(i) + "out of " + str(len(rsync_all)) + " files copied.")
    i += 1
