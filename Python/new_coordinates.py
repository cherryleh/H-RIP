#!/usr/bin/env python
# coding: utf-8

# In[218]:


import os
#Directory here
#os.chdir('/Users/cherryleheu/Codes/NIDIS-Codes/H-RIP/Python')
os.chdir('./Python')

import ee
service_account = 'my-service-account@...gserviceaccount.com'
#Key goes here
credentials = ee.ServiceAccountCredentials(service_account, '')
ee.Initialize(credentials)



import geopandas as gpd
import shapely 
from shapely.geometry import Point
import matplotlib.pyplot as plt
from dms2dec.dms_convert import dms2dec
import numpy as np
import pandas as pd
import rasterio
from rasterio.plot import show
from rasterstats import zonal_stats
from datetime import datetime, timedelta
import calendar
from dateutil.relativedelta import *
from standard_precip import spi


# In[221]:


'''
Log
RS60 19°47ʻ51.00"N   155°52ʻ43.68"W
RS61 19°46ʻ31.04"N   155°52ʻ17.69"W
RS62 19°45ʻ17.00"N   155°52ʻ12.32"W
RS63 19.38270000000 -155.88800000000 BI
RS64 Ponoholo makai 20.12450000000 -155.84400000000
RS65 Ponoholo mauka 20.13640000000 -155.77700000000

'''


# In[222]:


'''
Log
RID077 -155.562160606208 19.8879886274348
RID078 -155.602329368419 19.873136978495
RID079 -155.570057029552 19.9767465825001
RID080 -155.6598359297 20.0048159791584
RID081 -155.670478935067 20.0481201384305
RID082 -155.73429405195 20.0863138483643
RID083 -155.751834149437 20.1375566978253
RID084 -155.83383619291 20.1670643761859
RID085 -155.684900164623 18.9424641452124
RID086 -155.667619060971	19.0055991086339
RID087 -155.485133587008	19.1629174428649
RID088 -155.679116602317	18.9347910168347
RID089 -155.915857220744	19.5064142062338
RID090 -155.933211721583	19.5235631522107
RID091 -155.946759847527	19.5190590350399
'''


# In[223]:


#Get the number of ranches in HRIP
dir_path = '../RID'
count = 0
for path in os.listdir(dir_path):
    if os.path.isdir(os.path.join(dir_path, path)):
        count += 1


# In[224]:


ranch_id='RID'+f"{count+1:03}"
ranch_name = ''
island='BI'

#if coordinates are in convert degree minute second format, convert to decimals below
#lat=dms2dec('''19°45ʻ17.00"N''') # converts to dec
#lon=dms2dec('''155°52ʻ12.32"W''') # converts to dec

lat = 19.5190590350399
lon = -155.946759847527


# In[225]:


p1 = Point(lon,lat)
points = gpd.GeoSeries([p1])

# Buffer the points using a square cap style
# Note cap_style: round = 1, flat = 2, square = 3
buffer = points.buffer(0.01, cap_style = 3)


# In[226]:


buffer.to_file('./shapefiles/RIDs/'+ranch_id+'.shp')  


# In[227]:


#Enter new location into shapefile compilations

ranchshp = gpd.read_file('./shapefiles/RID.shp')


# In[228]:


newshp = gpd.read_file('./shapefiles/RIDs/'+ranch_id+'.shp')
newshp['Polygon']= ranch_id
#Name of area (optional)
newshp['Area']= ranch_name
#Island
newshp['IS']= island
new=ranchshp.append(newshp, ignore_index=True)
new.to_file('./shapefiles/RID.shp')  
os.mkdir('../RID/'+ranch_id)


# In[229]:


a = "var ranchSquares = "+new.to_json()
file_path = "../Leaflet/ranches.js"

with open(file_path, "w") as js_file:
    js_file.write(a)


# In[230]:


months = np.arange(1,13,1)
legacyYears = np.arange(1920,1990)
newYears=np.arange(1990,2020)

thisYear=(datetime.today().strftime("%Y"))
thisMonth=int((datetime.today().strftime("%m")))

if int(datetime.today().strftime("%m"))==1:
    lastMonth=12
    recentYears=np.arange(2020,int(thisYear))
    year=int(thisYear)-1
else:
    thisMonth=int((datetime.today().strftime("%m")))
    recentYears=np.arange(2020,int(thisYear)+1)
    year=int(thisYear)


# In[231]:


today = datetime.today()

last_month = today.replace(day=1) - timedelta(days=1)
first_day_of_last_month = last_month.replace(day=1)

lastM = first_day_of_last_month.strftime('%m/%d/%y')
lastM


# In[232]:


r = count+1

