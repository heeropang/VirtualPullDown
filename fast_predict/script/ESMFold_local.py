#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import requests
import subprocess

url = "https://api.esmatlas.com/foldSequence/v1/pdb/"
if len(sys.argv) > 1:
    protein_sequence = sys.argv[1]
else:
    print("Error: Protein sequence not provided.")
    sys.exit()

# Find the path of pymol
pymol_path = os.popen("which pymol").read().strip()

if not pymol_path:
    print("Error: PyMOL is not installed.")
    sys.exit()

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

os.system(f"{pymol_path} ESMFold_structure.pdb")
