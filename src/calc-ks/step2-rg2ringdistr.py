# this script is adapted from
# https://github.com/humnetlab/Urban_Dynamics

import pickle
import numpy as np
import matplotlib.pyplot as plt
import os
import csv
from tqdm import tqdm
import itertools
from ks_utils import haversine, cities, seasons
import ks_utils

def homeDistanceToCBD(individualInfo, city, cityRadius, cityCBDs):
    '''calc home loc distance to CBD loc for each individual'''
    homeToCBD = {}
    homeLoc = {}

    cbd_lon, cbd_lat = cityCBDs[city]

    for person_id, data in individualInfo.items():
        home_lat = data['home']['lat']
        home_long = data['home']['long']

        dist = haversine(cbd_lat, cbd_lon, home_lat, home_long)

        if dist > cityRadius:
            continue

        homeToCBD[person_id] = dist
        homeLoc[person_id] = (home_long, home_lat)

    return homeLoc, homeToCBD


def RgDistribution(individualInfo, city, cityInfo, cityCBDs, log_file=None):
    '''calc Rg distributions based on distance from CBD in rings'''
    # load city radius
    cityRadius, _, _, _, _, _ = cityInfo[city]
    
    # calculate home loc and dist to CBD
    homeLoc, homeToCBD = homeDistanceToCBD(individualInfo, city, cityRadius, cityCBDs)

    ringGyrations = [[] for _ in range(int(cityRadius))]  # exact radius gyrations
    gyrationsInGroups = [[] for _ in range(7)]            # 3-km rings
    userDistribution = [0] * 7                            # user counts per 3-km ring

    # individual gyrations
    for person_id, data in tqdm(individualInfo.items(), total=len(individualInfo), desc=f'Processing {city}'):
        if person_id not in homeLoc:
            continue

        mean_gyration = data['rg']  # in km
        distanceToCBD = homeToCBD[person_id]

        # assign to rings (ringGyrations)
        radius = int(np.floor(distanceToCBD))
        if radius < cityRadius:
            ringGyrations[radius].append(mean_gyration)

        # assign to 3-km rings (gyrationsInGroups)
        groupIdx = int(np.floor(distanceToCBD / 3.0))
        if groupIdx < 7:
            gyrationsInGroups[groupIdx].append(mean_gyration)
            userDistribution[groupIdx] += 1

    allGyrations = list(itertools.chain(*ringGyrations))
    numUsers = len(allGyrations)

    return ringGyrations, gyrationsInGroups, userDistribution


def main():
    cityInfo = pickle.load(open(ks_utils.city_info, 'rb'))
    cityCBDs = pickle.load(open(ks_utils.city_cbds, 'rb'))

    for city in cities:
        for season in seasons:
            input_file = os.path.join(ks_utils.indiv_rg, f'IndivTrips_{city}_{season}.pkl')
            output_file = os.path.join(ks_utils.ring_rg, f'Rgs_{city}_{season}.pkl')
            
            print(f'\n{city}_{season}-------')
            individualInfo = pickle.load(open(input_file, 'rb'))
                
            # calc Rg distributions
            ringGyrations, gyrationsInGroups, userDistribution = RgDistribution(
                individualInfo, city, cityInfo, cityCBDs)
            
            with open(output_file, 'wb') as f:
                pickle.dump([ringGyrations, gyrationsInGroups, userDistribution], f, pickle.HIGHEST_PROTOCOL)
                
            print(f'done {city}_{season}\n')

if __name__ == '__main__':
    main()
