import math

# Code converted from JS: http://latlong.mellifica.se/

axis = 6378137.0
flattening = 1.0 / 298.257222101

central_meridian = 15.00
lat_of_origin = 0.0
scale = 0.9996
false_northing = 0.0
false_easting = 500000.0


def grid_to_geodetic(x, y):
    e2 = flattening * (2.0 - flattening)
    n = flattening / (2.0 - flattening)
    a_roof = axis / (1.0 + n) * (1.0 + n * n / 4.0 + n * n * n * n / 64.0)
    delta1 = n / 2.0 - 2.0 * n * n / 3.0 + 37.0 * n * n * n / 96.0 - n * n * n * n / 360.0
    delta2 = n * n / 48.0 + n * n * n / 15.0 - 437.0 * n * n * n * n / 1440.0
    delta3 = 17.0 * n * n * n / 480.0 - 37 * n * n * n * n / 840.0
    delta4 = 4397.0 * n * n * n * n / 161280.0

    Astar = e2 + e2 * e2 + e2 * e2 * e2 + e2 * e2 * e2 * e2
    Bstar = -(7.0 * e2 * e2 + 17.0 * e2 * e2 * e2 + 30.0 * e2 * e2 * e2 * e2) / 6.0
    Cstar = (224.0 * e2 * e2 * e2 + 889.0 * e2 * e2 * e2 * e2) / 120.0
    Dstar = -(4279.0 * e2 * e2 * e2 * e2) / 1260.0

    deg_to_rad = math.pi / 180
    lambda_zero = central_meridian * deg_to_rad
    xi = (x - false_northing) / (scale * a_roof)
    eta = (y - false_easting) / (scale * a_roof)
    xi_prim = xi - delta1 * math.sin(2.0 * xi) * math.cosh(2.0 * eta) - \
        delta2 * math.sin(4.0 * xi) * math.cosh(4.0 * eta) - \
        delta3 * math.sin(6.0 * xi) * math.cosh(6.0 * eta) - \
        delta4 * math.sin(8.0 * xi) * math.cosh(8.0 * eta)
    eta_prim = eta - \
        delta1 * math.cos(2.0 * xi) * math.sinh(2.0 * eta) - \
        delta2 * math.cos(4.0 * xi) * math.sinh(4.0 * eta) - \
        delta3 * math.cos(6.0 * xi) * math.sinh(6.0 * eta) - \
        delta4 * math.cos(8.0 * xi) * math.sinh(8.0 * eta)
    phi_star = math.asin(math.sin(xi_prim) / math.cosh(eta_prim))
    delta_lambda = math.atan(math.sinh(eta_prim) / math.cos(xi_prim))
    lon_radian = lambda_zero + delta_lambda
    lat_radian = phi_star + math.sin(phi_star) * math.cos(phi_star) * \
        (Astar +
         Bstar * math.pow(math.sin(phi_star), 2) +
         Cstar * math.pow(math.sin(phi_star), 4) +
         Dstar * math.pow(math.sin(phi_star), 6))

    return lat_radian * 180.0 / math.pi, lon_radian * 180.0 / math.pi


def distance_in_km((lat1, lon1), (lat2, lon2)):
    R = 6371  # Radius of the earth in km
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat / 2) * math.sin(dLat / 2) + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(dLon / 2) * math.sin(dLon / 2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c  # Distance in km
    return d

