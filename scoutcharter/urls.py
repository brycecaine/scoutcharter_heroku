from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'advancement.views.index', name='index'),
    url(r'^home/?$', 'advancement.views.home', name='home'),
    url(r'^home/scout/(?P<scouter_id>\d+)/?$', 'advancement.views.home', name='home'),
    url(r'^signup/?$', 'advancement.views.signup', name='signup'),
    url(r'^login/?$', 'django.contrib.auth.views.login', name='my_login'),
    url(r'^logout/?$', 'django.contrib.auth.views.logout', name='my_logout'),
    url(r'^scouter/edit/?$', 'advancement.views.edit_scouter', name='edit_scouter'),
    url(r'^scouter/edit/(?P<username>\w+)/?$', 'advancement.views.edit_scouter', name='edit_scouter'),
    url(r'^meritbadges/?$', 'advancement.views.meritbadges', name='meritbadges'),
    url(r'^ranks/?$', 'advancement.views.ranks', name='ranks'),
    url(r'^update-scoutmeritbadge/?$', 'advancement.views.update_scoutmeritbadge', name='update_scoutmeritbadge'),
    url(r'^update-scoutrank/?$', 'advancement.views.update_scoutrank', name='update_scoutrank'),

    url(r'^rank-requirements/?$', 'advancement.views.rank_requirements', name='rank_requirements'),
    url(r'^rank-requirements/(?P<scoutrank_id>\d+)/?$', 'advancement.views.rank_requirements', name='rank_requirements'),
    
    url(r'^request-mbbook/?$', 'advancement.views.request_mbbook', name='request_mbbook'),
    url(r'^view-mbcounselors/(?P<meritbadge_id>\d+)/?$', 'advancement.views.view_mbcounselors', name='view_mbcounselors'),

    url(r'^export/?$', 'advancement.views.export', name='export'),
    url(r'^report/scout/list/?$', 'advancement.views.report_list', name='report_list'),
    url(r'^report/scout/all-detail/?$', 'advancement.views.report_scout', name='report_scout'),
    url(r'^report/scout/(?P<scouter_id>\d+)/?$', 'advancement.views.report_scout', name='report_scout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/?', include(admin.site.urls)),
)

handler404 = 'advancement.views.custom_404'
handler500 = 'advancement.views.custom_500'
