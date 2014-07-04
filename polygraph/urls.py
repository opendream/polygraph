import os
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()


urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^files-widget/', include('files_widget.urls')),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^account/', include('account.urls')),
    url(r'^tagging_autocomplete_tagit/', include('tagging_autocomplete_tagit.urls')),
    url(r'^tagging_autocomplete_tagit/', include('tagging_autocomplete_tagit.urls')),
    url(r'^about/$', TemplateView.as_view(template_name='about.html')),
    url(r'^contact/$', TemplateView.as_view(template_name='contact.html')),

    url(r'', include('domain.urls', app_name='domain')),

)

# serve static pages
for page in os.listdir(settings.PAGE_ROOT):

    if '.html' in page:

        urlpatterns += patterns('',
            url(r'^%s/$' % page.replace('.html', ''), TemplateView.as_view(template_name=page)),
        )


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )