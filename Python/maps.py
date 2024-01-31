#!/usr/bin/env python
# coding: utf-8

import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
import rasterio
import geopandas as gpd
from rasterio.plot import show
import matplotlib.pyplot as plt
#import cartopy.crs as ccrs
import pandas as pd
import numpy as np

import os
#os.environ["PROJ_LIB"]="/Users/cherryleheu/opt/anaconda3/pkgs/proj-8.0.1-h1512c50_0/share/proj/"

#os.chdir('/Users/cherryleheu/Codes/NIDIS-Codes/H-RIP/Python')
os.chdir('./Python')

coastline = gpd.read_file('./shapefiles/Coastline.shp')
coastline = coastline.to_crs("epsg:4326")
ranches = gpd.read_file('./shapefiles/RID.shp')
ranches = ranches.to_crs("epsg:4326")

island_lats = {'BI': {'xlim': [-156.1, -154.8], 'ylim': [18.9, 20.3]}, 'MA':{'xlim': [-156.72, -155.95], 'ylim': [20.55, 21.05]}, 
              'OA':{'xlim': [-158.3,-157.645], 'ylim': [21.25, 21.73]}, 'KA':{'xlim': [-159.8,-159.28], 'ylim': [21.86,22.25]}, 
              'KO':{'xlim': [-156.71,-156.52], 'ylim': [20.49, 20.61]}, 'LA':{'xlim': [-157.08,-156.8], 'ylim': [20.7, 20.95]}, 
              'MO':{'xlim': [-157.32,-156.7], 'ylim': [21.03, 21.23]}, } 



#Get the number of ranches in HRIP
dir_path = '../RID'
count = 0
for path in os.listdir(dir_path):
    if os.path.isdir(os.path.join(dir_path, path)):
        count += 1

#datetime variables
lastMonth = (datetime.today() + relativedelta(months=-1)).strftime("%m")
lastMonthYr = (datetime.today() + relativedelta(months=-1)).strftime("%Y")


with rasterio.open('./rainmaps/2020-/rainfall_'+lastMonthYr+'_'+lastMonth+'.tif') as src:
    rf_mm = src.read(1, masked=True)
    rf_in = rf_mm/25.4
    noData = src.nodata
    with rasterio.open('output_raster_rf.tif', 'w', **src.profile) as dst:
        dst.write(rf_in, 1)
        
rf = rasterio.open('output_raster_rf.tif',noData=noData)



for r in np.arange(1, count):
    y = ranches[ranches.Polygon == f"RID{r:03d}"]
    island = y['IS'].values[0]
    fig, ax = plt.subplots(figsize=(15, 10), dpi=80)
    coastline.plot(ax=ax, facecolor='none', edgecolor='black')
    ranches.plot(ax=ax, facecolor='none',edgecolor='orange',linewidth=2)
    y.plot(ax=ax, facecolor='none',edgecolor='red',linewidth=3)
    rasterio.plot.show(rf, ax=ax,cmap='viridis_r')
    plt.rcParams['font.size'] = '20'
    ax.set_ylim(island_lats[island]['ylim'])
    ax.set_xlim(island_lats[island]['xlim'])
    raster = rasterio.plot.show(rf, ax=ax,cmap='viridis_r')
    im=raster.get_images()[0]
    cbar = fig.colorbar(im,ax=ax)
    cbar.ax.tick_params(labelsize=20) 
    monthName = calendar.month_name[int(lastMonth)]
    plt.title(f'Average Rainfall (in.) - {monthName}, {lastMonthYr}')
    plt.savefig(f'../RID/RID{r:03d}/RID{r:03d}_rf.png',bbox_inches="tight")


with rasterio.open('./temp_monthly_maps/mean/t_month_mean_'+lastMonthYr+'_'+lastMonth+'.tif') as src:
    temp_c = src.read(1, masked=True)
    temp = (temp_c * 9/5) + 32
    noData = src.nodata
    with rasterio.open('output_raster_temp.tif', 'w', **src.profile) as dst:
        dst.write(temp, 1)
        
temp = rasterio.open('output_raster_temp.tif',noData=noData)

