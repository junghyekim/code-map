import pandas as pd
import shapefile
from shapely.geometry import shape, Point
from pyproj import Proj, transform
import urllib, urllib2
import json

## change data to user input
address = "233 E Washington St"

# add in geocoding
def decode_address_to_coordinates(address):
    params = {
            'address' : address +" Syracuse,NY",
            'sensor' : 'false',
    }
    url = 'http://maps.google.com/maps/api/geocode/json?' + urllib.urlencode(params)
    response = urllib2.urlopen(url)
    result = json.load(response)
    try:
        return result['results'][0]['geometry']['location']
    except:
        return None

#potholes = data[['inspector_name', 'address', 'longitude', 'latitude']]
def convert_proj(x,y):
    inProj = Proj(init='epsg:4326')
    outProj = Proj(init='epsg:32016')
    x1,y1 = x,y
    x2,y2 = transform(inProj,outProj,x1,y1)
    x2 = 3.2808399 * x2
    y2 = 3.2808399 * y2
    return Point(x2, y2)

def zone_finder(address):
    # geocode address
    dec_address= decode_address_to_coordinates(address)

    # read in the shapefile
    r = shapefile.Reader("S:/Housing Stability/Data/Inspector Catchment Areas/CATCHMENTS.shp")

    # get the shapes and convert them to Shapely polygons
    polys = [shape(x) for x in r.shapes()]

    # get the records from the shapefile
    records = r.records()

    # create new dataframe for adding TNT's
    #code_with_inspector = potholes.copy()

    # add an empty column for storing TNT name
    #code_with_inspector["inspector_name"] = ''

    # create new dataframe for adding TNT's
    #code_with_inspector = potholes.copy()

    # add an empty column for storing TNT name
    #code_with_inspectort["inspector_name"] = ''


    point = convert_proj(dec_address['longitude'], dec_address['latitude'])

    # iterates through the neighborhood polygons and find the one that the point is within
    # assigns the TNT name of the containing polygon to the row in the new potholes dataframe
    for i in range(len(polys)):
        if point.within(polys[i]):
            print "inspector_name", records[i][6]
            break
