#!/bin/bash
#SBATCH -J create_links
#SBATCH -e error%j.txt
#SBATCH -o output%j.txt 
#SBATCH -n 1
#SBATCH -t 00:10:00
#SBATCH -p serial
#SBATCH --mem-per-cpu=4000
#SBATCH --mail-type=END
#SBATCH --mail-user=diego.aliaga@helsinki.fi

# assumes that I have made the initial conditions (met_em*.nc)
# creates links and run directory

# after running this, you still need to modify the namelist
# and run real.exe and main.exe

# set the directory where you installed WRF
export wrf_dir=${USERAPPL}/WRF4/WRF/

# set the directory where you have your met_em* files
# I moved these into their own directory
# !! EDIT THIS!!
export wps_dir=${WRKDIR}/DONOTREMOVE/saltena_2018/tucu-april-data-v02/WPS/

# set the directory where you want to run WRF / where the output will be
#  !!! EDIT THIS !!!
export run_dir=${WRKDIR}/DONOTREMOVE/saltena_2018/tucu-april-data-v02/WRF/


mkdir -p ${run_dir}
rm ${run_dir}namelist.input
cp ./namelist.input ${run_dir}
cd ${run_dir}

echo link executables 
ln -sf ${wrf_dir}/main/*.exe .

echo link gribmap info
ln -sf ${wrf_dir}/run/gribmap.txt . 

echo linking to RRTM_DATA 
ln -sf ${wrf_dir}/run/RRTM* .

echo linking to look-up tables 
ln -sf ${wrf_dir}/run/*TBL .
ln -sf ${wrf_dir}/run/*tbl .

echo linking to ozone data 
ln -sf ${wrf_dir}/run/ozone* .


echo linking met files
ln -sf ${wps_dir}/met_em* .

#cp ${wrf_dir}/run/namelist.input .






