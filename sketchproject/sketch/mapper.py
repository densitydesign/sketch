"""
mapper module

In sketch, a mapping is a set of operations to be performed on a record, adding or modifying
its properties.

The mapping is represented as a dictionary, where: 

    * keys represent the name of a property to be set on the record object
    * values are dictionaries describing functions to be called to calculate the property
      and arguments to be passed in. This is a "trasformation describer".
      For each key in the mapping, the transformation describer needs the following keys:
    
      transform:  the name of the transform function to be called
      args: list of arguments to be passed to the function
    
Keyword arguments are not supported at the moment.
Each argument can be of two types:

    * the name of a property of the original record. A lookup is performed and the value of
      the given record property is passed to the transform. The special name '__self__' refers
      to the whole record
    
    * another transformation descriptor

"""

from copy import deepcopy
import inspectutils

class RecordMapper(object):

    def __init__(self):
        self.transformFunctions = {}
        
    def registerTransform(self, function):
        """
        register a transform function. 
        The function will be referenced by its name
        It would be nice to add an exception policy.
        """
        self.transformFunctions[function.__name__] = function
        
        
    def getTransforms(self):
        return self.transformFunctions.keys()
        
        
    def mapField(self, record, mappingItem):
        """
        """
        mappingItemType = type(mappingItem)

        if mappingItemType is str:
            if mappingItem == "__self__":
                return record
            return record[mappingItem]
            
        if mappingItemType is dict:
            transform = mappingItem['transform']
            args = mappingItem.get('args', tuple())       
            
            #TODO: implement kwargs
            #kwargs = mappingItem.get('kwargs', dict())

            recordArgs = []
            for arg in args:
                recordArg = self.mapField(record, arg)
                recordArgs.append(recordArg)
            
            transformFunction = self.transformFunctions[transform]
            return transformFunction(*recordArgs)
        
        #raising an exception
        raise TypeError
        

    def mapRecord(self, record, mapping, constants={}):
        """
        Maps a record, given a mapping.
        
        record: a dictionary
        
        mapping: a dictionary containing the mapper description
        
        constants: dictionary of properties to be copied directly
                   to the record.
                   Note that constanst are copied as last step, so if
                   its keys are already present in the record they will be 
        """
    
        #TODO: is deepcopy necessary/useful?
        newRecord = deepcopy(record)
    
        for key in mapping:
            mappingItem = mapping[key]
            newRecord[key] = self.mapField(newRecord, mappingItem)                
            
        newRecord.update(constants)
        return newRecord
        
    def validateMapping(self, mapping):
        """
        """
        
        #element validation logic
        #TODO: use recursively if other transforms are found in args or kwargs
        def validateMappingElement(el):
            if type(el) is str:
                return true
            if type(el) is dict:
                
                for k in el.keys():
                    if k not in ['transform', 'args', 'kwargs']:
                        raise KeyError("Found invalid key %s in mapping" % k)
                
                if 'transform' not in el:
                    raise KeyError("transform key not found in mapping")
                
                transform = el['transform']
                
                if transform not in self.transformFunctions:
                    raise KeyError("mapping uses unknown %s transform" % transform)
                else:
                    requiredArgs = inspectutils.getRequiredArgs(self.transformFunctions[transform])
                    if requiredArgs:
                        args = el.get('args', [])
                        argsLen = len(args)
                        requiredArgsLen = len(requiredArgs)
                        if argsLen != requiredArgsLen:
                            raise ValueError("Transform %s requires %d arguments but %d arguments provided in mapping" % (transform,
                                requiredArgsLen, argsLen))
                    
        
        if type(mapping) is not dict and type(mapping) is not str:
            raise TypeError("Mapping item should be a dictionary or a string")

        if type(mapping) is dict:
            for k in mapping.keys():
                valid = validateMappingElement(mapping[k])
    
        return True





#TODO: move this to a test case
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