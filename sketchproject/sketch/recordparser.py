import sys
import json
import StringIO


class ParserError(object):

    def __init__(self, raw_data, exception_message):
        self.raw_data = raw_data
        #expecting a string, forcing conversion anyway
        self.exception_message = str(exception_message)


class BaseRecordParser(object):

    def __init__(self, data):
        self.data = data
        
        
    def objects(self):
        raise NotImplementedError
        
        
class CSVRecordParser(BaseRecordParser):
    
    def objects(self):
        raise NotImplementedError
    

class JSONListParser(BaseRecordParser):
    
    def objects(self):
        items = json.loads(self.data)
        if type(items) is list:
            for item in items:
                yield item
        else:
            raise TypeError('Data should be a json list')
            

class JSONTextFileParser(BaseRecordParser):    

    def objects(self):
        buffer = StringIO.StringIO(self.data)
        for line in buffer.readlines():
            try:
                item = json.loads(line)
                yield item

            except Exception, e:
                yield ParserError(line, str(e))


#TODO: move allowed parsers to settings
ALLOWED_PARSERS = {
    #'csv' : 'CSVRecordParser', 
    'jsonlist' : 'JSONListParser',
    'jsontext' : 'JSONTextFileParser'
}


def parserFactory(parserName, data):

    currentModule = sys.modules[__name__]
    try:
        constructorName = ALLOWED_PARSERS[parserName]
    except:
        raise ValueError('parser %s is not available. Available parsers are: %s' % (parserName, str(ALLOWED_PARSERS.keys())))
    
    try:
        constructor = getattr(currentModule, constructorName) 
    except:
        raise Exception("class %s not available as a parser" % constructorName)
        
    return constructor(data)
    