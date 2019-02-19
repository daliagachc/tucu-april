#!/bin/bash
#SBATCH -e ./run_logs/error%j.txt
#SBATCH -o ./run_logs/output%j.txt 
#SBATCH -n 1
#SBATCH -t 00:10:00
#SBATCH -p serial
#SBATCH --mem-per-cpu=8000
#SBATCH --mail-type=END
#SBATCH --mail-user=diego.aliaga@helsinki.fi

# first set the environemt
source ./env_WRFv4.bash


run_dir=./tucu-april-data/WRF/
rm ${run_dir}/namelist.input
cp ./namelist.input ${run_dir}/

exe_real=real.exe 
cd ${run_dir}

## run the executable
srun ${exe_real}

