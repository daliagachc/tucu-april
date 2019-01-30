#!/bin/bash
#SBATCH -e error%j.txt
#SBATCH -o output%j.txt 
#SBATCH -n 1
#SBATCH -t 00:10:00
#SBATCH -p serial
#SBATCH --mem-per-cpu=4000
#SBATCH --mail-type=END
#SBATCH --mail-user=diego.aliaga@helsinki.fi

# first set the environemt
source $USERAPPL/env_WRFv4.bash


run_dir=${WRKDIR}/DONOTREMOVE/saltena_2018/tucu-april-data/WRF/

exe_real=real.exe 
cd ${run_dir}

## run the executable
srun ${exe_real}