#Legacy
rf= pd.DataFrame({'Year': [],'Month':[],'RF_mm': []})
for i in legacyYears:
    for j in months:
        ranchshp = gpd.read_file(f'./shapefiles/RIDs/RID{r:03d}.shp')

        with rasterio.open(f"./rainmaps/legacy/MoYrRF_{i}_{j:02d}.tif") as src:
            affine = src.transform
            array = src.read(1)
            df_zonal_stats = pd.DataFrame(zonal_stats(ranchshp, array, affine=affine,nodata=-3.3999999521443642e+38,stats = ['mean']))
        RF= df_zonal_stats['mean'].iloc[0]
        rf=rf.append({'Year':i,'Month':j,'RF_mm':RF},ignore_index=True)
        rf['RF_in']=rf['RF_mm']/25.4
        rf.to_csv(f'./ranch_rf/legacy/RID{r:03d}_rf.csv')
#New

csv = pd.read_csv(f'./ranch_rf/legacy/RID{r:03d}_rf.csv',index_col=[0])
for i in newYears:
    for j in months:
        with rasterio.open(f"./rainmaps/new/{i}_{j:02d}_statewide_rf_mm_v1.tif") as src:
            affine = src.transform
            array = src.read(1)
            df_zonal_stats = pd.DataFrame(zonal_stats(ranchshp, array, affine=affine,nodata=-3.3999999521443642e+38,stats = ['mean']))
        RF= df_zonal_stats['mean'].iloc[0]
        csv = csv.append({'Year':i,'Month':j,'RF_mm':RF,'RF_in':RF/25.4},ignore_index=True)
        csv.to_csv(f'./ranch_rf/new/RID{r:03d}_rf.csv')

#2020-now

csv = pd.read_csv(f'./ranch_rf/new/RID{r:03d}_rf.csv',index_col=[0])
for i in recentYears:
    for j in months:
        if int(i) == int(thisYear) and int(j)>(int(thisMonth)-1):
            break
        with rasterio.open(f"./rainmaps/2020-/rainfall_{i}_{j:02}.tif") as src:
            affine = src.transform
            array = src.read(1)
            df_zonal_stats = pd.DataFrame(zonal_stats(ranchshp, array, affine=affine,nodata=-3.3999999521443642e+38,stats = ['mean']))
        RF= df_zonal_stats['mean'].iloc[0]
        csv=csv.append({'Year':i,'Month':j,'RF_mm':RF,'RF_in':RF/25.4},ignore_index=True)
csv['datetime']=pd.date_range('1/1/1920',lastM,freq='MS')
csv.to_csv(f'../RID/RID{r:03d}/RID{r:03d}_rf.csv')


# In[233]:


datem = datetime.today().strftime("%m")
monthInd = -int(datem)+1
def rf_avg(arr):
    rfdf = arr.groupby(['Month'],as_index=False).mean()
    rfdf['Month'] = rfdf['Month'].astype(np.uint8).apply(lambda x: calendar.month_name[x])
    rfdf['rolledMonth'] = np.roll(rfdf.Month, monthInd)
    rfdf['RF'] = np.roll(rfdf.RF_in, monthInd)
    rfdf = rfdf.rename(columns={"Month":"oldMonth","rolledMonth":"Month"})
    return rfdf

#last 12 months
def rf_12m(arr):
    rf12m = arr
    rf12m['Month'] = rf12m['Month'].astype(np.uint8).apply(lambda x: calendar.month_name[x])
    rf12m = rf12m.tail(12)
    rf12m['RF'] = rf12m['RF_in'] 
    return rf12m


# In[234]:


#rf = pd.read_csv(f"/Users/cherryleheu/Codes/NIDIS-Codes/RID/RID{r:03d}/RID{r:03d}_rf.csv",index_col=0)
rf = pd.read_csv(f"../RID/RID{r:03d}/RID{r:03d}_rf.csv",index_col=0)
rfdf=rf_avg(rf)
rfdf=rfdf.drop(['Year','RF_mm'],axis=1)
rf12m=rf_12m(rf)
rf12m=rf12m.drop(['Year','datetime','RF_mm','RF_in'],axis=1)
rfdf.to_csv(f'../RID/RID{r:03d}/RID{r:03d}_rf_month.csv') 
rf12m.to_csv(f'../RID/RID{r:03d}/RID{r:03d}_rf_12m.csv')


# In[235]:


rf = pd.read_csv(f'../RID/RID{r:03d}/RID{r:03d}_rf.csv',index_col=[0])
spi_rain = spi.SPI()
spi_3=[]
spi_3 = spi_rain.calculate(csv, 'datetime', 'RF_in', freq="M", scale=3, fit_type="lmom", dist_type="gam")
spi_3=spi_3.rename(columns={"RF_in_scale_3_calculated_index": "SPI-3"})
spi_3.to_csv(f'../RID/RID{r:03d}/RID{r:03d}_spi.csv')


# In[236]:


ranchshp = gpd.read_file('./shapefiles/RID.shp')
ranch = ranchshp.loc[ranchshp['Polygon']==f"RID{r:03d}"]

