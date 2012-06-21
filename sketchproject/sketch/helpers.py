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