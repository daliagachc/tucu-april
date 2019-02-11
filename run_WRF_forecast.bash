#!/bin/bash
#SBATCH -e ./run_logs/error%j.txt
#SBATCH -o ./run_logs/output%j.txt 
#SBATCH -J WRF_forecast
#SBATCH -n 48
#SBATCH -t 20:00:00
#SBATCH -p parallel
#SBATCH --mem-per-cpu=1000
#SBATCH --mail-type=END
#SBATCH --mail-user=diego.aliaga@helsinki.fi

# first set the environemt
source $USERAPPL/env_WRFv4.bash


run_dir=./tucu-april-data/WRF/
rm ${run_dir}/namelist.input
cp ./namelist.input ${run_dir}/

exe_wrf=wrf.exe 
cd ${run_dir}

## run my MPI executable
srun ${exe_wrf}

