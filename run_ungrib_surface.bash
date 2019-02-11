#!/bin/bash
#SBATCH -e error%j.txt
#SBATCH -o output%j.txt 
#SBATCH -n 1	
#SBATCH -t 04:10:00
#SBATCH -p serial
#SBATCH --mem-per-cpu=8000
#SBATCH --mail-type=END
#SBATCH --mail-user=diego.aliaga@helsinki.fi

# first set the environemt
source ./env_WRFv4.bash
pre=SURFACE
pre_short=sur
run_dir=./tucu-april-data/WPS
exe=ungrib.exe

python ./util/change_prefix.py namelist.wps ${pre}

rm ${run_dir}/Vtable
rm ${run_dir}/namelist.wps

cp ./namelist.wps ${run_dir}/
cp ./Vtable.CFSR ${run_dir}/Vtable

cd ${run_dir}
./link_grib.csh ../${pre_short}/${pre_short}_
## run the executable
srun ${exe}

