#!/Users/cherryleheu/opt/anaconda3/bin/python3
# coding: utf-8

# In[1]:
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
import rasterio
import geopandas as gpd
from rasterio.plot import show
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from rasterstats import zonal_stats
from standard_precip import spi

lastMonth = (datetime.today() + relativedelta(months=-1)).strftime("%m")
lastMonthYr = (datetime.today() + relativedelta(months=-1)).strftime("%Y")
import os
os.chdir('/Users/cherryleheu/Codes/NIDIS-Codes/Python')
path = os.getcwd()



url = 'https://ikeauth.its.hawaii.edu/files/v2/download/public/system/ikewai-annotated-data/HCDP/production/rainfall/new/month/statewide/data_map/'+lastMonthYr+'/rainfall_new_month_statewide_data_map_'+lastMonthYr+'_'+lastMonth+'.tif'
#https:/ikeauth.its.hawaii.edu/files/v2/download/public/system/ikewai-annotated-data/HCDP/production/rainfall/new/month/statewide/data_map/2022/rainfall_new_month_statewide_data_map_2022_03.tif --output-file rf-wget.tif

r = requests.get(url)
file=f"./rainmaps/2020-/rainfall_{lastMonthYr}_{lastMonth}.tif"
open(file, 'wb').write(r.content)


# In[7]:


#Get the number of ranches in HRIP
dir_path = '../RID'
count = 0
for path in os.listdir(dir_path):
    if os.path.isdir(os.path.join(dir_path, path)):
        count += 1


ranches = np.arange(1,count+1)

for r in ranches:
    ranchshp = gpd.read_file('./shapefiles/RID.shp',rows=slice(r-1, r))
    ranch = ranchshp['Polygon'].iloc[0]
    csv = pd.read_csv('../RID/'+ranch+'/'+ranch+'_rf.csv',index_col=[0])
    #csv.to_csv('../RID/'+ranch+'/'+ranch+'_rf.csv')
    with rasterio.open(file) as src:
        affine = src.transform
        array = src.read(1)
        df_zonal_stats = pd.DataFrame(zonal_stats(ranchshp, array, affine=affine,nodata=-3.3999999521443642e+38,stats = ['mean']))
    RF= df_zonal_stats['mean'].iloc[0]
    csv=csv.append({'Year':int(lastMonthYr),'Month':lastMonth,'RF_mm':RF,'RF_in':RF/25.4},ignore_index=True)
    csv['datetime']=pd.date_range('1/1/1920',lastMonth+'/01/'+lastMonthYr,freq='MS')
    csv.to_csv('../RID/'+ranch+'/'+ranch+'_rf.csv')

    spi_rain = spi.SPI()
    spi_3=[]
    spi_3 = spi_rain.calculate(csv, 'datetime', 'RF_in', freq="M", scale=3, fit_type="lmom", dist_type="gam")
    spi_3=spi_3.rename(columns={"RF_in_scale_3_calculated_index": "SPI-3"})
    spi_3.to_csv(f'../RID/'+ranch+'/'+ranch+'_spi.csv')

    '''spi_pos=spi_3
    spi_pos['SPI-3'] = spi_pos['SPI-3'].clip(lower=0)
    spi_3 = pd.read_csv(f'../ranches/RS{h:02d}/RS{h:02d}_spi.csv',index_col=[0])
    spi_neg=spi_3
    spi_neg['SPI-3'] = spi_neg['SPI-3'].clip(upper=0)
    spi_pos.to_csv(f'../ranches/RS{h:02d}/RS{h:02d}_spiPOS.csv')
    spi_neg.to_csv(f'../ranches/RS{h:02d}/RS{h:02d}_spiNEG.csv')'''  



