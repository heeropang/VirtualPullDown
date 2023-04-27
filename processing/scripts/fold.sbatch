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

##nvidia-smi

colabfold_batch --use-gpu-relax --num-recycle 5 --num-models 5 msas predictions 
