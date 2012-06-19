def createBaseResponseObject():
    """
    Creates a dict used as a request in json responses
    """

    out = dict()
    out['status'] = '1'
    out['results'] = []
    out['errors'] = []

    return out