temp = pd.DataFrame({'Year': [],'Month':[],'Temp': []})
for i in np.arange(1990,int(thisYear)+1):
    for j in months:
        if int(i) == int(thisYear) and int(j)>(int(thisMonth)-4):
            break
        with rasterio.open(f'./temp_monthly_maps/mean/{i}_{j:02d}_t_month_mean.tif') as src:
            affine = src.transform
            array = src.read(1)
            df_zonal_stats = pd.DataFrame(zonal_stats(ranch, array, affine=affine,nodata=-9999,stats = ['mean']))
        temp_f = 9/5*df_zonal_stats['mean'].iloc[0]+32
        new_row = pd.DataFrame({'Year':i,'Month':j,'Temp':temp_f},index=[0])
        temp=pd.concat([temp, new_row],ignore_index=True)

temp.to_csv(f'../RID/RID{r:03d}/RID{r:03d}_temp.csv')

temp_min = pd.DataFrame({'Year': [],'Month':[],'Temp': []})
for i in np.arange(1990,int(thisYear)+1):
    for j in months:
        if int(i) == int(thisYear) and int(j)>(int(thisMonth)):
            break
        with rasterio.open(f'./temp_monthly_maps/min/{i}_{j:02d}_t_month_min.tif') as src:
            affine = src.transform
            array = src.read(1)
            df_zonal_stats = pd.DataFrame(zonal_stats(ranch, array, affine=affine,nodata=-9999,stats = ['mean']))
        temp_f = 9/5*df_zonal_stats['mean'].iloc[0]+32
        new_row = pd.DataFrame({'Year':i,'Month':j,'Temp':temp_f},index=[0])
        temp_min=pd.concat([temp_min, new_row],ignore_index=True)

temp_min.to_csv(f'../RID/RID{r:03d}/RID{r:03d}_temp_min.csv')

temp_max = pd.DataFrame({'Year': [],'Month':[],'Temp': []})
for i in np.arange(1990,int(thisYear)+1):
    for j in months:
        if int(i) == int(thisYear) and int(j)>(int(thisMonth)-4):
            break
        with rasterio.open(f'./temp_monthly_maps/max/{i}_{j:02d}_t_month_max.tif') as src:
            affine = src.transform
            array = src.read(1)
            df_zonal_stats = pd.DataFrame(zonal_stats(ranch, array, affine=affine,nodata=-9999,stats = ['mean']))
        temp_f = 9/5*df_zonal_stats['mean'].iloc[0]+32
        new_row = pd.DataFrame({'Year':i,'Month':j,'Temp':temp_f},index=[0])
        temp_max=pd.concat([temp_max, new_row],ignore_index=True)

temp_max.to_csv(f'../RID/RID{r:03d}/RID{r:03d}_temp_max.csv')


# In[237]:


#average monthly
def temp_avg(arr):
    tdf = arr.groupby(['Month'],as_index=False).mean()
    tdf['Month'] = tdf['Month'].astype(np.uint8).apply(lambda x: calendar.month_name[x])
    tdf['rolledMonth'] = np.roll(tdf.Month, -a)
    tdf['rolledTemp'] = np.roll(tdf.Temp, -a)
    tdf = tdf.rename(columns={"Temp": "oldTemp", "rolledTemp": "Temp","Month":"oldMonth","rolledMonth":"Month"})
    return tdf

#last 12 months
def temp_12m(arr):
    t12m = arr.tail(12)
    t12m['Month'] = t12m['Month'].astype(np.uint8).apply(lambda x: calendar.month_name[x]) 
    return t12m


# In[238]:


temp=pd.read_csv(f'../RID/RID{r:03d}/RID{r:03d}_temp.csv',index_col=0)
a = int(temp['Month'].iloc[-1])
tdf=temp_avg(temp)
tdf=tdf.drop(['Year'],axis=1)
t12m=temp_12m(temp)
tdf.to_csv(f'../RID/RID{r:03d}/RID{r:03d}_t_month.csv') 
t12m.to_csv(f'../RID/RID{r:03d}/RID{r:03d}_t_12m.csv')


# In[239]:


'''ranchshp = gpd.read_file('./shapefiles/RID.shp')
ranch = ranchshp.loc[ranchshp['Polygon']==f"RID{r:03d}"]
temp = pd.DataFrame({'Year': [],'Month':[],'Temp': []})
for i in np.arange(1990,int(thisYear)+1):
    for j in months:
        if int(i) == int(thisYear) and int(j)>(int(thisMonth)-4):
            break
        with rasterio.open(f'./temp_monthly_maps/min/{i}_{j:02d}_t_month_min.tif') as src:
            affine = src.transform
            array = src.read(1)
            df_zonal_stats = pd.DataFrame(zonal_stats(ranch, array, affine=affine,nodata=-9999,stats = ['mean']))
        t = 9/5*df_zonal_stats['mean'].iloc[0]+32
        temp=temp.append({'Year':i,'Month':j,'Temp':t},ignore_index=True)
temp.to_csv(f'../RID/RID{r:03d}/RID{r:03d}_temp_min.csv',index=False)'''


# In[240]:


