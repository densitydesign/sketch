from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, render_to_response
from django.views.decorators.csrf import csrf_exempt

import datetime
import settings
import json
import bson
import bson.json_util

import decorators
from mongowrapper import MongoWrapper
from helpers import createBaseResponseObject, createResponseObjectWithError

#TODO: as pymongo creates a db or collection if it does not exits,
# we should prevent this by allowing queries only on existing objects
# for example using decorators like @existing_database, existing_collection

#TODO: handle read permissions, with decorator

def query(request, collection, command, database=None):
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

#TODO: handle write permissions, with decorator

@decorators.login_required
@decorators.must_own_collection
#temporarily remove crsf control to test easily with curl
@csrf_exempt
def import(request, collection, database=None):
    """
    View used to import data
    """
    
    out = createBaseResponseObject()
    
    database = database or settings.MONGO_SERVER_DEFAULT_DB
    mongo = MongoWrapper()
    mongo.connect()
    
    #TODO: mapping should come from url, in form of id
    mapping = { '__key__' : 'id', 
      '__upperName__' : { 'transform' : 'upperCase', 'args' : ['name'] },
#      '__fullName__' : { 'transform' : 'concatStrings', 'args' : ['name', 'surname'] },
#      '__fullNameUpper__' : { 'transform' : 'concatStrings', 
#                              'args' : [{ 'transform' : 'upperCase', 'args' : ['name'] }, { 'transform' : 'upperCase', 'args' : ['surname'] }] },
    }

    
    if request.POST:
        #TODO: data should be parsed according to format
        #TODO: handle errors
        data = json.loads(request.raw_post_data)
        for d in data:
            newRecord = mappingManager.mapRecord(d, mapping)
            mongo._insert(database, collection, newRecord)
            out['results'].append(newRecord)
    
    mongo.connection.close()
    return HttpResponse(json.dumps(out, default=bson.json_util.default))
    
