from django.conf.urls import url, patterns


urlpatterns = patterns('domain.views',
    url(r'^$', 'home', name='home'),
    url(r'^statement/list/$', 'statement_list', name='statement_list'),
    url(r'^statement/detail/(?P<statement_permalink>[A-Za-z0-9-_.]+)/$', 'statement_detail', name='statement_detail'),

    url(r'^people/edit/(?P<people_id>\d+)/$', 'people_edit', name='people_edit'),

)