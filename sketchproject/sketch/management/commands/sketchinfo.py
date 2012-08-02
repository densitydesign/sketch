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
    
    )
    
    args = 'server|db|parsers|formatters|mappers|transforms|processors'

    command_name = 'sketchinfo'
    
    @property
    def help(self):
        lines = ['Sketch command line interface.', '', 'Available commands:']
        return '\n'.join(lines)
        
    #todo: decide what to output exactly, the implementation is not consistent         
    def handle(self, *args, **options):
    
        if 'server' in args:
            data = sketch.views.getServerInfo()
            print data

        if 'db' in args:
            database = options['database']
            database = database or sketch.settings.MONGO_SERVER_DEFAULT_DB
            data = sketch.views.getDbInfo(database)
            print data
            
        if 'parsers' in args:
            data = sketch.recordparser.ALLOWED_PARSERS.keys()
            print data
            
        if 'transforms' in args:
            data = sketch.mappermanager.mappingManager.getTransforms()
            print data
            
        if 'processors' in args:
            data = sketch.processingmanager.processingManager.getProcessors()
            print data
            
            
        if 'mappers' in args:
            objs = sketch.models.SketchMapper.objects.all()
            data = []
            for o in objs:
                data.append(sketch.helpers.instanceDict(o))
            print data
            
    
