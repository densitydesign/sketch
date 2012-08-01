from __future__ import absolute_import

from django.core.management.base import BaseCommand
from optparse import make_option
import sketch
import sketch.models
import sketch.views
import sketch.settings
import sketch.recordparser
import sketch.mappermanager
import sketch.processingmanager
import sketch.helpers
import sketch.mongowrapper

class Command(BaseCommand):
    
    option_list = BaseCommand.option_list + (
        make_option('--database', action='store', dest='database', default='',
        help='Selects database'),
        
        make_option('--query', action='store', dest='query', default='',
        help='Query'),
        
        make_option('--limit', action='store', dest='limit', default='',
        help='Limit'),

        make_option('--collection', action='store', dest='collection', default='',
        help='Selects collection'),

        
    )
    
    args = 'database collection'

    command_name = 'sketchobjects'
    
    @property
    def help(self):
        lines = ['Sketch command line interface.', '', 'Available commands:']
        return '\n'.join(lines)
        
    def handle(self, *args, **options):
        
        database = options['database']
        database = database or sketch.settings.MONGO_SERVER_DEFAULT_DB   
        
        collection = options['collection']
        if not collection:
            print "Collection must be specified with --collection"
            return

        print collection
        
        
        query = options['query']
        try:
            limit = int(options['limit'])
        except:
            limit = 0
        
        try:
            offset = int(options['offset'])        
        except:
            offset = 0
        
        #TODO: get objects    
    
