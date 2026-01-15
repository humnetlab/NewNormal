# this script is adapted from
# https://github.com/humnetlab/Urban_Dynamics

import os
import pickle
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from tqdm import tqdm
import itertools
from ks_utils import cities, seasons
import ks_utils

gapDistance = 3

def KSTest(gyrations1, gyrations2):
    return stats.ks_2samp(gyrations1, gyrations2).statistic

def removeLargeRgs_100(ringGyrations):
    allGyrations = list(itertools.chain(*ringGyrations))
    allGyrations = sorted(allGyrations)
    RgThres = np.percentile(allGyrations, 95)
    
    ringGyrations_new = []
    for group in ringGyrations:
        group = [rg for rg in group if rg < RgThres]
        group = [rg for rg in group if rg < 100]
        ringGyrations_new.append(group)
    return ringGyrations_new

def KS_slope(city, ringGyrations):
    gapDistance = 3
    
    if len(ringGyrations) > 50:
        ringGyrations = ringGyrations[:51]

    dmax = len(ringGyrations)
    dmax = dmax // 3 * 3 + int(np.ceil((dmax % 3) / 3.0)) * 3
    X = []
    Y = []

    ringGyrations_d = ringGyrations[:gapDistance]
    allGyrations_0 = [g for g in itertools.chain(*ringGyrations_d) if g > 0]

    for d in range(len(ringGyrations)):
        if d % gapDistance != 0:
            continue
        x = d / dmax 
        ringGyrations_d = ringGyrations[d:d + gapDistance]
        allGyrations_d = [g for g in itertools.chain(*ringGyrations_d) if g > 0]

        try:
            ks = np.abs(KSTest(allGyrations_d, allGyrations_0))
        except ValueError:
            continue

        X.append(x)
        Y.append(ks)

    if len(X) > 1: 
        a_s, b_s, r, tt, stderr = stats.linregress(X, Y)
        log_message = f'KS Slope: a={a_s:.4f}, intercept={b_s:.4f}, std_err={stderr:.4f}'
        print(log_message)
        return X, Y, a_s, stderr
    else:
        log_message = f'Insufficient data for regression. Defaulting KS Slope to 0.'
        print(log_message)
        return [], [], 0, 0

for season in tqdm(seasons, desc='Init...'):
    cityA2values = {}
    cityKSindex = {}

    for city in tqdm(cities, desc=f'Now: {season.upper()}'):
        ringGyrations, _, _ = pickle.load(
            open(os.path.join(ks_utils.ring_rg, f'Rgs_{city}_{season}.pkl'), 'rb'))

        ringGyrations = removeLargeRgs_100(ringGyrations)

        X, Y, a_s, stderr = KS_slope(city, ringGyrations)

        cityA2values[city] = a_s
        cityKSindex[city] = [X, Y]

        log_message = f'{city}, {season}: KS slope = {a_s:.6f}, stderr = {stderr:.6f}'
        print(log_message)

    pickle.dump(cityA2values, open(os.path.join(ks_utils.ks_a2, f'cityA2values_{season}.pkl'), 'wb'), pickle.HIGHEST_PROTOCOL)
    pickle.dump(cityKSindex, open(os.path.join(ks_utils.ks_index, f'cityKSindex_{season}.pkl'), 'wb'), pickle.HIGHEST_PROTOCOL)
    
    log_message = f'done {season}'
    print(log_message)
