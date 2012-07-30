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
    
    url(r'server/$', 'server'),
    url(r'parsers/$', 'parsersì'),
    url(r'transforms/$', 'transforms'),
    url(r'processors/$', 'processors'),

    url(r'db/(?P<database>\w+)/$', 'db'),
    
    url(r'ajaxlogin/$', 'ajaxLogin')

    
    
)
