# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
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
# lets have al the imports here
from tucu_saltena_fun import *


# %%
# lets plot the file names in the directory
from tucu_saltena_fun import print_var_starting_with

dir_path = '../tucu-april-rm-data/WRF/'
file_list = get_file_list(dir_path, ext='wrfout_d')
file_list.sample(5)

# %%
# lets choose a random path
row = file_list[file_list.dom == 'd04'].iloc[1] 

# %%
dd=['d01','d02','d03','d04']
mega_l={}
for d in dd:
    mega_l[d]=get_mega_list(d,file_list)

# %%
mega_l['d03']


# %%
mega_list=mega_l['d04']

# %%
mega_list.sample(2)

# %%
mega_list.wrf_index.plot()

# %%
plt.plot_date(mega_list.index,mega_list.wrf_index+1)


# %%
mega_list.sample()

# %%
print_var_starting_with(mega_list.iloc[0].path, "Tsdf")

# %%
plt.plot_date(mega_list[::30].index,mega_list[::30].index)


# %%
plt.plot_date('date','wrf_index',data=mega_list[::30].reset_index())


# %%
def plot_from(row, fig, w, h, i):
    path=row.path
    idx=row.wrf_index

    nc_ds = netCDF4.Dataset(path,)
    par_name = 'tc'
    comment = 'surface'
    level = 0
    wrf_diag = wrf.getvar(nc_ds, par_name, timeidx=idx)[level]

    cart_proj = wrf.get_cartopy(wrf_diag)
    ax = fig.add_subplot(w, h, i, projection=cart_proj)
#     fig, ax = plt.subplots(subplot_kw={'projection':prog})
#     plt.close(fig)
    ax = wrf_plot_par(wrf_diag,ax)
#     ax.figure
    return ax 


# %%
mega_list.iloc[::30]

# %%
fig = plt.figure()
small_list = mega_list.iloc[::30]
len(small_list)

# %%
w, h, = 5, 5 
for i, (index, row) in enumerate(small_list.iterrows()):
    ax = plot_from(row, fig, w,h,i+1 )
    print(i,'done')
fig.set_size_inches(*[
    4*x for x in [w,h]
])
fig

# %%
fig.savefig('/tmp/fig.pdf')

# %%
wrf_diag[0][0]


# %%
p = print 
ti 


# %%
fig

# %%
ds_path = netCDF4.Dataset(path)
par_name = "wspd_wdir"
par_name1 = 'z'
tc = wrf.getvar(ds_path, par_name, units="kt")[0, :]
z = wrf.getvar(ds_path, par_name1)
la, lo = wrf.latlon_coords(tc)

start_point = wrf.CoordPair(lat=-16.4, lon=-68.8)
end_point = wrf.CoordPair(lat=-16.4, lon=-67.5)

tmp_cross = wrf.vertcross(tc, z, wrfin=ds_path, start_point=start_point,
                          end_point=end_point, latlon=True, meta=True)
fig, ax = plt.subplots()

ctemp = ax.contourf(wrf.to_np(tmp_cross), levels=20, cmap=matplotlib.cm.get_cmap("jet"))

# Add the color bar
cb_temp = fig.colorbar(ctemp, ax=ax)
cb_temp.ax.tick_params(labelsize=10)

# Set the x-ticks to use latitude and longitude labels
coord_pairs = wrf.to_np(tmp_cross.coords["xy_loc"])
x_ticks = np.arange(coord_pairs.shape[0])
x_labels = [pair.latlon_str() for pair in wrf.to_np(coord_pairs)]
ax.set_xticks(x_ticks[::20])
ax.set_xticklabels(x_labels[::20], rotation=45)

# Set the y-ticks to be height
vert_vals = wrf.to_np(tmp_cross.coords["vertical"])
v_ticks = np.arange(vert_vals.shape[0])
ax.set_yticks(v_ticks[::20])
ax.set_yticklabels(vert_vals[::20], fontsize=10)
ax.set_ylabel('z [m]')
ax.set_xlabel('lat lon')
ax.set_title('wind speed[knots]')

