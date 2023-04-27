#!/usr/bin/env python
import sys
import subprocess
import re

#this script is using a urlapi of phaster to identify the region(s) of prophage in the genome
#provide the accession number of genomic sequence
#############################################
                                            #
accession_number = sys.argv[1]          #
                                            #
#############################################

url = f'http://phaster.ca/phaster_api?acc={accession_number}'

# Run wget command and get the stdout output
result = subprocess.run(['wget', '-qO-', url], stdout=subprocess.PIPE)

# Decode the stdout output as a string
output = result.stdout.decode()

# Find all occurrences of the range in the output
keywords = re.findall(r'intact\(\d{1,10}\)|questionable\(\d{1,10}\)|incomplete\(\d{1,10}\)', output)
ranges = re.findall(r'\d{1,10}-\d{1,10}', output)
print('Please copy and paste the identified prophage position into the filter_prey_fasta.py...')
print('Provided accession number is  :' + ' '+accession_number)
if not ranges:
    print("Prophage is not found")
else:
    completeness = ' | '.join([f"{kw} {rg}" for kw, rg in zip(keywords, ranges)])
    print('Completeness and Position are :', completeness)
    filter_start = int(ranges[0].split('-')[0])
    filter_end = int(ranges[-1].split('-')[1])
    with open('range.txt', 'w') as f:
       f.write(str(filter_start) + ' ' + str(filter_end))
