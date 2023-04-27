#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import subprocess
import numpy as np
import glob

#this script will extract pTM, ipTM from *_seed_000.json files and plot them to compare between files
########################################
bait_name    ='Bt24'
title_offset = 2
folder_path  ='.'
f_width      = 12 #figure width
f_height     = 5  #figure height
fontsize     = 10
margin_top   = 10
margin_bot   = 10
margin_left  = 10
margin_right = 11
key_position = 'left'
########################################
ptms=[]
iptms=[]
pae_data=[]
gnu_data=[]
json_files = glob.glob(f'{folder_path}/*_seed_000.json')
for json_file in sorted(json_files):
    with open (json_file) as f:
        data=json.load(f)
        ptms.append(data['ptm'])
        iptms.append(data['iptm'])
for i, p, ip in zip(sorted(json_files), ptms, iptms):
    pae_data.append(\
f"{i.split('.fa_pair_scores_rank')[0][2:]+'_'+i.split('.fa_pair_scores_rank_00')[1][:1]} {p:.2f} {ip:.2f}")

for data in pae_data:
    gnu_data.append(data.replace('_','.'))


# Plot the graph using gnuplot
with open('%s.gp'%(bait_name), 'w') as f:
    # Define the plot settings
    f.write('set term x11"\n')
    f.write('set tmargin %d\n'%(margin_top))
    f.write('set bmargin %d\n'%(margin_bot))
    f.write('set lmargin %d\n'%(margin_left))
    f.write('set rmargin %d\n'%(margin_right))
    f.write('set title "%s alphafold pulldown" font "Helvetica-Bold, 18" offset 0,%d \n'%(bait_name,title_offset))
    f.write('set xlabel "predicted models"\n')
    f.write('set ylabel "pTM and ipTM values"\n')
    f.write('set key %s\n'%(key_position))
    f.write('set xtics rotate by -45\n')
    f.write('set key box lt -1 lw 2\n')
    f.write('set x2tics out\n')
    f.write('set x2tics rotate by 45\n')
    f.write('set grid xtics\n')
    f.write('set grid x2tics\n')
    f.write('set terminal postscript eps enhanced color solid "Helvetica" %d size %d,%d\n'%(fontsize, f_width, f_height))
    f.write('set output "%s.eps"\n'%(bait_name))
    # Plot the data
    f.write('plot "-" u 1:3:4:xticlabels(2) w p pt 7 lc rgb "red" notitle, "-" u 1:3:4:x2ticlabel(2) w p pt 7 lc rgb "red" notitle, "-" u 1:4 w lp pt 7 lc rgb "blue" t "ipTM", "-" u 1:3 w lp pt 7 lc rgb "red" t "pTM" \n')
    
    for i in range(0,len(gnu_data),2):
        f.write('{} {}\n'.format(i+1,gnu_data[i]))
    f.write('e\n')
    for i in range(1,len(gnu_data),2): 
        f.write('{} {}\n'.format(i+1,gnu_data[i]))
    f.write('e\n')
    for i in range(len(gnu_data)):
        f.write('{} {}\n'.format(i+1,gnu_data[i]))
    f.write('e\n')
    for i in range(len(gnu_data)):
        f.write('{} {}\n'.format(i+1,gnu_data[i]))
    f.write('e\n')
# Call gnuplot to create the graph
subprocess.call(['gnuplot', '%s.gp'%(bait_name)])
