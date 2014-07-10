from django.conf import settings
from django.conf.urls import patterns, url


urlpatterns = patterns('account.views',
    #url(r'^register/$', 'account_register', name='account_register'),
    url(r'^$', 'account', name='account'),
    url(r'^login/$', 'account_login', name='account_login'),

    url(r'^edit/$', 'account_edit', name='account_edit'),
    url(r'^password_reset/$', 'account_reset_password', name='account_reset_password'),
    url(r'^password_reset/done/$', 'account_reset_password_done', name='account_reset_password_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'account_reset_password_confirm', name='account_reset_password_confirm'),

    url(r'^invitation/$', 'account_invite', name='account_invite'),
    #url(r'^invitation/(?P<invitation_key>\w+)/$', 'claim_user_invitation', name='claim_user_invitation'),
)

urlpatterns += patterns('',
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': settings.LOGIN_URL}, name='account_logout'),

)