#!/bin/bash
#Usage:        ./template_auto.py
#Author:       Heewhan Shin
#Author_email: hshin40@gmail.com
#Date:         April 25, 2023
#Description:  This script identifies prophages (if any) then produces paired input sequence files for multimer predictions using localcolabfold.

args=(
NZ_NVLR01000020.1
Bt24
range.txt
)

if [ ! -f "sequence.txt" ]; then
    echo -e "Error: please check if the genomic sequence is saved in the directory \n"
    exit 1
fi
 
if [ ! -f "${args[1]}.fasta" ]; then
    echo -e "Error: ${args[1]}.fasta does not exist \n"
    exit 1
fi

if [ ! -f "${args[1]}_bait_truncated.fasta" ]; then
    echo -e "Error: ${args[1]_bait_truncated.fasta} does not exist \n"
    exit 1
fi
sed 's/\[db_xref=[^]]*\] //g' sequence.txt >sequence_check.txt

mkdir -p fa ready
echo -e "fa and ready directories created...\n"

python find_prophage_range_auto.py "${args[0]}"

if [ ! -f "${args[2]}" ]; then
    echo -e "Error: ${args[2]} does not exist \n"
    exit 1
fi

echo -e "identified range of prophages applied... \n"

python create_mastertable_auto.py "${args[1]}"
echo -e "creating master table ${args[1]}_master.xlsx ... \n"
python filter_prey_fasta_auto.py "${args[1]}" "${args[2]}"
echo creating filtered table ${args[1]}_filtered.xlsx ... 
echo -e "genrating prey sequences and moving them into fa/ directory... \n"
mv *.fa fa

python combine_pairwise_batch_auto.py "${args[1]}"
echo -e "pairing bait and prey sequences... \n"
mv fa/*.fasta ready
ls ready 

echo pre-processing completed...
