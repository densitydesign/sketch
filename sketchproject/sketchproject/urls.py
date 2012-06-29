from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sketchproject.views.home', name='home'),
    # url(r'^sketchproject/', include('sketchproject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'sketch_ui/login.html'}, name="login"),
    url (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page' : '/login/'}, name="logout"),

    url(r'^sketch/', include('sketch.urls')),
    url(r'^', include('sketch_ui.urls')),
    
)


if settings.DEBUG:
    urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'', include('django.contrib.staticfiles.urls')),
) + urlpatterns

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
