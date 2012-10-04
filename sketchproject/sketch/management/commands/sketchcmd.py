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
        help='drops a collection'),
        
        make_option('--drop-database', action='store_true', dest='drop_database', default='',
        help='drops a database'),
    
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
        drop_database = options['drop_database']
        
        if drop_collection or drop_database:
        
            mongo = sketch.mongowrapper.MongoWrapper()
            try:
                mongo.connect()
            except Exception, err:
                print "Mongo connection error", str(err)
                return
                
            if drop_collection:
                mongo.dropCollection(database, drop_collection)
                try:
                    coll = sketch.models.SketchCollection.objects.get(name=drop_collection, database=database)
                    coll.delete()
                except Exception, e:
                    print "Error during sql deletion:", str(e)
            
            if drop_database:
                mongo.dropDatabase(database)
                try:
                    colls = sketch.models.SketchCollection.objects.filter(database=database)
                    for coll in colls:
                        coll.delete()
                except Exception, e:
                    print "Error during sql deletion:", str(e)
                
            try:
                mongo.connection.close()
            except:
                pass
            
    
