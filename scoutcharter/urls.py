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
    url(r'^ranks/?$', 'advancement.views.ranks', name='ranks'),
    url(r'^update-scoutmeritbadge/?$', 'advancement.views.update_scoutmeritbadge', name='update_scoutmeritbadge'),
    url(r'^update-scoutrank/?$', 'advancement.views.update_scoutrank', name='update_scoutrank'),

    url(r'^request-mbbook/?$', 'advancement.views.request_mbbook', name='request_mbbook'),
    url(r'^view-mbcounselors/(?P<meritbadge_id>\d+)/?$', 'advancement.views.view_mbcounselors', name='view_mbcounselors'),

    url(r'^export/(?P<start_date>\w+)/(?P<end_date>\w+)/?$', 'advancement.views.export', name='export'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/?', include(admin.site.urls)),
)
