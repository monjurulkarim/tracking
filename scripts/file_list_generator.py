'''
Input: folder directory
output: a text file with files in the input folder
'''
import os
import csv
from natsort import natsorted

folder_dir ='gary_3rd_set/gary_normal'

folder_list = natsorted(os.listdir(folder_dir))
tmp_file = 'gary_3rd_set/gary_normal.txt'



with open(tmp_file, 'a') as f:
    for item in folder_list:
        f.write(item)
        f.write('\n')
