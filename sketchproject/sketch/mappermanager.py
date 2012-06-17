from mapper import RecordMapper

mappingManager = RecordMapper()

def upperCase(value):
    return str(value).upper()
   
def concatStrings(*strings):
    return " ".join(strings)

mappingManager.registerTransform(upperCase)
mappingManager.registerTransform(concatStrings)
        