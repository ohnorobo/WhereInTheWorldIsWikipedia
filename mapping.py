#!/usr/local/bin/python

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from pprint import pprint
import csv
#import shapefile




def read_in_shapefile():

  '''
  b = Basemap(projection="lcc", 
              llcrnrlon=west,
              llcrnrlat=south,
              urcrnrlon=east,
              urcrnrlat=north,
              lat_0=(south+north)/2,
              lon_0=(east+west)/2)
  '''
  b = Basemap(projection="robin", lon_0=0, lat_0=0)

  print("reading in file")
  countries = b.readshapefile("./data/50/ne_50m_admin_0_countries", "countries") #secondary
  #r = shapefile.Reader("~/data/gadm_v2_shp/gadm2")
  print("read in file")
  return countries



def read_in_data():
  pv_data = csv.reader(open("./data/language_pageviews_per_country.tsv"), delimiter='\t', quotechar="\"")

  data = {}

  for row in pv_data:
    lang, project, country, percent = row

    if not (lang, project) in data:
      data[(lang, project)] = []
    data[(lang, project)].append((country, percent))

  return data



import matplotlib.colors as colors
import matplotlib.cm as cmx
cm = plt.get_cmap('gist_rainbow') 
cNorm  = colors.Normalize(vmin=0, vmax=100) #percentages
scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cm)


def graph_a_thing(countries, values, language, project):
    ax = plt.subplot(111)
    # shapes is the shapefile
    # values is a dict mapping of the GEOIDs in shapes to the heatmap values
    shapes = countries[4]

    for line in shapes:
        # x and y are empty lists to be populated with the coords of each geometry.
        x = []
        y = []

        #geoid = int(info['GEOID'])
        #value = values[geoid]

        for j in range(0,len(border)):

            # get x and y coordinates.
            tempx = float(border[j][0]) #x
            tempy = float(border[j][1]) #y
            x.append(tempx)
            y.append(tempy) # Populate the lists  

        # Creates a polygon in matplotlib for each geometry in the shapefile
        if value == 0:
            color = (0.0, 0.0, 0.0, 0.0)
        else:
            color = scalarMap.to_rgba(value)
        plt.fill(x,y, fc=color)

    plt.axis('equal')
    # This sets the x and y axes as equal intervals.
    # NB this script will only work for projected data, for geographical
    # coordinate systems get ready to do some maths  

    #plt.show() # Draws the map!
    plt.axis('off')

    b1 = ax.bar([0, 1, 2], [0.2, 0.3, 0.1], color=scalarMap.to_rgba(600), width=0.4, align="edge")
    b2 = ax.bar([0, 1, 2], [0.2, 0.3, 0.1], color=scalarMap.to_rgba(550), width=0.4, align="edge")
    b3 = ax.bar([0, 1, 2], [0.2, 0.3, 0.1], color=scalarMap.to_rgba(500), width=0.4, align="edge")
    b4 = ax.bar([0, 1, 2], [0.2, 0.3, 0.1], color=scalarMap.to_rgba(450), width=0.4, align="edge")

    ax.legend([b1, b2, b3, b4], ["600", "550", "500", "450"])
    ax.set_title("Title")

    plt.savefig("state.png", figsize=(600,500), dpi=500)




data = read_in_data()
countries = read_in_shapefile()

print(countries)

plt.savefig("world.png", figsize=(400,200), dpi=1000)


for language, project in data.keys():
  graph_a_thing(countries, data[(language, project)], language, project)


