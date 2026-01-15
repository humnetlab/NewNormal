# this script is adapted from
# https://github.com/humnetlab/Urban_Dynamics

import os
import pandas as pd
import numpy as np
from osgeo import gdal, ogr, gdalnumeric
from PIL import Image, ImageDraw
import pickle

input_dir = 'data/fig3/'
output_dir = 'gini-output'
os.makedirs(output_dir, exist_ok=True)

with open(os.path.join(input_dir, 'city_cbds.pkl'), 'rb') as f:
    cityCBDs = pickle.load(f)

year = 2019

cities = [
    'Atlanta--Athens-ClarkeCounty--SandySprings_GA-AL',
    'Boston-Worcester-Providence_MA-RI-NH',
    'Chicago-Naperville_IL-IN-WI',
    'Cleveland-Akron-Canton_OH',
    'Dallas-FortWorth_TX-OK',
    'Detroit-Warren-AnnArbor_MI',
    'Houston-Pasadena_TX',
    'LosAngeles-LongBeach_CA',
    'NewYork-Newark_NY-NJ-CT-PA',
    'Orlando-Lakeland-Deltona_FL',
    'Philadelphia-Reading-Camden_PA-NJ-DE-MD',
    'Phoenix-Mesa_AZ',
    'Sacramento-Roseville_CA',
    'SanJose-SanFrancisco-Oakland_CA',
    'StLouis-StCharles-Farmington_MO-IL'
]

def haversine(lat1, lon1, lat2, lon2):
    '''calc haversine distance between two points'''
    R = 6372.8
    dLat = np.radians(lat2 - lat1)
    dLon = np.radians(lon2 - lon1)
    a = np.sin(dLat/2)**2 + np.cos(np.radians(lat1))*np.cos(np.radians(lat2))*np.sin(dLon/2)**2
    c = 2*np.arcsin(np.sqrt(a))
    return R * c

def gini(arr):
    '''calc gini coefficient for a given array'''
    sorted_arr = arr.copy()
    sorted_arr.sort()
    n = arr.size
    coef_ = 2. / n
    const_ = (n + 1.) / n
    weighted_sum = sum([(i+1)*yi for i, yi in enumerate(sorted_arr)])
    return coef_*weighted_sum/(sorted_arr.sum()) - const_

def crowding(population):
    '''calc mean and crowding index'''
    delta = np.var(population)
    mean = np.mean(population)
    crowding = mean + delta/mean - 1
    return mean, crowding

