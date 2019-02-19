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
    ndw = pd.DataFrame({'date': dates, 'wrf_index': index})
    ndw = ndw.set_index('date')
    ndw['name'] = row['name']
    ndw['dom'] = row['dom']
    ndw['path'] = row['path']
    return ndw


def wrf_get_base_tc_from_row(row, t1=0):
    ds = xr.open_dataset(row.path)
    ds.Time
    b1 = 0
    ds1 = ds.isel(Time=slice(t1, t1 + 2), bottom_top=slice(b1, b1 + 2))[['P', 'T', 'PB']].copy()
    # ds1
    save_path = '/tmp/wrf_tmp' + str(t1) + str(np.random.randint(1000000))

    try:
        os.remove(save_path)
    except:
        pass
    ds1.to_netcdf(save_path)
    nds = wrf.getvar(netCDF4.Dataset(save_path), 'tc', timeidx=0)[0]
    return nds


# def _get_fun(fun):
#     res = np.array([fun(i).values for i in [nds3, nds4]])
#     return res

def plot_double_surface_temp(
        nds3, nds4, d3, d4,
        cb_legend='surface temp [C]',
        par=.2,
        vm=-10,
        vM=40,
):
    min_since_run = int(nds3.XTIME.values)
    fig, ax = plt.subplots()
    # nds3.plot.imshow()
    # vm=min(fu_.get_fun(xr.DataArray.min))
    # vM=max(fu_.get_fun(xr.DataArray.max))
    m1 = nds3.plot(x='XLONG', y='XLAT', ax=ax, add_colorbar=False, vmin=vm, vmax=vM)
    nds4.plot(x='XLONG', y='XLAT', ax=ax, add_colorbar=False, vmin=vm, vmax=vM)
    fig.set_size_inches(10, 7)
    cb = fig.colorbar(m1)
    cb.set_label(cb_legend)

    gb = wrf.geo_bounds(nds4)

    lam = gb.bottom_left.lat
    lom = gb.bottom_left.lon
    laM = gb.top_right.lat
    loM = gb.top_right.lon

    lad = laM - lam
    lod = loM - lom
    lap = lad * par
    lop = lod * par

    ax.set_ylim(lam - lap, laM + lap)
    ax.set_xlim(lom - lop, loM + lop)
    ax.set_title(
        '{} | t = {}\n din={} | dout={}'.format(
            ye.dt64_2_iso(nds3.Time.values),
            min_since_run
            , d3, d4
        )
    )
    ax.scatter(*ye.LOLA_CHC, c='r')
    ax.scatter(*ye.LOLA_LPZ, c='b')
    ax.set_aspect('equal')
    plt.close(fig)
    return fig


def get_py_id(

):
    py_id = None
    ho = os.path.expanduser('~')
    # print(ho)
    try:
        file = open(ho + '/.py_id')
        try:
            py_id = file.readline()
            py_id = py_id.replace('\n', '')
        finally:
            file.close()
    except:
        print('could not open file id')
    # print(py_id)
    return py_id


def save_plots_double_domain(
        *,
        dic_i,
        ind,
        plot_path,
        d_pairs,
        mega_l,
):
    d3 = d_pairs[dic_i]['d3']
    d4 = d_pairs[dic_i]['d4']
    row3 = mega_l[d3].iloc[ind]
    row4 = mega_l[d4].iloc[ind]

    nds3 = wrf.getvar(netCDF4.Dataset(row3.path), 'tc', timeidx=row3.wrf_index)[0]
    nds4 = wrf.getvar(netCDF4.Dataset(row4.path), 'tc', timeidx=row4.wrf_index)[0]

    min_since_run = ye.dt64_2_iso(nds3.Time.values)
    file_name = '{}-{}_t-{}.png'.format(d3, d4, min_since_run)
    mid_name = '{}-{}'.format(d3, d4, min_since_run)
    print(file_name)
    mid_path = os.path.join(plot_path, mid_name)
    print(mid_path)
    os.makedirs(mid_path, exist_ok=True)
    file_path = os.path.join(mid_path, file_name)
    print(file_path)
    fig = plot_double_surface_temp(nds3, nds4, d3, d4, par=.2)

    fig.savefig(file_path)

    fig


def save_plots_double_domain_w(
        *,
        dic_i,
        ind,
        plot_path,
        d_pairs,
        mega_l,
):
    d3 = d_pairs[dic_i]['d3']
    d4 = d_pairs[dic_i]['d4']
    row3 = mega_l[d3].iloc[ind]
    row4 = mega_l[d4].iloc[ind]

    nds3 = xr.open_dataset(row3.path).isel(Time=row3.wrf_index, bottom_top_stag=1)
    nds4 = xr.open_dataset(row4.path).isel(Time=row4.wrf_index, bottom_top_stag=1)
    min_since_run = ye.dt64_2_iso(nds3.XTIME.values)
    print(min_since_run)
    file_name = 'w_{}-{}_t-{}.png'.format(d3, d4, min_since_run)
    mid_name = '{}-{}'.format(d3, d4, min_since_run)
    print(file_name)
    mid_path = os.path.join(plot_path, mid_name)
    print(mid_path)
    os.makedirs(mid_path, exist_ok=True)
    file_path = os.path.join(mid_path, file_name)
    print(file_path)
    fig = plot_double_surface_w(nds3, nds4, d3, d4, par=.2)

    fig.savefig(file_path)

    fig


