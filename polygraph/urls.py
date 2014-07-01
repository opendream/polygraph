from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'polygraph.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^files-widget/', include('files_widget.urls')),
    url(r'autocomplete/', include('autocomplete_light.urls')),
    url(r'^account/', include('account.urls')),
    url(r'^tagging_autocomplete_tagit/', include('tagging_autocomplete_tagit.urls')),
    url(r'', include('domain.urls', app_name='domain')),


)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )