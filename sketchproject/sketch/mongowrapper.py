import datetime
import settings
import pymongo
import json
import bson
import bson.json_util

class MongoWrapper(object):
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
        

    def dropCollection(self, db_name, collection_name):
        db = self.getDb(db_name)
        collection = getattr(db, collection_name)
        collection.drop()
        
        
        
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
        
        
    
    def objects(self, db_name, collection_name, query_dict={}, offset=0, limit=100, formatter=None):
        """
        Performs find on a collection, with offset and limit parameters
        
        Passing None as limit to this function returns all objects.
        The web view should not permit it.
        
        """
        collection = self.getCollection(db_name, collection_name)
        cursor = collection.find(query_dict)
        
        #TODO: formatter

        records = []
        counted = 0
        has_more = False
        
        for r in cursor[offset:]:
            if counted < limit or limit is None:
                records.append(r)
                counted += 1
            else:
                has_more = True
                break
        
        out = {'records' : records, 'has_more' : has_more, 'num_records' : counted }
        return out
    
    
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
        queryDict = self.parseJsonDict(queryDict)
        
        collection = self.getCollection(db_name, collection_name)
        if queryDict:
            return [collection.find(queryDict).count()]

        return [collection.count()]
        
    
        
        
        
    def parseJsonDict(self, jsonString):
        #TODO: handle a list of dicts        
        try:
            obj = json.loads(jsonString)
            return dict(obj)
        except:
            return {}