'''ranchshp = gpd.read_file('./shapefiles/RID.shp')
ranch = ranchshp.loc[ranchshp['Polygon']==f"RID{r:03d}"]
temp = pd.DataFrame({'Year': [],'Month':[],'Temp': []})
for i in np.arange(1990,int(thisYear)+1):
    for j in months:
        if int(i) == int(thisYear) and int(j)>(int(thisMonth)-3):
            break
        with rasterio.open(f'./temp_monthly_maps/max/{i}_{j:02d}_t_month_max.tif') as src:
            affine = src.transform
            array = src.read(1)
            df_zonal_stats = pd.DataFrame(zonal_stats(ranch, array, affine=affine,nodata=-9999,stats = ['mean']))
        t = 9/5*df_zonal_stats['mean'].iloc[0]+32
        temp=temp.append({'Year':i,'Month':j,'Temp':t},ignore_index=True)
temp.to_csv(f'../RID/RID{r:03d}/RID{r:03d}_temp_max.csv',index=False)'''


# In[241]:


#ET
lastM='10/1/2023'

ranchshp = gpd.read_file('./shapefiles/RID.shp')
ranch = ranchshp.loc[ranchshp['Polygon']==f"RID{r:03d}"]
et = pd.DataFrame({'Year': [],'Month':[],'ET': []})
for i in np.arange(2001,int(thisYear)+1):
    for j in np.arange(1,13):
        if int(i) == int(thisYear) and int(j)>(int(thisMonth)-1):
            break
        else:
            with rasterio.open(f'./ETmaps/{i}_{j:02d}_et.tif') as src:
                affine = src.transform
                array = src.read(1)
                nodata = src.nodata
                df_zonal_stats = pd.DataFrame(zonal_stats(ranch, array, affine=affine,nodata=nodata,stats = ['mean']))
            ET= df_zonal_stats['mean'].iloc[0]
            et=et.append({'Year':i,'Month':j,'ET':ET},ignore_index=True)

et['ET'].replace(0, np.nan, inplace=True)
et['datetime']=pd.date_range('1/1/2001',lastM,freq='MS')
et['ET']=et['ET']/8
et.to_csv(f'../RID/RID{r:03d}/RID{r:03d}_et.csv')


# In[242]:


#average monthly
def et_avg(arr):
    etdf = arr.groupby(['Month'],as_index=False).mean()
    etdf['Month'] = etdf['Month'].astype(np.uint8).apply(lambda x: calendar.month_name[x])
    etdf['rolledMonth'] = np.roll(etdf.Month, -a)
    etdf['rolledET'] = np.roll(etdf.ET, -a)
    etdf = etdf.rename(columns={"ET": "oldET", "rolledET": "ET","Month":"oldMonth","rolledMonth":"Month"})
    return etdf

#last 12 months
def et_12m(arr):
    et12m = arr.tail(12)
    et12m['Month'] = et12m['Month'].astype(np.uint8).apply(lambda x: calendar.month_name[x]) 
    return et12m


# In[243]:


et = pd.read_csv(f'../RID/RID{r:03d}/RID{r:03d}_et.csv')
a = int(et['Month'].iloc[-1])
etdf=et_avg(et)
#etdf=etdf.drop(['Year'],axis=1)
et12m=et_12m(et)
etdf.to_csv(f'../RID/RID{r:03d}/RID{r:03d}_et_month.csv',index=False) 
et12m.to_csv(f'../RID/RID{r:03d}/RID{r:03d}_et_12m.csv',index=False)


# In[244]:


ranchshp = gpd.read_file('./shapefiles/RID.shp')
ranch = ranchshp.loc[ranchshp['Polygon']==f"RID{r:03d}"]
ndvi = pd.DataFrame({'Year': [],'Month':[],'NDVI': []})
for i in np.arange(2000,int(thisYear)+1):
    if i == 2000:
        range = np.arange(2,13)
    else:
        range=np.arange(1,13)
    for j in range:
        if int(i) == int(thisYear) and int(j)>(int(thisMonth)-2):
            break
        with rasterio.open(f'./NDVImaps/{i}_{j:02d}_NDVI.tif') as src:
            affine = src.transform
            array = src.read(1)
            nodata = src.nodata
            df_zonal_stats = pd.DataFrame(zonal_stats(ranch, array, affine=affine,nodata=nodata,stats = ['mean']))
        NDVI= df_zonal_stats['mean'].iloc[0]
        ndvi=ndvi.append({'Year':i,'Month':j,'NDVI':NDVI},ignore_index=True)
ndvi['NDVI'].replace(0, np.nan, inplace=True)
ndvi['datetime']=pd.date_range('2/1/2000',lastM,freq='MS')
ndvi.to_csv(f'../RID/RID{r:03d}/RID{r:03d}_ndvi.csv')


# In[245]:


#average monthly
def ndvi_avg(arr):
    ndvidf = arr.groupby(['Month'],as_index=False).mean()
    ndvidf['Month'] = ndvidf['Month'].astype(np.uint8).apply(lambda x: calendar.month_name[x])
    ndvidf['rolledMonth'] = np.roll(ndvidf.Month, -a)
    ndvidf['rolledNDVI'] = np.roll(ndvidf.NDVI, -a)
    ndvidf = ndvidf.rename(columns={"NDVI": "oldNDVI", "rolledNDVI": "NDVI","Month":"oldMonth","rolledMonth":"Month"})
    return ndvidf

