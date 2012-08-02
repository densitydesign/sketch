from recordformatter import RecordFormatter
import operator

formattersManager = RecordFormatter()


#example formatter function
def dummyFormatter(record):
    return record
                    


def foursquare_geojson(object):
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
    
    return out

formattersManager.registerFormattingFunction(dummyFormatter)
formattersManager.registerFormattingFunction(foursquare_geojson)


#TODO: AUTODISCOVER FORMATTING FUNCTIONS