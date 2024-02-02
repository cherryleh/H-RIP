#!/usr/bin/env python
# coding: utf-8


import pandas as pd
#import plotly.graph_objects as go
import matplotlib.pyplot as plt
from numpy import radians, cos, sin, pi
import os
#os.chdir('/Users/cherryleheu/Codes/NIDIS-Codes/H-RIP/Python')
#os.chdir('./Python')
import sys
from subprocess import run
from PIL import Image, ImageFont, ImageDraw 

ONI=pd.read_csv("https://origin.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/detrend.nino34.ascii.txt",delim_whitespace=True)
ANOM = ONI.iloc[-1]['ANOM']

if ANOM > 1.1: 
    inputgauge = '../gauge/gauge-7.png'
elif 1.1 >= ANOM >0.5:
    inputgauge = '../gauge/gauge-6.png'
elif 0.5>=ANOM>0:
    inputgauge = '../gauge/gauge-5.png'
elif ANOM==0:
    inputgauge = '../gauge/gauge-4.png'
elif 0>ANOM>=-0.5:
    inputgauge = '../gauge/gauge-3.png'
elif -0.5> ANOM >= -1.1:
    inputgauge = '../gauge/gauge-2.png'
elif ANOM < -1.1:
    inputgauge = '../gauge/gauge-1.png'
else:
    print("Error")

from datetime import datetime
from dateutil.relativedelta import relativedelta

now = datetime.now()

lastMonth = (now+relativedelta(months=-1)).strftime("%B")

run(['cp',inputgauge,'../gauge/gauge.png'])

oni_image = Image.open('../gauge/gauge.png')

myFont = ImageFont.truetype('../Lato/Lato-Light.ttf', 65)

from PIL import Image, ImageDraw, ImageFont
import textwrap

astr = f"Last updated: {lastMonth}"
para = textwrap.wrap(astr)

MAX_W, MAX_H = 1500,650
im = Image.new('RGB', (MAX_W, MAX_H), (0, 0, 0, 0))
draw = ImageDraw.Draw(im)

oni_image = Image.open('../gauge/gauge.png')
gauge = ImageDraw.Draw(oni_image)
current_h, pad = 900, 10
for line in para:
    w, h = draw.textsize(line, font=myFont)
    gauge.text(((MAX_W - w) / 2, current_h), line, font=myFont,fill='#000')
    current_h += h + pad

oni_image.save('../gauge/gauge.png')

