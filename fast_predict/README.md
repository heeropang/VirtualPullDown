# ESMFold_local
<!-- What is this for? -->
**ESMFold** is a deep neural network-based method for predicting protein structure from amino acid sequence, which features up to 60x faster predictions compared to the current state-of-the-art structural prediction method. This is ideal for users when quickly deciding where to truncate the protein sequence (for the purpose of domain-wise analysis and speeding up the computation) if the predicted structure of interest is provided within seconds.

The `ESMFold_local` uses [ESMFold](https://colab.research.google.com/github/sokrypton/ColabFold/blob/main/ESMFold.ipynb) to quickly generate predicted structure without having to install ESMFold and download param files. The script will allow user to input protein sequence of interest to predict structure and make decision on truncating the protein sequence based on the predicted model. The script generates truncated fasta sequence to be used for `VirtualPullDown`. 

-----------------------------
## Usage
The script asks for amino acid sequence (limited to < 200) to be predicted and returns an ouput file in pdb. The predicted structure will be displayed in PyMol for the user to decide the region to truncate. Once PyMol closes, the user can input the unique protein sequence (at least 4 residues or longer) of the region to truncate. The user can also decide to truncate N-terminus or C-terminus of the specified region.


