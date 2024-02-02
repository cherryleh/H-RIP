#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
#Directory here
#os.chdir('/Users/cherryleheu/Codes/NIDIS-Codes/H-RIP/Python')
#os.chdir('./Python')

#Cherryle's Google Earth Engine Service Account
import ee
service_account = 'my-service-account@...gserviceaccount.com'

#GEE CREDENTIALS GO HERE
credentials = ee.ServiceAccountCredentials(service_account, '/keys/cheu-361201-8e8573aa9c7a.json')
ee.Initialize(credentials)

import numpy as np
from calendar import monthrange
import calendar
import requests
from zipfile import ZipFile
from datetime import datetime
from dateutil.relativedelta import *
import pandas as pd
import geopandas as gpd
import rasterio
from rasterstats import zonal_stats


#Geometric points 
hi = ee.Geometry.Polygon( [[-160.53524634027852,18.677598565033925],
                         [-153.56991430902852,18.490156020569056],
                         [-153.72372290277852,22.360360725173077], 
                         [-160.61215063715352,22.43146437219467],
                         [-160.53524634027852,18.677598565033925]])

#Last month's year and month
now = datetime.now()
i = int((now + relativedelta(months=-1)).strftime("%Y"))
j = int((now + relativedelta(months=-1)).strftime("%m"))

#Month and year last logged in the ET csv
a = pd.read_csv('../RID/RID001/RID001_et.csv')
l = datetime.strptime(a['datetime'].iloc[-1], '%Y-%m-%d').month
k = datetime.strptime(a['datetime'].iloc[-1], '%Y-%m-%d').year

#Create a list of dates to process
datem_et = datetime.today().strftime("%m")
monthInd_et = -int(datem_et)+1
dates_et = pd.date_range(f'{k}-{l}',f'{i}-{j}', freq='MS').strftime("%Y-%m").tolist()

#Get the last available day for dataset
collection = ee.ImageCollection('MODIS/061/MOD16A2')
lastDate = ee.Date(collection.sort('system:time_start',False).first().get('system:time_start')).format('Y-M').getInfo()

#Remove the dates from list if it is unavailable in GEE
b = dates_et.copy()
b.reverse()

for date in np.arange(len(dates_et)):
    if datetime.strptime(b[date], "%Y-%m")>datetime.strptime(lastDate, "%Y-%m"):
        dates_et.remove(b[date])
    elif datetime.strptime(b[date], "%Y-%m")==datetime.strptime(lastDate, "%Y-%m"):
        break
        
#Month and year last logged in ET csv
a = pd.read_csv('../RID/RID001/RID001_ndvi.csv')
l = datetime.strptime(a['datetime'].iloc[-1], '%Y-%m-%d').month
k = datetime.strptime(a['datetime'].iloc[-1], '%Y-%m-%d').year

datem_ndvi = datetime.today().strftime("%m")
monthInd_ndvi = -int(datem_ndvi)+1
dates_ndvi = pd.date_range(f'{k}-{l}',f'{i}-{j}', freq='MS').strftime("%Y-%m").tolist()

#Get the last date available from the GEE dataset
collection = ee.ImageCollection('MODIS/061/MOD13Q1')
lastDate = ee.Date(collection.sort('system:time_start',False).first().get('system:time_start')).format('Y-M').getInfo()

#Remove the dates from list if it is unavailable in GEE
b = dates_ndvi.copy()
b.reverse()

for i in np.arange(len(dates_ndvi)):
    if datetime.strptime(b[i], "%Y-%m")>datetime.strptime(lastDate, "%Y-%m"):
        dates_ndvi.remove(b[i])
    elif datetime.strptime(b[i], "%Y-%m")==datetime.strptime(lastDate, "%Y-%m"):
        break

#Ranch count
dir_path = '../RID'
count = 0
for path in os.listdir(dir_path):
    if os.path.isdir(os.path.join(dir_path, path)):
        count += 1


ranches = np.arange(1,count+1)

