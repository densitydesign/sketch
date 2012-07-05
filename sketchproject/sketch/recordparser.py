import sys
import json
import StringIO


class BaseRecordParser(object):
    def __init__(self, data)
        self.data = data
        
        
    def objects(self):
        raise NotImplementedError
        
        
class CSVRecordParser(BaseRecordParser):
    
    def objects(self):
        raise NotImplementedError
    

class JSONListParser(BaseRecordParser):
    
    def objects(self):
        items = json.loads(self.data)
        if type(jsondata) is list:
            for item in items:
                yield item
        else:
            raise TypeError('Data should be a json list')
            

class JSONTextFileParser(BaseRecordParser):    
    def objects(self):
        buffer = StringIO.StringIO(self.data)
        for line in buffer.readlines():
            item = json.loads(line)
            yield item


#TODO: move allowed parsers to settings
#TODO: expose available parsers list to rest api
ALLOWED_PARSERS = {
    #'csv' : 'CSVRecordParser', 
    'jsonlist' : 'JSONListParser',
    'jsontext' : 'JSONTextFileParser'
}


def parserFactory(parserName, data):

    currentModule = sys.modules[__name__]
    try:
        constructorName = ALLOWED_PARSERS[formatterName]
    except:
        raise ValueError('parser %S is not available. Available parsers are: %s' % (parserName, str(ALLOWED_PARSERS.keys())))
    
    try:
        constructor = getattr(currentModule, constructorName) 
    except:
        raise Exception("class %s not available as a parser" % constructorName)
        
    return constructor(data)
    