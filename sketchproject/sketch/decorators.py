#from functools import wraps
from django.http import HttpResponse
from django.utils.functional import wraps
import json


def login_required(view):    
    @wraps(view)
    def inner_decorator(request,*args, **kwargs):
        try:
            if request.user.is_authenticated():
                return view(request, *args, **kwargs)
        except:
            pass

        out = dict()
        out['status'] = 1
        out['results'] = []
        out['errors'] = ['You must be logged in to use this feature']
        return HttpResponse(json.dumps(out))


    return inner_decorator
    
    
def must_own_collection(view):    
    @wraps(view)
    def inner_decorator(request,*args, **kwargs):
        if 'collection' not in kwargs:
            return func(request, *args, **kwargs)
    
        collection = kwargs['collection']
        try:
            #TODO: check user and collection
            return view(request, *args, **kwargs)
        except:
            pass

        out = dict()
        out['status'] = 1
        out['results'] = []
        out['errors'] = ['You must own collection %s' % collection]
        return HttpResponse(json.dumps(out))

    return inner_decorator