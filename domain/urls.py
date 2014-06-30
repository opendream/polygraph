from django.conf.urls import url, patterns

urlpatterns = patterns('domain.views',
    url(r'^$', 'home', name='home'),

    url(r'^people/create/$', 'people_create', name='people_create'),
    url(r'^people/(?P<people_id>\d+)/edit/$', 'people_edit', name='people_edit'),
    url(r'^people/(?P<people_permalink>[A-Za-z0-9-_.]+)/$', 'people_detail', name='people_detail'),

    url(r'^topic/create/$', 'topic_create', name='topic_create'),
    url(r'^topic/(?P<topic_id>\d+)/edit/$', 'topic_edit', name='topic_edit'),
    url(r'^topic/(?P<topic_id>\d+)/$', 'topic_detail', name='topic_detail'),

    url(r'^tags/(?P<tags_id>\d+)/$', 'tags_detail', name='tags_detail'),
    url(r'^meter/(?P<statement_permalink>[A-Za-z0-9-_.]+)/$', 'meter_detail', name='meter_detail'),

    url(r'^statement/create/$', 'statement_create', name='statement_create'),
    url(r'^statement/(?P<statement_id>\d+)/edit/$', 'statement_edit', name='statement_edit'),
    url(r'^statement/(?P<statement_permalink>[A-Za-z0-9-_.]+)/$', 'statement_detail', name='statement_detail'),
    url(r'^statement/$', 'statement_list', name='statement_list'),

    url(r'^(?P<inst_name>[A-Za-z0-9-_.]+)/delete/(?P<id>\d+)/$', 'domain_delete', name='domain_delete'),

)
