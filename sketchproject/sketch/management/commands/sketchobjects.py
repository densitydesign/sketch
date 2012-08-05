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
import sketch.formattersmanager
import sketch.helpers
import sketch.mongowrapper
import json
import bson.json_util

#TODO: replace all print statements with self.stdout.write('...')
#TODO: consider throwing exception vs return

class Command(BaseCommand):
    
    option_list = BaseCommand.option_list + (
        make_option('--database', action='store', dest='database', default='',
        help='Selects database'),
        
        make_option('--query', action='store', dest='query', default='',
        help='Query'),
        
        make_option('--limit', action='store', dest='limit', default='',
        help='Limit'),
        
        make_option('--offset', action='store', dest='offset', default='',
        help='Offset'),
        
        make_option('--formatter', action='store', dest='formatter', default='',
        help='Formatter'),

        make_option('--collection', action='store', dest='collection', default='',
        help='Selects collection'),
    )
    
    args = ''
    command_name = 'sketchobjects'
    
    @property
    def help(self):
        #TODO: write help text
        return ""
        
    def handle(self, *args, **options):
        
        database = options['database']
        database = database or sketch.settings.MONGO_SERVER_DEFAULT_DB   
        
        collection = options['collection']
        if not collection:
            print "Collection must be specified with --collection"
            return

        #TODO: formatter           
        formatter = options['formatter']
        formatters = sketch.formattersmanager.formattersManager.getFormatters()
        if formatter and formatter not in formatters:
            print "Formatter %s is not available" % formatter
            return
        if formatter:
            formatter_callback = sketch.formattersmanager.formattersManager.getFormatter(formatter)
        else:
            formatter_callback = None
        
        
        query = options['query']
        if query:
            try:
                query_dict = json.loads(query, object_hook=bson.json_util.object_hook)
            except Exception, err:
                print "Invalid query:", str(err)
                return
        else:
            query_dict  = dict()
        
        try:
            limit = int(options['limit'])
        except:
            limit = None
        
        try:
            offset = int(options['offset'])        
        except:
            offset = 0
        
        #TODO: get objects    
        mongo = sketch.mongowrapper.MongoWrapper()
        
        out = sketch.helpers.createBaseResponseObject()
    
        try:
            mongo.connect()
        
            existing_dbs = mongo.connection.database_names()
            if database not in existing_dbs:
                raise Exception("Database %s does not exist" % database)
                
            database_object = mongo.getDb(database)
            existing_collections = database_object.collection_names()
            if collection not in existing_collections:
                raise Exception("Collection %s does not exist" % collection)
            
            
            query_result = mongo.objects(database, collection, query_dict=query_dict, offset=offset, limit=limit, 
                                         formatter_callback=formatter_callback)
             
            out.update(query_result)
        
        except Exception, e:
            out['errors'] = str(e)
            out['status'] = 0
        
        try:
            mongo.connection.close()
        except:
            pass
        
        
        print out
        
        
