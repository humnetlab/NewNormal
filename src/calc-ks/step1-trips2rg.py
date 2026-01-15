# this script is adapted from
# https://github.com/humnetlab/Urban_Dynamics

import os
import csv
import pickle
import math
from tqdm import tqdm
from ks_utils import haversine, cities, seasons
import ks_utils


def calc_rg(trips, home_lat, home_lng):
    '''Rg: √(Σ(d^2)/n), where d is the distance of each trip from home'''
    n = len(trips)
    if n == 0:
        return 0

    sum_squared_dist = 0
    for trip in trips:
        dest_lat = trip['dest_lat']
        dest_lng = trip['dest_lng']
        
        # calc haversine distance from home loc to each destination
        distance = haversine(home_lat, home_lng, dest_lat, dest_lng)
        sum_squared_dist += distance ** 2

    return math.sqrt(sum_squared_dist / n)


def proc_trips(file_path):
    unique_trip_takers = set()  
    valid_trip_takers = set()   
    individual_info = {}        
    skipped_trips = 0           

    with open(file_path, 'r') as file:
        total_rows = sum(1 for _ in file) - 1

    # step 1: load
    with open(file_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        for row in tqdm(csv_reader, desc='Proc trips', total=total_rows):
            person_id = row['trip_taker_person_id']
            activity_id = row['activity_id']
            unique_trip_takers.add(person_id)

            # check for 'Out of Region' or missing data
            try:
                home_lat = float(row['trip_taker_home_bgrp_lat_2020'])
                home_lng = float(row['trip_taker_home_bgrp_lng_2020'])
                origin_lat = float(row['origin_bgrp_lat_2020'])
                origin_lng = float(row['origin_bgrp_lng_2020'])
                dest_lat = float(row['destination_bgrp_lat_2020'])
                dest_lng = float(row['destination_bgrp_lng_2020'])
                work_lat = float(row['trip_taker_work_bgrp_lat_2020'])
                work_lng = float(row['trip_taker_work_bgrp_lng_2020'])
            except ValueError:
                skipped_trips += 1
                continue

            # init individual_trips if first encounter
            if person_id not in individual_info:
                individual_info[person_id] = {
                    'home': {'lat': home_lat, 'long': home_lng},
                    'work': {'lat': work_lat, 'long': work_lng},
                    'rg': None,  # placeholder for Rg value
                    'trips': []
                }

            # append trips for Rg calc
            individual_info[person_id]['trips'].append({
                'activity_id': activity_id,
                'origin_lat': origin_lat,
                'origin_lng': origin_lng,
                'dest_lat': dest_lat,
                'dest_lng': dest_lng,
            })

            valid_trip_takers.add(person_id)

    # step 2: calc individual Rgs
    for person_id, data in tqdm(individual_info.items(), desc='Calc Rgs', total=len(individual_info)):
        home_lat = data['home']['lat']
        home_lng = data['home']['long']
        trips = data['trips']
        individual_info[person_id]["rg"] = calc_rg(trips, home_lat, home_lng)

    # step 3: print stats
    log_message = (
        f'\nskipped trips: {skipped_trips}\n'
        f'% skipped trips: {skipped_trips / total_rows:.2%}\n'
        f'unique trip takers: {len(unique_trip_takers)}\n'
        f'unique trip takers with valid trips: {len(valid_trip_takers)}\n'
    )
    print(log_message)

    return individual_info, skipped_trips, total_rows, len(unique_trip_takers), len(valid_trip_takers)


def main():
    for city in cities:
        for season in seasons:
            input_file = os.path.join(ks_utils.trips, f'{city}_{season}.csv')
            output_file = os.path.join(ks_utils.indiv_rg, f'IndivTrips_{city}_{season}.pkl')
            
            print(f'\n{city}_{season}-------')

            individual_info, skipped_trips, total_rows, unique_trip_takers, valid_trip_takers = proc_trips(input_file)

            with open(output_file, 'wb') as f:
                pickle.dump(individual_info, f, pickle.HIGHEST_PROTOCOL)

            print(f'done {city}_{season}\n')

if __name__ == '__main__':
    main()
