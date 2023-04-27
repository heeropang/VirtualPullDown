<!-- What is this for? -->

## Get started with `VirtualPullDown`
This package contains three steps to streamline virtual pulldown experiments using ColabFold: 
1) Preprocessing: preparing input files (paired sequences) in batch for ColabFold
2) Predictions: using ColabFold to predict models of monomer/multimer 
3) Postprocessing: making figures to navigate virtual pull down results

## Install with `pip`

```
git clone https://github.com/heeropang/VirtualPullDown.git

```

<!-- Why it might be a good choice? -->
<!-- Minimal dependency -->
## Preprocessing
preprocessing sequence input files for ColabFold. Genomic sequence retrieved from NCBI will be used to search for prophages and fetch those prophage sequences or user specified regions in the genomic sequence. Then, these sequences are paired with the sequence of interest to be screened for binding partner(s) via ColabFold
## Dependencies

This package needs --['BIO'](https://biopython.org),--['openpyxl'](https://foss.heptapod.net/openpyxl/openpyxl).  

### Import the library

```Python
import run
```
### Search for prophage

The following code snippet search for prophage using --['phaster'](https://phaster.ca/)'s URLAPI with genomic sequence's accession code.  

```Python
from run import identify_prophage_region
import re
import subprocess
import sys
from Bio import SeqIO
from os.path import join
from openpyxl import Workbook
path            = "./"                  #Working directory
filename        = 'sequence'            #Genomic sequence
prey_size_limit = 400                   #Residue size
bait_name       = 'Sa34'                #Name of integrase
accession_number= 'NZ_FJQW01000022.1'
identify_prophage_region(accession_number)
```

### Create a master table to naviagate gene information

The method `create_mastertable` returns a mastertable.xlsx with locus_tag, gene description, gene size, and location information.
The following example shows how to achieve it using create_mastertable.

```Python
# Create a master table ...
from run import create_mastertable 
path            = "./"                  #Working directory
filename        = 'sequence'            #Genomic sequence
prey_size_limit = 400                   #Residue size
bait_name       = 'Sa34'                #Name of integrase
create_mastertable(path, filename, prey_size_limit, bait_name)
```

A master table keeps gene information.

![Master table](./preprocessing/figures/mastertable.png)

### Apply the range of interest 
The method `filter_prey_sequences` applies identified prophage or user-specified range and returns a filtered.xlsx table, gene sequences.
The following example show how to achieve it using filter_prey_sequences

```Python
# Fetch sequences to screen
from run import filter_prey_sequences
path            = "./"                  #Working directory
filename        = 'sequence'            #Genomic sequence
prey_size_limit = 400                   #Residue size
bait_name       = 'Sa34'                #Name of integrase
filter_start    = 36108        
filter_end      = 57723   
filter_prey_sequences(path, filename, prey_size_limit, bait_name, filter_start, filter_end)
```
A filtered table keeps track of which sequences are fetched and skipped.
![Filtered table](./figures/filtered.png)

### Pair sequences to be screened to the sequence of interest
The method `combine_pairwise_batch` returns paired sequences in fasta format (seq1:seq2, seq1:seq3,...,seq1:seqn) to to be used as input files for Alphafold.
The following example show how to achieve it using combine_pairwise_batch

```Python
# Pairing sequences
from run import combine_pairwise_batch
path            = "./"                  #Working directory
filenames       = sorted(glob.glob("./fa/"+"*.fa"))
bait_name       = 'Sa34'                #Name of integrase
combine_pairwise_batch(path, filenames, bait_name)
```

### One step preprocessing using template_auto.py
The following example show how to acheive all the preprocessing steps with template_auto
```Python
#!/usr/bin/env python

from run import create_mastertable, identify_prophage_region, filter_prey_sequences, combine_pairwise_batch
import subprocess
import glob
import os
import sys

## Specify inputs
###########################################################
path            = "./"                  #Working directory
filename        = 'sequence'            #Genomic sequence
prey_size_limit = 400                   #Residue size
bait_name       = 'Sa34'                #Name of integrase
accession_number= 'NZ_FJQW01000022.1'
###########################################################

## Checking prerequisite files
if not os.path.isfile("%s.txt"%(filename)):
    print("Error: please check if the genomic sequence is saved in the directory")
    exit(1)
if not os.path.isfile("%s.fasta"%(bait_name)):
    print("Error: %s.fasta does not exist\n"%(bait_name))
    exit(1)
if not os.path.isfile("%s_bait_truncated.fasta"%(bait_name)):
    print("Error: %s_bait_truncated.fasta does not exist\n"%(bait_name))
    exit(1)

## Fixing the genomic sequence formatting issue if it exists
sed_cmd = "sed -e 's/\[db_xref=[^]]*\] //g' sequence.txt >sequence_check.txt"
subprocess.call(sed_cmd, shell=True)

## Preparing subdirectories
subprocess.call("mkdir fa ready", shell=True)
subprocess.call("rm fa/*", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
subprocess.call("rm ready/*", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
range           = 'range.txt'
filenames       = sorted(glob.glob("./fa/"+"*.fa"))

## create mastertable
create_mastertable(path, filename, prey_size_limit, bait_name)
subprocess.call("echo Searching for prophage using Phaster..\n", shell=True)

## Search prophage
identify_prophage_region(accession_number)

if os.path.isfile(range):
    user_input = input("Prophage file exists. Do you want to use the identified range? (y/n): ")
    if user_input.lower() == "y":
        with open(range, 'r') as f:
            filter_start, filter_end= f.readline().strip().split()
            filter_start    = int(filter_start)
            filter_end      = int(filter_end)
            print("Using identified range from Phaster: %d to %d"%(filter_start, filter_end))
    elif user_input.lower()=="n":
        print("Proceed with manual input of the range.")
        filter_start = int(input("Enter the range start: "))
        filter_end   = int(input("Enter the range end: "))
    else:
        print("Invalid input. Please enter 'y or 'no'.")
        exit(1)
else:
    print("Prophage file does not exist. Proceed with manual input of the range.")
    filter_start = int(input("Enter the range start: "))
    filter_end   = int(input("Enter the range end: "))

# Filter prey sequences
filter_prey_sequences(path, filename, prey_size_limit, bait_name, filter_start, filter_end)
subprocess.call("mv ./*.fa fa/", shell=True)

combine_pairwise_batch(path, filenames, bait_name)
subprocess.call("mv fa/*.fasta ready/", shell=True)
subprocess.call("echo Preprocessing is complete..\n", shell=True)
subprocess.call("echo Input files saved in ready folder..\n", shell=True)
```
if the prophage is not found, then the script will ask the user for manual inputs to specify the range of interest.
![if prophage not found](./preprocessing/figures/manual_input.png)

if the prophage is found via Phaster, then the script will ask the user to proceed with or without manual inputs.
![if prophage found](./preprocessing/figures/yn_input.png)

Applying the prophage range found via Phaster
![Applying the range](./preprocessing/figures/automatic_input.png)


## Sbatch scripts for structure predictions
sbatch scripts for generating MSA and predicted files using localcolabfold
<!-- What is this for? --> 
This is for submitting preprocessed sequence files in batch on slurm to generate multiple sequence alignments (MSA) and structure predictions using ['ColabFold'](https://github.com/sokrypton/ColabFold). 

### Before we start...
['localcolabfold'](https://github.com/YoshitakaMo/localcolabfold) needs to be installed on your local PC. 
(installation guidelines can be found --['here'](https://github.com/YoshitakaMo/localcolabfold)).
We also need ColabFold ['database'](https://colabfold.mmseqs.com/) on your local PC.
Finally, we need to compile GPU supporting ['Jax'](https://github.com/markusschmitt/vmc_jax/blob/master/documentation/readme/compile_jax_on_cluster.md).

### Bash script to make project directories
Preprocessed fasta sequences will be stored in ready directory

```Bash
#!/bin/bash
echo "setting up directories for $1 integrase"
echo "copy and paste the following line for rsync"
echo "rsync -auvz * heewhan@midway3.rcc.uchicago.edu:/beagle3/price/top_search/$1/ready"
mkdir $1 
cd $1
mkdir ready msas predictions log
```
### SBATCH script for generating MSA files
The following script returns MSA (.a3m) files in the msas and log files in the log directory

```Bash
#!/bin/bash
#SBATCH --job-name=msa_search
#SBATCH --account=pi-price
#SBATCH -c 4                                 # Requested cores
#SBATCH --time=42:00:00                    # Runtime in D-HH:MM format
#SBATCH --partition=beagle3                    # Partition to run in
#SBATCH --mem=128GB                           # Requested Memory
#SBATCH -o ./log/search.out                          
#SBATCH -e ./log/search.err                        

module load gcc/10.2.0 cuda/11.2
source ~/.bash_profile

colabfold_search --db-load-mode 0 \
--mmseqs mmseqs \
--use-env 1 \
--use-templates 0 \
--threads 3 \
ready /software/colabfold-data msas
```

### SBATCH script for structure predictions
The following script returns predicted output files in the predictions and log files in the log directory

```Bash
#!/bin/bash
#SBATCH --job-name=Predict
#SBATCH --account=pi-price
#SBATCH --partition=beagle3
#SBATCH --nodes=1
#SBATCH --time=12:00:00
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:2
#SBATCH --constraint=a100
#SBATCH --mem=48G
#SBATCH --output=./log/predict.out
#SBATCH --error=./log/predict.err

#module load alphafold/2.2.0 cuda/11.3
module load cuda/11.5
cd $SLURM_SUBMIT_DIR

echo "GPUs available: $CUDA_VISIBLE_DEVICES"
echo "CPU cores: $SLURM_CPUS_PER_TASK"

nvidia-smi

colabfold_batch --use-gpu-relax --num-recycle 5 --num-models 5 msas predictions
```

<!-- What is this for? -->

## Postprocessing 
postprocessing scripts for Alphafold output files return a scatter plot and figure to help users navigate the result quickly.

<!-- Minimal dependency -->

### Rename output files
a python script to rename output files from Alphafold
```Python
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
  ##rest of the files
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
```

This package needs --['numpy'](https://numpy.org/), --['pillow'](https://pillow.readthedocs.io/en/stable/).
### Concetanate PAE plots

The following code snippet concatenate all PAE plots in the project directory and returns one figure.  

```Python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
from PIL import Image, ImageDraw, ImageFont
import os

def concatenate_images(folder_path, title_font_size=16):
    # Get all PNG files in the directory
    image_files = glob.glob(f'{folder_path}/*.png')

    # Open all images
    images = [Image.open(img) for img in image_files]

    # Get dimensions of the first image
    width, height = images[0].size

    # Create a new image with the same width and the combined height of all images
    result = Image.new('RGB', (width, height * len(images)), color='white')

    # Paste each image into the result image vertically
    for i, img in enumerate(images):
        result.paste(img, (0, i * height))

    # Add a title to each image
    title_font = ImageFont.load_default()
    draw = ImageDraw.Draw(result)
    title_font_size = 24
    for i, img_file in enumerate(image_files):
        label = os.path.basename(img_file)
        label_width, label_height = draw.textsize(label, font=title_font)
        draw.text((0, i * height), label, font=title_font, fill=(0, 0, 0))

    return result

folder_path = './'
result = concatenate_images(folder_path)
result.save('result.png')
```
Concatenated PAEs allow a quick comparison of PAE plots

![PAE figure](./postprocessing/figures/Nm60_pae.png)

### Plot pTM and ipTM values

The method `plot_ptm_iptm` fetches pTM and ipTM values from json files of Alphafold output and use gnuplot to plot the values.

```Python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import subprocess
import numpy as np
import glob

#this script will extract pTM, ipTM from *_seed_000.json files and plot them to compare between files
########################################
bait_name    ='Se37'
title_offset = 2
folder_path  ='.'
f_width      = 12 #figure width
f_height     = 5  #figure height
fontsize     = 10
margin_top   = 10
margin_bot   = 10
margin_left  = 10
margin_right = 11
key_position = 'left'
########################################
ptms=[]
iptms=[]
pae_data=[]
gnu_data=[]
json_files = glob.glob(f'{folder_path}/*_seed_000.json')
for json_file in sorted(json_files):
    with open (json_file) as f:
        data=json.load(f)
        ptms.append(data['ptm'])
        iptms.append(data['iptm'])

for i, p, ip in zip(sorted(json_files), ptms, iptms):
    pae_data.append(\
f"{i.split('.fa_pair_scores_rank')[0][2:]+'_'+i.split('.fa_pair_scores_rank_00')[1][:1]} {p:.2f} {ip:.2f}")

for data in pae_data:
    gnu_data.append(data.replace('_','.'))


# Plot the graph using gnuplot
with open('%s.gp'%(bait_name), 'w') as f:
    # Define the plot settings
    f.write('set term x11"\n')
    f.write('set tmargin %d\n'%(margin_top))
    f.write('set bmargin %d\n'%(margin_bot))
    f.write('set lmargin %d\n'%(margin_left))
    f.write('set rmargin %d\n'%(margin_right))
    f.write('set title "%s alphafold pulldown" font "Helvetica-Bold, 18" offset 0,%d \n'%(bait_name,title_offset))
    f.write('set xlabel "predicted models"\n')
    f.write('set ylabel "pTM and ipTM values"\n')
    f.write('set key %s\n'%(key_position))
    f.write('set xtics rotate by -45\n')
    f.write('set key box lt -1 lw 2\n')
    f.write('set x2tics out\n')
    f.write('set x2tics rotate by 45\n')
    f.write('set grid xtics\n')
    f.write('set grid x2tics\n')
    f.write('set terminal postscript eps enhanced color solid "Helvetica" %d size %d,%d\n'%(fontsize, f_width, f_height))
    f.write('set output "%s.eps"\n'%(bait_name))
    # Plot the data
    f.write('plot "-" u 1:3:4:xticlabels(2) w p pt 7 lc rgb "red" notitle, "-" u 1:3:4:x2ticlabel(2) w p pt 7 lc rgb "red" notitle, "-" u 1:4 w lp pt 7 lc rgb "blue" t "ipTM", "-" u 1:3 w lp pt 7 lc rgb "red" t "pTM" \n')
    
    for i in range(0,len(gnu_data),2):
        f.write('{} {}\n'.format(i+1,gnu_data[i]))
    f.write('e\n')
    for i in range(1,len(gnu_data),2): 
        f.write('{} {}\n'.format(i+1,gnu_data[i]))
    f.write('e\n')
    for i in range(len(gnu_data)):
        f.write('{} {}\n'.format(i+1,gnu_data[i]))
    f.write('e\n')
    for i in range(len(gnu_data)):
        f.write('{} {}\n'.format(i+1,gnu_data[i]))
    f.write('e\n')
# Call gnuplot to create the graph
subprocess.call(['gnuplot', '%s.gp'%(bait_name)])
```
A scatter plot of pTM and ipTM values allows users to quickly identify the predicted complex model in the screening assay. 

![pTM and ipTM plot](./postprocessing/figures/Nm60.png)