def clip_raster(rast, features_path, gt=None, nodata=0):
    '''
    Clips a raster to a polygon layer provided by a shp.
    Returns an array and mask.
    '''
    def image_to_array(i):
        a = np.frombuffer(i.tobytes(), dtype='b')
        a.shape = i.im.size[1], i.im.size[0]
        return a

    def world_to_pixel(geo_matrix, x, y):
        ulX = geo_matrix[0]
        ulY = geo_matrix[3]
        xDist = geo_matrix[1]
        pixel = int((x - ulX) / xDist)
        line = int((ulY - y) / xDist)
        return (pixel, line)

    if not isinstance(rast, np.ndarray):
        gt = rast.GetGeoTransform()
        rast = rast.ReadAsArray()

    features = ogr.Open(features_path)
    if features.GetDriver().GetName() == 'ESRI Shapefile':
        lyr = features.GetLayer(os.path.split(os.path.splitext(features_path)[0])[1])
    else:
        lyr = features.GetLayer()

    poly = lyr.GetNextFeature()
    minX, maxX, minY, maxY = lyr.GetExtent()
    ulX, ulY = world_to_pixel(gt, minX, maxY)
    lrX, lrY = world_to_pixel(gt, maxX, minY)
    pxWidth = int(lrX - ulX)
    pxHeight = int(lrY - ulY)

    iY = ulY
    if gt[3] < maxY:
        iY = ulY
        ulY = 0

    try:
        clip = rast[:, ulY:lrY, ulX:lrX]
    except IndexError:
        clip = rast[ulY:lrY, ulX:lrX]

    gt2 = list(gt)
    gt2[0] = minX
    gt2[3] = maxY

    points = []
    pixels = []
    geom = poly.GetGeometryRef()
    numPolygons = geom.GetGeometryCount()
    print("# of polygons:", numPolygons)

    ptsLen = []
    for n in range(numPolygons):
        pts = geom.GetGeometryRef(n)
        ptsLen.append(pts.GetPointCount())

    p = np.argmax(ptsLen)
    pts = geom.GetGeometryRef(int(p))
    print("pts.GetPointCount():", pts.GetPointCount())

    for p in range(pts.GetPointCount()):
        points.append((pts.GetX(p), pts.GetY(p)))

    for p in points:
        pixels.append(world_to_pixel(gt2, p[0], p[1]))

    raster_poly = Image.new('L', (pxWidth, pxHeight), 1)
    rasterize = ImageDraw.Draw(raster_poly)
    rasterize.polygon(pixels, 0)

    if gt[3] < maxY:
        premask = image_to_array(raster_poly)
        mask = np.ndarray((premask.shape[-2] - abs(iY), premask.shape[-1]), premask.dtype)
        mask[:] = premask[abs(iY):, :]
        mask.resize(premask.shape)
        gt2[3] = maxY - (maxY - gt[3])
    else:
        mask = image_to_array(raster_poly)

    try:
        clip = gdalnumeric.choose(mask, (clip, nodata))
    except ValueError:
        rshp = list(mask.shape)
        if mask.shape[-2] != clip.shape[-2]:
            rshp[0] = clip.shape[-2]
        if mask.shape[-1] != clip.shape[-1]:
            rshp[1] = clip.shape[-1]
        mask.resize(*rshp, refcheck=False)
        clip = gdalnumeric.choose(mask, (clip, nodata))

    return (clip, ulX, ulY, gt2), mask

def clipCity(city):
    '''
    Clips the population raster to the boundary of the given CSA.
    Saves the resulting mask as a pickle file.
    '''
    shpFilePath = os.path.join(input_dir, 'shp', city, city)
    print(f'Processing {shpFilePath}.shp for year {year}')

    populationFile = os.path.join(input_dir, f'landscan-global-{year}.tif')
    ds = gdal.Open(populationFile)
    data = ds.ReadAsArray()
    gt = ds.GetGeoTransform()

    res, mask = clip_raster(data, shpFilePath + '.shp', gt, nodata=0)

    city_output_dir = os.path.join(output_dir, city)
    os.makedirs(city_output_dir, exist_ok=True)

    mask_path = os.path.join(city_output_dir, f"{city}_mask_global{year}.pkl")
    with open(mask_path, 'wb') as f:
        pickle.dump(mask, f, pickle.HIGHEST_PROTOCOL)
    return res, mask

