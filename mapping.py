#!/usr/local/bin/python

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from pprint import pprint
import csv
#import shapefile




def read_in_shapefile():

  b = Basemap(projection="robin", lon_0=0, lat_0=0)

  print("reading in file")
  countries = b.readshapefile("./data/50/ne_50m_admin_0_countries", "countries") #secondary
  #r = shapefile.Reader("~/data/gadm_v2_shp/gadm2")
  print("read in file")
  #b.drawcountries(color="#FFFFFF", linewidth=5)
  #b.drawmapboundary(fill_color='#FFFFFF') #turn all boundaries white
  return b



def read_in_data():
  pv_data = csv.reader(open("./data/language_pageviews_per_country.tsv"), delimiter='\t', quotechar="\"")

  data = {}

  for row in pv_data:
    lang, project, country, percent = row

    if not (lang, project) in data:
      data[(lang, project)] = {}
    data[(lang, project)][country] = percent

  return data



import matplotlib.colors as colors
import matplotlib.cm as cmx
cm = plt.get_cmap('brg') 
cNorm  = colors.Normalize(vmin=0, vmax=100) #percentages
scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cm)


def graph_a_thing(values, language, project):
    m = read_in_shapefile()

    ax = plt.subplot(111)
    # shapes is the shapefile
    # values is a dict mapping of the GEOIDs in shapes to the heatmap values
    shapes = m.countries
    info = m.countries_info
    used_names = []

    #print(shapes)
    #print(info[0])


    for i in range(0, len(shapes)):
        # x and y are empty lists to be populated with the coords of each geometry.
        x = []
        y = []


        border = shapes[i]
        name = info[i]['brk_name']

        if name in values: # and name not in used_names:
          used_names.append(name)
          value = int(values[name])
          #print((name, value))
          #print(info[i])

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
          plt.fill(x,y, facecolor=color, edgecolor='none')

    plt.axis('equal')
    # This sets the x and y axes as equal intervals.
    # NB this script will only work for projected data, for geographical
    # coordinate systems get ready to do some maths  

    #plt.show() # Draws the map!
    plt.axis('off')

    b1 = ax.bar([0, 1, 2], [0.2, 0.3, 0.1], color=scalarMap.to_rgba(90), width=0.4, align="edge")
    b2 = ax.bar([0, 1, 2], [0.2, 0.3, 0.1], color=scalarMap.to_rgba(70), width=0.4, align="edge")
    b3 = ax.bar([0, 1, 2], [0.2, 0.3, 0.1], color=scalarMap.to_rgba(50), width=0.4, align="edge")
    b4 = ax.bar([0, 1, 2], [0.2, 0.3, 0.1], color=scalarMap.to_rgba(30), width=0.4, align="edge")
    b5 = ax.bar([0, 1, 2], [0.2, 0.3, 0.1], color=scalarMap.to_rgba(10), width=0.4, align="edge")

    ax.legend([b1, b2, b3, b4, b5], ["90%", "70%", "50%", "30%", "10%"], loc=3)

    title = language.decode('utf8') + " " + project.decode("utf8")
    print(title)
    print(set(used_names))
    ax.set_title(title)

    plt.savefig("./images/"+language+"-"+project+".png", figsize=(600,500), dpi=500)




data = read_in_data()

for language, project in data.keys():
  #print((language, keys))
  graph_a_thing(data[(language, project)], language, project)


