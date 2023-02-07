#!/bin/bash
#SBATCH --time=01:00:00
#SBATCH --output=/gpfs/fs0/scratch/m/mchakrav/patelmo6/HCP/hcp-micro-func/analysis/pls/k4/logs/bug-%J.out
#SBATCH --chdir=/gpfs/fs0/scratch/m/mchakrav/patelmo6/HCP/hcp-micro-func/analysis/pls/k4
#SBATCH --nodes=1
#SBATCH -p debug
source /home/m/mchakrav/patelmo6/virtual_envs/PLS_venv/bin/activate
python plsc.py x_brain_k4.csv ../y_behavs.csv 100 100 ./
