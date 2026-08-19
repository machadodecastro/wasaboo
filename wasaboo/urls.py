#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from wasaboo import settings

from wasaboo import views as project_views


admin.autodiscover()

urlpatterns = patterns('',
    
    #About Wasaboo
    url(r'^about/$', 'wasaboo.views.about', name='about'),
    url(r'^policy/$', 'wasaboo.views.politics', name='politics'),
    url(r'^contact/thankyou/$', 'wasaboo.views.thankyou', name='thankyou'),
    url(r'^contact/$', 'wasaboo.views.contact', name='contact'),
	url(r'^sitemap/$', 'wasaboo.views.sitemap', name='sitemap'),

    
    #Apps
    url(r'^', include('perfis.urls')),
    url(r'^', include('_usuarios.urls')),
    url(r'^', include('haystack.urls')),
    url(r'^', include('wpanel.urls')),        
)


handler404 = project_views.error_404
handler500 = project_views.error_500  
    
if not settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}),

        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT})                            
    )