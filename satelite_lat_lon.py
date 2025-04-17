#!  /usr/bin/env python
#!  /usr/bin/python
#!  /usr/local/bin/python
#!  /python
import subprocess,os
import requests,matplotlib.pyplot as plt;import cartopy.crs as ccrs;import cartopy.feature as cfeature;from matplotlib.dates import datetime;from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

def start():
    a = ['requests','matplotlib','cartopy','datetime','numpy']
    b = []
    d = os.system('pip list > inpack.txt')
    
    for i in open('./inpack.txt','r'):
        i.splitlines()
        # for j in a:
        #     print(j[0])
            # if i != j:
            #     for m in range(0,len(a)):
            #         if m <4:
            #             subprocess.Popen(['pip','install',a[m]])
            #         else:
            #             break
start()

# def sol_coord(sun_noise):



# def interferention(lat_sat,lon_sat,lat_earth,lon_earth):
#     atten = 0.036 / 