def plot_double_surface_w(
        nds3, nds4, d3, d4,
        cb_legend='surface W [m s-1]',
        par=.2,
        vm=-2,
        vM=2,
):
    min_since_run = int(nds3.XTIME.values)
    fig, ax = plt.subplots()
    # nds3.plot.imshow()
    # vm=min(fu_.get_fun(xr.DataArray.min))
    # vM=max(fu_.get_fun(xr.DataArray.max))
    # print(nds3.W)
    m1 = nds3.W.plot(x='XLONG', y='XLAT', ax=ax, add_colorbar=False, vmin=vm, vmax=vM)
    nds4.W.plot(x='XLONG', y='XLAT', ax=ax, add_colorbar=False, vmin=vm, vmax=vM)
    fig.set_size_inches(10, 7)
    cb = fig.colorbar(m1)
    cb.set_label(cb_legend)

    gb = wrf.geo_bounds(nds4)

    lam = gb.bottom_left.lat
    lom = gb.bottom_left.lon
    laM = gb.top_right.lat
    loM = gb.top_right.lon

    lad = laM - lam
    lod = loM - lom
    lap = lad * par
    lop = lod * par

    ax.set_ylim(lam - lap, laM + lap)
    ax.set_xlim(lom - lop, loM + lop)
    ax.set_title(
        '{} | t = {}\n din={} | dout={}'.format(
            ye.dt64_2_iso(nds3.XTIME.values),
            min_since_run
            , d3, d4
        )
    )
    ax.scatter(*ye.LOLA_CHC, c='r')
    ax.scatter(*ye.LOLA_LPZ, c='b')
    ax.set_aspect('equal')
    plt.close(fig)
    return fig


def get_cross_section_around_chc(path, idx):
    wrfin = netCDF4.Dataset(path)
    z = wrf.getvar(wrfin, 'z', timeidx=idx)
    wa = wrf.getvar(wrfin, 'wa', timeidx=idx)
    lalo = wrf.CoordPair(
        lat=ye.LOLA_CHC[1],
        lon=ye.LOLA_CHC[0]
    )
    v_cross = wrf.vertcross(wa, z, pivot_point=lalo, angle=90, latlon=True, wrfin=wrfin)
    re = v_cross.xy_loc
    lons = [r.values.item().lon for r in re]
    lons_a = re.copy()
    lons_a.values = np.array(lons)
    lons_a.name = ['lons']
    v_cross = v_cross.assign_coords(lons=lons_a)
    return v_cross


def save_plots_double_domain_w_cross(
        *,
        dic_i,
        ind,
        plot_path,
        d_pairs,
        mega_l,
):
    d3 = d_pairs[dic_i]['d3']
    d4 = d_pairs[dic_i]['d4']
    par = d_pairs[dic_i]['par']
    row3 = mega_l[d3].iloc[ind]
    row4 = mega_l[d4].iloc[ind]

    nds3 = get_cross_section_around_chc(row3.path, row3.wrf_index)
    nds4 = get_cross_section_around_chc(row4.path, row4.wrf_index)
    # print(nds3)
    min_since_run = ye.dt64_2_iso(nds3.Time.values)
    print(min_since_run)
    file_name = 'w_cross_{}-{}_t-{}.png'.format(d3, d4, min_since_run)
    mid_name = '{}-{}'.format(d3, d4, min_since_run)
    print(file_name)
    mid_path = os.path.join(plot_path, mid_name)
    print(mid_path)
    os.makedirs(mid_path, exist_ok=True)
    file_path = os.path.join(mid_path, file_name)
    print(file_path)
    fig = plot_double_cross_w(nds3, nds4, d3, d4, par=par)

    fig.savefig(file_path)

    fig


def plot_double_cross_w(
        nds3, nds4, d3, d4,
        cb_legend='surface W [m s-1]',
        par=.2,
        vm=-9,
        vM=9,
):
    min_since_run = int(nds3.XTIME.values)
    fig, ax = plt.subplots()

    cmap = matplotlib.cm.RdBu_r
    cmap.set_bad('black', 1.)
    m1 = nds3.plot.imshow(x='lons', y='vertical', ax=ax, cmap=cmap, vmin=vm, vmax=vM, add_colorbar=False)
    nds4.plot.imshow(x='lons', y='vertical', ax=ax, cmap=cmap, vmin=vm, vmax=vM, add_colorbar=False)
    ax.set_ylabel('geo height [m]')
    fig.set_size_inches(10, 7)

    cb = fig.colorbar(m1)
    cb.set_label(cb_legend)
    # print(nds4)
    # gb = wrf.geo_bounds(nds4)

    # lam = gb.bottom_left.lat
    lom = nds4.lons[0].values
    # laM = gb.top_right.lat
    loM = nds4.lons[-1].values

    # lad = laM - lam
    lod = loM - lom
    # lap = lad * par
    lop = lod * par

    # ax.set_ylim(lam - lap, laM + lap)
    ax.set_xlim(lom - lop, loM + lop)
    ax.set_title(
        '{} | t = {}\n din={} | dout={}'.format(
            ye.dt64_2_iso(nds3.Time.values),
            min_since_run
            , d3, d4
        )
    )
    # ax.scatter(*ye.LOLA_CHC, c='r')
    # ax.scatter(*ye.LOLA_LPZ, c='b')
    # ax.set_aspect('equal')
    plt.close(fig)
    return fig
