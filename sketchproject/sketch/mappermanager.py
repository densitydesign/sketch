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

mappingManager.registerTransform(upperCase)
mappingManager.registerTransform(concatStrings)
        