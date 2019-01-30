#!/bin/bash
#SBATCH -e error%j.txt
#SBATCH -o output%j.txt 
#SBATCH -J WRF_forecast
#SBATCH -n 24
#SBATCH -t 10:00:00
#SBATCH -p parallel
#SBATCH --mem-per-cpu=8000
#SBATCH --mail-type=END
#SBATCH --mail-user=diego.aliaga@helsinki.fi

# first set the environemt
source $USERAPPL/env_WRFv4.bash


run_dir=${WRKDIR}/DONOTREMOVE/saltena_2018/tucu-april-data/WRF/

exe_wrf=wrf.exe 
cd ${run_dir}

## run my MPI executable
srun ${exe_wrf}

