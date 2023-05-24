#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import requests
import subprocess
import json
from requests import get
from time import sleep

# This script incoporates ESMFold to predict the structure from the protein sequence. Then, uses Foldseek to search for structure-based homologs 
# First Script - Generate PDB from Protein Sequence

url = "https://api.esmatlas.com/foldSequence/v1/pdb/"
if len(sys.argv) > 1:
    protein_sequence = sys.argv[1]
else:
    print("Error: Protein sequence not provided.")
    sys.exit()
print("The number of residues submitted = "+str(len(protein_sequence))+"  ##The structure prediction is limited to <400 residues..\n")
# Define the request headers
headers = {
    "Content-Type": "text/plain"
}

# Define the request body
data = protein_sequence

# Send the POST request to the API
response = requests.post(url, headers=headers, data=data)

# Check the status code of the response
if response.status_code == 200:
    # Print the raw response text
    with open("ESMFold_structure.pdb", "w") as f:
        f.write(response.text)
else:
    print(f"Error: {response.status_code}")
    sys.exit()

# Second Script - Obtain List of Homologs from PDB

foldseek_url = "https://search.foldseek.com/api/ticket"

# Check if PDB file exists
if not os.path.exists("ESMFold_structure.pdb"):
    print("Error: PDB file not found.")
    sys.exit()

# Define the cURL command
curl_command = [
    "curl",
    "-X", "POST",
    "-F", f"q=@ESMFold_structure.pdb",
    "-F", "mode=3diaa",
    "-F", "database[]=afdb50",
    "-F", "database[]=afdb-swissprot",
    "-F", "database[]=afdb-proteome",
    ##"-F", "database[]=cath50",
    ##"-F", "database[]=mgnify_esm30",
    ##"-F", "database[]=pdb100",
    ##"-F", "database[]=gmgcl_id",
    "-F", "taxonomy[]=bacteria",  # Add your taxonomic filter here
    foldseek_url
]

# Execute the cURL command
try:
    output = subprocess.check_output(curl_command, universal_newlines=True)
    print(output)
except subprocess.CalledProcessError as e:
    print(f"Error executing cURL command: {e}")
    sys.exit()

# Parse the output to obtain the ticket ID
ticket = json.loads(output)
if not ticket:
    print("Error: Failed to retrieve the ticket ID.")
    sys.exit()

while True:
    if ticket['status'] == "ERROR":
        print("Job encountered an error.")
        sys.exit(0)
    elif ticket['status'] == "PENDING":
        print("Job is still running. Waiting...")
        sleep(10)
        results_url=f"https://search.foldseek.com/api/result/{ticket['id']}/0"
        results_response=get(results_url)
        try:
            results=results_response.json()
            break
        except json.JSONDecodeError:
            print("Error decoding JSON response:", results_response.text)
            continue
    elif ticket['status'] == "COMPLETE":
        print("Job is completed... Preparing list of hits...")
        results_url = f"https://search.foldseek.com/api/result/{ticket['id']}/0"
        results_response = get(results_url)
        try:
            results = results_response.json()
            break
        except json.JSONDecodeError:
            print("Error decoding JSON response:", results_response.text)
            sys.exit(1)
print(ticket['status'])    
print("Job completed... Preparing the list of hits...")

targets       = []
descriptions  = []
probabilities = []
evalues       = []
taxNames      = []
for result in results['results']:
    db = result['db']
    alignments=result.get('alignments')
    if alignments:
        for alignment in alignments:
            target=alignment['target']
            prob = alignment['prob']
            eval = alignment['eval']
            taxName = alignment['taxName']
            targets.append(target.split('-F1')[0])
            descriptions.append(target.split('v4 ')[1])
            probabilities.append(prob)
            evalues.append(eval)
            taxNames.append(taxName)

# Determine the maximum width for the description column
max_target_width = max(len(target) for target in targets)
max_description_width = max(len(description) for description in descriptions)

# Print the list of targets
print(f"{'Targets':<{max_target_width}} {'Descriptions':<{max_description_width}} {'Prob.':<10} {'E-value':<10} {'Scientific Name':<10}")
for target, description, probability, ev, sciname in zip(targets, descriptions, probabilities, evalues, taxNames):
    print(f"{target:<{max_target_width}} {description:<{max_description_width}} {probability:<10.3f} {ev:<10} {sciname:<10}")
print("-" * (10 + max_description_width + 10))
print("Please copy and paste the link below into a browser for the graphical interface"+'\n')
print(f"https://search.foldseek.com/result/{ticket['id']}/0")
