# find_homologs.py for efficient homology search
<!-- What is this for? -->
Conventionally, we use sequence alignment tools such as protein blast, followed by downstream bioinformatics tools such as secondary structure predictions, to identify evolutionarily conserved genes from the sequence of interest. These methods can be time-consuming and often limited to closely related homologs. Find_homologs offers a fast and efficient alternative by utilizing a protein blast-style search for homologs based on structural similarity. This approach allows for the inclusion of evolutionarily distant homologs in the bioinformatic procedure

**Foldseek** is a sequence alignment tool which converts amino acid sequences into 3Di sequences containing nearest neighbor structural elements for alignment. The software incorporates a trained neural network model which dramatically improved processing speed to seconds compared to the conventional sequeunce alignement softwares such as Dali or TMalign which usually takes days or weeks. This makes it ideal for users who need to quickly decide where to truncate the protein sequence for domain-wise analysis and to speed up computation.

The `find_homologs` script uses the [ESMFold](https://colab.research.google.com/github/sokrypton/ColabFold/blob/main/ESMFold.ipynb) to quickly generate predicted protein structure, but without having to install ESMFold and download param files. Then, the [Foldseek](https://search.foldseek.com) to generate 3di sequences used for structure based homologs search.

-----------------------------
## Usage
The script requires an user input of an amino acid sequence (limited to < 400 residues), which generates a predicted structure and returns a list the evolutionarily distant homologs.

Here is an example how you can run the script...
```
./find_homologs.py KEWYINYKADFEKHKQDDKLKETQVIQMNEAALRKLEKELVDVQKQKN 
```

```
The number of residues submitted = 47  ##The structure prediction is limited to <400 residues..

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 98703  100    68  100 98635     30  43936  0:00:02  0:00:02 --:--:-- 43985
```
The script will then prepare a list of hits 
```
{"id":"HsvHhnelGZq9jcQfeHRXopF3GbwHt2dfZ7IqIw","status":"COMPLETE"}

Job is completed... Preparing list of hits...
COMPLETE
Targets       Descriptions                                                     Prob.      E-value    Scientific Name
AF-I1L8R7     HECT domain-containing protein                      0.076      4.331      Glycine max
AF-A0A6B5J4Z7 Mobile element-associated protein                   1.000      1.526e-16  Staphylococcus aureus
AF-A0A6B5FYA7 Mobile element-associated protein                   1.000      2.258e-15  Staphylococcus aureus
AF-Q9F0K3     Orf15                                               1.000      1.098e-14  Staphylococcus aureus
AF-A0A024P946 Uncharacterized protein                             1.000      0.0007996  Halobacillus karajensis
AF-A0A3A0W5L9 PriCT_1 domain-containing protein                   1.000      1.249e-05  Staphylococcus gallinarum
AF-A0A0M4FYI7 Uncharacterized protein                             1.000      0.00258    Bacillus sp. FJAT-22090
AF-A0A2T5G4D9 Prophage Lp4 protein 7, DNA replication             1.000      0.0005004  Hydrogenibacillus schlegelii
AF-A0A6P1X0W8 Mobile element-associated protein                   1.000      1.579e-05  Staphylococcus sp. MI 10-1553
AF-A0A4P7GWG3 DNA primase                                         1.000      0.008827   Thermaerobacter sp. FW80
AF-A0A4S2EI77 DNA replication protein                             1.000      0.002901   Ligilactobacillus murinus
AF-A0A5F0TSU8 PriCT_1 domain-containing protein                   1.000      4.275e-05  Mammaliicoccus lentus
AF-A0A4Y9H9D0 Mobile element-associated protein                   1.000      1.048e-05  Gemella sp. WT2a
AF-A0A7U3TFS7 Bifunctional DNA primase/polymerase                 1.000      0.008325   Limosilactobacillus fermentum
AF-A0A4P6YQZ5 Uncharacterized protein                             1.000      0.01183    Periweissella cryptocerci
AF-A0A679JGJ5 Uncharacterized protein                             1.000      0.0008989  Methylobacterium bullatum
AF-A0A4R5Y7R8 PriCT_1 domain-containing protein                   1.000      3.008e-05  Macrococcus bohemicus
AF-A0A529AQI6 DNA primase                                         1.000      0.01254    Mesorhizobium sp.
AF-A0A3D8VE11 DNA primase                                         1.000      0.004914   Halobacillus trueperi
AF-A0A3M0Z5Q0 DNA primase                                         1.000      0.003458   Gammaproteobacteria bacterium
AF-A0A1W7ACH7 PriCT_1 domain-containing protein                   1.000      0.001523   Macrococcus canis
AF-A0A0H4IXH5 PriCT_1 domain-containing protein                   1.000      0.01254    Methylophilales bacterium MBRS-H7
AF-A0A0A8K7G8 Uncharacterized protein                             1.000      0.009924   Methyloceanibacter caenitepidi
AF-A0A1D2SLS0 Uncharacterized protein                             1.000      0.0006707  Lautropia sp. SCN 69-89

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
   ```
</details>
