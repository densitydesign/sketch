from django.conf.urls import patterns, include, url

urlpatterns = patterns('sketch.views',
    # Examples:
    # url(r'^$', 'sketchproject.views.home', name='home'),
    # url(r'^sketchproject/', include('sketchproject.foo.urls')),
    
    url(r'query/(?P<collection>\w+)/(?P<command>\w+)/$', 'api_call'),
    url(r'query/(?P<database>\w+)/(?P<collection>\w+)/(?P<command>\w+)/$', 'api_call'),
    
    
    url(r'import/(?P<collection>\w+)/$', 'mapper_call'),
    url(r'import/(?P<database>\w+)/(?P<collection>\w+)/$', 'mapper_call'),

    
    
)
