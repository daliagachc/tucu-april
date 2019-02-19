# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 0.8.6
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import tucu_saltena_fun as fu
import di_python.ya_esta as ye
import importlib
import os
importlib.reload(fu);

# %%
PY_ID = fu.get_py_id()
print(PY_ID)

# %%
if PY_ID=='taito_diego':
    TMP_DIR = '/tmp/aliagadi'
    dir_path = '../tucu-april-data/WRF/'
    plot_path = '/tmp/aliagadi/plots'
if PY_ID=='mac_diego':
    TMP_DIR = '/tmp/wrf_tmp'
    dir_path = '../tucu-april-rm-data/WRF/'
    plot_path = '/tmp/wrf_tmp'

# %%

file_list = fu.get_file_list(dir_path, ext='wrfout')

# %%
dd=['d01','d02','d03','d04']
mega_l={}
for d in dd:
    mega_l[d]=fu.get_mega_list(d,file_list)

# %%
d_pairs = [
    {'d3':'d01','d4':'d02','par':.2},
    {'d3':'d02','d4':'d03','par':.2},
    {'d3':'d03','d4':'d04','par':.5},
    ]

# %%
iind = len(mega_l['d01'])
di = 3

# %%
for ind in range(iind):
    for dic_i in range(di):
        fu.save_plots_double_domain(
           dic_i    =dic_i    ,      
           ind      =ind      ,       
           plot_path=plot_path, 
           d_pairs  =d_pairs  ,  
           mega_l   =mega_l   , 
        )
        

# %%

