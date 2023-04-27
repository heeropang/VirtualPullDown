#!/bin/bash
#SBATCH --job-name=msa_search
#SBATCH --account=pi-price
#SBATCH -c 4                                 # Requested cores
#SBATCH --time=42:00:00                    # Runtime in D-HH:MM format
#SBATCH --partition=beagle3                    # Partition to run in
#SBATCH --mem=128GB                           # Requested Memory
#SBATCH -o ./log/search.out                          
#SBATCH -e ./log/search.err                        

module load gcc/10.2.0 cuda/11.2
source ~/.bash_profile

colabfold_search --db-load-mode 0 \
--mmseqs mmseqs \
--use-env 1 \
--use-templates 0 \
--threads 3 \
ready /software/colabfold-data msas 
