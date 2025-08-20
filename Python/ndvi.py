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


lastMonth = (datetime.today() + relativedelta(months=-1)).strftime("%m")
lastMonthYr = (datetime.today() + relativedelta(months=-1)).strftime("%Y")
import os
#os.chdir('/Users/cherryleheu/Codes/NIDIS-Codes/H-RIP/Python')
os.chdir('./Python')
path = os.getcwd()

url = 'https://ikeauth.its.hawaii.edu/files/v2/download/public/system/ikewai-annotated-data/HCDP/production/rainfall/new/month/statewide/data_map/'+lastMonthYr+'/rainfall_new_month_statewide_data_map_'+lastMonthYr+'_'+lastMonth+'.tif'
#https:/ikeauth.its.hawaii.edu/files/v2/download/public/system/ikewai-annotated-data/HCDP/production/rainfall/new/month/statewide/data_map/2022/rainfall_new_month_statewide_data_map_2022_03.tif --output-file rf-wget.tif
