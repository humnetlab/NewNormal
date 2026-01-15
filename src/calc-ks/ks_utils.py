from math import radians, sin, cos, sqrt, atan2


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

seasons = ['fa19']

# paths
trips = 'trips'
indiv_rg = 'deltaks/a_indiv-rg'
ring_rg = 'deltaks/b_ring-rg'
ks_a2 = 'deltaks/c_ks/a2'
ks_index = 'deltaks/c_ks/ks-index'
city_info = 'city_info_2019.pkl'
city_cbds = 'city_cbds.pkl'


def haversine(lat1, lon1, lat2, lon2):
    '''calc great circle distance between two points on earth.'''
    R = 6371.0  # earth radius in kilometers
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c
