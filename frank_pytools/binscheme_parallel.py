"""
Written by Frank Wang and Ben Jameson, July 12 2024
This code should be run with wrapper codes that add the binning directory (NIFS_LP_binning) to $PATH,
in the same way that dir_nifskin_py is added to $PATH.  Also, everything will be output to a single
directory; we are changing the names of the logfiles. 

This code will create:
1). folders titled snXthresY, where X = bin S/N and Y = threshold S/N. 
    These folders should be placed within the binning code directory on Grace (NIFS_LP_binning)
2). a jobs_ppxf file, which should be placed within the binning code directory on Grace (NIFS_LP_binning)
3). a launcher_ppxf file, doesn't matter where this is placed, but I'd put it in the directory with the slurm files.
"""

import numpy as np
import os
import stat

master_wrapper_file = '/Users/zfwang2/Desktop/wrapper_findbinning_pgc12557_ben.py'

# bin S/N and thres_sn you want to test
bin_sn = [40]#[40, 45, 50, 55]
thres_sn = [4, 5] #[6, 7, 8]

# line numbers of the sample_binsn and sample_thressn lines
# in the master wrapper file. count for these two numbers 
# starts at 1.
binsn_lineno = 192#195
thressn_lineno = 193#196
outdir_lineno = 65#67

output_dir = '/Users/zfwang2/Desktop/'

# grace_dir is the directory where your binning code is located
grace_dir = '/scratch/user/zfwang2/ben_test/bin_codes/'

# launcher file parameters. These MUST all be strings, no numbers:
job_name = 'binning_A'
job_time = '10:00:00'
job_ntasks = '20'
job_ntasks_per_node = '20'
job_memory = '7G'
grace_acct_no = '132719841048'

virtual_env_name = 'ppxf_env'

# no need to edit anything below this line #

# open your 'master' wrapper file (your original one)
master = open(master_wrapper_file)
master_lines = master.readlines()

# create list for jobs file:
jobs_list = []

