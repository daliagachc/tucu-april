#! /bin/bash
new_branch_name=v07
old_branch_name=v06
git_path=/homeappl/home/aliagadi/saltena_2018/tucu-april/
data_link=tucu-april-data
base_data_path=/wrk/aliagadi/DONOTREMOVE/saltena_2018/
data_path=${base_data_path}${data_link}-${new_branch_name}
echo ${data_path}

cd ${git_path}
mkdir -p ${data_path}
rm -f ${data_link}
ln -s ${data_path} ${data_link}

