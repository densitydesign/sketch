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

from mongowrapper import MongoWrapper



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
    
    mongo = MongoWrapper()
    
    commandMethod = getattr(mongo, command, None)
    if not commandMethod or command not in mongo.available_commands:
        raise Exception("Command %s not supported" % command)

    mongo.connect()
    
    results = commandMethod(database, collection, request)
    if results:
        out['results'] = results
    
    mongo.connection.close()
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
    mongo = MongoWrapper()
    mongo.connect()
    
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
            mongo._insert(database, collection, newRecord)
            out['results'].append(newRecord)
    
    mongo.connection.close()
    return HttpResponse(json.dumps(out, default=bson.json_util.default))
    
