from copy import deepcopy


class RecordProcessor(object):

    def __init__(self):
        self.processingFunctions = {}
        
        
    def registerProcessingFunction(self, function):
        """
        register a processing function. 
        """
        self.processingFunctions[function.__name__] = function
    
    def getProcessors(self):
        return self.processingFunctions.keys()
        
        
    def processRecords(self, recordsList, functionName, *args, **kwargs):
        
        pf = self.processingFunctions[functionName]
        return pf(recordsList, *args, **kwargs)
        
        
    def process(self, recordsList, functionNamesAndArgs):
        
        out = copy.deepcopy(records)
        for functionNameAndArgs in functionNamesAndArgs:
            functionName = functionNameAndArgs['process']
            args = functionNameAndArgs.get('args', tuple())
            kwargs = functionNameAndArgs.get('kwargs', dict())
            out = self.processRecords(out, functionName, *args, **kwargs)
        
        return out
        
        
        