#!/usr/local/bin/python

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from pprint import pprint
import csv
from math import log
#import shapefile




def read_in_shapefile():

  b = Basemap(projection="robin", lon_0=0, lat_0=0)

  print("reading in file")
  countries = b.readshapefile("./data/50/ne_50m_admin_0_countries", "countries", color="#3B3B3B", linewidth=.2) #secondary
  print("read in file")
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
cm = plt.get_cmap('gnuplot') 
cNorm  = colors.Normalize(vmin=0, vmax=log(100)) #percentages
scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cm)


def graph_a_thing(m, values, language, project):

    m = read_in_shapefile() #this redraws the lines, but it's a silly way to do it

    ax = plt.subplot(111)
    # shapes is the shapefile
    shapes = m.countries
    info = m.countries_info
    used_names = []

    for i in range(0, len(shapes)):
        # x and y are empty lists to be populated with the coords of each geometry.
        x = []
        y = []

        border = shapes[i]
        name = info[i]['brk_name']

        if name in values: 
          used_names.append(name)
          #print((name, values[name]))
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
              color = scalarMap.to_rgba(log(100)-log(value))
          plt.fill(x,y, facecolor=color, edgecolor='none')

    plt.axis('equal')
    # This sets the x and y axes as equal intervals.
    # NB this script will only work for projected data, for geographical
    # coordinate systems get ready to do some maths  

    plt.axis('off')

    percentages = [100, 50, 25, 12, 6, 3, 1]
    labels = [ax.bar([0, 1, 2], [0.2, 0.3, 0.1],
                      color=scalarMap.to_rgba(log(100)-log(percentage)), 
                      width=0.4, align="edge") 
              for percentage in percentages]
    label_titles = [str(percentage)+"%" for percentage in percentages]

    ax.legend(labels, label_titles, loc=3)

    title = language.decode('utf8') + " " + project.decode("utf8")
    print(title)
    print(set(used_names))
    ax.set_title(title)

    plt.savefig("./images/"+language+"-"+project+".png", figsize=(600,500), dpi=500)
    plt.clf()




m = read_in_shapefile()
data = read_in_data()

for language, project in sorted(data.keys()):
  print((language, project))
  graph_a_thing(m, data[(language, project)], language, project)


