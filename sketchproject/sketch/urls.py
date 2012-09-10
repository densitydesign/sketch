from django.conf.urls import patterns, include, url

urlpatterns = patterns('sketch.views',
    # Examples:
    # url(r'^$', 'sketchproject.views.home', name='home'),
    # url(r'^sketchproject/', include('sketchproject.foo.urls')),
    
    url(r'query/(?P<collection>\w+)/(?P<command>\w+)/$', 'query'),
    url(r'query/(?P<database>\w+)/(?P<collection>\w+)/(?P<command>\w+)/$', 'query'),
    
    url(r'objects/(?P<collection>\w+)/$', 'objects'),
    url(r'objects/(?P<database>\w+)/(?P<collection>\w+)/$', 'objects'),
    
    #todo: probably this should be handled as a "POST" request to objects
    url(r'import/(?P<collection>\w+)/$', 'importCall'),
    url(r'import/(?P<database>\w+)/(?P<collection>\w+)/$', 'importCall'),
    
    # introspection views
    # These view describe the state of a particular sketch instance,
    # showing available resources in terms of databases, collections, parsers, mappers,
    # transforms, processors
    url(r'server/$', 'server'),
    url(r'db/(?P<database>\w+)/$', 'db'),
    url(r'parsers/$', 'parsers'),
    url(r'mappers/$', 'mappers'), 
    url(r'transforms/$', 'transforms'),
    url(r'processors/$', 'processors'), 
    url(r'formatters/$', 'formatters'), 

    #ajax login view.
    url(r'ajaxlogin/$', 'ajaxLogin'),
    
    #single object views
    url(r'object/(?P<collection>\w+)/(?P<oid>\w+)/$', 'object'),
    url(r'object/(?P<database>\w+)/(?P<collection>\w+)/(?P<oid>\w+)/$', 'object'),
    
)
