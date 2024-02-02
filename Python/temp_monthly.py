import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterstats import zonal_stats
from datetime import datetime
from dateutil.relativedelta import relativedelta
import requests
import calendar

import os
#os.chdir('/Users/cherryleheu/Codes/NIDIS-Codes/H-RIP/Python')

#Get the number of ranches in HRIP
dir_path = '../RID'
count = 0
for path in os.listdir(dir_path):
    if os.path.isdir(os.path.join(dir_path, path)):
        count += 1

lastMonth = (datetime.today() + relativedelta(months=-1)).strftime("%m")
lastMonthYr = (datetime.today() + relativedelta(months=-1)).strftime("%Y")

#Mean temperature download
url = 'https://ikeauth.its.hawaii.edu/files/v2/download/public/system/ikewai-annotated-data/HCDP/production/temperature/mean/month/statewide/data_map/'+lastMonthYr+'/temperature_mean_month_statewide_data_map_'+lastMonthYr+'_'+lastMonth+'.tif'

r = requests.get(url)
file=f"./temp_monthly_maps/mean/{lastMonthYr}_{lastMonth}_t_month_mean.tif"
open(file, 'wb').write(r.content)

dir_path = '../RID'
count = 0
for path in os.listdir(dir_path):
    if os.path.isdir(os.path.join(dir_path, path)):
        count += 1

ranches = np.arange(1,count+1)

for r in ranches:
    ranchshp = gpd.read_file('./shapefiles/RID.shp',rows=slice(r-1, r))
    ranch = ranchshp['Polygon'].iloc[0]
    csv = pd.read_csv('../RID/'+ranch+'/'+ranch+'_temp.csv',index_col=[0])
    with rasterio.open(file) as src:
        affine = src.transform
        array = src.read(1)
        noData=src.nodata
        df_zonal_stats = pd.DataFrame(zonal_stats(ranchshp, array, affine=affine,nodata=noData,stats = ['mean']))
    temp_c= df_zonal_stats['mean'].iloc[0]
    temp_f = 9/5*temp_c+32
    new_row = pd.DataFrame({'Year':int(lastMonthYr),'Month':int(lastMonth),'Temp':temp_f},index=[0])
    csv=pd.concat([csv, new_row],ignore_index=True)
    csv['datetime']=pd.date_range('1/1/1990',lastMonth+'/01/'+lastMonthYr,freq='MS')
    csv.to_csv('../RID/'+ranch+'/'+ranch+'_temp.csv')


def temp_avg(arr):
    tdf = arr.groupby(['Month'],as_index=False)['Temp'].mean()
    tdf['Month'] = tdf['Month'].astype(np.uint8).apply(lambda x: calendar.month_name[x])
    tdf['rolledMonth'] = np.roll(tdf.Month, monthInd) 
    tdf['NewTemp'] = np.roll(tdf.Temp, monthInd)
    tdf = tdf.rename(columns={"Month":"oldMonth","Temp":"OldTemp","NewTemp": "Temp","rolledMonth":"Month"})
    return tdf

def temp_12m(arr):
    tdf12m = arr
    tdf12m['Month'] = t.tail(12)['Month'].astype(np.uint8).apply(lambda x: calendar.month_name[x])
    tdf12m = arr.tail(12)
    return tdf12m

for r in ranches:
    temp = pd.read_csv(f"../RID/RID{r:03d}/RID{r:03d}_temp.csv",index_col=0)    
    tdf=temp_avg(temp)
    tdf12m=temp_12m(temp)
    tdf12m=tdf12m.drop(['Year','datetime'],axis=1)
    tdf.to_csv(f'../RID/RID{r:03d}/RID{r:03d}_t_month.csv') 
    tdf12m.to_csv(f'../RID/RID{r:03d}/RID{r:03d}_t_12m.csv')
    


#Minimum temperature download
url = 'https://ikeauth.its.hawaii.edu/files/v2/download/public/system/ikewai-annotated-data/HCDP/production/temperature/min/month/statewide/data_map/'+lastMonthYr+'/temperature_min_month_statewide_data_map_'+lastMonthYr+'_'+lastMonth+'.tif'

r = requests.get(url)
file_min=f"./temp_monthly_maps/min/{lastMonthYr}_{lastMonth}_t_month_min.tif"
open(file_min, 'wb').write(r.content)

for r in ranches:
    ranchshp = gpd.read_file('./shapefiles/RID.shp',rows=slice(r-1, r))
    ranch = ranchshp['Polygon'].iloc[0]
    csv = pd.read_csv('../RID/'+ranch+'/'+ranch+'_temp_min.csv',index_col=[0])
    with rasterio.open(file_min) as src:
        affine = src.transform
        array = src.read(1)
        noData=src.nodata
        df_zonal_stats = pd.DataFrame(zonal_stats(ranchshp, array, affine=affine,nodata=noData,stats = ['mean']))
    temp_c= df_zonal_stats['mean'].iloc[0]
    temp_f = 9/5*temp_c+32
    new_row = pd.DataFrame({'Year':int(lastMonthYr),'Month':int(lastMonth),'Temp':temp_f},index=[0])
    csv=pd.concat([csv, new_row],ignore_index=True)
    csv['datetime']=pd.date_range('1/1/1990',lastMonth+'/01/'+lastMonthYr,freq='MS')
    csv.to_csv('../RID/'+ranch+'/'+ranch+'_temp_min.csv')

#Maximum temperature download
    
url = 'https://ikeauth.its.hawaii.edu/files/v2/download/public/system/ikewai-annotated-data/HCDP/production/temperature/max/month/statewide/data_map/'+lastMonthYr+'/temperature_max_month_statewide_data_map_'+lastMonthYr+'_'+lastMonth+'.tif'

r = requests.get(url)
file_max=f"./temp_monthly_maps/max/{lastMonthYr}_{lastMonth}_t_month_max.tif"
open(file_max, 'wb').write(r.content)

for r in ranches:
    ranchshp = gpd.read_file('./shapefiles/RID.shp',rows=slice(r-1, r))
    ranch = ranchshp['Polygon'].iloc[0]
    csv = pd.read_csv('../RID/'+ranch+'/'+ranch+'_temp_max.csv',index_col=[0])
    with rasterio.open(file_max) as src:
        affine = src.transform
        array = src.read(1)
        noData=src.nodata
        df_zonal_stats = pd.DataFrame(zonal_stats(ranchshp, array, affine=affine,nodata=noData,stats = ['mean']))
    temp_c= df_zonal_stats['mean'].iloc[0]
    temp_f = 9/5*temp_c+32
    new_row = pd.DataFrame({'Year':int(lastMonthYr),'Month':int(lastMonth),'Temp':temp_f},index=[0])
    csv=pd.concat([csv, new_row],ignore_index=True)
    csv['datetime']=pd.date_range('1/1/1990',lastMonth+'/01/'+lastMonthYr,freq='MS')
    csv.to_csv('../RID/'+ranch+'/'+ranch+'_temp_max.csv')


