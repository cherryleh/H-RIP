#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import calendar
import os
#os.chdir('/Users/cherryleheu/Codes/NIDIS-Codes/H-RIP/Python')
os.chdir('./Python')
path = os.getcwd()

from datetime import datetime
from dateutil.relativedelta import relativedelta

now = datetime.now()

thisMonth = (now).strftime("%B")

ONI=pd.read_csv("https://origin.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/detrend.nino34.ascii.txt",delim_whitespace=True)
ANOM = ONI.iloc[-1]['ANOM']

from datetime import datetime
from dateutil.relativedelta import relativedelta


now = datetime.now()
month = now.strftime("%b")

a = int((now+relativedelta(months=+0)).strftime("%m"))
b = int((now+relativedelta(months=+2)).strftime("%m"))

#Get the number of ranches in HRIP
dir_path = '../RID'
count = 0
for path in os.listdir(dir_path):
    if os.path.isdir(os.path.join(dir_path, path)):
        count += 1
        
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

for r in np.arange(1,count):
    #table=pd.read_csv(f"/Users/cherryleheu/Codes/NIDIS-Codes/H-RIP/RID/RID{r:03d}/RID{r:03d}_query.csv",index_col=0)
    table=pd.read_csv(f"../RID/RID{r:03d}/RID{r:03d}_query.csv",index_col=0)
    rf_df=pd.DataFrame({'A' : []})
    
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
    

    # Create a figure and axis with a larger width
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the data
    line1 = ENSO.plot(ax=ax, x='MonthName', y=['MRF', 'MeRF', 'MnRF'], kind="bar", legend=False, color=['#004c6d', '#6996b3', '#c1e7ff'])

    # Create a legend for the first line.
    first_legend = ax.legend(['Mean', '%s Mean'% title, '%s Minimum' % title], fontsize=12, bbox_to_anchor=(1, 1), edgecolor="black",loc="upper left")

    # Set labels and title
    ax.set_xlabel('')
    ax.set_ylabel('Rainfall (in)')

    text = f"Mean                                     {mean:.2f} in\n{title} Mean             {p_mean:.2f} in\n{title} Minimum       {p_min:.2f} in"
    plt.text(0.73, 0.74, text, fontsize=10, transform=plt.gcf().transFigure,
            bbox={'facecolor': 'white', 'alpha': 0.5})

    # Use tight_layout to ensure the plot is fully visible
    plt.tight_layout()
    plt.savefig(f"../RID/RID{r:03d}/RID{r:03d}_rainfall.png",bbox_inches="tight")
    plt.show()
    

