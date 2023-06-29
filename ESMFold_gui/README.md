# ESMFold_gui.py for a quick structure prediction
<!-- What is this for? -->
Graphical User Interface for ESMFold

The Graphical User Interface (GUI) for ESMFold is designed to provide users with a convenient way to visualize protein structures based on an amino acid sequence of interest (<400 amino acid residues). 

Here's an overview of its features:

**Sequence Input**:     The user can copy and paste the amino acid sequence into a designated input field.

**Prediction Button**:   Once the sequence is pasted, the user can click on the "Predict" button to initiate the structure prediction process. 
After the prediction is complete, the GUI will automatically generate the predicted protein structure and the corresponding FASTA sequence. 

**Structure Visualization**:   If the user has Pymol installed on their system, the GUI provides an additional button for visualizing the predicted protein structure. 
By clicking on the "Visualize" button, the user can view the structure in Pymol.

**Sequence Truncation**:   The GUI also offers a convenient way to truncate sequences. If the user wants to visualize only a specific portion of the protein, they can input the desired starting and ending positions. The GUI will truncate the sequence accordingly and update the predicted structure and FASTA sequence in real-time.


