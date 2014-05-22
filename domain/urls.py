from django.conf.urls import url, patterns


urlpatterns = patterns('domain.views',
    url(r'^$', 'domain_home', name='domain_home'),
    url(r'^statement/list/$', 'domain_statement_list', name='domain_statement_list'),
    url(r'^statement/detail/(?P<statement_permalink>[A-Za-z0-9-_.]+)/$', 'domain_statement_detail', name='domain_statement_detail'),

)