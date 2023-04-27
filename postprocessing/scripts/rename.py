#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

new_names=[
    "FS868_RS17480.fa_pair",
    "FS868_RS17485.fa_pair",
    "FS868_RS17490.fa_pair",
    "FS868_RS17495.fa_pair",
    "FS868_RS17500.fa_pair",
    "FS868_RS17505.fa_pair",
    "FS868_RS17510.fa_pair",
    "FS868_RS17515.fa_pair",
    "FS868_RS17535.fa_pair",
    "FS868_RS17540.fa_pair",
    "FS868_RS17545.fa_pair",
    "FS868_RS17550.fa_pair",
    "FS868_RS17555.fa_pair",
    "FS868_RS17560.fa_pair",
    "FS868_RS17565.fa_pair",
    "FS868_RS17570.fa_pair",
    "FS868_RS17575.fa_pair",
    "FS868_RS17585.fa_pair",
    "FS868_RS17590.fa_pair",
    "FS868_RS17595.fa_pair",
    "FS868_RS17600.fa_pair",
    "FS868_RS17610.fa_pair",
    "FS868_RS17615.fa_pair",
    "FS868_RS17625.fa_pair",
    "FS868_RS17630.fa_pair",
    "FS868_RS17640.fa_pair",
    "FS868_RS17645.fa_pair",
    "FS868_RS17650.fa_pair",
    "FS868_RS17660.fa_pair",
    "FS868_RS17665.fa_pair",
    "FS868_RS17670.fa_pair",
    "FS868_RS17675.fa_pair",
    "FS868_RS17680.fa_pair",
    "FS868_RS17685.fa_pair",
    "FS868_RS17690.fa_pair",
    "FS868_RS17695.fa_pair",
    "FS868_RS17700.fa_pair",
    "FS868_RS27700.fa_pair",
    "FS868_RS27705.fa_pair",
    "FS868_RS28195.fa_pair"
]

# Directory containing the files
directory = "./"

# Get a list of files in the directory
files = os.listdir(directory)

# Filter the files to get only the ones with .a3m extension
a3m_files = sorted([f for f in files if f.endswith(".a3m")])
a3m_files = sorted(a3m_files, key=lambda x: int(x.split(".")[0]))

# Iterate over the a3m files and rename the corresponding files with the new names
name_dict = {}
for a3m_file, new_file in zip(a3m_files, new_names):
    keyword = a3m_file.split(".")[0] + '_'
    name_dict[keyword] = new_file
for file in files:
    # check if file starts with any of the keys in name_dict
    for key in name_dict.keys():
        if file.startswith(key):
            new_filename = file.replace(key, name_dict[key]+'_',1)
            #rename
            os.rename(os.path.join(directory, file), os.path.join(directory, new_filename))
            break