# loop through all bin S/Ns
for y in thres_sn:
    for x in bin_sn:
        # initialize your new file as an empty list
        new_file = []
        i = 0
        # loop through all lines in your 'master' wrapper file
        while i < len(master_lines):
            # making an output directory for the binning scheme
            if i == outdir_lineno-1:
                new_file.append('    outdir_main ='+"'"+grace_dir+'sn'+str(x)+'_thressn'+str(y) + '/' + 'output/'+"'"+'\n')
                i += 1
            # replace the 'sample_binsn' line with your desired bin S/N
            if i == binsn_lineno-1: # index of 'sample_binsn' line, you need to track down what this is.
                new_file.append('sample_binsn = ['+str(x)+']\n')
                i += 1
            # replace the 'sample_thressn' line with your desired S/N threshold
            if i == thressn_lineno-1: # index of 'sample_thressn' line, you need to track down what this is.
                new_file.append('sample_thressn = ['+str(y)+']\n')
                i += 1
            else:
                new_file.append(master_lines[i])
                i += 1

        os.mkdir(output_dir + 'sn' + str(x) + '_thressn'+ str(y))
        os.mkdir(output_dir + 'sn' + str(x) + '_thressn'+ str(y) + '/output')
        new_dir = output_dir + 'sn' + str(x) + '_thressn'+ str(y) +'/'
        # write the new wrapper file with your new bin S/N out.
        with open(new_dir + 'new_wrapper_binsn'+str(x)+'_thressn'+str(y)+'.py', 'w') as f:
            for line in new_file:
                f.write(f"{line}")

        # add execute permissions to wrapper file
        st = os.stat(new_dir + 'new_wrapper_binsn'+str(x)+'_thressn'+str(y)+'.py')
        os.chmod(new_dir + 'new_wrapper_binsn'+str(x)+'_thressn'+str(y)+'.py', st.st_mode | stat.S_IEXEC)
        st = os.stat(new_dir + 'new_wrapper_binsn'+str(x)+'_thressn'+str(y)+'.py')
        os.chmod(new_dir + 'new_wrapper_binsn'+str(x)+'_thressn'+str(y)+'.py', st.st_mode | stat.S_IXOTH)
        st = os.stat(new_dir + 'new_wrapper_binsn'+str(x)+'_thressn'+str(y)+'.py')
        os.chmod(new_dir + 'new_wrapper_binsn'+str(x)+'_thressn'+str(y)+'.py', st.st_mode | stat.S_IXGRP)
        
        # creating command files
        cmdlist = ['#!/bin/bash', 'cd ' + grace_dir + 'sn' + str(x) + '_thressn'+str(y) +'/',
                    'ml purge', 'ml Anaconda3/5.3.0', 'ml intel/2020b', 'source activate ' + virtual_env_name, 'ml',
                    'python ' + 'new_wrapper_binsn'+str(x)+'_thressn'+str(y)+'.py']
        with open(new_dir + 'cmd_sn'+str(x)+'_thressn'+str(y), 'w') as f:
            for line in cmdlist:
                f.write(f"{line}\n")
        
        # change file permissions
        st = os.stat(new_dir + 'cmd_sn'+str(x)+'_thressn'+str(y))
        os.chmod(new_dir + 'cmd_sn'+str(x)+'_thressn'+str(y), st.st_mode | stat.S_IEXEC)
        st = os.stat(new_dir + 'cmd_sn'+str(x)+'_thressn'+str(y))
        os.chmod(new_dir + 'cmd_sn'+str(x)+'_thressn'+str(y), st.st_mode | stat.S_IXOTH)
        st = os.stat(new_dir + 'cmd_sn'+str(x)+'_thressn'+str(y))
        os.chmod(new_dir + 'cmd_sn'+str(x)+'_thressn'+str(y), st.st_mode | stat.S_IXGRP)

        # add command file directory to jobs list
        jobs_list.append(grace_dir + 'sn'+str(x)+'_thressn'+str(y) + '/' + 'cmd_sn'+str(x)+ '_thressn'+str(y))

# write out jobs file and change jobs file permisions
with open(output_dir + 'jobs_ppxf', 'w') as f:
    for line in jobs_list:
        f.write(f"{line}\n")

st = os.stat(output_dir + 'jobs_ppxf')
os.chmod(output_dir + 'jobs_ppxf', st.st_mode | stat.S_IEXEC)
st = os.stat(output_dir + 'jobs_ppxf')
os.chmod(output_dir + 'jobs_ppxf', st.st_mode | stat.S_IXOTH)
st = os.stat(output_dir + 'jobs_ppxf')
os.chmod(output_dir + 'jobs_ppxf', st.st_mode | stat.S_IXGRP)

# creating the launcher file, writing it out, and changing permissions
launch_list = ['#!/bin/bash',
               '',
               '#SBATCH --job-name='+job_name,
               '#SBATCH --time='+job_time,
               '#SBATCH --ntasks='+job_ntasks,
               '#SBATCH --ntasks-per-node='+job_ntasks_per_node,
               '#SBATCH --mem='+job_memory,
               '#SBATCH --output='+job_name+'.o%J',
               '#SBATCH --account='+grace_acct_no,
               '',
               'cd ' + grace_dir,
               'tamulauncher ' + 'jobs_ppxf']

with open(output_dir + 'launcher_ppxf', 'w') as f:
    for line in launch_list:
        f.write(f"{line}\n")

st = os.stat(output_dir + 'launcher_ppxf')
os.chmod(output_dir + 'launcher_ppxf', st.st_mode | stat.S_IEXEC)
st = os.stat(output_dir + 'launcher_ppxf')
os.chmod(output_dir + 'launcher_ppxf', st.st_mode | stat.S_IXOTH)
st = os.stat(output_dir + 'launcher_ppxf')
os.chmod(output_dir + 'launcher_ppxf', st.st_mode | stat.S_IXGRP)
