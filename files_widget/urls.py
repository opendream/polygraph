try:
    from django.conf.urls.defaults import patterns, url
except:
    from django.conf.urls import patterns, url

from django.conf import settings

urlpatterns = patterns("files_widget.views",
    url(u'^upload/$', "upload", name="files_widget_upload"),
    url(u'^thumbnail-url/$', "thumbnail_url", name="files_widget_get_thumbnail_url"),
)