# %%



# %%
ds_path = netCDF4.Dataset(path)
par_name = 'tc'
par_name1 = 'wspd_wdir'
tc = wrf.getvar(ds_path, par_name)
z = wrf.getvar(ds_path, par_name1)[0, :]
la, lo = wrf.latlon_coords(tc)

start_point = wrf.CoordPair(lat=-16.4, lon=-68.8)
end_point = wrf.CoordPair(lat=-16.4, lon=-67.5)

tmp_cross = wrf.vertcross(tc, z, wrfin=ds_path, start_point=start_point,
                          end_point=end_point, latlon=True, meta=True)
fig, ax = plt.subplots()

ctemp = ax.contourf(wrf.to_np(tmp_cross), levels=20, cmap=matplotlib.cm.get_cmap("jet"))

# Add the color bar
cb_temp = fig.colorbar(ctemp, ax=ax)
cb_temp.ax.tick_params(labelsize=10)

# Set the x-ticks to use latitude and longitude labels
coord_pairs = wrf.to_np(tmp_cross.coords["xy_loc"])
x_ticks = np.arange(coord_pairs.shape[0])
x_labels = [pair.latlon_str() for pair in wrf.to_np(coord_pairs)]
ax.set_xticks(x_ticks[::20])
ax.set_xticklabels(x_labels[::20], rotation=45)

# Set the y-ticks to be height
vert_vals = wrf.to_np(tmp_cross.coords["vertical"])
v_ticks = np.arange(vert_vals.shape[0])
ax.set_yticks(v_ticks[::20])
ax.set_yticklabels(vert_vals[::20], fontsize=10)
ax.set_ylabel('z [m]')
ax.set_xlabel('lat lon')

# %%



wrf.getvar()

# %%
def get_rows(cols,tot):
#     tot = 21
#     cols = 5 
    rows = int(np.ceil(tot/cols)) 
    print(rows*cols, 'tot', tot)
    return rows 

# %%
get_rows(5,21)

# %%



# %%
tot = 21 
cols = 5 
rows = 22//5
print(rows)

# %%
tot = 21 
cols = 5 
rows = 24//5
print(rows)

# %%
np.ceil(3.4)

# %%
row = mega_list.iloc[1]

# %%
row

# %%
ds = xr.open_dataset(row.path)
ds.Time

# %%
t1=5
b1=0
ds1 = ds.isel(Time=slice(t1,t1+2),bottom_top=slice(b1,b1+2))[['P','T','PB']].copy()
# ds1

# %%
save_path='/tmp/er'+str(t1)
try: os.remove(save_path)
except: pass
ds1.to_netcdf(save_path)

# %%
nds = wrf.getvar(netCDF4.Dataset(save_path),'tc',timeidx=0)[0]

# %%
nds.plot(x='XLONG',y='XLAT',robust=True,vmin=nds.min(),vmax=nds.max())

# %%
d1 = mega_l['d01']
d2 = mega_l['d02']
d3 = mega_l['d03']
d4 = mega_l['d04']
dds = [d1,d2,d3,d4]
lds = [len(l) for l in dds]
lds

# %%
def get_nds(row, t1=0):
    ds = xr.open_dataset(row.path)
    ds.Time
    b1=0
    ds1 = ds.isel(Time=slice(t1,t1+2),bottom_top=slice(b1,b1+2))[['P','T','PB']].copy()
    # ds1
    save_path='/tmp/wrf_tmp'+str(t1)+str(np.random.randint(1000000))
    
    try: os.remove(save_path)
    except: pass
    ds1.to_netcdf(save_path)
    nds = wrf.getvar(netCDF4.Dataset(save_path),'tc',timeidx=0)[0]
    return nds


# %%
ind = 10
row3 = mega_l['d03'].iloc[ind]
row4 = mega_l['d04'].iloc[ind]

# %%
nds3 = get_nds(row3)
nds4 = get_nds(row4)

