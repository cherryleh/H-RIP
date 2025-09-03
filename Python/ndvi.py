import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterstats import zonal_stats
from datetime import datetime
from dateutil.relativedelta import relativedelta
import requests
import calendar
from calendar import monthrange

import os
#os.chdir('/Users/cherryleheu/Codes/NIDIS-Codes/H-RIP/Python')
os.chdir('./Python')
#Get the number of ranches in HRIP
dir_path = '../RID'
count = 0
for path in os.listdir(dir_path):
    if os.path.isdir(os.path.join(dir_path, path)):
        count += 1

lastMonth = (datetime.today() + relativedelta(months=-1)).strftime("%m")
lastMonthYr = (datetime.today() + relativedelta(months=-1)).strftime("%Y")

datem = datetime.today().strftime("%m")
monthInd = -int(datem)+1

last_day = calendar.monthrange(int(lastMonthYr), int(lastMonth))[1]

# step backwards until day 1
for d in range(last_day, 0, -1):
    url = f"https://ikeauth.its.hawaii.edu/files/v2/download/public/system/ikewai-annotated-data/HCDP/production/ndvi_modis/day/statewide/data_map/{lastMonthYr}/{lastMonth}/ndvi_modis_day_statewide_data_map_{lastMonthYr}_{lastMonth}_{d:02d}.tif"
    r = requests.get(url)

    if r.status_code == 200:
        file = f"./NDVI_maps/NDVI_{lastMonthYr}_{lastMonth}.tif"
        with open(file, "wb") as f:
            f.write(r.content)
        break 

dir_path = '../RID'
count = 0
for path in os.listdir(dir_path):
    if os.path.isdir(os.path.join(dir_path, path)):
        count += 1

ranches = np.arange(1,count+1)

for r in ranches:
    ranchshp = gpd.read_file('./shapefiles/RID.shp',rows=slice(r-1, r))
    ranch = ranchshp['Polygon'].iloc[0]
    csv = pd.read_csv('../RID/'+ranch+'/'+ranch+'_ndvi.csv')
    with rasterio.open(file) as src:
        affine = src.transform
        array = src.read(1)
        noData=src.nodata
        df_zonal_stats = pd.DataFrame(zonal_stats(ranchshp, array, affine=affine,nodata=noData,stats = ['mean']))
    ndvi= df_zonal_stats['mean'].iloc[0]
    new_row = pd.DataFrame({'Year':int(lastMonthYr),'Month':int(lastMonth),'NDVI':ndvi},index=[0])
    csv=pd.concat([csv, new_row],ignore_index=True)
    csv['datetime']=pd.date_range('4/1/2000',lastMonth+'/01/'+lastMonthYr,freq='MS')
    csv.to_csv('../RID/'+ranch+'/'+ranch+'_ndvi.csv', index=False)


def ndvi_avg(arr):
    arr = arr.drop(['datetime'], axis=1)
    ndvidf = arr.groupby(['Month'],as_index=False).mean()
    ndvidf['Month'] = ndvidf['Month'].astype(np.uint8).apply(lambda x: calendar.month_name[x])
    ndvidf['rolledMonth'] = np.roll(ndvidf.Month, monthInd)
    ndvidf['rolledNDVI'] = np.roll(ndvidf.NDVI, monthInd)
    ndvidf=ndvidf.drop(['Year'],axis=1)
    ndvidf = ndvidf.rename(columns={"Month":"oldMonth","rolledMonth":"Month","NDVI":"oldNDVI","rolledNDVI":"NDVI"})
    return ndvidf

#last 12 months
def ndvi_12m(arr):
    ndvi12m = arr.copy()
    ndvi12m['Month'] = ndvi12m['Month'].astype(np.uint8).apply(lambda x: calendar.month_name[x])
    ndvi12m = ndvi12m.tail(12)
    return ndvi12m

for r in ranches:
    ndvi = pd.read_csv(f"../RID/RID{r:03d}/RID{r:03d}_ndvi.csv")    
    ndvidf=ndvi_avg(ndvi)
    ndvi12m=ndvi_12m(ndvi)
    ndvi12m=ndvi12m.drop(['Year','datetime'],axis=1)
    ndvidf.to_csv(f'../RID/RID{r:03d}/RID{r:03d}_ndvi_month.csv', index=False) 
    ndvi12m.to_csv(f'../RID/RID{r:03d}/RID{r:03d}_ndvi_12m.csv')


