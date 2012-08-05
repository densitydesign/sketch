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


#TODO: replace all print statements with self.stdout.write('...')
#TODO: consider throwing exception vs return

class Command(BaseCommand):
    
    option_list = BaseCommand.option_list + (
        make_option('--database', action='store', dest='database', default='',
        help='selects database'),
        
        make_option('--drop-collection', action='store', dest='drop_collection', default='',
        help='selects database'),

    
    )
    
    args = ''

    command_name = 'sketchcmd'
    
    @property
    def help(self):
        lines = ['Sketch command line interface.', '', 'Available commands:']
        return '\n'.join(lines)
        
    #todo: decide what to output exactly, the implementation is not consistent         
    def handle(self, *args, **options):
    
        database = options['database']
        database = database or sketch.settings.MONGO_SERVER_DEFAULT_DB   
        
        drop_collection = options['drop_collection']
        if drop_collection:
            mongo = sketch.mongowrapper.MongoWrapper()
            try:
                mongo.connect()
            except Exception, err:
                print "Mongo connection error", str(err)
                return
                
            mongo.dropCollection(database, drop_collection)
                
                
            try:
                mongo.connection.close()
            except:
                pass
            
    