#last 12 months
def ndvi_12m(arr):
    ndvi12m = arr.tail(12)
    ndvi12m['Month'] = ndvi12m['Month'].astype(np.uint8).apply(lambda x: calendar.month_name[x]) 
    return ndvi12m


# In[246]:


ndvi = pd.read_csv(f'../RID/RID{r:03d}/RID{r:03d}_ndvi.csv',index_col=0)
a = int(ndvi['Month'].iloc[-1])
ndvidf=ndvi_avg(ndvi)
ndvidf=ndvidf.drop(['Year'],axis=1)
ndvi12m=ndvi_12m(ndvi)
ndvidf.to_csv(f'../RID/RID{r:03d}/RID{r:03d}_ndvi_month.csv',index=False) 
ndvi12m.to_csv(f'../RID/RID{r:03d}/RID{r:03d}_ndvi_12m.csv',index=False)


# In[247]:


#Query Table
phases = 'SEL','WEL','NUT','WLA','SLA'

#Query Table
def phaseCalc(ANOM):
    if ANOM > 1.1: 
        phase='SEL'
    elif 1.1 >= ANOM >0.5:
        phase='WEL'
    elif 0.5>=ANOM>=-0.5:
        phase = 'NUT'
    elif -0.5> ANOM >= -1.1:
        phase = 'WLA'
    elif ANOM < -1.1:
        phase = 'SLA'
    else:
        print("Error")
    return phase

ONI=pd.read_csv("https://origin.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/detrend.nino34.ascii.txt",delim_whitespace=True)
ONI['PHASE'] = ONI['ANOM'].apply(phaseCalc)

ONI=ONI.sort_values(by=['MON', 'PHASE'])


# In[248]:


rf = pd.read_csv(f'../RID/RID{r:03d}/RID{r:03d}_rf.csv',index_col=0)
rf = rf[rf['Year']>1949]
temp = pd.read_csv(f'../RID/RID{r:03d}/RID{r:03d}_temp.csv',index_col=0)
query = pd.DataFrame()
m3=pd.DataFrame()
for i in months:
    for j in phases:
        #Get MRF, Me, Mn and anoms. Add to query ()
        MRF = (rf[(rf['Month']==i)]).RF_in.mean()
        MT = (temp[(temp['Month']==i)]).Temp.mean()
        phase = j
        count = len(ONI[(ONI['MON']==i)&(ONI['PHASE']==j)])
        list = ONI.loc[(ONI['MON'] == i) & (ONI['PHASE'] == j)].YR.values.tolist()
        dfrf = rf[rf['Year'].isin(list)]
        dft = temp[temp['Year'].isin(list)]
        MeRF = (dfrf[(dfrf['Month']==i)]).RF_in.mean()
        MnRF = (dfrf[(dfrf['Month']==i)]).RF_in.min()
        MeT = (dft[(dft['Month']==i)]).Temp.mean()
        MnT = (dft[(dft['Month']==i)]).Temp.min()
        MeAnom = MeRF - MRF
        MnAnom = MnRF - MRF
        df2 = {'Month':i,'MRF': MRF, 'Phase':j,'Count':count,'MeRF':MeRF,'MnRF':MnRF,'MeAnom':MeAnom,'MnAnom':MnAnom,'MT':MT,'MeT':MeT,'MnT':MnT}
        query = query.append(df2,ignore_index=True)
        '''if i==11:
            MRF3M = query[query['Phase']==j].iloc[np.r_[0, -2:0]].MRF.sum()
            MeRF3M = query[query['Phase']==j].iloc[np.r_[0, -2:0]].MeRF.sum()
            MnRF3M = query[query['Phase']==j].iloc[np.r_[0, -2:0]].MnRF.sum()
        elif i==12:
            MRF3M = query[query['Phase']==j].iloc[np.r_[0:2, -1:0]].MRF.sum()
            MeRF3M = query[query['Phase']==j].iloc[np.r_[0:2, -1:0]].MeRF.sum()
        MnRF3M = query[query['Phase']==j].iloc[np.r_[0:2, -1:0]].MnRF.sum()
        else:
            MRF3M = query[query['Phase']==j][i-1:i+2].MRF.sum()
            MeRF3M = query[query['Phase']==j][i-1:i+2].MeRF.sum()
            MnRF3M = query[query['Phase']==j][i-1:i+2].MnRF.sum()
        m3=m3.append({'MRF3M':MRF3M,'MeRF3M':MeRF3M,'MnRF3M':MnRF3M},ignore_index=True)'''
        #Calculate quarterly forage production 


#query = pd.concat([query, m3], axis=1)


