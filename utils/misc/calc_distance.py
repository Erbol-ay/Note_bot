from math import radians, cos, sin, asin, sqrt, ceil

R = 6378.1

def calc_distance(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    # c = 2 * math.atan2(sqrt(a), sqrt(1 - a))
    # Radius of earth in kilometers is 6371
    km = R * c
    return ceil(km * 1000)