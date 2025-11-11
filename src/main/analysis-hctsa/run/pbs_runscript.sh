#!/bin/bash
# Set name of job
#PBS -P hctsa
#PBS -N h_b_dsct
#PBS -o jobOutput.txt
#PBS -j oe
# Specify a queue:
#PBS -q defaultQ
#PBS -l select=1:ncpus=1:mem=8GB
# Set your minimum acceptable walltime, format: day-hours:minutes:seconds
#PBS -l walltime=10:00:00
# Email user if job ends or aborts
#PBS -m ea
#PBS -M tdal0054@uni.sydney.edu.au
#PBS -V

# ---------------------------------------------------
cd "$PBS_O_WORKDIR"

# Show the host on which the job ran
hostname

# Load matlab module
module load matlab/R2020a

# Launch the Matlab job
matlab -nodisplay -nosplash -singleCompThread -r "HCTSA_Runscript; exit"
