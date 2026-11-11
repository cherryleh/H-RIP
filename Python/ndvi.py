#!/usr/bin/env python
# coding: utf-8
#
# Monthly NDVI update for every ranch.
#
# HCDP publishes a gap-filled MODIS NDVI map for every day (about 2 days behind),
# but no monthly map. For each month this script downloads all of that month's
# daily maps, averages them into NDVI_maps/NDVI_YYYY_MM.tif (the file New Coords
# and maps.py already read), then adds the ranch averages to each RIDxxx_ndvi.csv
# and rebuilds RIDxxx_ndvi_month.csv and RIDxxx_ndvi_12m.csv.
#
# It catches up on its own: every month after a ranch's last row, up to the last
# complete month, is filled in. A month whose daily maps aren't all published yet
# is skipped and picked up on the next run.
#
# Usage (from the H-RIP folder or the Python folder):
#   python Python/ndvi.py                     # normal monthly run
#   python Python/ndvi.py --since 2025-08     # rebuild maps and rows from Aug 2025 on
#   python Python/ndvi.py --ranch RID118      # only these ranches (repeatable)

import rasterio  # import before geopandas: avoids a GDAL/brotli load-order clash on some installs
from rasterstats import zonal_stats
import geopandas as gpd
import numpy as np
import pandas as pd

import argparse
import calendar
import os
import tempfile
from datetime import date

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

os.chdir(os.path.dirname(os.path.abspath(__file__)))

DAILY_URL = ('https://ikeauth.its.hawaii.edu/files/v2/download/public/system/ikewai-annotated-data/'
             'HCDP/production/ndvi_modis/day/statewide/data_map/{y}/{m:02d}/'
             'ndvi_modis_day_statewide_data_map_{y}_{m:02d}_{d:02d}.tif')
MAPS = './NDVI_maps'
NODATA = -9999.0
# Maps from Aug 2025 on were saved from a single day by the old script; rebuild them as true monthly means.
SINGLE_DAY_FROM = (2025, 8)


def month_iter(start, end):
    y, m = start
    while (y, m) <= end:
        yield y, m
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)


def next_month(y, m):
    return (y + 1, 1) if m == 12 else (y, m + 1)


def session():
    s = requests.Session()
    s.mount('https://', HTTPAdapter(max_retries=Retry(total=4, backoff_factor=2, status_forcelist=[500, 502, 503, 504])))
    return s


def is_monthly_mean(path):
    with rasterio.open(path) as src:
        return 'NDVI_DAYS' in src.tags()


def build_month(y, m, http, force=False):
    """Average every daily map of the month. Returns the map path, or None if days are still missing."""
    out = f'{MAPS}/NDVI_{y}_{m:02d}.tif'
    if os.path.exists(out) and not force and ((y, m) < SINGLE_DAY_FROM or is_monthly_mean(out)):
        return out

    ndays = calendar.monthrange(y, m)[1]
    total = count = profile = None
    missing = []
    for d in range(1, ndays + 1):
        r = http.get(DAILY_URL.format(y=y, m=m, d=d), timeout=120)
        if r.status_code != 200:
            missing.append(d)
            continue
        with tempfile.NamedTemporaryFile(suffix='.tif') as tmp:
            tmp.write(r.content)
            tmp.flush()
            with rasterio.open(tmp.name) as src:
                a = src.read(1).astype('float64')
                valid = np.isfinite(a) & (a != src.nodata) & (a >= -1) & (a <= 1)
                if total is None:
                    total, count, profile = np.zeros_like(a), np.zeros(a.shape, 'uint16'), src.profile.copy()
                total[valid] += a[valid]
                count[valid] += 1
    if missing:
        print(f'  {y}-{m:02d}: {len(missing)} of {ndays} daily maps not published yet (first missing: day {missing[0]}), skipping')
        return None

    mean = np.full(total.shape, NODATA, 'float32')
    mean[count > 0] = (total[count > 0] / count[count > 0]).astype('float32')
    profile.update(dtype='float32', nodata=NODATA, compress='deflate', predictor=3, tiled=True, blockxsize=256, blockysize=256)
    tmp_out = out + '.part'
    with rasterio.open(tmp_out, 'w', **profile) as dst:
        dst.write(mean, 1)
        dst.update_tags(NDVI_DAYS=str(ndays), SOURCE='HCDP ndvi_modis daily, monthly mean')
    os.replace(tmp_out, out)
    print(f'  {y}-{m:02d}: monthly mean of {ndays} daily maps -> {out}')
    return out


