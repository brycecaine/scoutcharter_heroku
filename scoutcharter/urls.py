from django.conf.urls import patterns, include, url
from advancement.api import ScoutResource

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

scout_resource = ScoutResource()

urlpatterns = patterns('',
    url(r'^$', 'advancement.views.home', name='home'),
    # url(r'^giftplanner/', include('giftplanner.urls')),
    # Examples:
    # url(r'^$', 'giftaway.views.home', name='home'),
    # url(r'^giftaway/', include('giftaway.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^api/', include(scout_resource.urls)),
)