'''for k in np.arange(len(query)):
    MRF_90 = query['MRF3M'][k]
    MeRF_90 = query['MeRF3M'][k]
    MnRF_90 = query['MnRF3M'][k]
    qfpM = 643.1+234.1*MRF_90
    qfpMe = 643.1+234.1*MeRF_90
    qfpMn = 643.1+234.1*MnRF_90
    QFPMe_c = ((qfpMe-qfpM)/qfpM)*100
    QFPMn_c = ((qfpMn-qfpM)/qfpM)*100
    qfp = qfp.append({'QFPMe_c':QFPMe_c,'QFPMn_c':QFPMn_c},ignore_index=True)'''

#query=pd.concat([query, qfp], axis=1)
query.to_csv(f'../RID/RID{r:03d}/RID{r:03d}_query.csv')


# In[249]:


csv = pd.read_csv(f'../RID/RID{r:03d}/RID{r:03d}_rf.csv',index_col=[0])
spi_rain = spi.SPI()
spi_3=[]
spi_3 = spi_rain.calculate(csv, 'datetime', 'RF_in', freq="M", scale=3, fit_type="lmom", dist_type="gam")
spi_3=spi_3.rename(columns={"RF_in_scale_3_calculated_index": "SPI-3"})
spi_3.to_csv(f'../RID/RID{r:03d}/RID{r:03d}_spi.csv')


# In[250]:


island_lats = {'BI': {'xlim': [-156.1, -154.8], 'ylim': [18.9, 20.3]}, 'Ma':{'xlim': [-156.72, -155.95], 'ylim': [20.55, 21.05]}, 
              'Oa':{'xlim': [-158.3,-157.645], 'ylim': [21.25, 21.73]}, 'Ka':{'xlim': [-159.8,-159.28], 'ylim': [21.86,22.25]}, 
              'Ko':{'xlim': [-156.71,-156.52], 'ylim': [20.49, 20.61]}, 'La':{'xlim': [-157.08,-156.8], 'ylim': [20.7, 20.95]}, 
              'Mo':{'xlim': [-157.32,-156.7], 'ylim': [21.03, 21.23]}, } 


# In[251]:


coastline = gpd.read_file('./shapefiles/Coastline.shp')
coastline = coastline.to_crs("epsg:4326")
ranches = gpd.read_file('./shapefiles/RID.shp')
ranches = ranches.to_crs("epsg:4326")
#rainfall = rasterio.open('rf_in.tif',nodata=noData)
#raster = rasterio.plot.show(rainfall, ax=ax,cmap='viridis_r')

#datetime variables
lastMonth = (datetime.today() + relativedelta(months=-1)).strftime("%m")
lastMonthYr = (datetime.today() + relativedelta(months=-1)).strftime("%Y")
lastMonth = 10


# In[252]:


with rasterio.open(f'./rainmaps/2020-/rainfall_{lastMonthYr}_{lastMonth:02d}.tif') as src:
    rf_mm = src.read(1, masked=True)

    rf_in = rf_mm/25.4

    with rasterio.open('output_raster.tif', 'w', **src.profile) as dst:
        dst.write(rf_in, 1)

a = rasterio.open('output_raster.tif')

y = ranches[ranches.Polygon == ranch_id]
fig, ax = plt.subplots(figsize=(15, 10), dpi=80)
coastline.plot(ax=ax, facecolor='none', edgecolor='black')
ranches.plot(ax=ax, facecolor='none',edgecolor='orange',linewidth=2)
y.plot(ax=ax, facecolor='none',edgecolor='red',linewidth=3)
rasterio.plot.show(a, ax=ax,cmap='viridis_r')
plt.rcParams['font.size'] = '20'
ax.set_ylim(island_lats[island]['ylim'])
ax.set_xlim(island_lats[island]['xlim'])
raster = rasterio.plot.show(a, ax=ax,cmap='viridis_r')
im=raster.get_images()[0]
cbar = fig.colorbar(im,ax=ax)
cbar.ax.tick_params(labelsize=20) 
plt.savefig(f'../RID/RID{r:03d}/RID{r:03d}_rf.png',bbox_inches="tight")
plt.show()


# In[253]:


with rasterio.open('./temp_monthly_maps/mean/'+lastMonthYr+'_'+lastMonth+'_t_month_mean.tif') as src:
    temp_c = src.read(1, masked=True)

    temp = (temp_c * 9/5) + 32
    noData = src.nodata
    with rasterio.open('output_raster.tif', 'w', **src.profile) as dst:
        dst.write(temp, 1)
        
temp_map = rasterio.open('output_raster.tif',noData=noData)

y = ranches[ranches.Polygon == ranch_id]
fig, ax = plt.subplots(figsize=(15, 10), dpi=80)
coastline.plot(ax=ax, facecolor='none', edgecolor='black')
ranches.plot(ax=ax, facecolor='none',edgecolor='orange',linewidth=2)
y.plot(ax=ax, facecolor='none',edgecolor='red',linewidth=3)
rasterio.plot.show(a, ax=ax,cmap='viridis')
plt.rcParams['font.size'] = '20'
ax.set_ylim(island_lats[island]['ylim'])
ax.set_xlim(island_lats[island]['xlim'])
raster = rasterio.plot.show(temp_map, ax=ax,cmap='viridis')
im=raster.get_images()[0]
cbar = fig.colorbar(im,ax=ax)
cbar.ax.tick_params(labelsize=20) 
plt.savefig(f'../RID/RID{r:03d}/RID{r:03d}_temp.png',bbox_inches="tight")
plt.show()


