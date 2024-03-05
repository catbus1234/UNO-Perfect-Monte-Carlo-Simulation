#!/bin/bash

#SBATCH --partition=gpus
#SBATCH --qos=project
#SBATCH --gpus 1
#SBATCH --mem 32g
#SBATCH --mail-type=begin        # send email when job begins
#SBATCH --mail-type=end          # send email when job ends
#SBATCH --mail-user=jochen@davidson.edu

python run.py