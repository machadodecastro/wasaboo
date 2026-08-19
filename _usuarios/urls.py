# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from django.contrib import admin

from _usuarios import admin, views
from views import RegistrarUsuarioView


urlpatterns = patterns('',
    url(r'^register/$', RegistrarUsuarioView.as_view(), name="registrar"),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
                       
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name':'login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', {'login_url':'/login/'}, name='logout'),
    
    
    url(r'^recover/(?P<signature>.+)/$', views.recover_done,name='password_reset_sent'),
    url(r'^recover/$', views.recover, name='password_reset_recover'),
    url(r'^reset/done/$', views.reset_done, name='password_reset_done'),
    url(r'^reset/(?P<token>[\w:-]+)/$', views.reset, name='password_reset_reset'),
)








