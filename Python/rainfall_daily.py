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

dir_path = '../RID'
count = 0
for path in os.listdir(dir_path):
    if os.path.isdir(os.path.join(dir_path, path)):
        count += 1

mean_url = f'https://ikeauth.its.hawaii.edu/files/v2/download/public/system/ikewai-annotated-data/HCDP/production/rainfall/new/day/statewide/data_map/{yest_year}/{yest_mon:02d}/rainfall_new_day_statewide_data_map_{yest_year}_{yest_mon:02d}_{yest_day:02d}.tif'
r = requests.get(mean_url)
file=f'./rain_daily_maps/{yest_year}_{yest_mon:02d}_{yest_day:02d}.tif'
open(file, 'wb').write(r.content)

for r in np.arange(1,count+1):
    ranchshp = gpd.read_file('./shapefiles/RID.shp',rows=slice(r-1, r))
    with rasterio.open(f'./rain_daily_maps/{yest_year}_{yest_mon:02d}_{yest_day:02d}.tif') as src:
        affine = src.transform
        array = src.read(1)
        df_zonal_stats = pd.DataFrame(zonal_stats(ranchshp, array, affine=affine,nodata=src.nodata,stats = ['mean']))
    rf = (df_zonal_stats['mean'].iloc[0])/25.4
    with open(f'../RID/RID{r:03d}/RID{r:03d}_rf_d.txt', 'w') as f:
        f.write(str(rf)+f'\n{yest_year}\n{yest_mon}\n{yest_day}') 

for r in np.arange(1,count+1):
    if yest_day == 1:
        os.remove(f'../RID/RID{r:03d}/RID{r:03d}_rf_daily_last_month.csv')
        os.rename(f'../RID/RID{r:03d}/RID{r:03d}_rf_daily_this_month.csv',f'../RID/RID{r:03d}/RID{r:03d}_rf_daily_last_month.csv')
        columns = ['Year','Month','Day','RF_in']
        df = pd.DataFrame(columns=columns)
        df.to_csv(f'../RID/RID{r:03d}/RID{r:03d}_rf_daily_this_month.csv',index=False)

for r in np.arange(1,count+1):
    try:
        rf_df = pd.read_csv(f'../RID/RID{r:03d}/RID{r:03d}_rf_daily_this_month.csv')
        ranchshp = gpd.read_file('./shapefiles/RID.shp',rows=slice(r-1, r))
        with rasterio.open(f'./rain_daily_maps/{yest_year}_{yest_mon:02d}_{yest_day:02d}.tif') as src:
            affine = src.transform
            array = src.read(1)
            df_zonal_stats = pd.DataFrame(zonal_stats(ranchshp, array, affine=affine,nodata=src.nodata,stats = ['mean']))
        rf = (df_zonal_stats['mean'].iloc[0])/25.4
        new_row = pd.DataFrame({'Year':yest_year,'Month':yest_mon,'Day':yest_day,'RF_in':rf},index=[0])
        csv=pd.concat([rf_df, new_row],ignore_index=True)
        csv.to_csv(f'../RID/RID{r:03d}/RID{r:03d}_rf_daily_this_month.csv',index=False)
        with open(f'../RID/RID{r:03d}/RID{r:03d}_consec_dry_days.txt', 'r') as f:
            consec_days = int(f.read())
        if rf<0.0393701:
            consec_days+=1
        else:
            consec_days = 0
        with open(f'../RID/RID{r:03d}/RID{r:03d}_consec_dry_days.txt', 'w') as f:
            f.write(str(consec_days))
    #If there is an error, mark the day's data as Nan. At the end of the month, the value will be filled
    except Exception as e:
        new_row = pd.DataFrame({'Year':yest_year,'Month':yest_mon,'Day':yest_day,'RF_in':np.nan},index=[0])
        csv=pd.concat([rf_df, new_row],ignore_index=True)
        csv.to_csv(f'../RID/RID{r:03d}/RID{r:03d}_rf_daily_this_month.csv',index=False)