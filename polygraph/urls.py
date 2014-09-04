import os
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import HttpResponse
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

    url(r'', include('domain.urls', app_name='domain')),

)

# serve static pages
for page in os.listdir(settings.PAGE_ROOT):

    if '.html' in page:

        url_name = page.replace('.html', '')

        urlpatterns += patterns('',
            url(r'^%s/$' % url_name.replace('_', '-'), TemplateView.as_view(template_name=page), name=url_name),
        )


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
    )

    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )

else:
    urlpatterns += patterns('',
        url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt')),
    )
