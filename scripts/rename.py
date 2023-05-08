#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

new_names=[]

# Directory containing the files
path = "./"

# Get a list of files in the directory
files = os.listdir(path)
##
# Filter the files to get only the ones with .a3m extension
a3m_files = sorted([f for f in files if f.endswith(".a3m")])
a3m_files = sorted(a3m_files, key=lambda x: int(x.split(".")[0]))
for a3m_file in a3m_files:
    with open(a3m_file, "r") as f:
        lines=f.readlines()
        second_line =lines[1]
        new_names.append(second_line.split( )[1])

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
            os.rename(os.path.join(path, file), os.path.join(path, new_filename))
            break
