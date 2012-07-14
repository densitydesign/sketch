import json
import settings

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
    try:
        obj = json.loads(jsonString)
        return dict(obj)
    except:
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


def getFormatter(self, var_name='formatter'):
    formatter = request.GET.get(var_name) or request.POST.get(var_name)
    return formatter

    