def findCityBoundary(city):

    print(f"------- {city} ({year}) -------")

    data, cityMask = clipCity(city)
    population = data[0]
    population = np.asarray(population, dtype=float)
    population[population<0] = 0
    print('Min population in grids:', np.min(population))
    print('Max population in grids:', np.max(population))

    geotransform = data[3]

    city_output_dir = os.path.join(output_dir, city)

    with open(os.path.join(city_output_dir, f'{city}_population.pkl'), 'wb') as f:
        pickle.dump(population, f)
    with open(os.path.join(city_output_dir, f'{city}_geotransform.pkl'), 'wb') as f:
        pickle.dump(geotransform, f)

    leftBoundary = geotransform[0]
    upBoundary = geotransform[3]
    interspace_H = geotransform[1]
    interspace_V = geotransform[5]
    numRow, numCol = np.shape(population)
    print(f'Grid dimensions: {numRow} x {numCol}')

    totalPopulation = np.nansum(population)
    print(f'Total population: {totalPopulation}')

    distanceToCBD = {}
    count = 0

    for r in range(numRow):
        maxLat = upBoundary + r*interspace_V
        minLat = upBoundary + (r+1)*interspace_V
        cenLat = 0.5*(minLat + maxLat)
        for c in range(numCol):
            if cityMask[r,c] == 1:
                population[r,c] = np.nan
                continue
            minLon = leftBoundary + c*interspace_H
            maxLon = leftBoundary + (c+1)*interspace_H
            cenLon = 0.5*(minLon + maxLon)
            dist = haversine(cityCBDs[city][1], cityCBDs[city][0], cenLat, cenLon)
            distanceToCBD[(r,c)] = dist
            count += 1

    print(f'# grids covered by population: {count} / {numRow*numCol}')

    maxDistance = max(distanceToCBD.values())
    radiusBins = range(int(maxDistance) + 1)
    ringPops = [0 for _ in radiusBins]

    for r in range(numRow):
        for c in range(numCol):
            if cityMask[r,c] == 1:
                continue
            pop = population[r,c]
            dist = distanceToCBD[(r,c)]
            radiusIdx = int(np.floor(dist))
            ringPops[radiusIdx] += pop

    popFractionInRings = np.divide(np.cumsum(ringPops), totalPopulation)

    popThreshold = 0.95
    popFractionInRings_flag = [i for i in radiusBins if popFractionInRings[i] >= popThreshold]
    cityRadius = popFractionInRings_flag[0]
    print(f'Max distance to CBD: {maxDistance}')
    print(f'Radius of {city}: {cityRadius}')

    urbanPopulations = []
    urbanPopulations_over500 = []

    for r in range(numRow):
        for c in range(numCol):
            if cityMask[r,c] == 1:
                continue
            pop = population[r,c]
            dist = distanceToCBD[(r,c)]
            if dist > cityRadius:
                continue
            if pop > 0:
                urbanPopulations.append(pop)
            if pop > 500:
                urbanPopulations_over500.append(pop)

    giniPop = gini(np.asarray(urbanPopulations))
    giniPop_over500 = gini(np.asarray(urbanPopulations_over500))
    meanPop, crowdingPop = crowding(np.asarray(urbanPopulations_over500))
    print(f'Mean and crowding: {meanPop:.2f} / {crowdingPop:.2f}')

    cityRadius_small = cityRadius
    for ri in radiusBins[:-5]:
        frac = popFractionInRings[ri] / popFractionInRings[ri+5]
        if frac >= popThreshold:
            cityRadius_small = ri
            break

    print(f'Small Radius of {city}: {cityRadius_small}')

    return cityRadius, int(totalPopulation), giniPop, giniPop_over500, meanPop, crowdingPop

def proc_cities():

        cityInfo = {}
        cityInfo_df = []

        for city in cities:
            cityRadius, totalPop, giniPop, giniPop_over500, meanPop, crowdingPop = findCityBoundary(city)
            cityInfo[city] = [cityRadius, totalPop, giniPop, giniPop_over500, meanPop, crowdingPop]
            cityInfo_df.append([city, cityRadius, totalPop, giniPop, giniPop_over500, meanPop, crowdingPop])

            log_line = f'{city}: radius={cityRadius}, gini={giniPop:.4f}, gini500={giniPop_over500:.4f}, mean={meanPop:.2f}, crowding={crowdingPop:.2f}'
            print(log_line)

        columns = ['City', 'Radius', 'TotalPopulation', 'Gini', 'Gini500', 'MeanPop', 'CrowdingIndex']
        pd.DataFrame(cityInfo_df, columns=columns).to_csv(
            os.path.join(output_dir, 'city_info_2019.csv'), index=False)
        with open(os.path.join(output_dir, 'city_info_2019.pkl'), 'wb') as f:
            pickle.dump(cityInfo, f, pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    proc_cities()