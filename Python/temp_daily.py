#!/usr/bin/env python
# coding: utf-8


import os
#os.chdir('/Users/cherryleheu/Codes/NIDIS-Codes/H-RIP/Python')
os.chdir('./Python')

import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
import rasterio
import pandas as pd
from rasterstats import zonal_stats
import geopandas as gpd
import time
import numpy as np


yest_year, yest_mon, yest_day = int((datetime.today() + relativedelta(days=-1)).strftime("%Y")),int((datetime.today() + relativedelta(days=-1)).strftime("%m")),int((datetime.today() + relativedelta(days=-1)).strftime("%d"))
#lastMonthYr = (datetime.today() + relativedelta(months=-1)).strftime("%Y")

#yest_year, yest_mon, yest_day = (datetime.today() + relativedelta(days=-1)).strftime("%Y"),(datetime.today() + relativedelta(days=-1)).strftime("%m"),(datetime.today() + relativedelta(days=-1)).strftime("%d")
#lastMonthYr = (datetime.today() + relativedelta(months=-1)).strftime("%Y")


mean_url = f'https://ikeauth.its.hawaii.edu/files/v2/download/public/system/ikewai-annotated-data/HCDP/production/temperature/mean/day/statewide/data_map/{yest_year}/{yest_mon:02d}/temperature_mean_day_statewide_data_map_{yest_year}_{yest_mon:02d}_{yest_day:02d}.tif'
r = requests.get(mean_url)
file=f'./temp_daily_maps/mean/{yest_year}_{yest_mon:02d}_{yest_day:02d}_mean.tif'
open(file, 'wb').write(r.content)

max_url = f'https://ikeauth.its.hawaii.edu/files/v2/download/public/system/ikewai-annotated-data/HCDP/production/temperature/max/day/statewide/data_map/{yest_year}/{yest_mon:02d}/temperature_max_day_statewide_data_map_{yest_year}_{yest_mon:02d}_{yest_day:02d}.tif'
r = requests.get(max_url)
file=f'./temp_daily_maps/max/{yest_year}_{yest_mon:02d}_{yest_day:02d}_max.tif'
open(file, 'wb').write(r.content)


min_url = f'https://ikeauth.its.hawaii.edu/files/v2/download/public/system/ikewai-annotated-data/HCDP/production/temperature/min/day/statewide/data_map/{yest_year}/{yest_mon:02d}/temperature_min_day_statewide_data_map_{yest_year}_{yest_mon:02d}_{yest_day:02d}.tif'
r = requests.get(min_url)
file=f'./temp_daily_maps/min/{yest_year}_{yest_mon:02d}_{yest_day:02d}_min.tif'
open(file, 'wb').write(r.content)


#Get the number of ranches in HRIP
dir_path = '../RID'
count = 0
for path in os.listdir(dir_path):
    if os.path.isdir(os.path.join(dir_path, path)):
        count += 1




a = ['mean','max','min']
temp = {}

for r in np.arange(1,count+1):
    for n in a:
        ranchshp = gpd.read_file('./shapefiles/RID.shp',rows=slice(r-1, r))
        with rasterio.open(f'./temp_daily_maps/{n}/{yest_year}_{yest_mon:02d}_{yest_day:02d}_{n}.tif') as src:
            affine = src.transform
            array = src.read(1)
            df_zonal_stats = pd.DataFrame(zonal_stats(ranchshp, array, affine=affine,nodata=-9999,stats = ['mean']))
        temp[n]=9/5*df_zonal_stats['mean'].iloc[0]+32 
    with open(f'../RID/RID{r:03d}/RID{r:03d}_temp_d.txt', 'w') as f:
        f.write(repr(temp['mean'])+'\n'+repr(temp['max'])+'\n'+repr(temp['min'])+f'\n{yest_year}\n{yest_mon}\n{yest_day}') 



a = os.listdir('./temp_daily_maps/mean/')
count = len(a)-1

while count>5:
    count = len(a)-1
    oldest_file = sorted([ "./temp_daily_maps/mean/"+f for f in os.listdir("./temp_daily_maps/mean/")], key=os.path.getctime)[0]
    os.remove(oldest_file)
    a = os.listdir('./temp_daily_maps/mean')
    count = len(a)-1
    if count ==5:
        break
        
    

a = os.listdir('./temp_daily_maps/max/')
count = len(a)-1

while count>5:
    oldest_file = sorted([ "./temp_daily_maps/max/"+f for f in os.listdir("./temp_daily_maps/max/")], key=os.path.getctime)[0]
    os.remove(oldest_file)
    a = os.listdir('./temp_daily_maps/max')
    count = len(a)-1
    if count ==5:
        break
        
    

a = os.listdir('./temp_daily_maps/min/')
count = len(a)-1

while count>5:
    oldest_file = sorted([ "./temp_daily_maps/min/"+f for f in os.listdir("./temp_daily_maps/min/")], key=os.path.getctime)[0]
    os.remove(oldest_file)
    a = os.listdir('./temp_daily_maps/min')
    count = len(a)-1
    if count ==5:
        break
        
    
'''temp = {}
a = ['mean','max','min']
temp = {}

for r in np.arange(1,63):
    for n in a:
        ranchshp = gpd.read_file('./shapefiles/ranches.shp',rows=slice(r-1, r))
        with rasterio.open(f'./temp/{n}/{yest_year}_{yest_mon:02d}_{yest_day:02d}_{n}.tif') as src:
            affine = src.transform
            array = src.read(1)
            df_zonal_stats = pd.DataFrame(zonal_stats(ranchshp, array, affine=affine,nodata=-9999,stats = ['mean']))
        temp[n]=9/5*df_zonal_stats['mean'].iloc[0]+32 
        if temp[n]<0:
            print(r)
            print(temp[n])
    #with open(f'../ranches/RS{r:02d}/RS{r:02d}_temp_d.txt', 'w') as f:
        #f.write(repr(temp['mean'])+'\n'+repr(temp['max'])+'\n'+repr(temp['min'])+f'\n{yest_year}\n{yest_mon}\n{yest_day}') 

'''
