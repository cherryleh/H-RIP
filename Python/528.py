import sys
import os
print("path before: " + os.getcwd())
os.chdir('./Python')
print("path after: " + os.getcwd())

import pandas as pd
import collections
from datetime import datetime
import numpy as np
import geopandas as gpd


ranch = sys.argv[1]
grasstype = sys.argv[2]
condition = sys.argv[3]

'''ranch = "RID084"
grasstype = "Signal"
condition = "Unimproved"'''

ranch = int(float(ranch[4:]))


ranchshp = gpd.read_file('./shapefiles/RID.shp',rows=slice(ranch-1, ranch))


ONI=pd.read_csv("https://origin.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/detrend.nino34.ascii.txt",delim_whitespace=True)
ANOM = ONI.iloc[-1]['ANOM']


if ANOM > 1.1: 
    phase = 'SEL'
    phase_name = 'Strong El Ni&#xf1;o'
elif 1.1 >= ANOM >0.5:
    phase = 'WLA'
    phase_name = 'Weak El Ni&#xf1;o'
elif 0.5>=ANOM>=-0.5:
    phase = 'NUT'
    phase_name = 'Neutral'
elif -0.5> ANOM >= -1.1:
    phase = 'WLA'
    phase_name = 'Weak La Ni&#xf1;a'
elif ANOM < -1.1:
    phase = 'SLA'
    phase_name = 'Strong La Ni&#xf1;a'

#Inputs - change this later
soilType = ranchshp['musym'].iloc[0]
island = ranchshp['IS'].iloc[0]

