from django.conf import settings

#mongo server configuration
MONGO_SERVER_HOSTNAME = getattr(settings, 'MONGO_SERVER_HOSTNAME', 'localhost')
MONGO_SERVER_PORT = getattr(settings, 'MONGO_SERVER_PORT', '27017')

MONGO_SERVER_DEFAULT_DB = getattr(settings, 'MONGO_SERVER_DEFAULT_DB', 'sketchdb')

DEFAULT_QUERY_LIMIT = 100
MAX_ERROR_RECORDS = getattr(settings, 'MAX_ERROR_RECORDS', 10000)


_ALLOWED_PARSERS = {
    #'csv' : 'CSVRecordParser', 
    'jsonlist' : 'JSONListParser',
    'jsontext' : 'JSONTextFileParser'
}

ALLOWED_PARSERS = getattr(settings, "ALLOWED_PARSERS", _ALLOWED_PARSERS)
