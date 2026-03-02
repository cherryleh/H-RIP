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

today = datetime.today()
yesterday = today + relativedelta(days=-1)

yest_year, yest_mon, yest_day = int(yesterday.strftime("%Y")), int(yesterday.strftime("%m")), int(yesterday.strftime("%d"))
do_rollover = (yesterday.month != today.month)
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



for r in np.arange(1, count + 1):
    if do_rollover:
        last_path = f'../RID/RID{r:03d}/RID{r:03d}_rf_daily_last_month.csv'
        this_path = f'../RID/RID{r:03d}/RID{r:03d}_rf_daily_this_month.csv'

        # remove old "last month" if it exists
        if os.path.exists(last_path):
            os.remove(last_path)

        # move "this month" -> "last month" if it exists
        if os.path.exists(this_path):
            os.rename(this_path, last_path)

        # create fresh "this month"
        columns = ['Year', 'Month', 'Day', 'RF_in']
        pd.DataFrame(columns=columns).to_csv(this_path, index=False)

for r in np.arange(1, count + 1):
    this_path = f'../RID/RID{r:03d}/RID{r:03d}_rf_daily_this_month.csv'

    # load (or initialize) monthly df
    if os.path.exists(this_path):
        try:
            rf_df = pd.read_csv(this_path)
        except Exception:
            rf_df = pd.DataFrame(columns=['Year','Month','Day','RF_in'])
    else:
        rf_df = pd.DataFrame(columns=['Year','Month','Day','RF_in'])

    try:
        ranchshp = gpd.read_file('./shapefiles/RID.shp', rows=slice(r-1, r))
        with rasterio.open(f'./rain_daily_maps/{yest_year}_{yest_mon:02d}_{yest_day:02d}.tif') as src:
            df_zonal_stats = pd.DataFrame(
                zonal_stats(ranchshp, src.read(1), affine=src.transform, nodata=src.nodata, stats=['mean'])
            )
        rf = (df_zonal_stats['mean'].iloc[0]) / 25.4
    except Exception:
        rf = np.nan

    # remove any existing row for the same date (prevents duplicate stacking on reruns)
    if len(rf_df) > 0:
        mask_same_day = (
            (rf_df['Year'] == yest_year) &
            (rf_df['Month'] == yest_mon) &
            (rf_df['Day'] == yest_day)
        )
        rf_df = rf_df.loc[~mask_same_day].copy()

    # append new row + save
    new_row = pd.DataFrame({'Year': yest_year, 'Month': yest_mon, 'Day': yest_day, 'RF_in': rf}, index=[0])
    out = pd.concat([rf_df, new_row], ignore_index=True)
    out.to_csv(this_path, index=False)