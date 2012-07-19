from copy import deepcopy


class RecordMapper(object):

    def __init__(self):
        self.transformFunctions = {}
        
        
    def registerTransform(self, function):
        """
        register a transform function. 
        It would be nice to add an exception policy.
        """
        self.transformFunctions[function.__name__] = function
        
        
    def getTransforms(self):
        return self.transformFunctions.keys()
        
        
    def mapField(self, record, mappingItem):
        
        mappingItemType = type(mappingItem)

        if mappingItemType is str:
            return record[mappingItem]
            
        if mappingItemType is dict:
            transform = mappingItem['transform']
            args = mappingItem.get('args', tuple())       
            
            #TODO (maybe): implement kwargs
            #kwargs = mappingItem.get('kwargs', dict())

            recordArgs = []
            for arg in args:
                recordArg = self.mapField(record, arg)
                recordArgs.append(recordArg)
            
            transformFunction = self.transformFunctions[transform]
            return transformFunction(*recordArgs)
        
        #raising an exception
        raise TypeError
        

    def mapRecord(self, record, mapping):
        #TODO: is deepcopy necessary/useful?
        newRecord = deepcopy(record)
    
        for key in mapping:
            mappingItem = mapping[key]
            newRecord[key] = self.mapField(newRecord, mappingItem)                
        return newRecord


if __name__ == '__main__':

    mapper = RecordMapper()

    def upperCase(value):
        return str(value).upper()
        
    def concatStrings(*strings):
        return " ".join(strings)
    
    mapper.registerTransform(upperCase)
    mapper.registerTransform(concatStrings)
        
    #todo: mapping should be able to refer to previous defined keys    
    mapping = { '__key__' : 'id', 
                '__upperName__' : { 'transform' : 'upperCase', 'args' : ['name'] },
                '__fullName__' : { 'transform' : 'concatStrings', 'args' : ['name', 'surname'] },
                '__fullNameUpper__' : { 'transform' : 'concatStrings', 
                                        'args' : [{ 'transform' : 'upperCase', 'args' : ['name'] }, { 'transform' : 'upperCase', 'args' : ['surname'] }] },
              }

    record = { 'id' : 100, 'name' : 'Mauro', 'surname': 'Bianchi'}

    newRecord = mapper.mapRecord(record, mapping)
    
    
    
    print newRecord