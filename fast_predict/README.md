# ESMFold_local
<!-- What is this for? -->
**ESMFold** is a deep neural network-based method for predicting protein structure from amino acid sequence, which features up to 60x faster predictions compared to the current state-of-the-art structural prediction method. This is ideal for users when quickly deciding where to truncate the protein sequence (for the purpose of domain-wise analysis and speeding up the computation) if the predicted structure of interest is provided within seconds.

The `ESMFold_local` uses ESMFold to quickly generate predicted structure and asks for user inputs (sequence motif) to truncate protein sequence based on the predicted model. The script returns truncated fasta sequence to be used for `VirtualPullDown`. 

-----------------------------
## Usage
The script asks for amino acid sequence (< 200) to be predicted and generate an ouput file in pdb. Then, the predicted structure will be displayed in PyMol for the user to decide the region to truncate. Once PyMol closes, the script asks for the sequence motif (at 4 residues or longer) of the region to truncate. The user can decide N-terminus or C-terminus of the sequence to truncate.
