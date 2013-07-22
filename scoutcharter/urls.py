from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'advancement.views.index', name='index'),
    url(r'^home/?$', 'advancement.views.home', name='home'),
    url(r'^home/scout/(?P<scouter_id>\d+)/?$', 'advancement.views.home', name='home'),
    url(r'^login/?$', 'django.contrib.auth.views.login', name='my_login'),
    url(r'^logout/?$', 'django.contrib.auth.views.logout', name='my_logout'),
    url(r'^meritbadges/?$', 'advancement.views.meritbadges', name='meritbadges'),
    url(r'^update-scoutmeritbadge/?$', 'advancement.views.update_scoutmeritbadge', name='update_scoutmeritbadge'),

    # url(r'^giftplanner/', include('giftplanner.urls')),
    # Examples:
    # url(r'^$', 'giftaway.views.home', name='home'),
    # url(r'^giftaway/', include('giftaway.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/?', include(admin.site.urls)),
)
