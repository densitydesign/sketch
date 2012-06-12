from django.conf.urls import patterns, include, url

urlpatterns = patterns('sketch.views',
    # Examples:
    # url(r'^$', 'sketchproject.views.home', name='home'),
    # url(r'^sketchproject/', include('sketchproject.foo.urls')),
    
    url(r'api/(?P<database>\w+)/(?P<collection>\w+)/(?P<query>\w+)/$', 'api_call'),
    
    
)
