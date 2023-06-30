#!/bin/bash
#SBATCH --job-name=AfDesign
#SBATCH --account=pi-price
#SBATCH --partition=beagle3
#SBATCH --nodes=1
#SBATCH --time=12:00:00
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:2
#SBATCH --constraint=a40
#SBATCH --mem=5G
#SBATCH --output=./log/AfDesign.out
#SBATCH --error=./log/AfDesign.err

module load cuda/11.5
module load ffmpeg/5.1
cd /beagle3/price/AfDesign
echo "GPUs available: $CUDA_VISIBLE_DEVICES"
echo "CPU cores: $SLURM_CPUS_PER_TASK"

nvidia-smi

python /beagle3/price/AfDesign/AfDesign.py

