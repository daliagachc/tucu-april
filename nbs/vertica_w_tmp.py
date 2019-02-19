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


# %%
vm = -.5
vM = .5
f_i = 188
row = file_list.iloc[f_i]
ds = xr.open_dataset(row.path)
ds1 = ds.isel(
    Time=2,
#     bottom_top_stag=0,
    south_north=40
    
)
# print(ds.dims)
# print(ds.variables)
fig, ax = plt.subplots()
img = ds1.W.plot(vmin=vm,vmax=vM,cmap='RdBu_r',ax=ax)
ax.set_aspect('equal')

# %%
z = wrf.getvar(netCDF4.Dataset(row.path),'z')
wa = wrf.getvar(netCDF4.Dataset(row.path),'wa')

# %%
res = wrf.vinterp(netCDF4.Dataset(row.path),wa,'ght_msl',np.arange(.01,10,.1))

# %%
res[:,40,:].plot(x='XLONG',y='interp_level')
