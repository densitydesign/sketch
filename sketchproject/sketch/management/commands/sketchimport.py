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
import sketch.recordparser
import django.contrib.auth.models as authmodels
import json



#TODO: replace all print statements with self.stdout.write('...')
#TODO: consider throwing exception vs return
#TODO: json output

class Command(BaseCommand):
    
    option_list = BaseCommand.option_list + (
        make_option('--database', action='store', dest='database', default='',
        help='Selects database'),

        make_option('--collection', action='store', dest='collection', default='',
        help='Selects collection'),

        make_option('--format', action='store', dest='format', default='',
        help='Selects format'),
        
        make_option('--mapper', action='store', dest='mapper', default='',
        help='Selects mapper'),
        
        make_option('--datafile', action='store', dest='datafile', default='',
        help='Selects datafile'),
        
        make_option('--commit', action='store_true', dest='commit', default=False,
        help='Enables commit'),
        
    )

    args = ''
    command_name = 'sketchimport'
    
    @property
    def help(self):
        out = """Management command to import data into sketch instance. \n\n
        Plase note: authentication is not handled right now"""
        return out
        
    def handle(self, *args, **options):
        
        datafile = options['datafile']
        if not datafile:
            print "no datafile!"
            return
            
        try:
            fl = open(datafile)
            data = fl.read()
            fl.close()
        
        except Exception, err:
            print "Invalid data file: ", str(err)    
            return
            
        database = options['database']
        database = database or sketch.settings.MONGO_SERVER_DEFAULT_DB   
        
        collection = options['collection']
        if not collection:
            print "Collection must be specified with --collection"
            return
            
        parser_class = options['format']
        if not parser_class:
            print "Format must be specified with --format"
            return
        if parser_class not in sketch.recordparser.ALLOWED_PARSERS.keys():
            print "Unrecognized import format: --format must be one of:\n" + "\n".join(sketch.recordparser.ALLOWED_PARSERS.keys())
            return

        #TODO: mapper name
        mapper = options['mapper']
        
        commit = options['commit']

        
        ####
        out = sketch.helpers.createBaseResponseObject()
        
        out['error_records'] = { 'parser' : [], 'mapper' : [] }
        out['ok_records_number'] = 0
        
        mongo = sketch.mongowrapper.MongoWrapper()
        try:
            mongo.connect()
        except Exception, err:
            print "Mongo connection error", str(err)
            return
        
        
        mapperName = mapper
        #todo: decide to use name or id for referencing mapper in request
        if mapperName:
            if mapperName in sketch.mappermanager.codedMappers:
                mapperObject = sketch.mappermanager.codedMappers[mapperName]
                
            else:
                sketchMapper = sketch.models.SketchMapper.objects.get(name=mapperName)
                mapperObject = sketchMapper.mapper
            

        record_errors_number = 0
        ok_records = []
        MAX_ERROR_RECORDS = sketch.settings.MAX_ERROR_RECORDS
        
        
        #TODO: refactor this try ... except section.
        #IT is repeated in views, provide a more  abstract version
            
        try:
            #parsing phase
            parser = sketch.recordparser.parserFactory(parser_class, data)
            for d in parser.objects():
                if d is sketch.recordparser.ParserError:
                    out['error_records']['parser'].append(str(d.exception_message) + ":" +d.raw_data)
                    continue
                
                #mapping phase
                if mapper:
                    try:
                        newRecord = sketch.mappermanager.mappingManager.mapRecord(d, mapperObject,  { '__mapper_name__' : mapperName })
                        ok_records.append(newRecord)
                
                    except Exception, err:
                        out['error_records']['mapper'].append(str(err))
    
                #mapper is none, record is imported as it is
                else:
                    ok_records.append(d)
                
                if len(out['error_records']['mapper']) + len(out['error_records']['parser']) > MAX_ERROR_RECORDS:
                    break
                    
    
            #commit phase
            if commit:
                #creating the collection model and set owner=user if collection does not exits
                #TODO: we could check again the number of allowed collections here, as in decorator
                try:
                    collectionInstance = sketch.models.SketchCollection.objects.get(name=collection)
                except:
                    user = authmodels.User.objects.get(pk=1)
                    collectionInstance = sketch.models.SketchCollection(owner=user, name=collection)
                    collectionInstance.save()
    
                #finally inserting records
                for record in ok_records:
                    mongo_id = mongo._insert(database, collection, record)
                    out['results'].append(mongo_id)
                    
        except Exception, e:
            out['errors'] = str(e)
            out['status'] = 0
             
        out['ok_records_number'] = len(ok_records)
            
        try:
            mongo.connection.close()
        except:
            pass
            
        print out
        
        
        
        
        
        
        
        
        
    
