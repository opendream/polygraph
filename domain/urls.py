from django.conf.urls import url, patterns


urlpatterns = patterns('domain.views',
    url(r'^$', 'home', name='home'),


    url(r'^people/edit/(?P<people_id>\d+)/$', 'people_edit', name='people_edit'),
    url(r'^people/create/$', 'people_create', name='people_create'),

    url(r'^topic/edit/(?P<topic_id>\d+)/$', 'topic_edit', name='topic_edit'),
    url(r'^topic/create/$', 'topic_create', name='topic_create'),

    url(r'^statement/edit/(?P<statement_id>\d+)/$', 'statement_edit', name='statement_edit'),
    url(r'^statement/create/$', 'statement_create', name='statement_create'),
    url(r'^statement/list/$', 'statement_list', name='statement_list'),
    url(r'^statement/detail/(?P<statement_permalink>[A-Za-z0-9-_.]+)/$', 'statement_detail', name='statement_detail'),

    url(r'^(?P<inst_name>[A-Za-z0-9-_.]+)/delete/(?P<id>\d+)/$', 'domain_delete', name='domain_delete'),

)