#!/usr/bin/env python
# coding: utf-8
#
# Monthly mean temperature update for every ranch.
#
# Downloads HCDP's monthly mean temperature map (temp_monthly_maps/mean/t_month_mean_YYYY_MM.tif,
# which maps.py draws from), adds each ranch's average in °F to RIDxxx_tmean.csv, and rebuilds
# RIDxxx_t_month.csv and RIDxxx_t_12m.csv from it. These are the files RID.php, plotly.js and
# the ranch page read:
#   RIDxxx_tmean.csv    Year, Month, tmean_f, datetime
#   RIDxxx_t_month.csv  (index), oldMonth, OldTemp, Month, Temp   - monthly averages, current month first
#   RIDxxx_t_12m.csv    (index), Month, Temp                      - last 12 months
#   RIDxxx_temp_m.txt   mean, max, min (°F), year, month, one per line - the latest month, for the dashboard
#
# It catches up on its own: every month after a ranch's last row, up to the last complete month,
# is filled in. A month HCDP hasn't published yet is skipped and picked up on the next run.
# It also repairs rows an earlier version wrote into a separate "Temp" column.
#
# Usage (from the H-RIP folder or the Python folder):
#   python Python/temp_monthly.py                    # normal monthly run
#   python Python/temp_monthly.py --since 2026-03    # redo rows from Mar 2026 on
#   python Python/temp_monthly.py --ranch RID118     # only these ranches (repeatable)

import rasterio  # import before geopandas: avoids a GDAL/brotli load-order clash on some installs
from rasterstats import zonal_stats
import geopandas as gpd
import numpy as np
import pandas as pd

import argparse
import calendar
import os
from datetime import date

import requests

os.chdir(os.path.dirname(os.path.abspath(__file__)))

MONTHLY_URL = ('https://ikeauth.its.hawaii.edu/files/v2/download/public/system/ikewai-annotated-data/'
               'HCDP/production/temperature/{kind}/month/statewide/data_map/{y}/'
               'temperature_{kind}_month_statewide_data_map_{y}_{m:02d}.tif')
MAPS = './temp_monthly_maps/{kind}'


def month_iter(start, end):
    y, m = start
    while (y, m) <= end:
        yield y, m
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)


def next_month(y, m):
    return (y + 1, 1) if m == 12 else (y, m + 1)


def get_map(y, m, kind='mean', force=False):
    """Download the month's mean/min/max temperature map (°C). Returns the path, or None if not published yet."""
    folder = MAPS.format(kind=kind)
    os.makedirs(folder, exist_ok=True)
    out = f'{folder}/t_month_{kind}_{y}_{m:02d}.tif'
    if os.path.exists(out) and os.path.getsize(out) > 10000 and not force:
        return out
    r = requests.get(MONTHLY_URL.format(kind=kind, y=y, m=m), timeout=180)
    if r.status_code != 200 or len(r.content) < 10000:
        print(f'  {y}-{m:02d}: monthly {kind} map not published yet, skipping')
        return None
    with open(out + '.part', 'wb') as f:
        f.write(r.content)
    os.replace(out + '.part', out)
    print(f'  {y}-{m:02d}: downloaded {out}')
    return out


def ranch_means_f(path, shapes):
    with rasterio.open(path) as src:
        stats = zonal_stats(shapes.to_crs(src.crs), src.read(1), affine=src.transform, nodata=src.nodata, stats=['mean'])
    return {p: (9 / 5 * s['mean'] + 32 if s['mean'] is not None else np.nan) for p, s in zip(shapes.Polygon, stats)}


def load_tmean(p):
    t = pd.read_csv(f'../RID/{p}/{p}_tmean.csv')
    if 'Temp' in t.columns:  # repair rows written to the wrong column
        t['tmean_f'] = t['tmean_f'].fillna(t['Temp'])
    return t[['Year', 'Month', 'tmean_f', 'datetime']].dropna(subset=['Year', 'Month'])


# Monthly averages, rolled so the current month comes first (same layout RID.php reads by position)
monthInd = -date.today().month + 1


