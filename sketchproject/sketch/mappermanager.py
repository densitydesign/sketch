#todo: transform file should be autodiscovered in other apps
from mapper import RecordMapper

mappingManager = RecordMapper()

def upperCase(value):
    return str(value).upper()
   
def concatStrings(*strings):
    return " ".join(strings)
    
#geocode dummy example
def geocodeAddress(address):
    #here we should call some geolocation api
    out = (0,0)
    
    return out
    
    
    
def GEOJsonFromFourSquareVenue(object):
    loc = object['location']

    properties = dict()
    properties['id'] = object['id']
    
    out =   { "type": "FeatureCollection",
              "features": [
                  { "type": "Feature",
                     "geometry": {"type": "Point", "coordinates": [loc['lat'], loc['lng']] },
                     "properties" : properties
                  }
              ]
            }
    
    print out
    return out


mappingManager.registerTransform(upperCase)
mappingManager.registerTransform(concatStrings)
mappingManager.registerTransform(GEOJsonFromFourSquareVenue)


#
#TODO: coded mappers should be autodiscovered in some way
#
codedMappers = {}

"""
import sketchmappers

for x in dir(sketchmappers):
    obj = getattr(sketchmappers, x)
"""


testMapper = { '__key__' : 'id',
               '__GEOJSON_BASE__' : {'transform' : 'GEOJsonFromFourSquareVenue', 'args' : ['__self__',] }
     }

codedMappers['test_four_square'] = testMapper