#Download the monthly data tifs
for date in dates_et:
    print(dates_et)
    i = int(date[0:4])
    j = int(date[5:7])
    dataset = ee.ImageCollection('MODIS/061/MOD16A2')
    num_days = monthrange(i,j)[1]
    dataset = dataset.select('ET','ET_QC').filterDate(f"{date}-01", f"{date}-{num_days}")
    hi_dataset_img = dataset.mean()
    hi_dataset_img = hi_dataset_img.select('ET').multiply(0.1)
    hi_link = hi_dataset_img.getDownloadURL({
        'scale': 500,
        'crs': 'EPSG:4326',
        'fileFormat': 'GeoTIFF',
        'region': hi})
    r = requests.get(hi_link, allow_redirects=True)
    open(f'./ETmaps/{i}_{j:02d}_et.zip', 'wb').write(r.content)
    if os.path.isfile(f'./ETmaps/{i}_{j:02d}_et.zip') == True:
        with ZipFile(f'./ETmaps/{i}_{j:02d}_et.zip','r') as zipObj:
           zipObj.extractall('./ETmaps')
        old_hi = './ETmaps/download.et.tif'
        new_hi = f'./ETmaps/{i}_{j:02d}_et.tif'
        os.rename(old_hi, new_hi)
        print(new_hi)
    else:
        break

#Delete the Zip Files
dir_name = "./ETmaps"
test = os.listdir(dir_name)

for item in test:
    if item.endswith(".zip"):
        os.remove(os.path.join(dir_name, item))
        
#Create an ET file for each ranch
for r in ranches:
    et = pd.read_csv(f"../RID/RID{r:03d}/RID{r:03d}_et.csv",index_col=0)
    ranchshp = gpd.read_file('./shapefiles/RID.shp',rows=slice(r-1, r))
    #ranch = ranchshp['Polygon'].iloc[0]
    for date in dates_et:
        i = int(date[0:4])
        j = int(date[5:7])
        with rasterio.open(f'./ETmaps/{i}_{j:02d}_ET.tif') as src:
            affine = src.transform
            array = src.read(1)
            nodata = src.nodata
            df_zonal_stats = pd.DataFrame(zonal_stats(ranchshp, array, affine=affine,nodata=nodata,stats = ['mean']))
        ET= df_zonal_stats['mean'].iloc[0]
        
        et_df = et.loc[(et['Month']==j) & (et['Year'] == i)]
        if et_df.empty:
            new_row = pd.DataFrame({'Year':i,'Month':j,'ET':ET/8},index=[0])
            et=pd.concat([et, new_row],ignore_index=True)
        else: 
            et['ET'] = np.where((et['Month'] == j) & (et['Year'] == i), ET/8, et['ET'])
    et['datetime']=pd.date_range('1/1/2001',str(j)+'/1/'+str(i),freq='MS')
    et.to_csv(f'../RID/RID{r:03d}/RID{r:03d}_et.csv')
    
#average monthly
def et_avg(arr):
    arr = arr.drop(['datetime'], axis=1)
    etdf = arr.groupby(['Month'],as_index=False).mean()
    etdf['Month'] = etdf['Month'].astype(np.uint8).apply(lambda x: calendar.month_name[x])
    etdf['rolledMonth'] = np.roll(etdf.Month, -a)
    etdf['rolledET'] = np.roll(etdf.ET, -a)
    etdf = etdf.rename(columns={"ET": "oldET", "rolledET": "ET","Month":"oldMonth","rolledMonth":"Month"})
    return etdf

#last 12 months
def et_12m(arr):
    et12m = arr.copy()
    et12m['Month'] = et12m['Month'].astype(np.uint8).apply(lambda x: calendar.month_name[x]) 
    et12m = et12m.tail(12)
    return et12m

for r in ranches:
    et = pd.read_csv(f'../RID/RID{r:03d}/RID{r:03d}_et.csv',index_col=0)
    a = int(et['Month'].iloc[-1])
    etdf=et_avg(et)
    etdf=etdf.drop(['Year'],axis=1)
    et12m=et_12m(et)
    et12m=et12m.drop(['Year','datetime'],axis=1)
    etdf.to_csv(f'../RID/RID{r:03d}/RID{r:03d}_et_month.csv') 
    et12m.to_csv(f'../RID/RID{r:03d}/RID{r:03d}_et_12m.csv')
    
