# ESMFold_local.py for efficient sequence truncation
<!-- What is this for? -->
Protein structure prediction has become a crucial preliminary step in structural biology, as it may provide insights into the functional mechanisms and interactions of proteins. Conventionally, we rely on homology search, sequence alignment, or secondary structure predictions to identify the region of interest for studying domain-wise structures. However, these methods can be time-consuming and may not always yield accurate results. ESMFold_local provides an efficient way to identify those regions within seconds, thereby accelerating the progress in drug discovery and related fields.

**ESMFold** is a deep neural network-based method for predicting protein structure from the amino acid sequence. It offers significant speed improvements, up to 60x faster than the current state-of-the-art structural prediction method. This makes it ideal for users who need to quickly decide where to truncate the protein sequence for domain-wise analysis and to speed up computation.

The `ESMFold_local` script uses the [ESMFold](https://colab.research.google.com/github/sokrypton/ColabFold/blob/main/ESMFold.ipynb) method to quickly generate predicted protein structure, but without having to install ESMFold and download param files. With this script, users can input a protein sequence of interest to predict its structure and make decisions on truncating the sequence based on the predicted model. The script generates a truncated fasta sequence that can be used for `VirtualPullDown`. 

-----------------------------
## Usage
The script prompts the user to input an amino acid sequence, which is limited to < 400 residues, and then predicts its structure. The predicted structure is displayed in PyMol, allowing the user to determine the region to truncate. Once PyMol is closed, the user can input the unique protein sequence of the region to be truncated, which should be at least 4 residues long or longer if needed. The user can also choose to truncate either the N-terminus or C-terminus of the specified region.

Here are the two ways you can run the script...
```
./ESMFold_local.py #The script will ask for the name of fasta and the protein sequence (see below for example)
or
./ESMFold_local.py Bt24 KEWYINYKADFEKHKQDDKLKETQVIQMNEAALRKLEKELVDVQKQKN... 
```
Then, the script will utilize PyMol to visualize the predicted structure...
```
Opening pymol to visualize the predicted structure...
Please identify the protein sequence of the region you wish to truncate...
```
![example](./example/pymol_example.png)

Once the protein sequence of the region to truncate is decided, then close PyMol and type the unique squence into the prompt...
The script will search the pattern and specify the first occurence to be the region to truncate.
The user can choose from either N-terminal or C-terminal from the region to keep.
```
Please enter the unique protein sequence of the region (4-5 residues) you wish to truncate i.e. DEFQ:HKQD
Found pattern 'HKQD' in Bt24 at positions 14-17
Do you want to keep N-terminal or C-terminal part from the motif? (n or c): c
```
The script will keep the C-terminal part starting with the motif and return the bait_truncated.fasta used for VirtualPulldown 
```
>Bt24
HKQDDKLKETQVIQMNEAALRKLEKELVDVQKQKN
```
<details>
   <summary> :rocket: Click here for the python script </summary>
   
   ```Python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import requests
import subprocess
from run import pdb_to_fasta
from Bio import SeqIO
import re
import argparse

#######################################
path        ='./'
bait_name   ='Bt24'
#######################################
pdb_file    =f"{bait_name}.pdb"
output_name =bait_name

parser = argparse.ArgumentParser(description='Predict protein structure based on the amino acid sequence provided using ESMFold')
parser.add_argument('bait_name_given', metavar='bait_name_given', type=str, nargs='?', default=None, help='Name of fasta')
parser.add_argument('sequence_given', metavar='sequence_given', type=str, nargs='?', default=None, help='Protein Sequence')
args = parser.parse_args()

url = "https://api.esmatlas.com/foldSequence/v1/pdb/"

if args.bait_name_given and args.sequence_given:
    bait_name = args.bait_name_given
    protein_sequence=args.sequence_given
    print(f"Name of integrase: {args.bait_name_given}")
    print(f"Protein sequence:{args.sequence_given}")
elif not args.bait_name_given and not args.sequence_given:
    bait_name= input("Please enter the name of fasta: ")
    protein_sequence=input("Please enter the protein sequence: ") 
elif len(str(args.bait_name_given))>=10:
    user_input=input("is this the name of fasta? (y or n) ")
    if user_input.lower() == "y":
        print("Please provide the protein sequence.")
        protein_sequence= input("Please enter the protein sequence: ")
    elif user_input.lower()=="n":
        bait_name= input("Please enter the name of fasta: ")
        protein_sequence=args.bait_name_given
        print(f"Using the file name {bait_name} and the protein sequence provided")
elif len(str(args.bait_name_given))<=10:
    user_input=input("is this the name of fasta? (y or n) ")
    if user_input.lower() == "y":
        print("Please provide the protein sequence.")
        protein_sequence= input("Please enter the protein sequence: ")
    elif user_input.lower()=="n":
        bait_name= input("Please enter the name of fasta: ")
        protein_sequence=args.bait_name_given
        print(f"Using the file name {bait_name} and the protein sequence provided")
else:
    bait_name = bait_name
    print("Error: Protein sequence not provided.")
    protein_sequence= input("Please enter the protein sequence: ")
    if not protein_sequence:
        print("Error: Protein sequence not provided.")
        sys.exit()
print("The number of sequence submitted= "+str(len(protein_sequence))+"  ##The structure prediction is limited to <400 residues..")
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
    with open(f"{pdb_file}", "w") as f:
        f.write(response.text)
    pdb_to_fasta(path, pdb_file, output_name)
    subprocess.call("echo Opening pymol to visualize the predicted structure... \n", shell=True)
    subprocess.call("echo Please identify the protein sequence of the region you wish to truncate... \n", shell=True)
    os.system(f"{pymol_path} -p {pdb_file}")
    seq_to_cut=input("Please enter an unique sequence pattern of the region (4-5 residues; longer if necessary) to truncate i.e. DEFQ:")
else:
    print(f"Error: {response.status_code}")
    sys.exit()

# Open the FASTA file
fasta_file = f"{output_name}.fasta"
for record in SeqIO.parse(fasta_file, "fasta"):
    # Search for a pattern using a regular expression
    pattern = seq_to_cut
    match = re.search(pattern, str(record.seq))
    if match:
        # Get the start and end positions of the match
        start_pos = match.start() + 1  # Add 1 to convert from 0-based to 1-based numbering
        end_pos = match.end()
        # Do something with the start and end positions
        print(f"Found pattern '{pattern}' in {record.id} at positions {start_pos}-{end_pos}") 
    else:
        print(f"Error: Pattern not found. Please check the sequence again...\n")
        exit(1)
ques=input("Do you want to keep N-terminal or C-terminal part from the motif? (n or c): ")
if ques.lower()=='n':
    with open (fasta_file) as f:
        data=f.readlines()
    for i in range (0, len(data), 2):
        seq_id=data[i].strip()
        seq = data[i+1].strip()
        pattern_pos=re.search(pattern, seq)
        if pattern_pos:
            truncated_seq=seq[:pattern_pos.start()]
            sys.stdout=open(f"{output_name}_bait_truncated.fasta","w")
            print(seq_id)
            print(truncated_seq)
elif ques.lower()=='c':
    with open (fasta_file) as f:
        data=f.readlines()
    for i in range (0, len(data), 2):
        seq_id=data[i].strip()
        seq = data[i+1].strip()
        pattern_pos=re.search(pattern, seq)
        if pattern_pos:
            truncated_seq=seq[pattern_pos.start():]
            sys.stdout=open(f"{output_name}_bait_truncated.fasta","w")
            print(seq_id)
            print(truncated_seq)
   ```
</details>
