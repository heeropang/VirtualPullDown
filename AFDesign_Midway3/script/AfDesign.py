#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import os
import subprocess
import base64
from colabdesign import mk_afdesign_model, clear_mem
## This script is based on the ColabDesign (specifically AFDesign) written by Sergey Sokrypton 
## It is used for de novo designing a binder for target protein without using a google colab notebook
## This will generate the following output files: binder sequence (check log file), target_binder.pdb and target_binder.mp4
###########################################
target_pdb    = "tg1_minus_turn"
input_chain   = "A"
target_site   = "74,78,82,241-245"
binder_length = 40
cycle_number  = 50
num_model     = 5
###########################################
##remove previously processed files to avoid appending
subprocess.call("rm %s_binder.pdb"%target_pdb, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
subprocess.call("rm %s_binder.mp4"%target_pdb, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
subprocess.call("rm temp.html", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
##checking the name of input target pdb file
if not os.path.isfile("%s.pdb"%(target_pdb)):
    print("Error: %s.pdb does not exist\n"%(target_pdb))
    exit(1)
##running de novo binder design
clear_mem()
af_model=mk_afdesign_model(protocol="binder")
af_model.prep_inputs(pdb_filename="%s.pdb"%target_pdb, chain=input_chain, hotspot=target_site, binder_len=int(binder_length))
af_model.design_3stage(cycle_number, cycle_number, num_model)
##saving the complex and getting the sequence of the binder
af_model.save_pdb("%s_binder.pdb"%target_pdb)
af_model.get_seqs()
##decoding the video output
html_video=af_model.animate()
with open ('temp.html','w') as f:
    f.write(html_video)
with open ('temp.html','r') as f:
    saved_html_video=f.read()
match=re.search(r'src="data:video/mp4;base64,([^"]+)"', saved_html_video)
if match:
    base64_data=match.group(1)
else:
    print("Base64 data was not found in the HTML video.")
video_data=base64.b64decode(base64_data)
with open ('%s_binder.mp4'%target_pdb,'wb') as f:
    f.write(video_data)
