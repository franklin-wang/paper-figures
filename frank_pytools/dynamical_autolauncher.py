"""
there can be up to 30 launchers for our dynamical modeling codes.
this code creates submit_jobname files that we can run in Grace using
'./submit_jobname' to automatically run all of them without having
to type in 'sbatch launcher_X' manually.  
"""
import numpy as np

job_name = 'orbstart'
launcher_name = 'launcher_p12557_nfwdm_kinpa_mypsf_modeldust_'
num_jobs = 5

grace_dir = '/scratch/user/zfwang2/LP_2016/frank_pgc12557_test/main_nfwdm_kinpa_mypsf_modeldust/'

outdir = '/Users/zfwang2/Desktop/'#'/Users/zfwang2/Desktop/main_nfwdm_kinpa_mypsf_modeldust/'

### no editing needed below here ###
launcher_list = [launcher_name + job_name + str(x) for x in np.arange(0, num_jobs, 1)+1]
cmd_list = ['#!/bin/bash', ' ']
for x in launcher_list:
    cmd_list.append('sbatch ' + grace_dir + x)


with open(outdir + 'submit_' + job_name, 'w') as f:
    for line in cmd_list:
        f.write(f"{line}\n")
