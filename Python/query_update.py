#!/usr/bin/env python
# coding: utf-8
#
# Rebuilds each ranch's ENSO query table (RIDxxx_query.csv): for every month and ENSO phase,
# the all-years mean rainfall/temperature and the mean and minimum in years of that phase.
# rainfall_outlook.py and the ranch page read it. Phases come from NOAA CPC's relative Niño-3.4
# index (RONI), the same source as ONI_gauge.py and New Coords.
#
# Usage (from the H-RIP folder or the Python folder):
#   python Python/query_update.py
#   python Python/query_update.py --ranch RID118     # only these ranches (repeatable)

import argparse
import os

import numpy as np
import pandas as pd

os.chdir(os.path.dirname(os.path.abspath(__file__)))

RONI_URL = 'https://www.cpc.ncep.noaa.gov/data/indices/Rnino34.ascii.txt'
PHASES = ['SEL', 'WEL', 'NUT', 'WLA', 'SLA']


def phase_of(anom):
    if anom > 1.1:
        return 'SEL'
    if anom > 0.5:
        return 'WEL'
    if anom >= -0.5:
        return 'NUT'
    if anom >= -1.1:
        return 'WLA'
    return 'SLA'


def build_query(rf, temp, oni):
    rows = []
    for i in range(1, 13):
        rf_m, t_m = rf[rf.Month == i], temp[temp.Month == i]
        MRF, MT = rf_m.RF_in.mean(), t_m.tmean_f.mean()
        for j in PHASES:
            years = oni.loc[(oni.MON == i) & (oni.PHASE == j), 'YR'].tolist()
            prf, pt = rf_m[rf_m.Year.isin(years)], t_m[t_m.Year.isin(years)]
            MeRF, MnRF = prf.RF_in.mean(), prf.RF_in.min()
            rows.append({'Month': i, 'MRF': MRF, 'Phase': j, 'Count': len(years), 'MeRF': MeRF, 'MnRF': MnRF,
                         'MeAnom': MeRF - MRF, 'MnAnom': MnRF - MRF,
                         'MT': MT, 'MeT': pt.tmean_f.mean(), 'MnT': pt.tmean_f.min()})
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--ranch', action='append', help='only update this ranch, e.g. RID118 (repeatable)')
    args = ap.parse_args()

    oni = pd.read_csv(RONI_URL, sep=r'\s+')
    oni = oni.rename(columns={'MTH': 'MON'})
    oni['ANOM'] = pd.to_numeric(oni['ANOM'], errors='coerce')
    oni = oni.dropna(subset=['ANOM'])
    oni = oni[oni.ANOM > -90]  # guard against missing-value markers
    oni['PHASE'] = oni['ANOM'].apply(phase_of)
    last = oni.iloc[-1]
    print(f"RONI through {int(last.YR)}-{int(last.MON):02d}: {last.ANOM:+.2f} ({last.PHASE})")

    ranches = sorted(d for d in os.listdir('../RID') if d.startswith('RID') and os.path.isdir(f'../RID/{d}'))
    if args.ranch:
        ranches = [r for r in ranches if r in args.ranch]

    done = 0
    for p in ranches:
        try:
            rf = pd.read_csv(f'../RID/{p}/{p}_rf.csv')
            temp = pd.read_csv(f'../RID/{p}/{p}_tmean.csv')
        except FileNotFoundError as e:
            print(f'  {p}: skipped, missing {os.path.basename(e.filename)}')
            continue
        rf = rf[rf.Year > 1949]  # RONI starts Dec 1949
        build_query(rf, temp, oni).to_csv(f'../RID/{p}/{p}_query.csv')
        done += 1
    print(f'Updated query tables for {done} ranches.')


if __name__ == '__main__':
    main()