# %%
def get_fun(fun):
    res = np.array([fun(i).values for i in [nds3, nds4]])
    return res

# %%
fig, ax = plt.subplots()
# nds3.plot.imshow()
vm=min(get_fun(xr.DataArray.min))
vM=max(get_fun(xr.DataArray.max))
m1 = nds3.plot(x='XLONG',y='XLAT',ax=ax,add_colorbar=False,vmin=vm,vmax=vM)
nds4.plot(x='XLONG',y='XLAT',ax=ax,add_colorbar=False,vmin=vm,vmax=vM)
fig.set_size_inches(10,10)
fig.colorbar(m1)

gb = wrf.geo_bounds(nds4)

gb.bottom_left.lat

lam = gb.bottom_left.lat
lom = gb.bottom_left.lon
laM = gb.top_right.lat
loM = gb.top_right.lon

lad = laM-lam
lod = loM-lom
par = .2
lap = lad * par 
lop = lod * par 

ax.set_ylim(lam-lap,laM+lap)
ax.set_xlim(lom-lop,loM+lop)
ax.set_title('')

ax.scatter(*ye.LOLA_CHC,c='r')

# %%
fig, ax = plt.subplots()
# nds3.plot.imshow()
vm=min(get_fun(xr.DataArray.min))
vM=max(get_fun(xr.DataArray.max))
m1 = nds3.plot(x='XLONG',y='XLAT',ax=ax,add_colorbar=False,vmin=vm,vmax=vM)
nds4.plot(x='XLONG',y='XLAT',ax=ax,add_colorbar=False,vmin=vm,vmax=vM)
fig.set_size_inches(10,10)
fig.colorbar(m1)

gb = wrf.geo_bounds(nds4)

gb.bottom_left.lat

lam = gb.bottom_left.lat
lom = gb.bottom_left.lon
laM = gb.top_right.lat
loM = gb.top_right.lon

lad = laM-lam
lod = loM-lom
par = .2
lap = lad * par 
lop = lod * par 

ax.set_ylim(lam-lap,laM+lap)
ax.set_xlim(lom-lop,loM+lop)
ax.set_title('')

ax.scatter(*ye.LOLA_CHC,c='r')

# %%
ind = 10
row3 = mega_l['d01'].iloc[ind]
row4 = mega_l['d02'].iloc[ind]

nds3 = get_nds(row3)
nds4 = get_nds(row4)

def get_fun(fun):
    res = np.array([fun(i).values for i in [nds3, nds4]])
    return res

fig, ax = plt.subplots()
# nds3.plot.imshow()
vm=min(get_fun(xr.DataArray.min))
vM=max(get_fun(xr.DataArray.max))
m1 = nds3.plot(x='XLONG',y='XLAT',ax=ax,add_colorbar=False,vmin=vm,vmax=vM)
nds4.plot(x='XLONG',y='XLAT',ax=ax,add_colorbar=False,vmin=vm,vmax=vM)
fig.set_size_inches(10,10)
fig.colorbar(m1)

gb = wrf.geo_bounds(nds4)

gb.bottom_left.lat

lam = gb.bottom_left.lat
lom = gb.bottom_left.lon
laM = gb.top_right.lat
loM = gb.top_right.lon

lad = laM-lam
lod = loM-lom
par = .2
lap = lad * par 
lop = lod * par 

ax.set_ylim(lam-lap,laM+lap)
ax.set_xlim(lom-lop,loM+lop)
ax.set_title('')

ax.scatter(*ye.LOLA_CHC,c='r')
ax.scatter(*ye.LOLA_LPZ,c='b')

# %%
ind = 10
row3 = mega_l['d03'].iloc[ind]
row4 = mega_l['d04'].iloc[ind]

# %%
nds3 = get_nds(row3)
nds4 = get_nds(row4)

# %%
def get_fun(fun):
    res = np.array([fun(i).values for i in [nds3, nds4]])
    return res

# %%



# %%
fig.savefig('/tmp/fig.pdf')

# %%



# %%




# %%


# %%

