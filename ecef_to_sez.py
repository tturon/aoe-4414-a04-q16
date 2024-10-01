# ecef_to_sez.py
#
# Usage: python3 ecef_to_sez.py o_x_km o_y_km o_z_km x_km y_km z_km.
# Converting ECEF to SEZ

# Parameters:
# o_x_km - x coordinate in the origin frame
# o_y_km - y coordinate in the origin frame
# o_z_km - z coordinate in the origin frame
# x_km - x position in ECEF
# y_km - y position in ECEF
# z_km - z position in ECEF

# Output:
#  Prints SEZ coords from ECEF coords in km
#
# Written by Thomas Turon
# Other contributors: None
#
# Optional license statement, e.g., See the LICENSE file for the license.

# import Python modules

import sys
import math

R_E_km = 6378.1363
e_E = 0.081819221456

o_x_km = ''
o_y_km = ''
o_z_km = ''
x_km = ''
y_km = ''
z_km = ''

def calc_denom(ecc,latitude_radians):
    return math.sqrt(1.0 - ecc**2 * math.sin(latitude_radians)**2)

if len(sys.argv) == 7:
    o_x_km = float(sys.argv[1])
    o_y_km = float(sys.argv[2])
    o_z_km = float(sys.argv[3])
    x_km = float(sys.argv[4])
    y_km = float(sys.argv[5])
    z_km = float(sys.argv[6])

else:
    print(\
        'Usage: python3 ecef_to_sez.py o_x_km o_y_km o_z_km x_km y_km z_km'

        )
    exit()

# write script below this line
ecefx_km = x_km - o_x_km
ecefy_km = y_km - o_y_km
ecefz_km = z_km - o_z_km

#finding longitude
long_rad = math.atan2(o_y_km,o_x_km)
long_deg = long_rad * 180/math.pi

#finding latitude
lat_rad = math.asin(o_z_km/math.sqrt(o_x_km**2 + o_y_km**2 + o_z_km**2))
rlon_km = math.sqrt(o_x_km**2 + o_y_km**2)
prev_lat_rad = float('nan')

c_E = float('nan')
count = 0
while (math.isnan(prev_lat_rad) or abs(lat_rad-prev_lat_rad)>10e-7) and count<5:
    denom = calc_denom(e_E,lat_rad)
    c_E = R_E_km/denom
    prev_lat_rad = lat_rad
    lat_rad = math.atan((o_z_km+c_E*(e_E**2)*math.sin(lat_rad))/rlon_km)
    count = count+1

#calculate hae
hae_km = rlon_km/math.cos(lat_rad) - c_E

#1st rotation
ry_x = ecefx_km * math.cos(long_rad) + ecefy_km * math.sin(long_rad)
ry_y = ecefx_km * -math.sin(long_rad) + ecefy_km * math.cos(long_rad)
ry_z = ecefz_km

#complete matrix
s_km = ry_x * math.sin(lat_rad) - ry_z * math.cos(lat_rad)
e_km = ry_y
z_km = ry_x * math.cos(lat_rad) + ry_z * math.sin(lat_rad)

#output
print(s_km)
print(e_km)
print(z_km)


