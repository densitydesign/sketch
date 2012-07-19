from django.conf.urls import patterns, include, url

urlpatterns = patterns('sketch.views',
    # Examples:
    # url(r'^$', 'sketchproject.views.home', name='home'),
    # url(r'^sketchproject/', include('sketchproject.foo.urls')),
    
    url(r'query/(?P<collection>\w+)/(?P<command>\w+)/$', 'query'),
    url(r'query/(?P<database>\w+)/(?P<collection>\w+)/(?P<command>\w+)/$', 'query'),
    
    url(r'objects/(?P<collection>\w+)/$', 'objects'),
    url(r'objects/(?P<database>\w+)/(?P<collection>\w+)/$', 'objects'),
    
    url(r'import/(?P<collection>\w+)/$', 'importCall'),
    url(r'import/(?P<database>\w+)/(?P<collection>\w+)/$', 'importCall'),
    
    url(r'meta/server/$', 'serverMeta'),
    url(r'meta/parsers/$', 'parsersMeta'),
    url(r'meta/transforms/$', 'transformsMeta'),
    url(r'meta/processors/$', 'processorsMeta'),

    url(r'meta/db/(?P<database>\w+)/$', 'dbMeta'),
    
    url(r'ajaxlogin/$', 'ajaxLogin')

    
    
)
