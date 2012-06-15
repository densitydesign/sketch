from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, render_to_response
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
        
        
    def insert(self, db_name, collection_name, request):
    
        document = request.GET.get('document') or request.POST.get('document')
        document = self.parseJsonDict(document)       
        
        collection = self.getCollection(db_name, collection_name)
        return collection.insert(document)    
        
    
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


def api_call(request, collection, command, database=None):
    """
    Main view to send commands to handler
    """

    out = dict()
    out['status'] = '0'
    out['results'] = []
    out['errors'] = []

    database = database or settings.MONGO_SERVER_DEFAULT_DB
    
    handler = MongoHandler()
    handler.connect()

    command = getattr(handler, command, None)
    if not command:
        raise Exception("Command %s not supported" % command)
    
    results = command(database, collection, request)
    if results:
        out['results'] = results
    
    
    return HttpResponse(json.dumps(out, default=bson.json_util.default))
    
    