for r in np.arange(1, count):
    y = ranches[ranches.Polygon == f"RID{r:03d}"]
    island = y['IS'].values[0]
    fig, ax = plt.subplots(figsize=(15, 10), dpi=80)
    coastline.plot(ax=ax, facecolor='none', edgecolor='black')
    ranches.plot(ax=ax, facecolor='none',edgecolor='orange',linewidth=2)
    y.plot(ax=ax, facecolor='none',edgecolor='red',linewidth=3)
    rasterio.plot.show(temp, ax=ax,cmap='viridis')
    plt.rcParams['font.size'] = '20'
    ax.set_ylim(island_lats[island]['ylim'])
    ax.set_xlim(island_lats[island]['xlim'])
    raster = rasterio.plot.show(temp, ax=ax,cmap='viridis')
    im=raster.get_images()[0]
    cbar = fig.colorbar(im,ax=ax)
    cbar.ax.tick_params(labelsize=20) 
    monthName = calendar.month_name[int(lastMonth)]
    plt.title(f'Average Temperature (C) - {monthName}, {lastMonthYr}')
    plt.savefig(f'../RID/RID{r:03d}/RID{r:03d}_temp.png',bbox_inches="tight")

et = pd.read_csv(f"../RID/RID001/RID001_et.csv", index_col=0)
lastMonth = et['Month'].iloc[-1]
lastMonthYr = et['Year'].iloc[-1]

url = f'./ETMaps/{int(lastMonthYr)}_{int(lastMonth):02d}_et.tif'
with rasterio.open(url) as src:
    et_8 = src.read(1, masked=True)
    et = et_8/8
    noData = src.nodata
    with rasterio.open('output_raster_et.tif', 'w', **src.profile) as dst:
        dst.write(et, 1)
    
et = rasterio.open('output_raster_et.tif',noData=noData)


# In[11]:


vmin = 0  
vmax = 5

for r in np.arange(1, count):
    print(f"RID{r:03d}")
    y = ranches[ranches.Polygon == f"RID{r:03d}"]
    island = y['IS'].values[0]
    fig, ax = plt.subplots(figsize=(15, 10), dpi=80)
    coastline.plot(ax=ax, facecolor='none', edgecolor='black')
    ranches.plot(ax=ax, facecolor='none',edgecolor='orange',linewidth=2)
    y.plot(ax=ax, facecolor='none',edgecolor='red',linewidth=3)
    rasterio.plot.show(et, ax=ax,vmin=vmin, vmax=vmax,cmap='YlGn_r')
    plt.rcParams['font.size'] = '20'
    ax.set_ylim(island_lats[island]['ylim'])
    ax.set_xlim(island_lats[island]['xlim'])
    raster = rasterio.plot.show(et, ax=ax,cmap='YlGn_r')
    im=raster.get_images()[0]
    cbar = fig.colorbar(im,ax=ax)
    cbar.ax.tick_params(labelsize=20) 
    monthName = calendar.month_name[int(lastMonth)]
    plt.title(f'Average Evapotranspiration (mm/day) - {monthName}, {lastMonthYr}')
    plt.savefig(f'../RID/RID{r:03d}/RID{r:03d}_et.png',bbox_inches="tight")


# In[12]:


#datetime variables
ndvi= pd.read_csv(f"../RID/RID001/RID001_ndvi.csv", index_col=0)
lastMonth = ndvi['Month'].iloc[-1]
lastMonthYr = ndvi['Year'].iloc[-1]

url = f'./NDVIMaps/{int(lastMonthYr)}_{int(lastMonth):02d}_ndvi.tif'
with rasterio.open(url) as src:
    ndvi = src.read(1, masked=True)
    noData = src.nodata
    with rasterio.open('output_raster_ndvi.tif', 'w', **src.profile) as dst:
        dst.write(ndvi, 1)
    
ndvi = rasterio.open('output_raster_ndvi.tif',noData=noData) 

vmin = 0
vmax = 1

for r in np.arange(1, count):
    y = ranches[ranches.Polygon == f"RID{r:03d}"]
    island = y['IS'].values[0]
    fig, ax = plt.subplots(figsize=(15, 10), dpi=80)
    coastline.plot(ax=ax, facecolor='none', edgecolor='black')
    ranches.plot(ax=ax, facecolor='none',edgecolor='orange',linewidth=2)
    y.plot(ax=ax, facecolor='none',edgecolor='red',linewidth=3)
    rasterio.plot.show(ndvi, ax=ax,vmin=vmin,vmax=vmax,cmap='RdYlGn')
    plt.rcParams['font.size'] = '20'
    ax.set_ylim(island_lats[island]['ylim'])
    ax.set_xlim(island_lats[island]['xlim'])
    raster = rasterio.plot.show(ndvi, ax=ax,cmap='RdYlGn')
    im=raster.get_images()[0]
    cbar = fig.colorbar(im,ax=ax)
    cbar.ax.tick_params(labelsize=20) 
    monthName = calendar.month_name[int(lastMonth)]
    plt.title(f'Average NDVI - {monthName}, {lastMonthYr}')
    plt.savefig(f'../RID/RID{r:03d}/RID{r:03d}_ndvi.png',bbox_inches="tight")
