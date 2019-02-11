#!/bin/bash
#SBATCH -e ./run_logs/error%j.txt
#SBATCH -o ./run_logs/output%j.txt 
#SBATCH -n 1	
#SBATCH -t 03:10:00
#SBATCH -p serial
#SBATCH --mem-per-cpu=8000
#SBATCH --mail-type=END
#SBATCH --mail-user=diego.aliaga@helsinki.fi

# first set the environemt
source ./env_WRFv4.bash

run_dir=./tucu-april-data/WPS
exe=metgrid.exe

rm ${run_dir}/Vtable
rm ${run_dir}/namelist.wps

cp ./namelist.wps ${run_dir}/
cp ./Vtable.CFSR ${run_dir}/Vtable
cd ${run_dir}

## run the executable
srun ${exe}

