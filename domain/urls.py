from django.conf.urls import url, patterns


urlpatterns = patterns('domain.views',
    url(r'^$', 'domain_home', name='domain_home'),
)