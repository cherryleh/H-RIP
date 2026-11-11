#!/usr/bin/env python
# coding: utf-8
#
# Draws each ranch's 3-month ENSO rainfall outlook (RIDxxx_rainfall.png) from its query table
# (RIDxxx_query.csv, made by query_update.py): the all-years mean, and the mean and minimum in
# years with the current ENSO phase, for this month and the next two. The phase comes from the
# latest monthly value of NOAA CPC's relative Niño-3.4 index (RONI).
#
# Usage (from the H-RIP folder or the Python folder):
#   python Python/rainfall_outlook.py
#   python Python/rainfall_outlook.py --ranch RID118     # only these ranches (repeatable)

import argparse
import calendar
import os
from datetime import datetime

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

os.chdir(os.path.dirname(os.path.abspath(__file__)))

RONI_URL = 'https://www.cpc.ncep.noaa.gov/data/indices/Rnino34.ascii.txt'
TITLES = {'SEL': 'Strong El Nino', 'WEL': 'Weak El Nino', 'NUT': 'Neutral',
          'WLA': r'Weak La Ni$\tilde{n}a$', 'SLA': r'Strong La Ni$\tilde{n}a$'}


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


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--ranch', action='append', help='only draw this ranch, e.g. RID118 (repeatable)')
    args = ap.parse_args()

    roni = pd.read_csv(RONI_URL, sep=r'\s+')
    roni['ANOM'] = pd.to_numeric(roni['ANOM'], errors='coerce')
    roni = roni[roni.ANOM > -90].dropna(subset=['ANOM'])
    latest = roni.iloc[-1]  # file is in date order; the last row is the newest month
    phase = phase_of(latest.ANOM)
    title = TITLES[phase]

    now = datetime.now()
    this_month = now.strftime('%B')
    months = [(now.month - 1 + k) % 12 + 1 for k in range(3)]  # this month and the next two, wrapping at December
    print(f"RONI {int(latest.YR)}-{int(latest.MTH):02d} {latest.ANOM:+.2f} -> {phase}; months {months}")

    ranches = sorted(d for d in os.listdir('../RID') if d.startswith('RID') and os.path.isdir(f'../RID/{d}'))
    if args.ranch:
        ranches = [r for r in ranches if r in args.ranch]

    done = 0
    for p in ranches:
        try:
            table = pd.read_csv(f'../RID/{p}/{p}_query.csv', index_col=0)
        except FileNotFoundError:
            print(f'  {p}: skipped, no query table')
            continue
        enso = table[table.Phase == phase].set_index('Month').loc[months].reset_index()
        enso['MonthName'] = enso['Month'].apply(lambda x: calendar.month_abbr[int(x)])
        mean, p_mean, p_min = enso['MRF'].iloc[0], enso['MeRF'].iloc[0], enso['MnRF'].iloc[0]

        fig, ax = plt.subplots(figsize=(12, 10))
        enso.plot(ax=ax, x='MonthName', y=['MRF', 'MeRF', 'MnRF'], kind='bar', legend=False, color=['#004c6d', '#377eb8', '#9ecae1'])
        ax.grid(axis='y', linestyle='--', linewidth=0.6, alpha=0.45)
        ax.set_ylabel('Monthly rainfall (inches)', fontsize=20)
        ax.tick_params(axis='x', labelsize=20)
        ax.tick_params(axis='y', labelsize=20)
        first_legend = ax.legend(['Mean', f'{title} Mean', f'{title} Minimum'], fontsize=20, bbox_to_anchor=(1, 1), edgecolor='black', loc='upper left')
        second_legend = ax.legend([f"Mean                         {mean:.2f} in\n{title} Mean             {p_mean:.2f} in\n{title} Minimum       {p_min:.2f} in"],
                                  loc='center left', handlelength=0, handletextpad=0, bbox_to_anchor=(1, 0.7),
                                  title=f'{p} {this_month} Rainfall', fontsize=20)
        second_legend.get_title().set_fontsize('20')
        ax.add_artist(first_legend)
        ax.set(xlabel=None)
        fig.savefig(f'../RID/{p}/{p}_rainfall.png', bbox_inches='tight')
        plt.close(fig)
        done += 1
    print(f'Drew rainfall outlooks for {done} ranches.')


if __name__ == '__main__':
    main()
