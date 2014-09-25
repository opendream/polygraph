"""
Django settings for polygraph project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, sys

BASE_PATH = os.path.abspath(os.path.dirname('.'))
if 'collectstatic' in sys.argv:
    BASE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), os.path.pardir)


import djcelery
djcelery.setup_loader()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(@5-b#)pkqawvcyo@2rgqakv6*%c=z-j#2wh-k!b2v*v02s9l!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    # Core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Library
    'south',
    'ckeditor',
    'sorl.thumbnail',
    'files_widget',
    'autocomplete_light',
    'tagging',
    'tagging_autocomplete_tagit',
    'activelink',
    'bootstrap3',
    'django_tables2',
    'compressor',
    #'debug_toolbar',
    #'debug_toolbar_line_profiler',
    #'template_timings_panel',
    'djcelery',

    # Project
    'common',
    'account',
    'domain',
)

MIDDLEWARE_CLASSES = (
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'common.middleware.ForceDefaultLanguageMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'maintenancemode.middleware.MaintenanceModeMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'common.middleware.EvilMiddleware',
)


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',

    'common.context_processors.helper'
)

ROOT_URLCONF = 'polygraph.urls'

WSGI_APPLICATION = 'polygraph.wsgi.application'


TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_PATH, 'templates'),
    os.path.join(BASE_PATH, 'page'),
    os.path.join(BASE_PATH, 'files_widget/templates'),

)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'polygraph',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LOCALE_PATHS = (
    os.path.join(BASE_PATH, 'locale'),
)

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_PATH, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_PATH, 'sitestatic/')
STATIC_URL = '/static/'

PAGE_ROOT = os.path.join(BASE_PATH, 'page')

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(BASE_PATH, 'static'),
    os.path.join(BASE_PATH, 'files_widget/static'),
)

AUTH_USER_MODEL = 'account.Staff'

AUTHENTICATION_BACKENDS = (
    'account.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend'
)

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/account/login/'

SESSION_COOKIE_AGE = 60*60*24
#SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

CKEDITOR_UPLOAD_PATH = 'uploads/'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
            ['Format'],
            ['Bold', 'Italic', 'Underline', 'Strike'],
            ['NumberedList', 'BulletedList'],
            ['Link', 'Unlink'],
            ['Image', 'Table'],
            ['MediaEmbed']
        ],
        'width': 'auto',
        'height': '200',
        'format_tags': 'h3;h4;h5',
        'removePlugins': 'resize',
        'extraPlugins': 'autogrow,mediaembed',
        'forcePasteAsPlainText': True,
    },
    'minimal': {
        'toolbar': [
            ['Bold', 'Italic'],
            ['NumberedList', 'BulletedList'],
        ],
        'width': 'auto',
        'height': '200',
        'removePlugins': 'resize',
        'extraPlugins': 'autogrow',
        'forcePasteAsPlainText': True,
    },
    'bold': {
        'toolbar': [
            ['Bold'],
        ],
        'width': 'auto',
        'height': '80',
        'autoGrow_minHeight': '80',
        'removePlugins': 'resize',
        'extraPlugins': 'autogrow',
        'forcePasteAsPlainText': True,
    },
}

ALLOWED_HOSTS = ['*']
DEFAULT_FROM_EMAIL = 'Polygraph <no-reply@polygraph.dev>'

THUMBNAIL_DEBUG = False
FILES_WIDGET_JQUERY_PATH = 'libs/jquery/jquery.min.js'
FILES_WIDGET_JQUERY_UI_PATH = 'libs/jquery-ui/js/jquery-ui-1.10.4.min.js'
FILES_WIDGET_TEMP_DIR = 'temp/files_widget/'
#FILES_WIDGET_FILES_DIR = 'uploads/images/files_widget/'
#FILES_WIDGET_JQUERY_PATH = 'libs/jquery/jquery.min.js'
#FILES_WIDGET_JQUERY_UI_PATH = 'libs/jquery-ui/js/jquery-ui-1.10.4.min.js'

DEFAULT_IMAGE = '%simages/default.png' % STATIC_URL

try:
    #import cv2
    THUMBNAIL_ENGINE = 'solr_facerecognition.engines.FaceRecognitionEngine'
except ImportError:
    pass

THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.redis_kvstore.KVStore'

GREATEST_FUNCTION = 'GREATEST'

TAGGING_AUTOCOMPLETE_JQUERY_UI_FILE = 'libs/jquery-ui/js/jquery-ui-1.10.4.min.js'
TAGGING_AUTOCOMPLETE_MAX_TAGS = 9999

DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': '%slibs/jquery/jquery.min.js' % STATIC_URL
}

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar_line_profiler.panel.ProfilingPanel',
    'template_timings_panel.panels.TemplateTimings.TemplateTimings',
]
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': 'common.toolbar_stuff.custom_show_toolbar'
}

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

COMPRESS_ENABLED = True
#COMPRESS_OFFLINE = True

COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter'
]
COMPRESS_JS_FILTERS = [
    'compressor.filters.jsmin.JSMinFilter'
]


CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': '127.0.0.1:6379:1',
        'TIMEOUT': 7*24*60*60,
        'OPTIONS': {
            'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
        }
    }
}

# Celery settings
BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'


MAINTENANCE_MODE = False
MAINTENANCE_IGNORE_URLS = (
    r'^/account/.*',
    r'^/statement/.*/item/',
)

CARD_WIDTH = 680



# CUSTOM POLYGRAPH PROJECT #############################

UPTODATE_DAYS = 7
SITE_LOGO_URL = '%simages/logo.png' % STATIC_URL
SITE_NAME = 'Polygraph'
SITE_FAVICON_URL = '%simages/favicon.ico' % STATIC_URL
GOOGLE_ANALYTICS_KEY = ''
DISPLAY_STATEMENT_REVISIONS = True


# Override Settings ###########################################################
try:
    from settings_local import *
except ImportError:
    pass

# TESTING #####################################################################
if 'test' in sys.argv:
    DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
    MEDIA_ROOT = os.path.join(BASE_PATH, 'test_media')
    MEDIA_URL = '/test_media/'
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    GREATEST_FUNCTION = 'MAX'

if 'runserver' in sys.argv:
    DEBUG = True


# DEBUG MODE ##################################################################

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    COMPRESS_ENABLED = False

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

    GOOGLE_ANALYTICS_KEY = ''
