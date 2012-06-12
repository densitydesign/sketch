from django.conf import settings

#mongo server configuration
MONGO_SERVER_HOSTNAME = getattr(settings, 'MONGO_SERVER_HOSTNAME', 'localhost')
MONGO_SERVER_PORT = getattr(settings, 'MONGO_SERVER_PORT', '27017')
