#from functools import wraps
from django.http import HttpResponse
from django.utils.functional import wraps
import json
from models import SketchCollection

from helpers import createBaseResponseObject


def login_required(view):    
    
    @wraps(view)
    def inner_decorator(request,*args, **kwargs):
    
         out = createBaseResponseObject()
        
        try:
            if request.user.is_authenticated():
                return view(request, *args, **kwargs)
    
        except Exception e:
            out['status'] = 0
            out['errors'] = [str(e)]
            return HttpResponse(json.dumps(out))
       
        out['status'] = 0
        out['errors'] = ['You must be logged in to use this feature']
        return HttpResponse(json.dumps(out))

    return inner_decorator
    
    
def must_own_collection(view):    
    
    @wraps(view)
    def inner_decorator(request, collection, *args, **kwargs):
        
        out = createBaseResponseObject()
        
        #if 'collection' not in kwargs:
        #    return func(request, *args, **kwargs)

        #collection = kwargs['collection']
        try:
            #TODO: check user and collection
            collectionInstance = SketchCollection.objects.get(name=collection)
            wa = collectionInstance.hasWriteAccess(request.user)
            
            if wa:
                return view(request, collection, *args, **kwargs)
        except Exception, e:
            out['status'] = 0
            out['errors'] = [str(e)]
            return HttpResponse(json.dumps(out))
        
        out['status'] = 0
        out['errors'] = ['You must own collection %s or have the right to write to it.' % collection]
        return HttpResponse(json.dumps(out))

    return inner_decorator