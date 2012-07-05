from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

import datetime
import settings
import json
import bson
import bson.json_util

import decorators
from mongowrapper import MongoWrapper
from helpers import createBaseResponseObject, createResponseObjectWithError
import recordparser



#login view
@csrf_exempt
def ajaxLogin(request):

    message = "No data"

    if request.POST and 'username' in request.POST and 'password' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                message = "You provided a correct username and password!"
            else:
                message = "Your account has been disabled!"
        else:
            message = "Your username and password were incorrect."

    return HttpResponse(json.dumps({'message' : message}))



#TODO: probably we want another type of response here
#TODO: wrap metadata calls in a single view (for example collection names)
def serverMeta(request):

    mongo = MongoWrapper()
    
    try:
        out = createBaseResponseObject()
        mongo.connect()
        existing_dbs = mongo.connection.database_names()
        out['results'] = existing_dbs
    
    except Exception, e:
        out['errors'] = str(e)
        out['status'] = 0
    
    try:
        mongo.connection.close()
    except:
        pass
    
    return HttpResponse(json.dumps(out, default=bson.json_util.default))




    
#TODO: probably we want another type of response here
#TODO: wrap metadata calls in a single view (for example collection names)
def dbMeta(request, database):

    mongo = MongoWrapper()
    
    try:
        out = createBaseResponseObject()
        mongo.connect()

        existing_dbs = mongo.connection.database_names()
        if database not in existing_dbs:
            raise Exception("Database %s does not exist" % database) 
        
        database_object = mongo.getDb(database)
        existing_collections = database_object.collection_names()

        out['results'] = existing_collections
    
    except Exception, e:
        out['errors'] = str(e)
        out['status'] = 0
    
    try:
        mongo.connection.close()
    except:
        pass
    
    return HttpResponse(json.dumps(out, default=bson.json_util.default))




#TODO: probably we want another type of response here
#TODO: wrap metadata calls in a single view (for example collection names)
def parsersMeta(request):
    
    out = createBaseResponseObject()
    try:
        out['results'] = recordparser.ALLOWED_PARSERS.keys()
    
    except Exception, e:
        out['errors'] = str(e)
        out['status'] = 0
        
    return HttpResponse(json.dumps(out, default=bson.json_util.default))






#TODO: handle read permissions, with decorator

def query(request, collection, command, database=None):
    """
    Main view to send commands to handler
    """
    out = createBaseResponseObject()

    database = database or settings.MONGO_SERVER_DEFAULT_DB
    
    mongo = MongoWrapper()
    
    commandMethod = getattr(mongo, command, None)
    
    try:
        
        if not commandMethod or command not in mongo.available_commands:
            raise Exception("Command %s not supported. Available commands are: %s" % (command, ", ".join(mongo.available_commands)))
        
        mongo.connect()
    
        existing_dbs = mongo.connection.database_names()
        if database not in existing_dbs:
            raise Exception("Database %s does not exist" % database)
            
        database_object = mongo.getDb(database)
        existing_collections = database_object.collection_names()
        if collection not in existing_collections:
            raise Exception("Collection %s does not exist" % collection)
            
        results = commandMethod(database, collection, request)
        if results:
            out['results'] = results
    
    except Exception, e:
        out['errors'] = str(e)
        out['status'] = 0
    
    try:
        mongo.connection.close()
    except:
        pass
        
    return HttpResponse(json.dumps(out, default=bson.json_util.default))
    


#this loads an instance of mapper
from mappermanager import mappingManager

#TODO: handle write permissions, with decorator

@decorators.login_required
@decorators.must_own_collection
#temporarily remove crsf control to test easily with curl
@csrf_exempt
def importCall(request, collection, database=None):
    """
    View used to import data.
    """

    #TODO: separate data collection and processing and write a view that handles FILES
    
    out = createBaseResponseObject()
    
    database = database or settings.MONGO_SERVER_DEFAULT_DB
    mongo = MongoWrapper()
    mongo.connect()
    
    #TODO: mapping should come from url, in form of id
    mapping = { '__key__' : 'id_str', 
#      '__upperName__' : { 'transform' : 'upperCase', 'args' : ['name'] },
#      '__fullName__' : { 'transform' : 'concatStrings', 'args' : ['name', 'surname'] },
#      '__fullNameUpper__' : { 'transform' : 'concatStrings', 
#                              'args' : [{ 'transform' : 'upperCase', 'args' : ['name'] }, { 'transform' : 'upperCase', 'args' : ['surname'] }] },
    }

    
    if request.POST:
        if 'data' in request.POST and 'format' in request.POST:
            format = request.POST['format'].lower()
            data = request.POST['data']
            
        try:
            parser = recordparser.parserFactory(format, data)
            for d in parser.objects():
                newRecord = mappingManager.mapRecord(d, mapping)
                mongo._insert(database, collection, newRecord)
                out['results'].append(newRecord)
        
        
        except Exception, e:
            out['errors'] = str(e)
            out['status'] = 0
            


        
        
    
    mongo.connection.close()
    return HttpResponse(json.dumps(out, default=bson.json_util.default))
    
