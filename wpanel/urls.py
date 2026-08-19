#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib import admin

from wpanel import views


admin.autodiscover()

urlpatterns = patterns('',
    
    #WASABOO CONTROL PANEL
    url(r'^wpanel/$', views.home, name='home'),
    url(r'^users/$', views.users, name='users'),
    url(r'^superusers/$', views.superusers, name='superusers'),
    url(r'^users_in_stealth/$', views.users_in_stealth, name='users_in_stealth'),
    url(r'^users_masculine/$', views.users_masculine, name='users_masculine'),
    url(r'^users_feminine/$', views.users_feminine, name='users_feminine'),
    url(r'^users_company/$', views.users_company, name='users_company'),
    url(r'^users_short_description/$', views.users_short_description, name='users_short_description'),    
    
    url(r'^cards/$', views.cards, name='cards'),
    url(r'^played_cards/$', views.played_cards, name='played_cards'),
    url(r'^removed_cards/$', views.removed_cards, name='removed_cards'),
    
    url(r'^users_favorites/$', views.users_favorites, name='users_favorites'),
    
    url(r'^users_followers/$', views.users_followers, name='users_followers'),
    
    url(r'^users_followed/$', views.users_followed, name='users_followed'),
    
    url(r'^users_decks/$', views.users_decks, name='users_decks'),
    
    url(r'^users_whoami/$', views.users_whoami, name='users_whoami'),
    url(r'^users_education/$', views.users_education, name='users_education'),
    url(r'^users_knows/$', views.users_knows, name='users_knows'),
    url(r'^users_jobs/$', views.users_jobs, name='users_jobs'),
    url(r'^users_company_about/$', views.users_company_about, name='users_company_about'),
    url(r'^users_location/$', views.users_location, name='users_location'),
)