def ranch_means(path, shapes):
    with rasterio.open(path) as src:
        stats = zonal_stats(shapes.to_crs(src.crs), src.read(1), affine=src.transform, nodata=src.nodata, stats=['mean'])
    return {p: (s['mean'] if s['mean'] is not None else np.nan) for p, s in zip(shapes.Polygon, stats)}


# Same outputs as before, used by RID.php and the ranch pages
monthInd = -date.today().month + 1


def ndvi_avg(arr):
    arr = arr.drop(['datetime'], axis=1)
    ndvidf = arr.groupby(['Month'], as_index=False).mean()
    ndvidf['Month'] = ndvidf['Month'].astype(np.uint8).apply(lambda x: calendar.month_name[x])
    ndvidf['rolledMonth'] = np.roll(ndvidf.Month, monthInd)
    ndvidf['rolledNDVI'] = np.roll(ndvidf.NDVI, monthInd)
    ndvidf = ndvidf.drop(['Year'], axis=1)
    return ndvidf.rename(columns={"Month": "oldMonth", "rolledMonth": "Month", "NDVI": "oldNDVI", "rolledNDVI": "NDVI"})


def ndvi_12m(arr):
    ndvi12m = arr.copy()
    ndvi12m['Month'] = ndvi12m['Month'].astype(np.uint8).apply(lambda x: calendar.month_name[x])
    return ndvi12m.tail(12)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--since', help='YYYY-MM: rebuild monthly maps and ranch rows from this month on')
    ap.add_argument('--ranch', action='append', help='only update this ranch, e.g. RID118 (repeatable)')
    args = ap.parse_args()

    today = date.today()
    last_complete = (today.year - 1, 12) if today.month == 1 else (today.year, today.month - 1)
    since = tuple(int(v) for v in args.since.split('-')) if args.since else None

    shapes = gpd.read_file('./shapefiles/RID.shp')
    shapes = shapes[shapes.Polygon.apply(lambda p: os.path.exists(f'../RID/{p}/{p}_ndvi.csv'))]
    if args.ranch:
        shapes = shapes[shapes.Polygon.isin(args.ranch)]
    if shapes.empty:
        raise SystemExit('No ranches with an NDVI file to update.')

    tables = {p: pd.read_csv(f'../RID/{p}/{p}_ndvi.csv') for p in shapes.Polygon}
    last_rows = {p: (int(t.Year.iloc[-1]), int(t.Month.iloc[-1])) for p, t in tables.items()}
    start = min(next_month(*v) for v in last_rows.values())
    if since:
        start = min(start, since)
    months = list(month_iter(start, last_complete))
    if not months:
        print(f'NDVI is up to date through {last_complete[0]}-{last_complete[1]:02d}.')
        return

    print(f'NDVI months to process: {months[0][0]}-{months[0][1]:02d} to {months[-1][0]}-{months[-1][1]:02d}')
    http = session()
    done = []
    for y, m in months:
        path = build_month(y, m, http, force=bool(since and (y, m) >= since))
        if path is None:
            break  # later months can't be complete either
        means = ranch_means(path, shapes)
        for p, t in tables.items():
            if (y, m) > last_rows[p] or (since and (y, m) >= since):
                t = t[~((t.Year == y) & (t.Month == m))]
                row = pd.DataFrame({'Year': [float(y)], 'Month': [float(m)], 'NDVI': [means[p]], 'datetime': [f'{y}-{m:02d}-01']})
                tables[p] = pd.concat([t, row], ignore_index=True)
        done.append((y, m))

    if not done:
        print('No new complete month yet; nothing written.')
        return

    for p, t in tables.items():
        t = t.sort_values(['Year', 'Month']).reset_index(drop=True)
        t['datetime'] = pd.to_datetime(dict(year=t.Year.astype(int), month=t.Month.astype(int), day=1)).dt.strftime('%Y-%m-%d')
        t = t[['Year', 'Month', 'NDVI', 'datetime']]
        t.to_csv(f'../RID/{p}/{p}_ndvi.csv', index=False)
        ndvi_avg(t).to_csv(f'../RID/{p}/{p}_ndvi_month.csv', index=False)
        ndvi_12m(t).drop(['Year', 'datetime'], axis=1).to_csv(f'../RID/{p}/{p}_ndvi_12m.csv')

    y, m = done[-1]
    print(f'Updated {len(tables)} ranches through {calendar.month_name[m]} {y}.')


if __name__ == '__main__':
    main()