def temp_avg(t):
    tdf = t.groupby(['Month'], as_index=False)['tmean_f'].mean()
    tdf['Month'] = tdf['Month'].astype(np.uint8).apply(lambda x: calendar.month_name[x])
    return pd.DataFrame({'oldMonth': tdf.Month, 'OldTemp': tdf.tmean_f,
                         'Month': np.roll(tdf.Month, monthInd), 'Temp': np.roll(tdf.tmean_f, monthInd)})


def temp_12m(t):
    last = t.tail(12)
    return pd.DataFrame({'Month': last.Month.astype(np.uint8).apply(lambda x: calendar.month_name[x]), 'Temp': last.tmean_f})


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--since', help='YYYY-MM: redo ranch rows from this month on')
    ap.add_argument('--ranch', action='append', help='only update this ranch, e.g. RID118 (repeatable)')
    args = ap.parse_args()

    today = date.today()
    last_complete = (today.year - 1, 12) if today.month == 1 else (today.year, today.month - 1)
    since = tuple(int(v) for v in args.since.split('-')) if args.since else None

    shapes = gpd.read_file('./shapefiles/RID.shp')
    shapes = shapes[shapes.Polygon.apply(lambda p: os.path.exists(f'../RID/{p}/{p}_tmean.csv'))]
    if args.ranch:
        shapes = shapes[shapes.Polygon.isin(args.ranch)]
    if shapes.empty:
        raise SystemExit('No ranches with a temperature file to update.')

    tables = {p: load_tmean(p) for p in shapes.Polygon}
    last_rows = {}
    for p, t in tables.items():
        good = t.dropna(subset=['tmean_f'])
        last_rows[p] = (int(good.Year.iloc[-1]), int(good.Month.iloc[-1]))
    start = min(next_month(*v) for v in last_rows.values())
    if since:
        start = min(start, since)

    months = list(month_iter(start, last_complete))
    if months:
        print(f'Temperature months to process: {months[0][0]}-{months[0][1]:02d} to {months[-1][0]}-{months[-1][1]:02d}')
    for y, m in months:
        path = get_map(y, m)
        if path is None:
            break
        means = ranch_means_f(path, shapes)
        for p, t in tables.items():
            if (y, m) > last_rows[p] or (since and (y, m) >= since):
                t = t[~((t.Year == y) & (t.Month == m))]
                row = pd.DataFrame({'Year': [float(y)], 'Month': [float(m)], 'tmean_f': [means[p]], 'datetime': [f'{y}-{m:02d}-01']})
                tables[p] = pd.concat([t, row], ignore_index=True)

    # Always rewrite: also repairs the column layout and rebuilds the averages from the full record
    for p, t in tables.items():
        t = t.dropna(subset=['tmean_f']).sort_values(['Year', 'Month']).drop_duplicates(['Year', 'Month'], keep='last').reset_index(drop=True)
        t['datetime'] = pd.to_datetime(dict(year=t.Year.astype(int), month=t.Month.astype(int), day=1)).dt.strftime('%Y-%m-%d')
        t.to_csv(f'../RID/{p}/{p}_tmean.csv', index=False)
        temp_avg(t).to_csv(f'../RID/{p}/{p}_t_month.csv')
        temp_12m(t).to_csv(f'../RID/{p}/{p}_t_12m.csv')

    # Dashboard tile: mean, max and min for the newest month every ranch has
    y, m = min((int(t.Year.iloc[-1]), int(t.Month.iloc[-1])) for t in tables.values())
    paths = {k: get_map(y, m, k) for k in ('mean', 'max', 'min')}
    if all(paths.values()):
        vals = {k: ranch_means_f(path, shapes) for k, path in paths.items()}
        for p in tables:
            with open(f'../RID/{p}/{p}_temp_m.txt', 'w') as f:
                f.write(f"{vals['mean'][p]}\n{vals['max'][p]}\n{vals['min'][p]}\n{y}\n{m}")
        print(f'Wrote dashboard min/max ({y}-{m:02d}) for {len(tables)} ranches.')
    else:
        print(f'Min/max maps for {y}-{m:02d} not published yet; dashboard tile left as is.')

    ends = pd.Series({p: f'{int(t.Year.iloc[-1])}-{int(t.Month.iloc[-1]):02d}' for p, t in tables.items()})
    print(f'Updated {len(tables)} ranches; latest month: ' + ', '.join(f'{k} ({v})' for k, v in ends.value_counts().items()))


if __name__ == '__main__':
    main()
