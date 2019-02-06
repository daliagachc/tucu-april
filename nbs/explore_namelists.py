
# coding: utf-8

# In[12]:


import f90nml
import numpy as np

# In[13]:


file_path = '../namelist.wps'
inp = f90nml.read(file_path)


# In[14]:


doms = 4
start_date = '2018-04-05_06:00:00'
end_date = '2018-04-05_07:00:00'
interval_seconds = 6*3600 # seconds
history_interval = 10 #minutes
time_step = 90 #secs for wrf. higher number produced error 


# In[15]:


shar = inp['share']

shar['start_date']=[start_date]*doms 
shar['end_date']=[end_date]*doms 
shar['interval_seconds']=interval_seconds 

geo = inp['geogrid']
geo['parent_grid_ratio'] = [1,4,3,3]
geo['i_parent_start'] = [1,28,80,70]
geo['j_parent_start'] = [1,18,65,122]

geo['e_we']= [118, 253, 274, 100]
geo['e_sn']= [86, 205, 214, 79]
geo['dx']= 38000
geo['dy']= 38000
geo['map_proj']= 'mercator'
geo['ref_lat']= -17
geo['ref_lon']= -66.3
geo['stand_lon']= geo['ref_lon']

ung = inp['ungrib']

ung['prefix'] = 'PRESSURE'
ung['prefix'] = 'SURFACE'

met = inp['metgrid']
met['fg_name'] = ['SURFACE','PRESSURE']


# In[16]:


inp


# In[17]:


f90nml.write(inp,file_path,force=True)


# # namelist.input 

# In[18]:


wrf_namelist = '../namelist.input'
inp_wrf = f90nml.read(wrf_namelist)


# In[19]:


import datetime


# In[20]:


def str2dat(st): 
    dt = datetime.datetime.strptime(st,'%Y-%m-%d_%H:%M:%S')
    return dt 

start_dt = str2dat(start_date)
s_y = start_dt.year
s_m = start_dt.month
s_d = start_dt.day
s_h = start_dt.hour

end_dt = str2dat(end_date)
e_y = end_dt.year
e_m = end_dt.month
e_d = end_dt.day
e_h = end_dt.hour


# In[21]:


tc_wrf = inp_wrf['time_control']

tc_wrf['start_year'] = [s_y]*doms
tc_wrf['start_month'] = [s_m]*doms
tc_wrf['start_day'] = [s_d]*doms
tc_wrf['start_hour'] = [s_h]*doms

tc_wrf['end_year'] = [e_y]*doms
tc_wrf['end_month'] = [e_m]*doms
tc_wrf['end_day'] = [e_d]*doms
tc_wrf['end_hour'] = [e_h]*doms

tc_wrf['interval_seconds'] = interval_seconds
tc_wrf['history_interval'] = history_interval

do_wrf = inp_wrf['domains']

do_wrf['time_step'] = time_step 
do_wrf['e_we'] = geo['e_we'] 
do_wrf['e_sn'] = geo['e_sn'] 

acc_rat_list = [geo['parent_grid_ratio'][0]]
for i,n in enumerate(geo['parent_grid_ratio'][1:]):
    nn = geo['parent_grid_ratio'][i+1] * acc_rat_list[i]
    acc_rat_list.append(nn)
    
do_wrf['dx'] = list(np.round(
    np.array(geo['dx'])/acc_rat_list,
    4))
do_wrf['dy'] = list(np.round(
    np.array(geo['dy'])/acc_rat_list,
    4))

do_wrf['parent_id'] = geo['parent_id']
do_wrf['parent_grid_ratio'] = geo['parent_grid_ratio']
do_wrf['i_parent_start'] = geo['i_parent_start']
do_wrf['j_parent_start'] = geo['j_parent_start']
do_wrf['parent_time_step_ratio'] = geo['parent_grid_ratio'] #copying from thomas


inp_wrf


# In[22]:


f90nml.write(inp_wrf,wrf_namelist,force=True)

