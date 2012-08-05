import json
import settings
import bson
import bson.json_util

def instanceDict(instance, key_format=None):
    "Returns a dictionary containing field names and values for the given instance"
    from django.db.models.fields.related import ForeignKey
    if key_format:
        assert '%s' in key_format, 'key_format must contain a %s'
    key = lambda key: key_format and key_format % key or key

    d = {}
    for field in instance._meta.fields:
        attr = field.name
        value = getattr(instance, attr)
        if value is not None and isinstance(field, ForeignKey):
            value = value._get_pk_val()
        d[key(attr)] = value
    for field in instance._meta.many_to_many:
        d[key(field.name)] = [obj._get_pk_val() for obj in getattr(instance, field.attname).all()]
    return d





def createBaseResponseObject():
    """
    Creates a dict used as a request in json responses.
    Status is set to 1 (success)
    """

    out = dict()
    out['status'] = '1'
    out['results'] = []
    out['errors'] = []

    return out

def createResponseObjectWithError(error):
    """
    Creates a dict used as a request in json responses,
    with an error in it and status set to 0 (failure)
    """

    out = dict()
    out['status'] = '0'
    out['results'] = []
    out['errors'] = [error]

    return out
    
    
def getQueryDict(request, var_name='query'):
    #TODO: handle a list of dicts        
    queryDict = request.GET.get(var_name) or request.POST.get(var_name)
    if not queryDict:
        return {}
        
    try:
        obj = json.loads(queryDict, object_hook=bson.json_util.object_hook)
        return dict(obj)
    except Exception, err:
        raise Exception("Query error: " + str(err) + ", Wrong query dict:" + str(queryDict))
        return {}    


def getLimit(request, var_name='limit'):
    limit = request.GET.get(var_name) or request.POST.get(var_name)
    try:
        obj = int(limit)
        return max(obj, settings.DEFAULT_QUERY_LIMIT)
    except:
        return settings.DEFAULT_QUERY_LIMIT    
        

def getOffset(request, var_name='offset'): 
    offset = request.GET.get(var_name) or request.POST.get(var_name)
    try:
        obj = int(limit)
        return obj
    except:
        return 0


def getFormatter(request, var_name='formatter'):
    formatter = request.GET.get(var_name) or request.POST.get(var_name)
    return formatter


def getMapper(request, var_name='mapper'):
    mapper = request.GET.get(var_name) or request.POST.get(var_name)
    return mapper 