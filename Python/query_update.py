#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import calendar
import numpy as np
import os
os.chdir('/Users/cherryleheu/Codes/NIDIS-Codes/H-RIP/Python')


dir_path = '../RID'
count = 0
for path in os.listdir(dir_path):
    if os.path.isdir(os.path.join(dir_path, path)):
        count += 1

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

months = np.arange(1,13,1)


for r in np.arange(1,count+1):
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
    query.to_csv(f'../RID/RID{r:03d}/RID{r:03d}_query.csv')

