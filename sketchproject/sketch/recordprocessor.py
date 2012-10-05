"""
recordprocessor module

"""

from copy import deepcopy


class RecordProcessor(object):
    """
    The recordprocessor class is a container for processing functions
    """

    def __init__(self):
        self.processingFunctions = {}
        
        
    def registerProcessingFunction(self, function):        
        """
        register a processing function. 
        The function is referenced by its name
        """
        
        self.processingFunctions[function.__name__] = function
        
    
    def getProcessors(self):
        return self.processingFunctions.keys()
        
        
    def processRecords(self, recordsList, functionName, *args, **kwargs):
        """
        Calls the registered function
        """
        
        #TODO: we should return a generator instead of a list
        pf = self.processingFunctions[functionName]
        return pf(recordsList, *args, **kwargs)
        
        
    def process(self, recordsList, functionNamesAndArgs):
        """
        recordsList: a list of records to be processed
        
        functionNamesAndArgs: a list of dictionaries
        containing the following keys:
            process: is the name of the processing function
            args: list of arguments to be passed in
            kwargs: dict of arguments to be passed as keyword arguments
            
        """
        
        #TODO: probably deepcopy is useless and overkill
        out = copy.deepcopy(records)
        
        for functionNameAndArgs in functionNamesAndArgs:
            functionName = functionNameAndArgs['process']
            args = functionNameAndArgs.get('args', tuple())
            kwargs = functionNameAndArgs.get('kwargs', dict())
            out = self.processRecords(out, functionName, *args, **kwargs)
        
        return out
        
        
        