# writing a command that can be placed into Grace, and will get info of the jobs you want to look at
# takes in myproject -j [acct no] output on Grace as input (see below on how to format table)
from astropy.io import ascii
import os
import stat
data_dir = '/Users/zfwang2/Desktop/SU_list.txt'
output_dir = '/Users/zfwang2/Desktop/'

# no need to edit from here #

# when typing in myproject -j [acct no] into Grace, you'll get a table that is formatted as:
# ----------------------List of jobs----------------------
# | column 1 | column 2 | column 3 | column 4 | column 5 |
# --------------------------------------------------------
# | datcol 1 | datcol 2 | datcol 3 | datcol 4 | datcol 5 |
# | ........ | ........ | ........ | ........ | ........ |
# --------------------------------------------------------
# | total jobs: X | total usage: Y |
# --------------------------------------------------------
# EVERYTHING but column X and datcolX needs to be deleted, i.e. remove all horizontal dashes.
data = ascii.read(data_dir)
cmd_file = []

# skip the first row, ascii adds the column headers as a row
cmd_file.append('seff ' + str(data['col3'][1]) + ' > run_info.txt')

# for all other rows but the first, we want to use >> instead of > as to not overwrite lines:
for x in data[2:]:
    cmd_file.append('seff ' + str(x['col3']) + ' >> run_info.txt')

# write out and change permissions
with open(output_dir + 'jobinfo_finder', 'w') as f:
    for line in cmd_file:
        f.write(f"{line}\n")

st = os.stat(output_dir + 'jobinfo_finder')
os.chmod(output_dir + 'jobinfo_finder', st.st_mode | stat.S_IEXEC)
st = os.stat(output_dir + 'jobinfo_finder')
os.chmod(output_dir + 'jobinfo_finder', st.st_mode | stat.S_IXOTH)
st = os.stat(output_dir + 'jobinfo_finder')
os.chmod(output_dir + 'jobinfo_finder', st.st_mode | stat.S_IXGRP)

####################################################################

# Formats run_info.txt from code above into a nicer list
from astropy.io import ascii
from astropy.table import Table
import os
import stat
import numpy as np

SUlist_dir = '/Users/zfwang2/Desktop/SU_list2.txt'
runinfo_dir = '/Users/zfwang2/Desktop/run_info.txt' # output from Grace
output_dir = '/Users/zfwang2/Desktop/'

# no need to edit anything from here #
su_data = ascii.read(SUlist_dir)

data_fin = Table()
data_fin['Job_ID'] = ['0']
data_fin['Nodes'] = ['0']
data_fin['Cores'] = ['0']
data_fin['CPU Time'] = ['0']
data_fin['Wall Time'] = ['0']
data_fin['Memory Used'] = ['0']
data_fin['SU Count'] = ['0']

low = np.arange(0, 11*(len(su_data)-1), 11)
high = np.arange(11, 11*(len(su_data))+11, 11)
i = 0
for x in su_data[1:]:
    suct = str(x['col10'])
    block = open(runinfo_dir).readlines()[low[i]:high[i]]
    block_clean = [x.strip('\n') for x in block]

    job_id = block_clean[0][block_clean[0].index(':') + 1:]
    nodes = block_clean[4][block_clean[4].index(':') + 1:]
    cores = block_clean[5][block_clean[5].index(':') + 1:]
    cpu_time = block_clean[6][block_clean[6].index('d:') + 2:]
    wall_time = block_clean[8][block_clean[8].index('e:') +2:]
    
    # sometimes, there's an 'estimated maximum' string in the memory utilized line.
    # getting rid of this
    if '(estimated maximum)' in block_clean[9]:
        mem_used = block_clean[9][block_clean[9].index(':')+1 : len(block_clean[9])-len('(estimated maximum)')]
    else:
        mem_used = block_clean[9][block_clean[9].index(':')+1 : ]
    data_fin.add_row([job_id, nodes, cores, cpu_time, wall_time, mem_used, suct])
    i += 1

data_fin = data_fin[1:]
data_fin.pprint_all()   
