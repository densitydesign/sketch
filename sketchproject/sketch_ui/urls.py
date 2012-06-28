from django.conf.urls import patterns, include, url

urlpatterns = patterns('sketch_ui.views',

    # Examples:
    # url(r'^$', 'sketchproject.views.home', name='home'),
    # url(r'^sketchproject/', include('sketchproject.foo.urls')),
        
    url(r'/$', 'index'),
    
)
