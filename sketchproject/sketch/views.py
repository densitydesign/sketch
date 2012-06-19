from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, render_to_response
from django.views.decorators.csrf import csrf_exempt
#from django.contrib.auth.decorators import login_required
import decorators

import datetime
import settings
import pymongo
import json
import bson
import bson.json_util

class MongoHandler(object):
    """
    This class interacts with Mongo Db instance 
    """
    
    available_commands = ['find_one', 'find', 'count']
    
    def __init__(self, server=None, port=None):
        self.server = server or settings.MONGO_SERVER_HOSTNAME
        self.port = int(port or settings.MONGO_SERVER_PORT)
        self.connection = None
        
    def connect(self):
    
        self.connection = pymongo.Connection(self.server, self.port)
        
        
    def getDb(self, db_name):
    
        db = getattr(self.connection, db_name)
        return db
        
        
    def getCollection(self, db_name, collection_name):
    
        db = self.getDb(db_name)
        collection = getattr(db, collection_name)
        return collection
        
        
    def _insert(self, db_name, collection_name, document):
    
        collection = self.getCollection(db_name, collection_name)
        return collection.insert(document)    
    
    
    def insert(self, db_name, collection_name, request):
    
        document = request.GET.get('document') or request.POST.get('document')
        document = self.parseJsonDict(document)       
        return self._insert(db_name, collection_name, document)
    
    
    def find_one(self, db_name, collection_name, request): 
    
        queryDict = request.GET.get('query') or request.POST.get('query')
        queryDict = self.parseJsonDict(queryDict)
        collection = self.getCollection(db_name, collection_name)
        return collection.find_one(queryDict)
        
        
    def find(self, db_name, collection_name, request): 
        
        queryDict = request.GET.get('query') or request.POST.get('query')
        queryDict = self.parseJsonDict(queryDict)

        collection = self.getCollection(db_name, collection_name)
        cursor = collection.find(queryDict)

        out = []
        for r in cursor:
            out.append(r)
        return out
        
        
    def count(self, db_name, collection_name, request): 
        
        queryDict = request.GET.get('query') or request.POST.get('query')
        queryDict = self.parseJsonQueryDict(queryDict)
        
        collection = self.getCollection(db_name, collection_name)
        
        if queryDict:
            return collection.find(queryDict).count()

        return collection.count()
        
        
    def parseJsonDict(self, jsonString):
        #TODO: handle a list of dicts        
        try:
            obj = json.loads(jsonString)
            return dict(obj)
        except:
            return {}



def createBaseResponseObject():
    """
    Creates a dict used as a request in json responses
    """

    out = dict()
    out['status'] = '0'
    out['results'] = []
    out['errors'] = []

    return out



def api_call(request, collection, command, database=None):
    """
    Main view to send commands to handler
    """
    out = createBaseResponseObject()

    database = database or settings.MONGO_SERVER_DEFAULT_DB
    
    handler = MongoHandler()
    
    commandMethod = getattr(handler, command, None)
    if not commandMethod or command not in handler.available_commands:
        raise Exception("Command %s not supported" % command)

    handler.connect()
    
    results = commandMethod(database, collection, request)
    if results:
        out['results'] = results
    
    handler.connection.close()
    return HttpResponse(json.dumps(out, default=bson.json_util.default))
    


#this loads an instance of mapper
from mappermanager import mappingManager


#temporarily remove crsf control to test easily with curl

@decorators.login_required
@decorators.must_own_collection
@csrf_exempt
def mapper_call(request, collection, database=None):
    """
    View used to import data
    """
    
    out = createBaseResponseObject()
    
    database = database or settings.MONGO_SERVER_DEFAULT_DB
    handler = MongoHandler()
    handler.connect()
    
    #mapping should come from url, in form of id
    mapping = { '__key__' : 'id', 
      '__upperName__' : { 'transform' : 'upperCase', 'args' : ['name'] },
#      '__fullName__' : { 'transform' : 'concatStrings', 'args' : ['name', 'surname'] },
#      '__fullNameUpper__' : { 'transform' : 'concatStrings', 
#                              'args' : [{ 'transform' : 'upperCase', 'args' : ['name'] }, { 'transform' : 'upperCase', 'args' : ['surname'] }] },
    }

    
    if request.POST:
        #TODO: data should be parsed according to format
        data = json.loads(request.raw_post_data)
        for d in data:
            newRecord = mappingManager.mapRecord(d, mapping)
            handler._insert(database, collection, newRecord)
            out['results'].append(newRecord)
    
    
    return HttpResponse(json.dumps(out, default=bson.json_util.default))
    
