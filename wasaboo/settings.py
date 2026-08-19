#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Django settings for wasaboo project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
#import smtplib
#from MySQLdb.constants.CLIENT import COMPRESS

'''ADMINS = (
    ('Igor Machado de Castro', 'IGORMCASTRO@GMAIL.COM'),
)

MANAGERS = ADMINS
'''

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Running locally so connect to either a local MySQL instance or connect to
# Cloud SQL via the proxy. To start the proxy via command line:
#
#     $ cloud_sql_proxy -instances=[INSTANCE_CONNECTION_NAME]=tcp:3306
#
# See https://cloud.google.com/sql/docs/mysql-connect-proxy
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '',
        'PORT': '3306',
        'NAME': 'wsbodb',
        'USER': 'root',
        'PASSWORD': 'root',
    }
}
    


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'h85!wxz@y)ki2ao(ce!+5eef#1_%s9th8i_tg-j8+5jb#ui!+%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']
#ALLOWED_HOSTS = ['www.wasaboo.com']

SITE_ID = 1

FILE_CHARSET='iso-8859-1'

AUTH_USER_MODEL = '_usuarios.User'

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'perfis',
    '_usuarios',
    'haystack',
    'opengraph',
    'wpanel',
)



TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates').replace('\\', '/'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.csrf',
    'django.core.context_processors.request',
    'perfis.context_processors.settings'
)


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"

#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
#STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATIC_URL = '/static/'

STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware', #Alterar o idioma
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.csrf.CsrfResponseMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'wasaboo.urls'

WSGI_APPLICATION = 'wasaboo.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True




# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
#BASE_DIR = 'C:/workspace/wasaboo/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
#MEDIA_ROOT = 'C:/workspace/sig/media/' 

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'


LOGIN_URL="/login/"
LOGOUT_URL="/logout/"
LOGIN_REDIRECT_URL="/feed/"


HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr',
        'TIMEOUT': 60 * 5,
        'INCLUDE_SPELLING':True,
        'INDEX_NAME': 'haystack'
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'


#Reset password from localhost - ok
#Command: python -m smtpd -n -c DebuggingServer localhost:2525

EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 2525
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'Wasaboo <contact@wasaboo.com>'
'''

#Reset from Gmail

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'contact@wasaboo.com'
EMAIL_HOST_PASSWORD = 'gcgnlqlvdzlljdbu'
DEFAULT_FROM_EMAIL = 'Wasaboo <contact@wasaboo.com>'
'''

# Reset from SMTP Server - ok
'''
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'correio.fiocruz.br'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'igor.machado@fiocruz.br'
EMAIL_HOST_PASSWORD = 'M0nk3ys@fiocruz'
DEFAULT_FROM_EMAIL = 'Wasaboo <igor.machado@fiocruz.br>'
'''

#Google Captcha
NORECAPTCHA_SITE_KEY = '6LcaiTkUAAAAAIHSA6rhyYVOEPp-EbY3cCzaoBot'
NORECAPTCHA_SECRET_KEY = '6LcaiTkUAAAAAKsjDH8F69_Kl3JyxZpHzmOC-nVS'

#Facebook sharing
OPENGRAPH_CONFIG = {
    'DEFAULT_IMAGE': '/static/img/wasaboo_logo.png',
    'SITE_NAME': 'Wasaboo',
}



LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}
