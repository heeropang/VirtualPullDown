#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys
from os.path import join
from Bio import SeqIO
import glob

#################################################
path      = "./"                                #path of sequence file 
filenames = sorted(glob.glob("./fa/"+"*.fa"))   #
prey_seq  = filenames                           #
bait_seq  = sys.argv[1]                         #
f2_txt    = f"{bait_seq}_bait_truncated.fasta"  #bait sequence of interest
                                                #
#################################################
txt2_path = os.path.join(path,f2_txt)
for fa in filenames:
    seq1     = list(SeqIO.parse(fa,'fasta'))
    seq2     = list(SeqIO.parse(txt2_path,'fasta'))
    seq_str = ''
    
    for seq2 in seq2:
        for seq1 in seq1:
            seq_str += '>' + seq1.id + '\n'
            seq_str += str(seq2.seq)+':'+str(seq1.seq) 
            of=open('%s_pair.fasta'%(fa),'w')
            of.write(seq_str)
            of.close()
            seq_str =''
