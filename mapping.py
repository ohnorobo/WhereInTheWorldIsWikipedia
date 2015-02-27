#!/usr/local/bin/python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from pprint import pprint








def read_in_shapefile():

  boundaries = (90, 0, 180, -180)
  north, south, east, west = boundaries
  b = Basemap(projection="lcc", 
              llcrnrlon=west,
              llcrnrlat=south,
              urcrnrlon=east,
              urcrnrlat=north,
              lat_0=(south+north)/2,
              lon_0=(east+west)/2)

  countries = b.readshapefile("./data/ne_110m_admin_0_countries", "countries") #secondary
  return countries



def read_in_data():
  pv_data = pd.read_csv("./data/language_pageviews_per_country.tsv", sep='\t')

  data = {}

  #print(pv_data[:5])
  languages = pv_data['language']
  projects = pv_data['project']
  countries = pv_data['country']
  pageviews = pv_data['pageviews_percentage']

  for lang, project, country, percent in zip(languages, projects, countries, pageviews):

    #pprint((lang, project, country, percent))

    if not (lang, project) in data:
      data[(lang, project)] = []
    data[(lang, project)].append((country, percent))

  return data


'''

plt.savefig("state.svg", figsize=(400,200), dpi=1000)
sorted(map(lambda x: [x['NAME'], x['GEOID']], districts_info))[:10]

cols = ['DISTRICT_CODE', 'DIST_NAME', 'SCHOOL_CODE', 'SCHOOL_NAME']
accountability = pd.read_csv("./MassEduDataChallenge/accountability/accountability_school_2007_2011.csv", sep=',', usecols=cols)
accountability[:10]

a_districts = accountability["DIST_NAME"].tolist()
a_dist_codes = accountability["DISTRICT_CODE"].tolist()
both = zip(a_districts, a_dist_codes)
sorted(list(set(both)))[:10]

cols = ['ORG_NCES_ID', 'ORG_CODE', 'ORG_NAME', 'DISTRICT_NAME']
ese_to_census = pd.read_csv("./MassEduDataChallenge/ese_orgs_names_mapped_to_census_org_names.csv", sep=',', usecols=cols)
ese_to_census[:10]


def get_org_code(nces_id):
    #given an nces id return an org code or throw an error
    filtered = ese_to_census[ese_to_census['ORG_NCES_ID'] == nces_id]
    if filtered.shape[0] == 0:
        raise Exception("no such id " + str(nces_id))
    elif filtered.shape[0] > 1:
        print(filtered)
        raise Exception("multiple ids " + str(filtered.count))
    return filtered['ORG_CODE'].values[0]
    
get_org_code(2501710) # Acton-Boxburough, 6000000





import matplotlib.axes as ax
import matplotlib.cm as cm
for border, info in zip(districts, districts_info):
    name = info["NAME"]
    score = len(name)
    color = cm.ScalarMappable(score)
    xx,yy = zip(*border)
    patch = ax.fill(xx, yy, facecolor=color, edgecolor=color)

cols = ['REC_YEAR', 'ORG_CODE', 'SAT_READ', 'SAT_WRITE', 'SAT_MATH', 'SAT_STU_GROUP_CODE']
sats = pd.read_csv("./MassEduDataChallenge/assessment/sat_performance_report_state_district_school_2005_2013.csv", sep='\t', usecols=cols)
sats_all = sats[sats['SAT_STU_GROUP_CODE'] == "ALL"] 



def get_values(frame, column_name, dist_column_name="ORG_CODE"):
    d = {}
    
    for info in districts_info:
        geoid = int(info['GEOID'])
        
        try:
            org_code = get_org_code(geoid)
            filtered = frame[frame[dist_column_name] == org_code]
        
            if filtered.shape[0] == 1:
                value = filtered[column_name].values[0]
                d[geoid] = value
            else:
                #print filtered.shape
                d[geoid] = 0
        except Exception as ex:
            #print ex
            d[geoid] = 0
            
    return d

values = get_values(sats_all_2005, 'SAT_MATH')
list(values.iteritems())[:20]
'''

import matplotlib.colors as colors
import matplotlib.cm as cmx
cm = plt.get_cmap('gist_rainbow') 
cNorm  = colors.Normalize(vmin=0, vmax=100) #percentages
scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cm)


def graph_a_thing(shapes, values):
    ax = plt.subplot(111)
    # shapes is the shapefile
    # values is a dict mapping of the GEOIDs in shapes to the heatmap values
    
    for i in range(0,len(shapes)):
        # x and y are empty lists to be populated with the coords of each geometry.
        x = []
        y = []
    
        border, info = shapes[i]
        geoid = int(info['GEOID'])
        value = values[geoid]
    
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


for language, project in data.keys():
  graph_a_thing(zip(countries, countries_info), values)


