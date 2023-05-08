#!/usr/bin/env python
"""
Usage:        ./template_auto.py
Author:       Heewhan Shin
Author_email: hshin40@gmail.com
Date:         April 25, 2023
Description:  This script identifies prophages (if any) then produces paired input sequence files for multimer predictions using localcolabfold.
"""

from run import create_mastertable, identify_prophage_region, filter_prey_sequences, combine_pairwise_batch
import subprocess
import glob
import os
import sys
import argparse

## Specify inputs
###########################################################
path            = "./"                  #Working directory
filename        = 'sequence'            #Genomic sequence
prey_size_limit = 400                   #Residue size
bait_name       = 'Bt24'                #Name of integrase
accession_number= 'NZ_NVLR01000020.1'
###########################################################

parser = argparse.ArgumentParser(description='Identify prophages and prepare input sequence files for multimer predictions using localcolabfold')
parser.add_argument('bait_name_given', metavar='bait_name_given', type=str, nargs='?', default=None, help='Name of integrase')
parser.add_argument('accession_number_given', metavar='accession_number_given', type=str, nargs='?', default=None, help='Accession number of the genomic sequence')
args = parser.parse_args()

if args.bait_name_given and args.accession_number_given:
    bait_name = args.bait_name_given
    accession_number = args.accession_number_given
    print(f"Name of integrase: {args.bait_name_given}")
    print(f"Accession number of the genomic sequence: {args.accession_number_given}")
else:
    bait_name = bait_name
    accession_number = accession_number
    print("No arguments provided...")
    print("Using the following inputs found in the script...")
    print(f"Name of integrase: {bait_name}")
    print(f"Accession number of the genomic sequence: {accession_number}")

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
    user_input = input("Regions of prophages identified. Do you want to use the identified range? (y/n): ")
    if user_input.lower() == "y":
        with open(range, 'r') as f:
            filter_start, filter_end= f.readline().strip().split()
            filter_start    = int(filter_start)
            filter_end      = int(filter_end)
            print("Using the identified range from Phaster: %d to %d"%(filter_start, filter_end))
    elif user_input.lower()=="n":
        print("Proceed with manual input of the range.")
        filter_start = int(input("Enter the range start: "))
        filter_end   = int(input("Enter the range end: "))
    else:
        print("Invalid input. Please enter 'y or 'no'.")
        exit(1)
else:
    print("Prophages not identified. Proceed with manual input of the range.")
    filter_start = int(input("Enter the range start: "))
    filter_end   = int(input("Enter the range end: "))

# Filter prey sequences
filter_prey_sequences(path, filename, prey_size_limit, bait_name, filter_start, filter_end)
subprocess.call("mv ./*.fa fa/", shell=True)

combine_pairwise_batch(path, filenames, bait_name)
subprocess.call("mv fa/*.fasta ready/", shell=True)
subprocess.call("echo Preprocessing is complete..\n", shell=True)
subprocess.call("echo Input files saved in ready folder..\n", shell=True)
