"""
recordparser module

The record parser is the object used to convert data from a textual source into records.
It is used at import time.

"""


import sys
import json
import StringIO
from sketch import settings


class ParserError(object):
    """
    Class used to store a parsing error, along with data generating the error
    """

    def __init__(self, raw_data, exception_message):
        self.raw_data = raw_data
        #expecting a string, forcing conversion anyway
        self.exception_message = str(exception_message)


class BaseRecordParser(object):
    """
    Abstract class for record parser.
    All parser classes should inherit from this class and must implement
    the 'objects' method.
    """

    def __init__(self, data):
        self.data = data
        
        
    def objects(self):
        """
        This method must be implemented in concrete classes.
        It should be implemented as a generator, which parses
        data passed in to the constructor and returns an object
        (in the form of a dictionary) while it's cycled on.
        """
        raise NotImplementedError
        
        
class CSVRecordParser(BaseRecordParser):
    """
    This parser allows reading records from a string representing records
    in csv format. The first line in the data should be a header with field names.
    """
    #TODO: implement this parser
    def objects(self):
        raise NotImplementedError
    

class JSONListParser(BaseRecordParser):
    """
    This parser allows reading records from a string representing a 
    list of objects in json format.
    """
    
    def objects(self):
        items = json.loads(self.data)
        if type(items) is list:
            for item in items:
                yield item
        else:
            raise TypeError('Data should be a json list')
            

class JSONTextFileParser(BaseRecordParser):    
    """
    This parser allows reading records from a string representing a set of
    json objects separated by newlines
    """

    def objects(self):
        buffer = StringIO.StringIO(self.data)
        for line in buffer.readlines():
            try:
                item = json.loads(line)
                yield item

            except Exception, e:
                yield ParserError(line, str(e))


#keeping a reference of ALLOWED_PARSERS within this module.
ALLOWED_PARSERS = settings.ALLOWED_PARSERS


#TODO: allow registration of parser by other modules.
def parserFactory(parserName, data):
    """
    Factory method that instantiates a parser given parser name and data to be parsed
    and returns it.
    Parser are referenced by the key used in settings.ALLOWED_PARSERS.
    Requested parser must be in settings.ALLOWED_PARSERS
    """
    
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
    