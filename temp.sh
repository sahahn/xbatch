#!/bin/sh
#SBATCH --partition=bluemoon
#SBATCH --time=30:00:00
#SBATCH --mem=12G
#SBATCH --job-name=12
#SBATCH --output=Job_Logs/%x_%j.out
#SBATCH --error=Job_Logs/%x_%j.err

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1 
#SBATCH --cpus-per-task=12

#SBATCH --array=200-8000

python something.py $SLURM_ARRAY_TASK_ID