# In[254]:


lastMonth = 10
url = f'./ETMaps/{int(lastMonthYr)}_{int(lastMonth):02d}_et.tif'
with rasterio.open(url) as src:
    et = src.read(1, masked=True)
    nodata = src.nodata

et = rasterio.open(url,nodata=nodata)


# In[255]:


y = ranches[ranches.Polygon == ranch_id]
fig, ax = plt.subplots(figsize=(15, 10), dpi=80)
coastline.plot(ax=ax, facecolor='none', edgecolor='black')
ranches.plot(ax=ax, facecolor='none',edgecolor='orange',linewidth=2)
y.plot(ax=ax, facecolor='none',edgecolor='red',linewidth=3)
rasterio.plot.show(et, ax=ax,cmap='viridis')
plt.rcParams['font.size'] = '20'
ax.set_ylim(island_lats[island]['ylim'])
ax.set_xlim(island_lats[island]['xlim'])
raster = rasterio.plot.show(et, ax=ax,cmap='viridis_r')
im=raster.get_images()[0]
cbar = fig.colorbar(im,ax=ax)
cbar.ax.tick_params(labelsize=20) 
plt.savefig(f'../RID/RID{r:03d}/RID{r:03d}_et.png',bbox_inches="tight")
plt.show()


# In[256]:


lastMonth = 9
url = f'./NDVIMaps/{int(lastMonthYr)}_{int(lastMonth):02d}_ndvi.tif'
with rasterio.open(url) as src:
   ndvi = src.read(1, masked=True)
ndvi = rasterio.open(url,nodata=noData)


# In[257]:


y = ranches[ranches.Polygon == ranch_id]
fig, ax = plt.subplots(figsize=(15, 10), dpi=80)
coastline.plot(ax=ax, facecolor='none', edgecolor='black')
ranches.plot(ax=ax, facecolor='none',edgecolor='orange',linewidth=2)
y.plot(ax=ax, facecolor='none',edgecolor='blue',linewidth=2)
rasterio.plot.show(ndvi, ax=ax,cmap='RdYlGn')
plt.rcParams['font.size'] = '20'
ax.set_ylim(island_lats[island]['ylim'])
ax.set_xlim(island_lats[island]['xlim'])
raster = rasterio.plot.show(ndvi, ax=ax,cmap='RdYlGn')
im=raster.get_images()[0]
cbar = fig.colorbar(im,ax=ax)
cbar.ax.tick_params(labelsize=20) 
plt.savefig(f'../RID/RID{r:03d}/RID{r:03d}_ndvi.png',bbox_inches="tight")
plt.show()


# In[258]:


def filter(rf_df,mode):
    if mode == 1:
        ENSO = []
        if ANOM > 1.1: 
            ENSO= rf_df[(rf_df['Month']>=a)&(rf_df['Month']<=b)].loc[rf_df['Phase'] == 'SEL']
            title="Strong El Nino"
        elif 1.1 >= ANOM >0.5:
            ENSO= rf_df[(rf_df['Month']>=a)&(rf_df['Month']<=b)].loc[rf_df['Phase'] == 'WEL']
            title="Weak El Nino"
        elif 0.5>=ANOM>=-0.5:
            ENSO= rf_df[(rf_df['Month']>=a)&(rf_df['Month']<=b)].loc[rf_df['Phase'] == 'NUT']
            title="Neutral"
        elif -0.5> ANOM >= -1.1:
            ENSO= rf_df[(rf_df['Month']>=a)&(rf_df['Month']<=b)].loc[rf_df['Phase'] == 'WLA']
            title=r'Weak La Ni$\tilde{n}a$'
        elif ANOM < -1.1:
            ENSO= rf_df[(rf_df['Month']>=a)&(rf_df['Month']<=b)].loc[rf_df['Phase'] == 'SLA']
            title=r'Strong La Ni$\tilde{n}a$'
        else:
            print("Error")
        return ENSO, title
    if mode == 2:
        ENSO = []
        if ANOM > 1.1: 
            ENSO= rf_df[(rf_df['Month']>=a)|(rf_df['Month']<=b)].loc[rf_df['Phase'] == 'SEL']
            title="Strong El Nino"
        elif 1.1 >= ANOM >0.5:
            ENSO= rf_df[(rf_df['Month']>=a)&(rf_df['Month']<=b)].loc[rf_df['Phase'] == 'WEL']
            title="Weak El Nino"
        elif 0.5>=ANOM>=-0.5:
            ENSO= rf_df[(rf_df['Month']>=a)&(rf_df['Month']<=b)].loc[rf_df['Phase'] == 'NUT']
            title="Neutral"
        elif -0.5> ANOM >= -1.1:
            ENSO= rf_df[(rf_df['Month']>=a)&(rf_df['Month']<=b)].loc[rf_df['Phase'] == 'WLA']
            title=r'Weak La Ni$\tilde{n}a$'
        elif ANOM < -1.1:
            ENSO= rf_df[(rf_df['Month']>=a)&(rf_df['Month']<=b)].loc[rf_df['Phase'] == 'SLA']
            title=r'Strong La Ni$\tilde{n}a$'
        else:
            print("Error")
        return ENSO, title


