from copy import deepcopy


class RecordFormatter(object):

    def __init__(self):
        self.formattingFunctions = {}
        
        
    def registerFormattingFunction(self, function):
        """
        register a formatting function. 
        """
        self.formattingFunctions[function.__name__] = function
    
    def getFormatters(self):
        return self.formattingFunctions.keys()
        
    def getFormatter(self, name):
        return self.formattingFunctions[name]
        
        
    def formatRecord(self, record, functionName, *args, **kwargs):
        
        pf = self.formattingFunctions[functionName]
        return pf(record, *args, **kwargs)
        
        return out
        
        
        
        