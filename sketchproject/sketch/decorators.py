"""
decorators module
"""

#from functools import wraps
from django.http import HttpResponse
from django.utils.functional import wraps
import json
from models import SketchCollection
from helpers import createBaseResponseObject
from sketch import settings


def login_required(view):    
    """
    Decorator for login required views.
    Response is in json format.
    """
    
    @wraps(view)
    def inner_decorator(request,*args, **kwargs):
    
        out = createBaseResponseObject()
        
        try:
            if request.user.is_authenticated():
                return view(request, *args, **kwargs)
    
        except Exception, e:
            out['status'] = 0
            out['errors'] = [str(e)]
            return HttpResponse(json.dumps(out))
       
        out['status'] = 0
        out['errors'] = ['You must be logged in to use this feature']
        return HttpResponse(json.dumps(out))

    return inner_decorator

    
#todo: limit number of collections per user    
def can_write_collection(view):    
    """
    Checks if a collection is writable by the current user
    Response is in json format.
    """
    
    @wraps(view)
    def inner_decorator(request, collection, *args, **kwargs):
        
        out = createBaseResponseObject()
        database = kwargs.get(database, settings.MONGO_SERVER_DEFAULT_DB)

        try:
            #check user and collection
            collectionInstance = SketchCollection.objects.get(name=collection, database=database)
            wa = collectionInstance.hasWriteAccess(request.user)
            if wa:
                return view(request, collection, database=database, *args, **kwargs)
        
        except SketchCollection.DoesNotExist:
            #TODO: we could limit the number of collections here
            return view(request, collection, database=database, *args, **kwargs)
        
        
        except Exception, e:
            out['status'] = 0
            out['errors'] = [str(e)]
            return HttpResponse(json.dumps(out))
        
        out['status'] = 0
        out['errors'] = ['You must own collection %s or have the right to write to it.' % collection]
        return HttpResponse(json.dumps(out))

    return inner_decorator
    
    
#todo: limit number of collections per user    
def can_read_collection(view):    
    """
    Checks if a collection is readable by the current user
    Response is in json format.
    """

    @wraps(view)
    def inner_decorator(request, collection, *args, **kwargs):
        
        out = createBaseResponseObject()
        database = kwargs.get(database, settings.MONGO_SERVER_DEFAULT_DB)
        
        try:
            #check user and collection
            collectionInstance = SketchCollection.objects.get(name=collection, database=database)
            wa = collectionInstance.hasReadAccess(request.user)
            if wa:
                return view(request, collection, database=database, *args, **kwargs)
        
        except Exception, e:
            out['status'] = 0
            out['errors'] = [str(e)]
            return HttpResponse(json.dumps(out))
        
        out['status'] = 0
        out['errors'] = ['You must own collection %s or have the right to read to it.' % collection]
        return HttpResponse(json.dumps(out))

    return inner_decorator