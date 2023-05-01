## Step 2. Using ColabFold for structure predictions
Sbatch scripts are submitted for generating MSA and predicted files using local ColabFold
<!-- What is this for? --> 
This is for submitting preprocessed sequence files in batch on slurm to generate multiple sequence alignments (MSA) and structure predictions using ['ColabFold'](https://github.com/sokrypton/ColabFold). 

### Before we start...
['localcolabfold'](https://github.com/YoshitakaMo/localcolabfold) needs to be installed on your local PC. 
(installation guidelines can be found --['here'](https://github.com/YoshitakaMo/localcolabfold)).
We also need ColabFold ['database'](https://colabfold.mmseqs.com/) on your local PC.
Finally, we need to compile GPU supporting ['Jax'](https://github.com/markusschmitt/vmc_jax/blob/master/documentation/readme/compile_jax_on_cluster.md).

### Bash script to make project directories
Preprocessed fasta sequences will be stored in ready directory
<details>
   <summary> :rocket: Click here for the bash script </summary>
   
   ```Bash
   #!/bin/bash
   echo "setting up directories for $1 integrase"
   echo "copy and paste the following line for rsync"
   echo "rsync -auvz * heewhan@midway3.rcc.uchicago.edu:/beagle3/price/top_search/$1/ready"
   mkdir $1 
   cd $1
   mkdir ready msas predictions log
   ```
</details>

### SBATCH script for generating MSA files
The following script returns MSA (.a3m) files in the msas and log files in the log directory
<details>
   <summary> :rocket: Click here for the bash script </summary>
   
   ```Bash
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
   ```
</details>

### SBATCH script for structure predictions
The following script returns predicted output files in the predictions and log files in the log directory

<details>
   <summary> :rocket: Click me for the bash script </summary>
   
   ```Bash
   #!/bin/bash
   #SBATCH --job-name=Predict
   #SBATCH --account=pi-price
   #SBATCH --partition=beagle3
   #SBATCH --nodes=1
   #SBATCH --time=12:00:00
   #SBATCH --ntasks-per-node=1
   #SBATCH --cpus-per-task=8
   #SBATCH --gres=gpu:2
   #SBATCH --constraint=a100
   #SBATCH --mem=48G
   #SBATCH --output=./log/predict.out
   #SBATCH --error=./log/predict.err

   #module load alphafold/2.2.0 cuda/11.3
   module load cuda/11.5
   cd $SLURM_SUBMIT_DIR
   
   echo "GPUs available: $CUDA_VISIBLE_DEVICES"
   echo "CPU cores: $SLURM_CPUS_PER_TASK"
   
   nvidia-smi
   
   colabfold_batch --use-gpu-relax --num-recycle 5 --num-models 5 msas predictions
   ```
</details>

----------------------------------------------------
