# Geographic visualization using Basemap
#conda install -c anaconda basemap
#conda install basemap-data-hires
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap # Matplotlib is already imported
plt.figure(figsize=(10,10))
m = Basemap(
     projection='ortho', 
     lat_0=10, lon_0=0,
     resolution='h', # h: high, l: low (faster)
     llcrnrx=-3000000, # map projection coordinates
     llcrnry=1000000, 
     urcrnrx=3000000, 
     urcrnry=6000000,        
)
m.drawmapboundary(fill_color='aqua')
m.fillcontinents(color='springgreen',lake_color='aqua')
m.drawcoastlines()
m.drawcountries()
x1,y1=m(-1.542831162,53.793163494) # Leeds
x2,y2=m( -0.118092,51.509865) # London
#m.scatter(x1,y1, marker='D',color='m', latlon=True) # Points get blocked using scatter when fillcontinents is used. Plot is preferred.
#m.scatter(x1,y1, marker='D',color='r', latlon=False) # latlon=True: Coordinates are in lat and lon, not map coordinates
m.plot(x1, y1, 'o', markersize=5, color='r', alpha=0.8)
plt.text(x1, y1, 'Leeds',fontsize=12,fontweight='bold',
                    ha='left',va='top',color='yellow',
                    bbox=dict(facecolor='b', alpha=0.2))
plt.title('Leeds, UK',fontsize=20,fontweight='bold')
plt.savefig('/Users/Documents/Leeds1.png')
plt.show()