# In[259]:


ONI=pd.read_csv("https://origin.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/detrend.nino34.ascii.txt",delim_whitespace=True)
ANOM = ONI.iloc[-1]['ANOM']

now = datetime.now()

thisMonth = (now).strftime("%B")
now = datetime.now()
month = now.strftime("%b")

a = int((now+relativedelta(months=+0)).strftime("%m"))
b = int((now+relativedelta(months=+2)).strftime("%m"))


# In[260]:


#table=pd.read_csv(f"/Users/cherryleheu/Codes/NIDIS-Codes/RID/RID{r:03d}/RID{r:03d}_query.csv",index_col=0)
table=pd.read_csv(f"../RID/RID{r:03d}/RID{r:03d}_query.csv",index_col=0)
rf_df=pd.DataFrame({'A' : []})
now = datetime.now()
thisMonth = (now).strftime("%B")

if a == 11 or a == 12:
    #creates a table that is from March to Feb
    rf_df=table.append(table.loc[:9])
    N=10
    rf_df=rf_df.iloc[N:,:]
    mode = 2
else:
    rf_df=table
    mode = 1

ENSO = filter(rf_df,mode)[0]
title=filter(rf_df,mode)[1]
ENSO['MonthName']= ENSO['Month'].astype(np.uint8).apply(lambda x: calendar.month_abbr[x])

#all mean
mean=ENSO['MRF'].iloc[0]
#phase mean
p_mean = ENSO['MeRF'].iloc[0]
#phase min
p_min = ENSO['MnRF'].iloc[0]

#probability
#mean_prob = int(ENSO['A_ProbMe'][0]*100)
#p_mean_prob = int(ENSO['E_ProbMe'][0]*100)
#p_min_prob = int(ENSO['E_ProbMn'][0]*100)

fig, ax = plt.subplots(figsize=(12,10))
line1 = ENSO.plot(ax=ax,x='MonthName',y=['MRF','MeRF','MnRF'],kind="bar",legend=False,color=['#004c6d','#6996b3','#c1e7ff'])

ax.set_ylabel("Monthly rainfall (inches)",fontsize=12)

first_legend = ax.legend(['Mean', '%s Mean' % title, '%s Minimum'% title],fontsize=20,bbox_to_anchor=(1,1),edgecolor="black")


second_legend = ax.legend([f"Mean                                    {mean:.2f} in\n{title} Mean             {p_mean:.2f} in\n{title} Minimum       {p_min:.2f} in"], loc='center left', 
                          handlelength=0, handletextpad=0,bbox_to_anchor=(1, 0.7), title=f'RID{r:03d} {thisMonth} Rainfall')



ax.add_artist(first_legend)
#ax.add_artist(second_legend)
ax.set(xlabel=None)
plt.savefig(f"../RID/RID{r:03d}/RID{r:03d}_rainfall.png",bbox_inches="tight")
plt.show()


# In[261]:


#Read soils shapefile, filter data
soils_path = './shapefiles/soils/soils.shp'
soils_shp = gpd.read_file(soils_path)
soils = soils_shp[['areasymbol','musym','geometry']]

pasture = pd.read_csv('./528/SoilPasture.csv')
soils_0 = pasture.loc[pasture['Pasture Group'] == 0]

nullSymbols = pasture[pasture['Poor'].isna()]['SoilSymbol'].tolist()
nullSymbols.extend(soils_0['SoilSymbol'].tolist())


# In[262]:


ranches = gpd.read_file('./shapefiles/RID.shp')
ranches = ranches.to_crs("epsg:4326")

y = ranches[ranches.Polygon == ranch_id]
a=y['Polygon']
clip = gpd.clip(soils,ranches.loc[y.index,'geometry'])
clip_proj = clip.to_crs(epsg=3857)
clip_proj['area']=clip_proj.geometry.area
final = clip_proj.dissolve(by='musym',aggfunc='sum').reset_index()
df = final.sort_values(by='area', ascending=False)
index_position = 0
musym = df['musym'].iloc[index_position]
if musym in nullSymbols:
    print('Changing musym...')
    while musym in nullSymbols:
        index_position += 1
        musym = df['musym'].iloc[index_position]
    print('Musym changed')

ranches.loc[y.index, 'musym']=musym
ranches.to_file('./shapefiles/RID.shp')  
musym


# In[263]:


ranches = gpd.read_file('./shapefiles/RID.shp')
ranches = ranches.to_crs("epsg:4326")
ranches.tail(10)


# In[ ]:





# In[ ]:




