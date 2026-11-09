#!/usr/bin/env python
# coding: utf-8
#
# Picks the ENSO gauge image from the latest monthly RONI value and writes
# gauge/gauge.json so web pages can show the current phase and update date.
# Run from the H-RIP folder: python Python/ONI_gauge.py

import json
import os
import shutil
from datetime import date

import pandas as pd

os.chdir(os.path.dirname(os.path.abspath(__file__)))

RONI = pd.read_csv("https://www.cpc.ncep.noaa.gov/data/indices/Rnino34.ascii.txt", sep=r"\s+")
latest = RONI.iloc[-1]
ANOM = float(latest['ANOM'])

if ANOM > 1.1:
    inputgauge = '../gauge/gauge-7.png'
elif 1.1 >= ANOM > 0.5:
    inputgauge = '../gauge/gauge-6.png'
elif 0.5 >= ANOM > 0:
    inputgauge = '../gauge/gauge-5.png'
elif ANOM == 0:
    inputgauge = '../gauge/gauge-4.png'
elif 0 > ANOM >= -0.5:
    inputgauge = '../gauge/gauge-3.png'
elif -0.5 > ANOM >= -1.1:
    inputgauge = '../gauge/gauge-2.png'
else:
    inputgauge = '../gauge/gauge-1.png'

shutil.copyfile(inputgauge, '../gauge/gauge.png')

# Phase uses the ±0.5 °C threshold; strength uses NOAA CPC's categories.
if ANOM >= 0.5:
    phase = 'El Niño'
elif ANOM <= -0.5:
    phase = 'La Niña'
else:
    phase = 'Neutral'

mag = abs(ANOM)
if phase == 'Neutral':
    strength = ''
elif mag >= 2.0:
    strength = 'Very strong'
elif mag >= 1.5:
    strength = 'Strong'
elif mag >= 1.0:
    strength = 'Moderate'
else:
    strength = 'Weak'

info = {
    'value': round(ANOM, 2),
    'year': int(latest['YR']),
    'month': int(latest['MTH']),
    'phase': phase,
    'strength': strength,
    'updated': date.today().isoformat(),
}
with open('../gauge/gauge.json', 'w') as f:
    json.dump(info, f, ensure_ascii=False, indent=2)

print(f"RONI {ANOM:+.2f} ({info['year']}-{info['month']:02d}) -> {strength} {phase}".strip(), '|', inputgauge)
