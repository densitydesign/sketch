from recordprocessor import RecordProcessor
import operator

processingManager = RecordProcessor()


#example processing function
def frequentWords(recordsList, textFieldName, numwords):
    out = {}
    for record in recordsList:
        text = record.get(textFieldName)
        if not text:
            continue
        
        words = text.split(" ")
        for word in words:
            if word not in out:
                out[word] = 0
            out[word] += 1
        
    outSorted = sorted(out.iteritems(), key=operator.itemgetter(1))
    outSorted = out_sorted[:numwords]
    
    return dict(outSorted)
                
processingManager.registerProcessingFunction(frequentWords)