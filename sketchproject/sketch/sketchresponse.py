import json
import bson
import bson.json_util


class SketchJSONResponse(object):
    """
    This class represents an object used to wrap
    a json response
    """

    def __init__(self):
        self.data = dict()
        self.data['status'] = 1
        self.data['request'] = None
        self.data['results'] = []
        self.data['error_records'] = { 'parser' : [], 'mapper' : [] }
        self.data['ok_records_number'] = 0
        
    def setErrorStatus(self):
        self.data['status'] = 0
        
        
    def setSuccessStatus(self):
        self.data['status'] = 1
        
        
    def setRequest(self, requestData):
        self.data['request'] = requestData
        
        
    def setResults(self, results):
        self.data['results'] = results
        
        
    def getJSON(self):
        json.dumps(self.data, default=bson.json_util.default)
        
    