today = datetime.now()
x  = collections.deque(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
forageData = {'Month':list(x)}
forage_avg = pd.DataFrame(data=forageData)

forage_phase = pd.DataFrame(data=forageData)
forage_min = pd.DataFrame(data=forageData)

table = pd.read_csv('./528/SoilPasture.csv')


#Using normal only
if condition == 'Improved':
    forageUsablePounds = int(table.loc[table['SoilSymbol'] == str(soilType), 'Good'].iloc[0])
elif condition == 'Unimproved':
    forageUsablePounds = int(table.loc[table['SoilSymbol'] == str(soilType), 'Poor'].iloc[0])

query = pd.read_csv(f'../RID/RID{ranch:03}/RID{ranch:03}_query.csv')


#528
#Is water a limiting factor?
waterLim = 'Yes'
#Does temp suppress growth?
tempSup = 'Yes'
#If yes, estimate % temp suppression
tempSupPercent = 30

#Constants
#Sun Distance
sunDistData = {'Month':['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
           '%':[7.686,7.227,8.398,8.557,9.204,9.088,9.309,9.088,8.297,8.130,7.517,7.592]}
sunDist = pd.DataFrame(sunDistData)

#Attenuated Curve Index
aci_avg = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
aci_phase = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
aci_min = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
diff_avg = []
diff_phase =[]
diff_min =[]

i_list = [1, 2, 11,12, 3, 4, 5, 6, 7, 8, 9, 10]

for i in i_list:
    if i == 1 or i == 2 or i == 11 or i == 12:
        MRF = query.loc[(query['Month'] == i)]['MRF'].iloc[0]
        aci_avg[i-1] = MRF * (1-(tempSupPercent/100))
        diff_avg.append(MRF-aci_avg[i-1])
        
        MeRF = query.loc[(query['Month'] == i)&(query['Phase']==phase)]['MeRF'].iloc[0]
        aci_phase[i-1] = MeRF * (1-(tempSupPercent/100))
        diff_phase.append(MeRF-aci_phase[i-1])
        
        MnRF = query.loc[(query['Month'] == i)&(query['Phase']==phase)]['MnRF'].iloc[0]
        aci_min[i-1] = MnRF * (1-(tempSupPercent/100))
        diff_min.append(MnRF-aci_min[i-1])
    else:
        MRF = query.loc[(query['Month'] == i)]['MRF'].iloc[0]
        aci_avg[i-1]=MRF + (sum(diff_avg)/8)
        MeRF = query.loc[(query['Month'] == i)&(query['Phase']==phase)]['MeRF'].iloc[0]
        aci_phase[i-1]=MeRF + (sum(diff_phase)/8)
        
        MnRF = query.loc[(query['Month'] == i)&(query['Phase']==phase)]['MnRF'].iloc[0]
        aci_min[i-1]=MnRF + (sum(diff_min)/8)

aci_norm_avg=[]
aci_norm_phase=[]
aci_norm_min=[]
#Normalized Attenuated Index
for i in np.arange(1,13):
    aci_norm_avg.append(aci_avg[i-1]/sum(aci_avg))
    aci_norm_phase.append(aci_phase[i-1]/sum(aci_phase))
    aci_norm_min.append(aci_min[i-1]/sum(aci_min))
    
#Forage Growth Curve
fgc_avg =[]
fgc_phase =[]
fgc_min =[]
for i in range(len(aci_norm_avg)):
    if i == 0:
        new_value_avg = (aci_norm_avg[i] + aci_norm_avg[-1]) / 2
        new_value_phase = (aci_norm_phase[i] + aci_norm_phase[-1]) / 2
        new_value_min = (aci_norm_min[i] + aci_norm_min[-1]) / 2
    else:
        new_value_avg = (aci_norm_avg[i] + aci_norm_avg[i - 1]) / 2
        new_value_phase = (aci_norm_phase[i] + aci_norm_phase[i - 1]) / 2
        new_value_min = (aci_norm_min[i] + aci_norm_min[i - 1]) / 2
    fgc_avg.append(new_value_avg)
    fgc_phase.append(new_value_phase)
    fgc_min.append(new_value_min)


forageYield_avg = []
forageYield_phase = []
forageYield_min = []
for i in np.arange(1,13):
    forageYield_avg.append(fgc_avg[i-1]*forageUsablePounds)
    forageYield_phase.append(fgc_phase[i-1]*forageUsablePounds)
    forageYield_min.append(fgc_min[i-1]*forageUsablePounds)

    
forage_avg['528']=forageYield_avg
forage_phase['528']=forageYield_phase
forage_min['528']=forageYield_min

#HFPET
if grasstype == "Guinea":
    pass
else: 
    convFactorData = {'Isl':['BI','KA','LA','MA','MO','OA'],
           'Factor':[105.6,171.6,165,217.8,165,165]}
    convFactor = pd.DataFrame(data=convFactorData)
    hfpet_avg =[]
    hfpet_phase =[]
    hfpet_min =[]
    for i in np.arange(1,13):
        MRF = query.loc[(query['Month'] == i)]['MRF'].iloc[0]
        hfpet_avg.append(convFactor.loc[(convFactor['Isl']==island)]['Factor'].iloc[0]*MRF)
        MeRF = query.loc[(query['Month'] == i)&(query['Phase']==phase)]['MeRF'].iloc[0]
        hfpet_phase.append(convFactor.loc[(convFactor['Isl']==island)]['Factor'].iloc[0]*MeRF)
        MnRF = query.loc[(query['Month'] == i)&(query['Phase']==phase)]['MnRF'].iloc[0]
        hfpet_min.append(convFactor.loc[(convFactor['Isl']==island)]['Factor'].iloc[0]*MnRF)

    forage_avg['hfpet']=hfpet_avg
    forage_phase['hfpet']=hfpet_phase
    forage_min['hfpet']=hfpet_min

#Get soil organic matter
soilOM = table.loc[table['SoilSymbol'] == str(soilType), 'Organic Matter'].iloc[0]
if soilOM <=0.1:
    soilOMYieldFactor = soilOM*1.5625
elif soilOM<=3.58:
    soilOMYieldFactor = soilOM*0.1347+0.1428
elif soilOM<=12.83:
    soilOMYieldFactor = soilOM*0.027+0.5282
elif soilOM<=20.08:
    soilOMYieldFactor = soilOM*0.0172+0.6538
else:
    soilOMYieldFactor = 1

#Reference table
ecoCropTable = pd.read_csv('./528/ecocropTable.csv')
a = {}

#Multiply soilOM by lbs/acre/year
for column in ecoCropTable.columns:
    if column == 'Parameter':
        a[column]='OM Adjusted - lbs/acre/year'
        continue
    a[column] = float(ecoCropTable.loc[ecoCropTable['Parameter'] == 'lbs/acre/year', column].iloc[0])*soilOMYieldFactor
        
ecoCropTable = ecoCropTable.append(a, ignore_index=True)

#Index if grasstype = ceci
ceci = [0.058,0.064,0.076,0.091,0.104,0.115,0.119,0.112,0.093,0.058,0.075,0.038]
#Get grass code
grassLookup = pd.read_csv('./528/GrassCodes.csv')
grassCode = grassLookup.loc[grassLookup['Forage'] == grasstype, 'Symbol'].iloc[0]
ecoMaxYield = {'Month':['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']}
ecoMaxYield['Max Yield']=[]

for i in range(12):
    if grassCode=='CECI':
        #ecoMaxYield['CECI'].append(float(ecoCropTable.loc[ecoCropTable['Parameter'] == 'OM Adjusted - lbs/acre/year', 'CECI'].iloc[0])*ceci[i])
        ecoMaxYield['Max Yield'].append(float(ecoCropTable.loc[ecoCropTable['Parameter'] == 'OM Adjusted - lbs/acre/year', 'CECI'].iloc[0])*ceci[i])
        continue
    ecoMaxYield['Max Yield'] = float(ecoCropTable.loc[ecoCropTable['Parameter'] == 'OM Adjusted - lbs/acre/year', grassCode].iloc[0])*1/12

ecoMaxYield = pd.DataFrame(ecoMaxYield)

eco_t_avg =[]
eco_rf_avg = []

minTemp = float(ecoCropTable.loc[ecoCropTable['Parameter'] == 'Temp (minF)', grassCode].iloc[0])
maxTemp = float(ecoCropTable.loc[ecoCropTable['Parameter'] == 'Temp (maxF)', grassCode].iloc[0])
optMinTemp = float(ecoCropTable.loc[ecoCropTable['Parameter'] == 'Optimum Temp (minF)', grassCode].iloc[0])
optMaxTemp = float(ecoCropTable.loc[ecoCropTable['Parameter'] == 'Optimum Temp (maxF)', grassCode].iloc[0])

minRF = float(ecoCropTable.loc[ecoCropTable['Parameter'] == 'Rain (minin)', grassCode].iloc[0])
maxRF = float(ecoCropTable.loc[ecoCropTable['Parameter'] == 'Rain (maxin)', grassCode].iloc[0])
optMinRF = float(ecoCropTable.loc[ecoCropTable['Parameter'] == 'Optimum Rain (minin)', grassCode].iloc[0])
optMaxRF = float(ecoCropTable.loc[ecoCropTable['Parameter'] == 'Optimum Rain (maxin)', grassCode].iloc[0])

for i in range(12):
    meanTemp = query.loc[(query['Month'] == i+1)]['MT'].iloc[0]
    if meanTemp <= minTemp:
        eco_t_avg.append(0)
    elif meanTemp <= optMinTemp:
        eco_t_avg.append((meanTemp-minTemp)/(optMinTemp-minTemp))
    elif meanTemp <= optMaxTemp:
        eco_t_avg.append(1)
    elif meanTemp <= maxTemp:
        eco_t_avg.append(1 - (meanTemp-optMaxTemp)/(maxTemp-optMaxTemp))
    else:
        eco_t_avg.append(0)

for i in range(12):
    meanRF = query.loc[(query['Month'] == i+1)]['MRF'].iloc[0]
    if meanRF <= minRF:
        eco_rf_avg.append(0)
    elif meanRF <= optMinRF:
        eco_rf_avg.append((meanRF-minRF)/(optMinRF-minRF))
    elif meanRF <= optMaxRF:
        eco_rf_avg.append(1)
    elif meanRF <= maxRF:
        eco_rf_avg.append((1 - (meanRF-optMaxRF)/(maxRF-optMaxRF)))
    else:
        eco_rf_avg.append(0)

eco_yield_avg = []
for i in range(0, len(eco_t_avg)):
    eco_yield_avg.append(eco_t_avg[i] * eco_rf_avg[i]*ecoMaxYield['Max Yield'].iloc[i])
    
eco_t_phase =[]
eco_rf_phase = []
for i in range(12):
    meanTempPhase = query.loc[(query['Month'] == i+1)&(query['Phase']==phase)]['MeT'].iloc[0]
    if meanTempPhase <= minTemp:
        eco_t_phase.append(0)
    elif meanTempPhase <= optMinTemp:
        eco_t_phase.append((meanTempPhase-minTemp)/(optMinTemp-minTemp))
    elif meanTempPhase <= optMaxTemp:
        eco_t_phase.append(1)
    elif meanTempPhase <= maxTemp:
        eco_t_phase.append(1 - (meanTempPhase-optMaxTemp)/(maxTemp-optMaxTemp))
    else:
        eco_t_phase.append(0)

for i in range(12):
    meanRFPhase = query.loc[(query['Month'] == i+1)&(query['Phase']==phase)]['MeRF'].iloc[0]
    if meanRFPhase <= minRF:
        eco_rf_phase.append(0)
    elif meanRFPhase <= optMinRF:
        eco_rf_phase.append((meanRFPhase-minRF)/(optMinRF-minRF))
    elif meanRFPhase <= optMaxRF:
        eco_rf_phase.append(1)
    elif meanRFPhase <= maxRF:
        eco_rf_phase.append((1 - (meanRFPhase-optMaxRF)/(maxRF-optMaxRF)))
    else:
        eco_rf_phase.append(0)

eco_yield_phase = []
for i in range(0, len(eco_t_phase)):
    eco_yield_phase.append(eco_t_phase[i] * eco_rf_phase[i]*ecoMaxYield['Max Yield'].iloc[i])

eco_t_min =[]
eco_rf_min = []
for i in range(12):
    minTempPhase = query.loc[(query['Month'] == i+1)&(query['Phase']==phase)]['MnT'].iloc[0]
    if minTempPhase <= minTemp:
        eco_t_min.append(0)
    elif minTempPhase <= optMinTemp:
        eco_t_min.append((minTempPhase-minTemp)/(optMinTemp-minTemp))
    elif minTempPhase <= optMaxTemp:
        eco_t_min.append(1)
    elif minTempPhase <= maxTemp:
        eco_t_min.append(1 - (minTempPhase-optMaxTemp)/(maxTemp-optMaxTemp))
    else:
        eco_t_min.append(0)
        

for i in range(12):
    minRFPhase = query.loc[(query['Month'] == i+1)&(query['Phase']==phase)]['MnRF'].iloc[0]
    if minRFPhase <= minRF:
        eco_rf_min.append(0)
    elif minRFPhase <= optMinRF:
        eco_rf_min.append((minRFPhase-minRF)/(optMinRF-minRF))
    elif minRFPhase <= optMaxRF:
        eco_rf_min.append(1)
    elif minRFPhase <= maxRF:
        eco_rf_min.append((1 - (minRFPhase-optMaxRF)/(maxRF-optMaxRF)))
    else:
        eco_rf_min.append(0)


eco_yield_min = []
for i in range(0, len(eco_t_min)):
    eco_yield_min.append(eco_t_min[i] * eco_rf_min[i]*ecoMaxYield['Max Yield'].iloc[i])

eco_yield_avg = [value * 1.1 for value in eco_yield_avg]
eco_yield_phase = [value * 1.1 for value in eco_yield_phase]
eco_yield_min = [value * 1.1 for value in eco_yield_min]

forage_avg['ecocrop']=eco_yield_avg
forage_phase['ecocrop']=eco_yield_phase
forage_min['ecocrop']=eco_yield_min

#Pasture Groups
#Get site's pasture group
pastureGroup = int(table.loc[table['SoilSymbol'] == str(soilType), 'Pasture Group'].iloc[0])

#Get pasture group data based on island
if island == "BI":
    pasture = pd.read_csv("./528/PastureGroups_HawaiiIsland.csv")
else:
    pasture = pd.read_csv("./528/PastureGroups_FourIslands.csv")

#Read values based on improved or unimproved
if condition == "Unimproved":
    pasture_forage = table.loc[table['SoilSymbol'] == str(soilType), 'Poor'].iloc[0]
elif condition == "Improved":
    pasture_forage = table.loc[table['SoilSymbol'] == str(soilType), 'Good'].iloc[0]

#Get yield
pasture_yield_1 = []
for i in range(12):
    pasture_yield_1.append(pasture[str(pastureGroup)].iloc[i])
    pasture_yield = [i * forageUsablePounds for i in pasture_yield_1]

forage_avg['pasture']=pasture_yield
forage_phase['pasture']=pasture_yield
forage_min['pasture']=pasture_yield

#Joe May
#Total Annual Rainfall
annualRF_avg = query[query['Phase']==phase]['MRF'].sum()
annualRF_phase = query[query['Phase']==phase]['MeRF'].sum()
annualRF_min = query[query['Phase']==phase]['MnRF'].sum()

#Range Type Table
rangeTypeTable = pd.read_csv("./528/JoeMay.csv")
#Range Type Growth Curve
rangeTypeGrowthCurve = pd.read_csv("./528/RangeTypeGrowthCurve.csv")

#Get range type
def is_between(number, lower_limit, upper_limit):
    return lower_limit <= number < upper_limit

for i in range(11):
    lower = float(rangeTypeTable.loc[rangeTypeTable['Parameter'] == 'Minimum Annual Rainfall', str(i+1)].iloc[0])
    upper = float(rangeTypeTable.loc[rangeTypeTable['Parameter'] == 'Maximum Annual Rainfall', str(i+1)].iloc[0])
    if is_between(annualRF_avg, lower, upper):
        cell_value = rangeTypeTable.loc[3, str(i+1)]
        if isinstance(cell_value, (int, np.integer)) and cell_value == float(pastureGroup):
            rangeType_avg = i+1
            break
        elif isinstance(cell_value, list) and pastureGroup in cell_value:
            rangeType_avg = i+1
            #print(f"The range type is {i+1}")
            break
    else:
        rangeType_avg = np.nan
        #print(f"{annualRF_avg} is NOT between {lower} and {upper}. Range type: {i+1}")

#Get range type
def is_between(number, lower_limit, upper_limit):
    return lower_limit <= number < upper_limit

for i in range(11):
    lower = float(rangeTypeTable.loc[rangeTypeTable['Parameter'] == 'Minimum Annual Rainfall', str(i+1)].iloc[0])
    upper = float(rangeTypeTable.loc[rangeTypeTable['Parameter'] == 'Maximum Annual Rainfall', str(i+1)].iloc[0])
    if is_between(annualRF_phase, lower, upper):
        #print(f"{annualRF_phase} is between {lower} and {upper}. Range type: {i+1}")
        cell_value = rangeTypeTable.loc[3, str(i+1)]
        if isinstance(cell_value, (int, np.integer)) and cell_value == float(pastureGroup):
            rangeType_phase = i+1
            #print(f"The range type is {i+1}")
            break
        elif isinstance(cell_value, list) and pastureGroup in cell_value:
            rangeType_phase = i+1
            #print(f"The range type is {i+1}")
            break
    else:
        rangeType_phase = np.nan
        #print(f"{annualRF_phase} is NOT between {lower} and {upper}. Range type: {i+1}")

        #Get range type
def is_between(number, lower_limit, upper_limit):
    return lower_limit <= number < upper_limit

for i in range(11):
    lower = float(rangeTypeTable.loc[rangeTypeTable['Parameter'] == 'Minimum Annual Rainfall', str(i+1)].iloc[0])
    upper = float(rangeTypeTable.loc[rangeTypeTable['Parameter'] == 'Maximum Annual Rainfall', str(i+1)].iloc[0])
    if is_between(annualRF_min, lower, upper):
        #print(f"{annualRF_min} is between {lower} and {upper}. Range type: {i+1}")
        cell_value = rangeTypeTable.loc[3, str(i+1)]
        if isinstance(cell_value, (int, np.integer)) and cell_value == float(pastureGroup):
            rangeType_min = i+1
            #print(f"The range type is {i+1}")
            break
        elif isinstance(cell_value, list) and pastureGroup in cell_value:
            rangeType_min = i+1
            #print(f"The range type is {i+1}")
            break
    else:
        rangeType_min = np.nan
        #print(f"{annualRF_min} is NOT between {lower} and {upper}. Range type: {i+1}")

if isinstance(rangeType_avg, int):
    JoeMay_avg = [value * rangeTypeTable.loc[rangeTypeTable['Parameter'] == 'Average Annual Yield (lbs/acre)', str(rangeType_avg)].iloc[0] for value in rangeTypeGrowthCurve[str(rangeType_avg)].tolist()]
    forage_avg['Joe May']=JoeMay_avg
else:
    pass

if isinstance(rangeType_phase, int):
    JoeMay_phase = [value * rangeTypeTable.loc[rangeTypeTable['Parameter'] == 'Average Annual Yield (lbs/acre)', str(rangeType_phase)].iloc[0] for value in rangeTypeGrowthCurve[str(rangeType_phase)].tolist()]
    forage_phase['Joe May']=JoeMay_phase
else:
    pass

if isinstance(rangeType_min, int):
    JoeMay_min = [value * rangeTypeTable.loc[rangeTypeTable['Parameter'] == 'Average Annual Yield (lbs/acre)', str(rangeType_min)].iloc[0] for value in rangeTypeGrowthCurve[str(rangeType_min)].tolist()]
    forage_min['Joe May']=JoeMay_min
else:
    pass


forage_avg['Average'] = forage_avg.iloc[:, 1:len(forage_avg.columns)+1].mean(axis=1)
forage_phase['Average'] = forage_phase.iloc[:, 1:len(forage_phase.columns)+1].mean(axis=1)
forage_min['Average'] = forage_min.iloc[:, 1:len(forage_min.columns)+1].mean(axis=1)

forage_phase['Percent Change'] = 0.0
forage_phase['Difference'] = 0.0
forage_phase['Color'] = ''
forage_phase['Arrow'] = ''
for i in range(len(forage_avg)):
    percent_change = (forage_phase['Average'].iloc[i] - forage_avg['Average'].iloc[i]) / forage_avg['Average'].iloc[i] * 100
    if percent_change < 10 and percent_change>0:
        percent_change = round(percent_change,1)
    else:
        percent_change = round(percent_change)
    diff = forage_phase['Average'].iloc[i] - forage_avg['Average'].iloc[i] 
    forage_phase.loc[i, 'Percent Change'] = str(percent_change)
    
    if diff>=0:
        forage_phase.loc[i, 'Difference'] = '+'+str(round(diff))
    else:
        forage_phase.loc[i, 'Difference'] = str(round(diff))
    if percent_change < 0:
        color = 'red'
        arrow = '&#x2193;'
    else:
        color = 'green'
        arrow = '&#x2191;'
    forage_phase.loc[i,'Color'] = color
    forage_phase.loc[i,'Arrow'] = arrow

forage_min['Percent Change'] = 0.0
forage_min['Difference'] = 0.0
forage_min['Color'] = ''
forage_min['Arrow'] = ''
for i in range(len(forage_avg)):
    percent_change = (forage_min['Average'].iloc[i] - forage_avg['Average'].iloc[i]) / forage_avg['Average'].iloc[i] * 100
    if percent_change < 10 and percent_change>0:
        percent_change = round(percent_change,1)
    else:
        percent_change = round(percent_change)
    diff = forage_min['Average'].iloc[i] - forage_avg['Average'].iloc[i] 
    forage_min.loc[i, 'Percent Change'] = str(percent_change)
    if diff>=0:
        forage_min.loc[i, 'Difference'] = '+'+str(round(diff))
    else:
        forage_min.loc[i, 'Difference'] = str(round(diff))
    if percent_change < 0:
        color = 'red'
        arrow = '&#x2193;'
    else:
        color = 'green'
        arrow = '&#x2191;'
    forage_min.loc[i,'Color'] = color
    forage_min.loc[i,'Arrow'] = arrow


if today.day < 8:
    subtr = 2
else:
    subtr = 1

    
forage_avg = forage_avg.iloc[np.roll(np.arange(len(forage_avg)), -(today.month - subtr))]
forage_phase = forage_phase.iloc[np.roll(np.arange(len(forage_phase)), -(today.month - subtr))]
forage_min = forage_min.iloc[np.roll(np.arange(len(forage_min)), -(today.month - subtr))]


print(
f'''

<div id="output">
    <div class="tabs">
        <input type="radio" name="tabs" id="tabone" checked="checked">
        <label for="tabone">3-Month Outlook</label>
        <div class="tab" id="three-month">
            <h3 class="" style="margin:0"> Estimated Forage Production: 3-Month Outlook</h3> 
            <div class="" style="margin-left:40px"><b>Grass Type:</b> {grasstype}<span style="margin-left:20px"></span><b>Conditions:</b> {condition}<span style="margin-left:20px"><b>ENSO Phase:</b> {phase_name}</div>
            <br>
            <table class="output-table">
                <colgroup>
                    <col>
                    <col class="outlined-3">
                    <col class="outlined-3">
                    <col class="outlined-3">
                </colgroup>
                <tr>
                    <th></th>
                    <th>{forage_avg['Month'].iloc[0]}</th>
                    <th>{forage_avg['Month'].iloc[1]}</th>
                    <th>{forage_avg['Month'].iloc[2]}</th>

                </tr>
                <tr>
                    <td>Average Production</td>
                    <td>{round(forage_avg['Average'].iloc[0])} <br> <span class="change"> lbs/acre </span> </td>
                    <td>{round(forage_avg['Average'].iloc[1])} <br> <span class="change"> lbs/acre </span>  </td>
                    <td>{round(forage_avg['Average'].iloc[2])} <br> <span class="change"> lbs/acre </span>  </td>

                </tr>
                <tr>
                    <td>Estimated Average Production</td>
                    <td style="color:{forage_phase['Color'].iloc[0]}">{forage_phase['Arrow'].iloc[0]}{forage_phase['Percent Change'].iloc[0]}% <br> <span class="change">{forage_phase['Difference'].iloc[0]} lbs/acre </span> </td>
                    <td style="color:{forage_phase['Color'].iloc[1]}">{forage_phase['Arrow'].iloc[1]}{forage_phase['Percent Change'].iloc[1]}% <br> <span class="change">{forage_phase['Difference'].iloc[1]} lbs/acre </span> </td>
                    <td style="color:{forage_phase['Color'].iloc[2]}">{forage_phase['Arrow'].iloc[2]}{forage_phase['Percent Change'].iloc[2]}% <br> <span class="change">{forage_phase['Difference'].iloc[2]} lbs/acre </span> </td>
                </tr>
                <tr>
                    <td>Estimated Minimum Production</td>
                    <td style="color:{forage_min['Color'].iloc[0]}"> {forage_min['Arrow'].iloc[0]}{forage_min['Percent Change'].iloc[0]}% <br> <span class="change">{forage_min['Difference'].iloc[0]} lbs/acre </span></td>
                    <td style="color:{forage_min['Color'].iloc[1]}"> {forage_min['Arrow'].iloc[1]}{forage_min['Percent Change'].iloc[1]}% <br> <span class="change">{forage_min['Difference'].iloc[1]} lbs/acre </span></td>
                    <td style="color:{forage_min['Color'].iloc[2]}"> {forage_min['Arrow'].iloc[2]}{forage_min['Percent Change'].iloc[2]}% <br> <span class="change">{forage_min['Difference'].iloc[2] } lbs/acre </span></td>
                </tr>

            </table>

        </div>

        <input type="radio" name="tabs" id="tabtwo">
        <label for="tabtwo">6-Month Outlook</label>
        <div class="tab six-month">
            <h3 style="margin:0"> Estimated Forage Production: 6-Month Outlook</h3>
            <div class="" style="margin-left:40px"><b>Grass Type:</b> {grasstype}<span style="margin-left:20px"></span><b>Conditions:</b> {condition}<span style="margin-left:20px"><b>ENSO Phase:</b>{phase_name}</div>
            <br>
            <div class="scroll">
                <table class="output-table">
                    <colgroup>
                        <col>
                        <col class="outlined-6">
                        <col class="outlined-6">
                        <col class="outlined-6">
                        <col class="outlined-6">
                        <col class="outlined-6">
                        <col class="outlined-6">
                    </colgroup>
                    <tr>
                        <th></th>
                        <th>{forage_avg['Month'].iloc[0]}</th>
                        <th>{forage_avg['Month'].iloc[1]}</th>
                        <th>{forage_avg['Month'].iloc[2]}</th>
                        <th>{forage_avg['Month'].iloc[3]}</th>
                        <th>{forage_avg['Month'].iloc[4]}</th>
                        <th>{forage_avg['Month'].iloc[5]}</th>

                    </tr>
                    <tr>
                        <td>Average Production</td>
                        <td>{round(forage_avg['Average'].iloc[0])} <br> <span class="change"> lbs/acre </span> </td>
                        <td>{round(forage_avg['Average'].iloc[1])} <br> <span class="change"> lbs/acre </span> </td>
                        <td>{round(forage_avg['Average'].iloc[2])} <br> <span class="change"> lbs/acre </span> </td>
                        <td>{round(forage_avg['Average'].iloc[3])} <br> <span class="change"> lbs/acre </span> </td>
                        <td>{round(forage_avg['Average'].iloc[4])} <br> <span class="change"> lbs/acre </span> </td>
                        <td>{round(forage_avg['Average'].iloc[5])} <br> <span class="change"> lbs/acre </span> </td>

                    </tr>
                    <tr>
                        <td>Average Production Outlook</td>
                        <td style="color:{forage_phase['Color'].iloc[0]}">{forage_phase['Arrow'].iloc[0]}{forage_phase['Percent Change'].iloc[0]}% <br> <span class="change">{forage_phase['Difference'].iloc[0]} lbs/acre </span> </td>
                        <td style="color:{forage_phase['Color'].iloc[1]}">{forage_phase['Arrow'].iloc[1]}{forage_phase['Percent Change'].iloc[1]}% <br> <span class="change">{forage_phase['Difference'].iloc[1]} lbs/acre </span> </td>
                        <td style="color:{forage_phase['Color'].iloc[2]}">{forage_phase['Arrow'].iloc[2]}{forage_phase['Percent Change'].iloc[2]}% <br> <span class="change">{forage_phase['Difference'].iloc[2]} lbs/acre </span> </td>
                        <td style="color:{forage_phase['Color'].iloc[3]}">{forage_phase['Arrow'].iloc[3]}{forage_phase['Percent Change'].iloc[3]}% <br> <span class="change">{forage_phase['Difference'].iloc[3]} lbs/acre </span> </td>
                        <td style="color:{forage_phase['Color'].iloc[4]}">{forage_phase['Arrow'].iloc[4]}{forage_phase['Percent Change'].iloc[4]}% <br> <span class="change">{forage_phase['Difference'].iloc[4]} lbs/acre </span> </td>
                        <td style="color:{forage_phase['Color'].iloc[5]}">{forage_phase['Arrow'].iloc[5]}{forage_phase['Percent Change'].iloc[5]}% <br> <span class="change">{forage_phase['Difference'].iloc[5]} lbs/acre </span> </td>

                    </tr>
                    <tr>
                        <td>Minimum Production Outlook</td>
                        <td style="color:{forage_min['Color'].iloc[0]}">{forage_min['Arrow'].iloc[0]}{forage_min['Percent Change'].iloc[0]}% <br> <span class="change">{forage_min['Difference'].iloc[0]} lbs/acre </span> </td>
                        <td style="color:{forage_min['Color'].iloc[1]}">{forage_min['Arrow'].iloc[1]}{forage_min['Percent Change'].iloc[1]}% <br> <span class="change">{forage_min['Difference'].iloc[1]} lbs/acre </span> </td>
                        <td style="color:{forage_min['Color'].iloc[2]}">{forage_min['Arrow'].iloc[2]}{forage_min['Percent Change'].iloc[2]}% <br> <span class="change">{forage_min['Difference'].iloc[2]} lbs/acre </span> </td>
                        <td style="color:{forage_min['Color'].iloc[3]}">{forage_min['Arrow'].iloc[3]}{forage_min['Percent Change'].iloc[3]}% <br> <span class="change">{forage_min['Difference'].iloc[3]} lbs/acre </span> </td>
                        <td style="color:{forage_min['Color'].iloc[4]}">{forage_min['Arrow'].iloc[4]}{forage_min['Percent Change'].iloc[4]}% <br> <span class="change">{forage_min['Difference'].iloc[4]} lbs/acre </span> </td>
                        <td style="color:{forage_min['Color'].iloc[5]}">{forage_min['Arrow'].iloc[5]}{forage_min['Percent Change'].iloc[5]}% <br> <span class="change">{forage_min['Difference'].iloc[5]} lbs/acre </span> </td>
                    </tr>

                </table>
            </div>
        </div>

        <input type="radio" name="tabs" id="tabthree">
        <label for="tabthree">Prior Months</label>
        <div class="tab six-month">
            <h3 style="margin:0"> Estimated Forage Production: Prior Months</h3>
            <div class="" style="margin-left:40px"><b>Grass Type:</b> {grasstype}<span style="margin-left:20px"></span><b>Conditions:</b> {condition}<span style="margin-left:20px"><b>ENSO Phase:</b>{phase_name}</div>
            <br>
            <div class="scroll">
                <table class="output-table">
                    <colgroup>
                        <col>
                        <col class="outlined-6">
                        <col class="outlined-6">
                        <col class="outlined-6">
                        <col class="outlined-6">
                        <col class="outlined-6">
                        <col class="outlined-6">
                    </colgroup>
                    <tr>
                        <th></th>
                        <th>{forage_avg['Month'].iloc[-1]}</th>
                        <th>{forage_avg['Month'].iloc[-2]}</th>
                        <th>{forage_avg['Month'].iloc[-3]}</th>
                        <th>{forage_avg['Month'].iloc[-4]}</th>
                        <th>{forage_avg['Month'].iloc[-5]}</th>
                        <th>{forage_avg['Month'].iloc[-6]}</th>

                    </tr>
                    <tr>
                        <td>Average Production</td>
                        <td>{round(forage_avg['Average'].iloc[-1])} <br> <span class="change"> lbs/acre </span> </td>
                        <td>{round(forage_avg['Average'].iloc[-2])} <br> <span class="change"> lbs/acre </span> </td>
                        <td>{round(forage_avg['Average'].iloc[-3])} <br> <span class="change"> lbs/acre </span> </td>
                        <td>{round(forage_avg['Average'].iloc[-4])} <br> <span class="change"> lbs/acre </span> </td>
                        <td>{round(forage_avg['Average'].iloc[-5])} <br> <span class="change"> lbs/acre </span> </td>
                        <td>{round(forage_avg['Average'].iloc[-6])} <br> <span class="change"> lbs/acre </span> </td>

                    </tr>
                    <tr>
                        <td>Average Production Outlook</td>
                        <td style="color:{forage_phase['Color'].iloc[-1]}">{forage_phase['Arrow'].iloc[-1]}{forage_phase['Percent Change'].iloc[-1]}% <br> <span class="change">{forage_phase['Difference'].iloc[-1]} lbs/acre </span> </td>
                        <td style="color:{forage_phase['Color'].iloc[-2]}">{forage_phase['Arrow'].iloc[-2]}{forage_phase['Percent Change'].iloc[-2]}% <br> <span class="change">{forage_phase['Difference'].iloc[-2]} lbs/acre </span> </td>
                        <td style="color:{forage_phase['Color'].iloc[-3]}">{forage_phase['Arrow'].iloc[-3]}{forage_phase['Percent Change'].iloc[-3]}% <br> <span class="change">{forage_phase['Difference'].iloc[-3]} lbs/acre </span> </td>
                        <td style="color:{forage_phase['Color'].iloc[-4]}">{forage_phase['Arrow'].iloc[-4]}{forage_phase['Percent Change'].iloc[-4]}% <br> <span class="change">{forage_phase['Difference'].iloc[-4]} lbs/acre </span> </td>
                        <td style="color:{forage_phase['Color'].iloc[-5]}">{forage_phase['Arrow'].iloc[-5]}{forage_phase['Percent Change'].iloc[-5]}% <br> <span class="change">{forage_phase['Difference'].iloc[-5]} lbs/acre </span> </td>
                        <td style="color:{forage_phase['Color'].iloc[-6]}">{forage_phase['Arrow'].iloc[-6]}{forage_phase['Percent Change'].iloc[-6]}% <br> <span class="change">{forage_phase['Difference'].iloc[-6]} lbs/acre </span> </td>

                    </tr>
                    <tr>
                        <td>Minimum Production Outlook</td>
                        <td style="color:{forage_min['Color'].iloc[-1]}">{forage_min['Arrow'].iloc[-1]}{forage_min['Percent Change'].iloc[-1]}% <br> <span class="change">{forage_min['Difference'].iloc[-1]} lbs/acre </span> </td>
                        <td style="color:{forage_min['Color'].iloc[-2]}">{forage_min['Arrow'].iloc[-2]}{forage_min['Percent Change'].iloc[-2]}% <br> <span class="change">{forage_min['Difference'].iloc[-2]} lbs/acre </span> </td>
                        <td style="color:{forage_min['Color'].iloc[-3]}">{forage_min['Arrow'].iloc[-3]}{forage_min['Percent Change'].iloc[-3]}% <br> <span class="change">{forage_min['Difference'].iloc[-3]} lbs/acre </span> </td>
                        <td style="color:{forage_min['Color'].iloc[-4]}">{forage_min['Arrow'].iloc[-4]}{forage_min['Percent Change'].iloc[-4]}% <br> <span class="change">{forage_min['Difference'].iloc[-4]} lbs/acre </span> </td>
                        <td style="color:{forage_min['Color'].iloc[-5]}">{forage_min['Arrow'].iloc[-5]}{forage_min['Percent Change'].iloc[-5]}% <br> <span class="change">{forage_min['Difference'].iloc[-5]} lbs/acre </span> </td>
                        <td style="color:{forage_min['Color'].iloc[-6]}">{forage_min['Arrow'].iloc[-6]}{forage_min['Percent Change'].iloc[-6]}% <br> <span class="change">{forage_min['Difference'].iloc[-6]} lbs/acre </span> </td>
                    </tr>

                </table>
            </div>
        </div>
    </div>


</div>''')

