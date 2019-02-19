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

# %% [markdown]
# # Imports

# %%
import matplotlib
import pandas
import xarray

from di_python.scalebar import scale_bar

# %%
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
from netCDF4 import Dataset as netcdf_dataset
import netCDF4
import cartopy.geodesic as cge
import wrf
import cartopy
import numpy as np
import xarray as xr
import di_python.ya_esta as ye

# %%


# %% [markdown]
# # Constants 

# %%
LANDUSE_DIC = {
    1 : 'Evergreen Needleleaf Forest',
    2 : 'Evergreen Broadleaf Forest',
    3 : 'Deciduous Needleleaf Forest',
    4 : 'Deciduous Broadleaf Forest',
    5 : 'Mixed Forests',
    6 : 'Closed Shrublands',
    7 : 'Open Shrublands',
    8 : 'Woody Savannas',
    9 : 'Savannas',
    10: 'Grasslands',
    11: 'Permanent Wetlands',
    12: 'Croplands',
    13: 'Urban and Built-Up',
    14: 'Cropland/Natural Vegetation Mosaic',
    15: 'Snow and Ice',
    16: 'Barren or Sparsely Vegetated',
    17: 'Water',
    18: 'Wooded Tundra',
    19: 'Mixed Tundra',
    20: 'Barren Tundra',
    21: 'LAKES',
}

# %%
REF_LAT = -17
REF_LON = -66.3
REF_LOLA = [REF_LON, REF_LAT]


# %% [markdown]
# # Functions  

# %%
def get_lola(path):
    file_ds = netcdf_dataset(path, 'r')
    latds = wrf.getvar(file_ds, "CLAT")
    la, lo = wrf.latlon_coords(latds)
    la0 = la.values[0, 0]
    la1 = la.values[-1, -1]
    lo0 = lo.values[0, 0]
    lo1 = lo.values[-1, -1]
    return lo0, lo1, la0, la1


# %%
def ax_draw_sq(ax, lola):
    lo0, lo1, la0, la1 = lola

    ax.plot(
        [lo0, lo0, lo1, lo1, lo0],
        [la0, la1, la1, la0, la0],
        transform=cartopy.crs.PlateCarree(),
        c='black'
    )

    return ax


# %%
def lola_plus_dis(lola, ang, dis_m):
    geo = cge.Geodesic()
    res = geo.direct(lola, ang, dis_m).base
    return res


# %%
def get_file_list(dir_path, ext='wrfout_d0'):
    all_files = pd.DataFrame(os.listdir(dir_path), columns=['name'])
    boo = all_files.name.str.contains(ext) & all_files.name.str.contains('d0')
    met_em_files = all_files[boo]
    met_em_files = met_em_files.sort_values('name')
    met_em_files['path'] = met_em_files.apply(
        lambda x:
        os.path.join(dir_path, x['name']),
        axis=1)
    met_em_files = met_em_files.reset_index(drop=True)
    met_em_files['dom'] = met_em_files.name.str.extract(r'(d0\d*)')
    return met_em_files


def wrf_plot_par(wrf_diag, ax, comment=''):
    la, lo = wrf.latlon_coords(wrf_diag)

    name = wrf_diag.name
    dt64 = ye.dt64_2_iso(wrf_diag.Time.values)

    #     cart_proj = wrf.get_cartopy(wrf_diag)
    ctrans = cartopy.crs.PlateCarree()
    #     fig,ax = plt.subplots(subplot_kw={'projection':cart_proj})
    fig = ax.get_figure()
    mapa = ax.contourf(
        wrf.to_np(lo),
        wrf.to_np(la),
        wrf.to_np(wrf_diag),
        10,
        transform=ctrans,

    )

    gl = ax.gridlines(color="black", linestyle="dotted", draw_labels=True, crs=ctrans)
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xlocator = matplotlib.ticker.MaxNLocator(nbins=5)
    gl.ylocator = matplotlib.ticker.MaxNLocator(nbins=5)
    ax.set_title('{} {}\n{} [{}]\n{}'.format(name, dt64, wrf_diag.description, wrf_diag.units, comment))
    cb = plt.colorbar(mapa, ax=ax)
    plt.close()
    plt.close(fig)
    return ax


def print_var_starting_with(path, start_string):
    xar = xr.open_dataset(path)
    ser = pd.Series(list(xar.variables))
    li = ser[ser.str.startswith(start_string)]
    li = list(li)
    for l in li:
        va = xar[l]
        #     print(va)
        try:
            des = va.attrs['description']
        except:
            des = ''
        print(l, '-', des)
        print('---------------')


def get_mega_list(d_string, file_list):
    file_list_short = file_list[file_list.dom == d_string]
    res = file_list_short.apply(

        lambda row: set_dt_to_path(row),
        axis=1
    )

    mega_list = pd.concat(list(res))
    return mega_list

def set_dt_to_path(row):
    path = row.path
    ds = xr.open_dataset(path)
    index = ds.Time.values
    dates = ds.XTIME.values
    ndw = pd.DataFrame({'date':dates,'wrf_index':index})
    ndw = ndw.set_index('date')
    ndw['name']= row['name']
    ndw['dom']= row['dom']
    ndw['path']= row['path']
    return ndw





