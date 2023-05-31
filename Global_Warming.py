!pip install netCDF4

# -------------------------------------------

import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as list_colors
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
import matplotlib.cm as cm

# -------------------------------------------

def wheather_stripes(meanData,cmap,title ):
    plt.figure()
    plt.xlabel('Year')
    plt.ylabel('Temperature (C)')
    plt.title(title)
    plt.imshow(meanData.reshape(1,180), cmap=cmap, aspect='auto')
    plt.xticks(np.arange(0,180,10), np.arange(1840,2020,10))
    plt.yticks([])
    #colorbar
    plt.colorbar()
    plt.show()
    
# -------------------------------------------

def fig_2(meanData,title):
    mean=np.mean(meanData)
    meanData-=mean
    norm=cm.colors.Normalize(vmin=meanData.min(), vmax=meanData.max()) #no tocar
    mappable= cm.ScalarMappable(cmap='seismic',norm=norm) #no tocar
 #   mappable.set_clim(vmin=meanData.min() - (meanData.min()*1.95)/(meanData.max()*16), vmax=meanData.max())
    print(mappable.get_cmap())
    #print(mappable.get_array())
    plt.figure(1)
    plt.title(title)
    plt.xlabel('Year')
    plt.ylabel('Temperature (C)')
    #use seismic colormap
    plt.bar(np.arange(1840,2020,1), meanData, width=1, color=mappable.to_rgba(meanData))
    #igual si se quiere cambiar,cambiar solo meanDataNoArtics 
    plt.show()

ncfile = nc.Dataset('air.2m.mon.mean.nc')
data = ncfile.variables['air'][:]
cmap = list_colors.ListedColormap([
    '#08306b', '#08519c', '#2171b5', '#4292c6',
    '#6baed6', '#9ecae1', '#c6dbef', '#deebf7',
    '#fee0d2', '#fcbba1', '#fc9272', '#fb6a4a',
    '#ef3b2c', '#cb181d', '#a50f15', '#67000d',
    ])

# -------------------------------------------

dataNoArtics=data[:, 20:160, :]
#get the mean for each year in data no artics
meanDataNoArtics=np.mean(dataNoArtics, axis=(1,2))
meanDataNoArtics=meanDataNoArtics-273.15
#meanDataNoArtics is a 1D array with the mean temperature of the 2x2 array
#it has data for 2180 months
#we want to get the mean of each year
#we can do this by reshaping the array to 182x12
#and then taking the mean of each row
meanDataNoArtics=meanDataNoArtics.reshape(180,12)
meanDataNoArtics=np.mean(meanDataNoArtics, axis=1)

wheather_stripes(meanDataNoArtics,cmap,'Mean temperature in the world excluding the arctic')
fig_2(meanDataNoArtics,'Mean temperature in the world excluding the arctic')

mexico = data[:, 90+16:33+90, 180+88:180+117]
mexico = np.mean(mexico, axis=(1,2))  -273.15
mexico_anual = np.mean(np.reshape(mexico,(int(np.size(mexico)/12),12)),axis=1)  
dif_mexico = meanDataNoArtics-mexico_anual

wheather_stripes(dif_mexico,cmap,'Mean temperature in Mexico excluding the arctic')
fig_2(dif_mexico,'Mean temperature in Mexico excluding the artic')

oaxaca=data[:, 90+16:18+90, 180+94:180+98] 
#for each element in oaxaca, get the mean of the 2x2 array
oaxaca=np.mean(oaxaca, axis=(1,2)) #temperatura de lats y lons
oaxaca=oaxaca-273.15#Convierte K a C
oaxaca=oaxaca.reshape(180,12) #reshape a años
oaxaca=np.mean(oaxaca, axis=1) #promedio por años
difoaxaca=meanDataNoArtics-oaxaca 
#diferencia con la temperatura por año
#difoaxaca=oaxaca-13.7 
#la linea de arriba se puede cambiar para usar la temperaatura promedio de 1970 a 2000 como comparación

wheather_stripes(difoaxaca,cmap,'Temperature difference between oaxaca and global mean')
fig_2(difoaxaca,'Temperature difference between oaxaca and global mean')

cdmx = np.mean(data[:,110:111,280:281], axis=(1,2)) -273.15
cdmx_anual = np.mean(np.reshape(cdmx,(int(np.size(cdmx)/12),12)),axis=1)   #18 cantidad de cuadrantes
dif_cdmx = meanDataNoArtics-cdmx_anual

wheather_stripes(dif_cdmx,cmap,'Temperature difference between CDMX and global mean')
fig_2(dif_cdmx,'Temperature difference between CDMX and global mean')