for date in dates_ndvi:
    i = int(date[0:4])
    j = int(date[5:7])
    dataset = ee.ImageCollection('MODIS/061/MOD13Q1')
    num_days = monthrange(i,j)[1]
    dataset = dataset.select('NDVI').filterDate(f"{date}-01", f"{date}-{num_days}")
    hi_dataset_img = dataset.mean()
    hi_dataset_img = hi_dataset_img.select('NDVI').multiply(0.0001)
    hi_link = hi_dataset_img.getDownloadURL({
        'scale': 250,
        'crs': 'EPSG:4326',
        'fileFormat': 'GeoTIFF',
        'region': hi})
    r = requests.get(hi_link, allow_redirects=True)
    open(f'./NDVImaps/{i}_{j:02d}_ndvi.zip', 'wb').write(r.content)
    with ZipFile(f'./NDVImaps/{i}_{j:02d}_ndvi.zip','r') as zipObj:
       zipObj.extractall('./NDVImaps')
    old_hi = './NDVImaps/download.ndvi.tif'
    new_hi = f'./NDVImaps/{i}_{j:02d}_ndvi.tif'
    os.rename(old_hi, new_hi)

dir_name = "./NDVImaps"
test = os.listdir(dir_name)

for item in test:
    if item.endswith(".zip"):
        os.remove(os.path.join(dir_name, item))
        
ranches = np.arange(1,count)
for r in ranches:
    ndvi = pd.read_csv(f"../RID/RID{r:03d}/RID{r:03d}_ndvi.csv",index_col=0)
    ranchshp = gpd.read_file('./shapefiles/RID.shp',rows=slice(r-1, r))
    for date in dates_ndvi:
        i = int(date[0:4])
        j = int(date[5:7])
        with rasterio.open(f'./NDVImaps/{i}_{j:02d}_ndvi.tif') as src:
            affine = src.transform
            array = src.read(1)
            nodata = src.nodata
            df_zonal_stats = pd.DataFrame(zonal_stats(ranchshp, array, affine=affine,nodata=nodata,stats = ['mean']))
        NDVI= df_zonal_stats['mean'].iloc[0]
        ndvi_df = ndvi.loc[(ndvi['Month']==j) & (ndvi['Year'] == i)]
        if ndvi_df.empty:
            new_row = pd.DataFrame({'Year':i,'Month':j,'NDVI':NDVI},index=[0])
            ndvi=pd.concat([ndvi, new_row],ignore_index=True)
        else: 
            ndvi['NDVI'] = np.where((ndvi['Month'] == j) & (ndvi['Year'] == i), NDVI, ndvi['NDVI'])
    ndvi['datetime']=pd.date_range('2/1/2000',str(j)+'/1/'+str(i),freq='MS')
    ndvi.to_csv(f'../RID/RID{r:03d}/RID{r:03d}_NDVI.csv')
    
#average monthly
def ndvi_avg(arr):
    arr = arr.drop(['datetime'], axis=1)
    ndvidf = arr.groupby(['Month'],as_index=False).mean()
    ndvidf['Month'] = ndvidf['Month'].astype(np.uint8).apply(lambda x: calendar.month_name[x])
    ndvidf['rolledMonth'] = np.roll(ndvidf.Month, -a)
    ndvidf['rolledNDVI'] = np.roll(ndvidf.NDVI, -a)
    ndvidf = ndvidf.rename(columns={"NDVI": "oldNDVI", "rolledNDVI": "NDVI","Month":"oldMonth","rolledMonth":"Month"})
    return ndvidf

#last 12 months
def ndvi_12m(arr):
    ndvi12m = arr.copy()
    ndvi12m['Month'] = ndvi12m['Month'].astype(np.uint8).apply(lambda x: calendar.month_name[x]) 
    ndvi12m = ndvi12m.tail(12)
    return ndvi12m

for r in ranches:
    ndvi = pd.read_csv(f'../RID/RID{r:03d}/RID{r:03d}_ndvi.csv',index_col=0)
    a = int(ndvi['Month'].iloc[-1])
    ndvidf=ndvi_avg(ndvi)
    ndvi12m=ndvi_12m(ndvi)
    ndvidf=ndvidf.drop(['Year'],axis=1)
    ndvi12m=ndvi12m.drop(['Year','datetime'],axis=1)
    ndvidf.to_csv(f'../RID/RID{r:03d}/RID{r:03d}_ndvi_month.csv') 
    ndvi12m.to_csv(f'../RID/RID{r:03d}/RID{r:03d}_ndvi_12m.csv')
