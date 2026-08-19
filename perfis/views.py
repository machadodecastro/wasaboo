from Tkconstants import LAST
from _codecs import decode, encode
import array
from audioop import reverse
from calendar import calendar
import copy
from datetime import date
from dircache import listdir
from genericpath import isfile
import hashlib
import hmac
from itertools import groupby
import json
import json
from mimetypes import MimeTypes
import os
from pickle import GET
import re
from symbol import decorator
import sys
import urlparse

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.core.validators import slug_re
from django.db import connection, transaction
from django.db.models.aggregates import Count
from django.db.models.base import get_absolute_url
from django.db.models.query_utils import Q
from django.forms.fields import SlugField
from django.http import HttpResponse
from django.http import HttpResponse
from django.http.response import HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.shortcuts import render
from django.template.context import RequestContext
from django.template.defaultfilters import last, join
from django.template.loader import render_to_string
from django.utils.html import linebreaks, strip_tags
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.views.generic.edit import UpdateView
from elasticsearch_dsl.field import Integer
from haystack.backends import SQ
from haystack.forms import ModelSearchForm
from haystack.inputs import AutoQuery
from haystack.query import SearchQuerySet
from kivy import args
from requests.api import get
import wand

import _usuarios
from _usuarios.urls import urlpatterns
from froala_editor import DjangoAdapter
from froala_editor import Image
from froala_editor.adapters import BaseAdapter
from froala_editor.file import File
from froala_editor.s3 import S3
import perfis
from perfis.forms import TipForm, PerfilForm, AvatarForm, WhoamiForm, \
    EducationForm, KnowsForm, JobsForm, LiveForm, HobbyForm, CompanyForm, \
    OfferForm, LocationForm, DeckForm, BackgroundForm
from perfis.models import Perfil, Convite, Tip, Favorites, Avatar, Folder, Deck, \
    Company, Location, Whoami, Education, Knows, Jobs, Background, Mensagem


#from django.core.files.base import File
#from froala_editor import File
@csrf_exempt
def public(request):
    '''results = Tip.objects.raw("""SELECT t.id, p.nome as name, t.content, 
                                    t.author_profile_id as author, t.type as type,
                                    p.usuario_id as profile_id, t.author_name as name,
                                    t.date, ifnull(f.id,0) as isfollowing, 
                                    f.followed_id, ifnull(a.upload,0) as upload, t.outdoor
                                    FROM wsbodb.perfis_perfil p, wsbodb.perfis_follow f,
                                    wsbodb.perfis_avatar a,
                                    wsbodb.perfis_tip t
                                    WHERE t.hided = 0
                                    AND t.author_profile_id = a.profile_id
                                    GROUP BY t.id
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""")
    return render(request, "home.html", locals())'''
    return render(request, "home.html")

@csrf_exempt
def how_it_works(request):
    return render(request, "how_it_works.html")

@login_required
def index(request):
    perfil = Perfil.objects.get(id=request.user.perfil.id)
    
    url2 = request.build_absolute_uri()
    url = url2.split('//')[-1].split('/')[0]
                      
    tips = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date, c.to_perfil_id as destiny, 
                            c.from_perfil_id as origin, p.usuario_id as profile_id, p.type as type, ifnull(f.id,0) as isfav
                            FROM wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites f ON (t.id = f.tip_id AND f.profile_id = %s), 
                            wsbodb.perfis_perfil_contatos c, wsbodb.perfis_perfil p
                            WHERE c.from_perfil_id = t.author_profile_id
                            AND c.to_perfil_id = p.id
                            AND p.usuario_id = %s
                            ORDER BY t.date DESC;""", [request.user.id, request.user.id])

                                    
    following = Tip.objects.raw("""SELECT t.id, p.nome as name, t.content, 
                                    t.author_profile_id as author, p.type as type,
                                    p.usuario_id as profile_id, t.author_name as name,
                                    t.date, ifnull(f.id,0) as isfollowing, ifnull(fav.id,0) as isfav,
                                    (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                    (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed,
                                    (t.author_profile_id IN (SELECT p.id FROM wsbodb.perfis_perfil p WHERE p.stealth=1 AND t.author_profile_id=%s)) as stealthed,
                                    (t.id IN (SELECT n.referenced_card FROM wsbodb.perfis_notifications n WHERE n.card_id NOT IN (SELECT re.card_id FROM wsbodb.perfis_removed re WHERE re.profile_id=%s) AND t.author_profile_id=%s)) as notified,
                                    (t.id IN (SELECT p.referenced_card FROM wsbodb.perfis_played_cards p WHERE p.played=1)) as waiting_hold,
                                    f.followed_id, ifnull(a.upload,0) as upload, t.outdoor
                                    FROM wsbodb.perfis_perfil p, wsbodb.perfis_follow f,
                                    wsbodb.perfis_avatar a, 
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                    ON (t.id = fav.tip_id AND fav.profile_id = %s) 
                                    WHERE t.author_profile_id = p.id
                                    AND t.author_profile_id = f.followed_id
                                    AND f.follower_id = %s 
                                    AND t.hided = 0
                                    AND t.world = 0
                                    AND f.followed_id = a.profile_id
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""", 
                                    [request.user.perfil.id, request.user.id, request.user.perfil.id, request.user.id, request.user.perfil.id, request.user.id, request.user.id])


    following_worlds = Tip.objects.raw("""SELECT t.id, p.nome as name, t.content,
                                    t.author_profile_id as author, p.type as type,
                                    p.usuario_id as profile_id, t.author_name as name,
                                    t.date, ifnull(f.id,0) as isfollowing, ifnull(fav.id,0) as isfav,
                                    (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                    (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed,
                                    (t.author_profile_id IN (SELECT p.id FROM wsbodb.perfis_perfil p WHERE p.stealth=1 AND t.author_profile_id=%s)) as stealthed,
                                    (t.id IN (SELECT n.referenced_card FROM wsbodb.perfis_notifications n WHERE n.card_id NOT IN (SELECT re.card_id FROM wsbodb.perfis_removed re WHERE re.profile_id=%s) AND t.author_profile_id=%s)) as notified,
                                    (t.id IN (SELECT p.referenced_card FROM wsbodb.perfis_played_cards p WHERE p.played=1)) as waiting_hold,
                                    f.followed_id, ifnull(a.upload,0) as upload, t.outdoor
                                    FROM wsbodb.perfis_perfil p, wsbodb.perfis_follow f,
                                    wsbodb.perfis_avatar a, 
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                    ON (t.id = fav.tip_id AND fav.profile_id = %s) 
                                    WHERE t.author_profile_id = p.id
                                    AND t.author_profile_id = f.followed_id
                                    AND f.follower_id = %s 
                                    AND t.hided = 0
                                    AND t.world <> 0
                                    AND f.followed_id = a.profile_id
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""", 
                                    [request.user.perfil.id, request.user.id, request.user.perfil.id, request.user.id, request.user.perfil.id, request.user.id, request.user.id])

    
    maps = Tip.objects.raw("""SELECT t.id, p.nome as name, t.content, 
                                    t.author_profile_id as author, p.type as type,
                                    p.usuario_id as profile_id, t.author_name as name,
                                    ifnull(a.upload,0) as upload, t.outdoor
                                    FROM wsbodb.perfis_perfil p,
                                    wsbodb.perfis_avatar a, 
                                    wsbodb.perfis_tip t 
                                    WHERE t.author_profile_id = p.id
                                    AND t.author_profile_id = a.profile_id
                                    AND t.hided = 0
                                    AND t.world = 1
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""")
    
    fys = Tip.objects.raw("""SELECT t.id, p.nome as name, t.content, 
                                    t.author_profile_id as author, p.type as type,
                                    p.usuario_id as profile_id, t.author_name as name,
                                    ifnull(a.upload,0) as upload, t.outdoor,
                                    ifnull(fav.id,0) as isfav,
                                    (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed
                                    FROM wsbodb.perfis_perfil p,
                                    wsbodb.perfis_avatar a, 
                                    wsbodb.perfis_tip t,
                                    wsbodb.perfis_favorites fav 
                                    WHERE t.author_profile_id = p.id
                                    AND t.author_profile_id = a.profile_id
                                    AND fav.profile_id = %s
                                    AND t.hided = 0
                                    AND t.world = 2
                                    GROUP BY t.id
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""", [request.user.id, request.user.id])
    
    nike = Tip.objects.raw("""SELECT t.id, p.nome as name, t.content, 
                                    t.author_profile_id as author, p.type as type,
                                    p.usuario_id as profile_id, t.author_name as name,
                                    ifnull(a.upload,0) as upload, t.outdoor,
                                    ifnull(fav.id,0) as isfav,
                                    (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed
                                    FROM wsbodb.perfis_perfil p,
                                    wsbodb.perfis_avatar a, 
                                    wsbodb.perfis_tip t,
                                    wsbodb.perfis_favorites fav 
                                    WHERE t.author_profile_id = p.id
                                    AND t.author_profile_id = a.profile_id
                                    AND t.hided = 0
                                    AND t.world = 3
                                    GROUP BY t.id
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""", [request.user.id])

                                                          
    is_contact = Tip.objects.raw("""SELECT t.id, f.followed_id as fid, p.nome as name, t.content, 
                                    t.author_profile_id as author, p.type as type,
                                    p.usuario_id as profile_id, t.author_name as name,
                                    t.date, ifnull(f.id,0) as isfollowing, ifnull(fav.id,0) as isfav, 
                                    f.followed_id
                                    FROM wsbodb.perfis_perfil p, wsbodb.perfis_follow f, 
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                    ON (t.id = fav.tip_id AND fav.profile_id = %s) 
                                    WHERE p.usuario_id = %s
                                    AND t.author_profile_id = f.followed_id 
                                    AND f.follower_id = %s 
                                    GROUP BY f.followed_id
                                    ORDER BY t.author_name ASC;""", [request.user.id, request.user.id, request.user.id])

    
    my_profile_image = Tip.objects.raw("""SELECT a.id, a.upload as upload, a.user_id
                                        FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                        ON(a.user_id = p.usuario_id)
                                        WHERE p.usuario_id = %s;""", [request.user.id]) 
    
    
    return render(request, 'index.html', {'perfil':perfil, 'perfis':Perfil.objects.all(), 
                                          'perfil_logado': get_perfil_logado(request), 'tips': tips,
                                          'url':url, 'following':following, 
                                          'following_worlds':following_worlds, 
                                          'maps':maps, 
                                          'fys':fys,
                                          'nike':nike,
                                          'is_contact':is_contact, 'my_profile_image': my_profile_image })

    
@login_required
def exibir(request, perfil_id):    
    url2 = request.build_absolute_uri()
    url = url2.split('//')[-1].split('/')[0]

    perfil = Perfil.objects.get(id=perfil_id)
    perfil_logado = get_perfil_logado(request)
    ja_eh_contato = perfil in perfil_logado.contatos.all()
    
    if perfil_logado.map == '0':
        following = Tip.objects.raw("""SELECT t.id, p.nome as name, t.content, t.outdoor,
                                    t.author_profile_id as author, p.type as type,
                                    p.usuario_id as profile_id, t.author_name as name, 
                                    t.date, ifnull(f.id,0) as isfollowing, ifnull(fav.id,0) as isfav,                                     
                                    f.followed_id,
                                    (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                    (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed,
                                    (t.author_profile_id IN (SELECT j.jobs_profile_id FROM wsbodb.perfis_jobs j WHERE j.status_work=1)) as work
                                    FROM wsbodb.perfis_perfil p, wsbodb.perfis_follow f, 
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                    ON (t.id = fav.tip_id AND fav.profile_id = %s) 
                                    WHERE p.usuario_id = %s
                                    AND t.author_profile_id = %s 
                                    AND t.hided = 0
                                    AND t.world = 0
                                    GROUP BY t.id
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""", 
                                    [request.user.perfil.id, request.user.id, request.user.id, request.user.id, perfil.id])
    else:
        following = Tip.objects.raw("""SELECT t.id, p.nome as name, t.content, t.outdoor,
                                    t.author_profile_id as author, p.type as type,
                                    p.usuario_id as profile_id, t.author_name as name, 
                                    t.date, ifnull(f.id,0) as isfollowing, ifnull(fav.id,0) as isfav,                                     
                                    f.followed_id,
                                    (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                    (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed,
                                    (t.author_profile_id IN (SELECT j.jobs_profile_id FROM wsbodb.perfis_jobs j WHERE j.status_work=1)) as work
                                    FROM wsbodb.perfis_perfil p, wsbodb.perfis_follow f, 
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                    ON (t.id = fav.tip_id AND fav.profile_id = %s) 
                                    WHERE p.usuario_id = %s
                                    AND t.author_profile_id = %s 
                                    AND t.hided = 0
                                    AND t.world <> 0
                                    GROUP BY t.id
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""", 
                                    [request.user.perfil.id, request.user.id, request.user.id, request.user.id, perfil.id])
        
    if perfil_logado.map == '0':
        profiletips = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date, p.usuario_id as profile_id, 
                                t.author_user_id as author_user, t.author_name as name,
                                (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                (t.id IN (SELECT n.referenced_card FROM wsbodb.perfis_notifications n WHERE n.card_id NOT IN (SELECT re.card_id FROM wsbodb.perfis_removed re WHERE re.profile_id=%s) AND t.author_profile_id=%s)) as notified
                                FROM wsbodb.perfis_tip t, wsbodb.perfis_perfil p
                                WHERE t.author_user_id = p.usuario_id
                                AND t.author_user_id IN ( SELECT usuario_id FROM wsbodb.perfis_perfil )
                                AND t.author_profile_id = %s
                                AND t.hided = 0
                                AND t.world = 0
                                ORDER BY ifnull(t.updated_date,t.date) DESC;""", [perfil_id, request.user.id, request.user.perfil.id, perfil_id])
    else:    
        profiletips = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date, p.usuario_id as profile_id, 
                                t.author_user_id as author_user, t.author_name as name,
                                (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                (t.id IN (SELECT n.referenced_card FROM wsbodb.perfis_notifications n WHERE n.card_id NOT IN (SELECT re.card_id FROM wsbodb.perfis_removed re WHERE re.profile_id=%s) AND t.author_profile_id=%s)) as notified
                                FROM wsbodb.perfis_tip t, wsbodb.perfis_perfil p
                                WHERE t.author_user_id = p.usuario_id
                                AND t.author_user_id IN ( SELECT usuario_id FROM wsbodb.perfis_perfil )
                                AND t.author_profile_id = %s
                                AND t.hided = 0
                                AND t.world <> 0
                                ORDER BY ifnull(t.updated_date,t.date) DESC;""", [perfil_id, request.user.id, request.user.perfil.id, perfil_id])
    
    followers_howmany = Tip.objects.raw("""SELECT f.id, (COUNT(*)-1) as howmany 
                                        FROM wsbodb.perfis_follow f, wsbodb.perfis_perfil p 
                                        WHERE f.followed_id = %s
                                        AND f.follower_id <> f.followed_id
                                        AND p.usuario_id = f.follower_id;""", [perfil_id]) 
        
    is_contact = Tip.objects.raw("""SELECT f.id, f.followed_id as followed, ifnull(f.followed_id,0) as isfollowing  
                                FROM wsbodb.perfis_follow f
                                WHERE f.follower_id = %s
                                AND f.followed_id = %s;""", [request.user.id, perfil_id])
    
    has_short_description = Tip.objects.raw("""SELECT d.id, d.description as description, 
                                ifnull(d.profile_id,0) as has_description  
                                FROM wsbodb.perfis_short_description d
                                WHERE d.profile_id = %s;""", [perfil_id]) 

    
    my_profile_image = Tip.objects.raw("""SELECT a.id, a.upload as upload, a.user_id
                                        FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                        ON(a.user_id = p.usuario_id)
                                        WHERE p.usuario_id = %s;""", [request.user.id])  
        
    has_profile_image = Tip.objects.raw("""SELECT a.id, a.upload as upload, a.user_id,
                                        ifnull(a.upload,0) as has_image
                                        FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                        ON(a.profile_id = p.id)
                                        WHERE p.id = %s;""", [perfil_id])         
    
    has_background_image = Tip.objects.raw("""SELECT b.id, b.bkg_upload as bkg_upload, b.user_id,
                                        ifnull(b.bkg_upload,0) as has_background
                                        FROM wsbodb.perfis_background b LEFT JOIN wsbodb.perfis_perfil p
                                        ON(b.profile_id = p.id)
                                        WHERE p.id = %s;""", [perfil_id])        
    
    company_tips = Tip.objects.raw("""SELECT c.id, c.company_profile_id, 
                                c.company_content as content, c.date, p.usuario_id as profile_id, 
                                c.company_user_id 
                                FROM wsbodb.perfis_company c, wsbodb.perfis_perfil p 
                                WHERE c.company_user_id = p.usuario_id
                                AND c.company_user_id IN ( SELECT usuario_id FROM wsbodb.perfis_perfil )
                                AND c.company_profile_id = %s
                                ORDER BY c.date DESC;""", [perfil_id])
    
    published_tips_count = Tip.objects.raw("""SELECT t.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_tip t 
                                WHERE t.author_profile_id = %s
                                AND t.hided = 0
                                ORDER BY t.date DESC;""", [perfil_id]) 
    
    company_description_count = Tip.objects.raw("""SELECT c.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_company c 
                                WHERE c.company_profile_id = %s
                                ORDER BY c.date DESC;""", [perfil_id])   
    
    company_offer_count = Tip.objects.raw("""SELECT o.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_offer o 
                                WHERE o.offer_profile_id = %s
                                ORDER BY o.date DESC;""", [perfil_id]) 
    
    company_location_count = Tip.objects.raw("""SELECT l.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_location l 
                                WHERE l.location_profile_id = %s
                                ORDER BY l.date DESC;""", [perfil_id])      
    
    person_whoami_count = Tip.objects.raw("""SELECT w.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_whoami w 
                                WHERE w.whoami_profile_id = %s
                                ORDER BY w.date DESC;""", [perfil_id]) 
    
    person_education_count = Tip.objects.raw("""SELECT e.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_education e 
                                WHERE e.education_profile_id = %s
                                ORDER BY e.date DESC;""", [perfil_id])  
    
    person_knows_count = Tip.objects.raw("""SELECT k.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_knows k 
                                WHERE k.knows_profile_id = %s
                                ORDER BY k.date DESC;""", [perfil_id]) 
    
    person_jobs_count = Tip.objects.raw("""SELECT j.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_jobs j 
                                WHERE j.jobs_profile_id = %s
                                ORDER BY j.date DESC;""", [perfil_id])
    
    person_live_count = Tip.objects.raw("""SELECT l.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_live l 
                                WHERE l.live_profile_id = %s
                                ORDER BY l.date DESC;""", [perfil_id]) 

    person_hobby_count = Tip.objects.raw("""SELECT h.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_hobby h 
                                WHERE h.hobby_profile_id = %s
                                ORDER BY h.date DESC;""", [perfil_id])

    card_on_profile_deck = Tip.objects.raw("""SELECT   d.id,
                                        d.id as deck,  
                                        t.id as tip,
                                        d.author_profile_id as fid, 
                                        d.author_user_id as user, 
                                        d.date as date,  
                                        d.author_name as name,
                                        d.deck_name as deck_name 
                                        FROM wsbodb.perfis_deck d,
                                        wsbodb.perfis_tip t,
                                        wsbodb.perfis_folder f
                                        WHERE d.id = f.folder_id
                                        AND t.id = f.card_id
                                        AND t.author_profile_id = f.profile_id
                                        AND t.author_profile_id = %s;""", [perfil_id]) 
    
    campaigns = Tip.objects.raw("""SELECT   d.id,
                                        d.id as deck,  
                                        t.id as tip,
                                        d.author_profile_id as author, 
                                        d.author_user_id as user, 
                                        d.date as date,  
                                        d.author_name as name,
                                        d.deck_name as campaign 
                                        FROM wsbodb.perfis_deck d,
                                        wsbodb.perfis_tip t,
                                        wsbodb.perfis_folder f
                                        WHERE d.id = f.folder_id
                                        AND t.id = f.card_id
                                        AND t.author_profile_id = f.profile_id
                                        AND t.author_profile_id = %s
                                        GROUP BY d.id;""", [perfil_id]) 
    
    return render(request, 'perfil.html', locals())



@login_required
def hided(request, perfil_id):

    perfil = Perfil.objects.get(id=perfil_id)
    perfil_logado = get_perfil_logado(request)
    ja_eh_contato = perfil in perfil_logado.contatos.all()
    
    url2 = request.build_absolute_uri()
    url = url2.split('//')[-1].split('/')[0]
    
    profilehided = Tip.objects.raw("""SELECT t.id, p.nome as name,t.author_profile_id as author, 
                                t.content, t.date, p.usuario_id as profile_id, t.hided,
                                t.author_user_id as author_user,
                                (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                (t.id IN (SELECT n.referenced_card FROM wsbodb.perfis_notifications n WHERE n.card_id NOT IN (SELECT re.card_id FROM wsbodb.perfis_removed re WHERE re.profile_id=%s) AND t.author_profile_id=%s)) as notified 
                                FROM wsbodb.perfis_tip t, wsbodb.perfis_perfil p 
                                WHERE t.author_user_id = p.usuario_id
                                AND t.author_user_id IN ( SELECT usuario_id FROM wsbodb.perfis_perfil )
                                AND t.author_profile_id = %s
                                AND t.hided = 1
                                ORDER BY t.date DESC;""", [perfil_id, request.user.id, request.user.perfil.id, perfil_id])
    
    

    my_profile_image = Tip.objects.raw("""SELECT a.id, a.upload as upload, a.user_id
                                        FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                        ON(a.user_id = p.usuario_id)
                                        WHERE p.usuario_id = %s;""", [request.user.id])
         
    has_profile_image = Tip.objects.raw("""SELECT a.id, ifnull(a.upload,0) as upload 
                                        FROM wsbodb.perfis_avatar a
                                        WHERE a.profile_id = %s;""", [perfil_id]) 
    
    has_short_description = Tip.objects.raw("""SELECT d.id, d.description as description, 
                                ifnull(d.profile_id,0) as has_description  
                                FROM wsbodb.perfis_short_description d
                                WHERE d.profile_id = %s;""", [perfil_id])      
    
    
    #Followers counting
    followers_howmany = Tip.objects.raw("""SELECT f.id, (COUNT(*) -1) as howmany 
                                            FROM wsbodb.perfis_follow f, wsbodb.perfis_perfil p 
                                            WHERE f.followed_id = %s
                                            AND p.usuario_id = f.follower_id;""", [perfil_id]) 
    

    is_contact = Tip.objects.raw("""SELECT f.id, f.followed_id as followed, ifnull(f.followed_id,0) as isfollowing  
                                FROM wsbodb.perfis_follow f
                                WHERE f.follower_id = %s
                                AND f.followed_id = %s;""", [request.user.id, perfil_id]) 
               
    return render(request, 'hided.html', locals())


 

#@permission_required('perfis.add_convite', raise_exception=True)
@login_required
def convidar(request, perfil_id):

    perfil_a_convidar = Perfil.objects.get(id=perfil_id)
    perfil_logado = get_perfil_logado(request)
    perfil_logado.convidar(perfil_a_convidar)            
    return redirect('index')

@login_required
def aceitar(request, convite_id):
    convite = Convite.objects.get(id=convite_id)
    convite.aceitar()
    return redirect('index')


@login_required
def get_perfil_logado(request):
    return request.user.perfil


 
@login_required
def notifications(request):
    perfil = Perfil.objects.get(id=request.user.perfil.id)
    
    url2 = request.build_absolute_uri()
    url = url2.split('//')[-1].split('/')[0]
    
    following_only_notified = Tip.objects.raw("""SELECT t.id, p.nome as name, t.content, 
                                    t.author_profile_id as author, p.type as type,
                                    p.usuario_id as profile_id, t.author_name as name,
                                    t.date, ifnull(f.id,0) as isfollowing, ifnull(fav.id,0) as isfav,
                                    (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                    (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed,
                                    (t.author_profile_id IN (SELECT p.id FROM wsbodb.perfis_perfil p WHERE p.stealth=1 AND t.author_profile_id=%s)) as stealthed,
                                    (t.id IN (SELECT n.referenced_card FROM wsbodb.perfis_notifications n WHERE n.card_id NOT IN (SELECT re.card_id FROM wsbodb.perfis_removed re WHERE re.profile_id=%s) AND t.author_profile_id=%s)) as notified,
                                    f.followed_id, ifnull(a.upload,0) as upload, t.outdoor
                                    FROM wsbodb.perfis_perfil p, wsbodb.perfis_follow f,
                                    wsbodb.perfis_avatar a, wsbodb.perfis_notifications notif,
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                    ON (t.id = fav.tip_id AND fav.profile_id = %s) 
                                    WHERE p.usuario_id = %s
                                    AND t.author_profile_id = f.followed_id
                                    AND f.follower_id = %s 
                                    AND f.followed_id = a.profile_id
                                    AND t.id = notif.referenced_card
                                    GROUP BY notif.referenced_card
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""", 
                                    [request.user.perfil.id, request.user.id, request.user.perfil.id, request.user.id, request.user.perfil.id, request.user.id, request.user.id, request.user.id])

       
    notifications = Tip.objects.raw("""SELECT n.id, n.card_id,
                                        n.player_id, n.holder_id,
                                        n.referenced_card,
                                        n.player_name, n.holder_name,
                                        t.content as content, 
                                        t.outdoor as outdoor,
                                        t.hide_image,
                                        t.direction
                                        FROM wsbodb.perfis_notifications n,
                                        wsbodb.perfis_tip t
                                        WHERE n.holder_id = %s
                                        AND t.id = n.referenced_card;""", [request.user.perfil.id])
    
    my_profile_image = Tip.objects.raw("""SELECT a.id, a.upload as upload, a.user_id
                                        FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                        ON(a.user_id = p.usuario_id)
                                        WHERE p.usuario_id = %s;""", [request.user.id]) 
            
    return render(request, 'notifications.html', {'perfis':Perfil.objects.all(),
                                                  'perfil': perfil,
                                                  'url': url, 
                                                  'perfil_logado': get_perfil_logado(request),
                                                  'my_profile_image': my_profile_image,
                                                  'notifications': notifications,
                                                  'following_only_notified': following_only_notified })




@login_required
def favorites(request, perfil_id):

    perfil = Perfil.objects.get(id=perfil_id)
    perfil_logado = get_perfil_logado(request)
    ja_eh_contato = perfil in perfil_logado.contatos.all()
    
    url2 = request.build_absolute_uri()
    url = url2.split('//')[-1].split('/')[0]
    
    if perfil_logado.map == '0':
        favorites =  Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date, 
                                a.upload as upload, p.nome as name, fav.favorite,
                                t.author_name as author_name,
                                (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed,
                                p.usuario_id as profile_id, p.type as type, ifnull(fav.id,0) as isfav,                                
                                ifnull(a.upload,0) as upload
                                FROM wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_avatar a  
                                ON (t.author_profile_id = a.profile_id), 
                                    wsbodb.perfis_perfil p,  wsbodb.perfis_favorites fav
                                WHERE t.author_profile_id = p.id
                                AND fav.id <> 0
                                AND fav.tip_id = t.id
                                AND fav.profile_id = %s
                                AND t.hided = 0
                                AND t.world = 0
                                ORDER BY ifnull(t.updated_date,t.date) DESC;""", 
                                [request.user.perfil.id, request.user.id, request.user.id])
    else:
        favorites =  Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date, 
                                a.upload as upload, p.nome as name, fav.favorite,
                                t.author_name as author_name,
                                (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed,
                                p.usuario_id as profile_id, p.type as type, ifnull(fav.id,0) as isfav,                                
                                ifnull(a.upload,0) as upload
                                FROM wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_avatar a  
                                ON (t.author_profile_id = a.profile_id), 
                                    wsbodb.perfis_perfil p,  wsbodb.perfis_favorites fav
                                WHERE t.author_profile_id = p.id
                                AND fav.id <> 0
                                AND fav.tip_id = t.id
                                AND fav.profile_id = %s
                                AND t.hided = 0
                                AND t.world <> 0
                                ORDER BY ifnull(t.updated_date,t.date) DESC;""", 
                                [request.user.perfil.id, request.user.id, request.user.id])
    
    #Not used now
    counting = Tip.objects.raw("""SELECT t.id, COUNT(*) as howmany, t.author_profile_id as author, t.content, t.date,  
                                p.usuario_id as profile_id, p.type as type, ifnull(fav.id,0) as isfav
                                FROM wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav ON (t.id = fav.tip_id AND fav.profile_id = %s), 
                                    wsbodb.perfis_perfil p
                                WHERE p.usuario_id = %s
                                AND fav.id <> 0
                                ORDER BY t.date DESC;""", [request.user.id, request.user.id])
     

    my_profile_image = Tip.objects.raw("""SELECT a.id, a.upload as upload, a.user_id
                                        FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                        ON(a.user_id = p.usuario_id)
                                        WHERE p.usuario_id = %s;""", [request.user.id])
         
    has_profile_image = Tip.objects.raw("""SELECT a.id, ifnull(a.upload,0) as upload 
                                        FROM wsbodb.perfis_avatar a
                                        WHERE a.profile_id = %s;""", [perfil_id])   
    
    
    has_short_description = Tip.objects.raw("""SELECT d.id, d.description as description, 
                                ifnull(d.profile_id,0) as has_description  
                                FROM wsbodb.perfis_short_description d
                                WHERE d.profile_id = %s;""", [perfil_id])     

    #Followers counting
    followers_howmany = Tip.objects.raw("""SELECT f.id, (COUNT(*) -1) as howmany 
                                            FROM wsbodb.perfis_follow f, wsbodb.perfis_perfil p 
                                            WHERE f.followed_id = %s
                                            AND p.usuario_id = f.follower_id;""", [perfil_id])
    

    is_contact = Tip.objects.raw("""SELECT f.id, f.followed_id as followed, ifnull(f.followed_id,0) as isfollowing  
                                FROM wsbodb.perfis_follow f
                                WHERE f.follower_id = %s
                                AND f.followed_id = %s;""", [request.user.id, perfil_id])  
           
    return render(request, 'favorites.html', locals() )
    


@login_required
def followers(request, perfil_id):

    perfil = Perfil.objects.get(id=perfil_id)
    perfil_logado = get_perfil_logado(request)
    ja_eh_contato = perfil in perfil_logado.contatos.all()
    
    url2 = request.build_absolute_uri()
    url = url2.split('//')[-1].split('/')[0]    
    
    followers = Tip.objects.raw("""SELECT  a.id, a.profile_id as fid, p.nome as name, 
                                    max(t.date) as date, max(t.updated_date) as updated_date, 
                                    a.upload as upload,
                                    s.description as description,
                                    t.author_name as author_name, 
                                    p.usuario_id as profile_id, p.type as type,
                                    ifnull(f.id,0) as isfollowing,
                                    f.followed_id, ifnull(a.upload,0) as upload
                                    FROM wsbodb.perfis_avatar a,
                                    wsbodb.perfis_perfil p, wsbodb.perfis_follow f,
                                    wsbodb.perfis_tip t,
                                    wsbodb.perfis_short_description s 
                                    WHERE p.usuario_id = f.follower_id 
                                    AND a.user_id = f.follower_id
                                    AND f.followed_id = %s
                                    GROUP BY f.follower_id
                                    ORDER BY p.nome;""", [perfil_id])
    
    #Followers counting
    followers_howmany = Tip.objects.raw("""SELECT f.id, (COUNT(*) -1) as howmany 
                                            FROM wsbodb.perfis_follow f, wsbodb.perfis_perfil p 
                                            WHERE f.followed_id = %s
                                            AND p.usuario_id = f.follower_id;""", [perfil_id])
    
    is_contact = Tip.objects.raw("""SELECT f.id, f.followed_id as followed, ifnull(f.followed_id,0) as isfollowing  
                                FROM wsbodb.perfis_follow f
                                WHERE f.follower_id = %s
                                AND f.followed_id = %s;""", [request.user.id, perfil_id]) 

    
    profiletips = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date, p.usuario_id as profile_id, 
                                t.author_user_id as author_user 
                                FROM wsbodb.perfis_tip t, wsbodb.perfis_perfil p 
                                WHERE t.author_user_id = p.usuario_id
                                AND t.author_user_id IN ( SELECT usuario_id FROM wsbodb.perfis_perfil )
                                AND t.author_profile_id = %s
                                ORDER BY t.date DESC;""", [perfil_id])
    
    
     
    
    my_profile_image = Tip.objects.raw("""SELECT a.id, a.upload as upload, a.user_id
                                        FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                        ON(a.user_id = p.usuario_id)
                                        WHERE p.usuario_id = %s;""", [request.user.id])
         
    has_profile_image = Tip.objects.raw("""SELECT a.id, ifnull(a.upload,0) as upload 
                                        FROM wsbodb.perfis_avatar a
                                        WHERE a.profile_id = %s;""", [perfil_id]) 
    
    has_short_description = Tip.objects.raw("""SELECT d.id, d.description as description, 
                                ifnull(d.profile_id,0) as has_description  
                                FROM wsbodb.perfis_short_description d
                                WHERE d.profile_id = %s;""", [perfil_id])
   
    return render(request, 'followers.html', locals())


@login_required
def contacts(request, perfil_id):

    perfil = Perfil.objects.get(id=perfil_id)
    perfil_logado = get_perfil_logado(request)
    ja_eh_contato = perfil in perfil_logado.contatos.all()
    
    url2 = request.build_absolute_uri()
    url = url2.split('//')[-1].split('/')[0]    
    
    is_contact = Tip.objects.raw("""SELECT a.id, f.followed_id as fid, p.nome as name, 
                                    max(t.date) as date, max(t.updated_date) as updated_date,
                                    a.upload as upload, 
                                    s.description as description,
                                    p.type as type,
                                    t.author_name as author_name,
                                    p.usuario_id as profile_id, ifnull(f.id,0) as isfollowing,
                                    f.followed_id, ifnull(a.upload,0) as upload
                                    FROM wsbodb.perfis_avatar a,
                                    wsbodb.perfis_perfil p, wsbodb.perfis_follow f,
                                    wsbodb.perfis_tip t,
                                    wsbodb.perfis_short_description s  
                                    WHERE p.id = f.followed_id
                                    AND a.profile_id = f.followed_id 
                                    AND f.follower_id = %s 
                                    GROUP BY f.followed_id
                                    ORDER BY p.nome;""", [request.user.id])
    
    #Menu followings counting
    contacts = Tip.objects.raw("""SELECT f.id, (COUNT(*)-1) as howmany
                                FROM wsbodb.perfis_follow f, wsbodb.perfis_avatar a  
                                WHERE a.profile_id = f.followed_id 
                                AND f.follower_id = %s;""", [request.user.id]) 
    
    profiletips = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date, p.usuario_id as profile_id, 
                                t.author_user_id as author_user 
                                FROM wsbodb.perfis_tip t, wsbodb.perfis_perfil p 
                                WHERE t.author_user_id = p.usuario_id
                                AND t.author_user_id IN ( SELECT usuario_id FROM wsbodb.perfis_perfil )
                                AND t.author_profile_id = %s
                                ORDER BY t.date DESC;""", [perfil_id])
         
    my_profile_image = Tip.objects.raw("""SELECT a.id, a.upload as upload, a.user_id
                                        FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                        ON(a.user_id = p.usuario_id)
                                        WHERE p.usuario_id = %s;""", [request.user.id])
         
    has_profile_image = Tip.objects.raw("""SELECT a.id, ifnull(a.upload,0) as upload 
                                        FROM wsbodb.perfis_avatar a
                                        WHERE a.profile_id = %s;""", [perfil_id]) 
    
    has_short_description = Tip.objects.raw("""SELECT d.id, d.description as description, 
                                                ifnull(d.profile_id,0) as has_description  
                                                FROM wsbodb.perfis_short_description d
                                                WHERE d.profile_id = %s;""", [perfil_id])    
    
    #Followers counting
    followers_howmany = Tip.objects.raw("""SELECT f.id, (COUNT(*) -1) as howmany 
                                            FROM wsbodb.perfis_follow f, wsbodb.perfis_perfil p 
                                            WHERE f.followed_id = %s
                                            AND p.usuario_id = f.follower_id;""", [perfil_id])
       
    return render(request, 'contacts.html', locals())

@login_required
def removed_cards(request, perfil_id):
    perfil = Perfil.objects.get(id=perfil_id)
    perfil_logado = get_perfil_logado(request)
    ja_eh_contato = perfil in perfil_logado.contatos.all()
    
    url2 = request.build_absolute_uri()
    url = url2.split('//')[-1].split('/')[0]    
    
    removed_cards = Tip.objects.raw("""SELECT t.id, p.nome as name, t.content, 
                                    t.author_profile_id as author, p.type as type,
                                    p.usuario_id as profile_id, t.author_name as name,
                                    t.date, ifnull(f.id,0) as isfollowing, ifnull(fav.id,0) as isfav,
                                    (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                    (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed,
                                    (t.id IN (SELECT p.card_id FROM wsbodb.perfis_played_cards p WHERE p.player_id=%s AND p.played=2)) as accepted,
                                    (t.id IN (SELECT n.referenced_card FROM wsbodb.perfis_notifications n WHERE n.card_id NOT IN (SELECT re.card_id FROM wsbodb.perfis_removed re WHERE re.profile_id=%s) AND t.author_profile_id=%s)) as notified,
                                    f.followed_id, ifnull(a.upload,0) as upload, t.outdoor
                                    FROM wsbodb.perfis_perfil p, wsbodb.perfis_follow f,
                                    wsbodb.perfis_avatar a, 
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                    ON (t.id = fav.tip_id AND fav.profile_id = %s) 
                                    WHERE p.usuario_id = %s
                                    AND f.follower_id = %s 
                                    AND t.author_profile_id = a.profile_id
                                    GROUP BY t.id
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""", 
                                    [request.user.perfil.id, request.user.id, request.user.perfil.id, request.user.id, request.user.perfil.id, request.user.id, request.user.id, request.user.id])

    
    profiletips = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date, p.usuario_id as profile_id, 
                                t.author_user_id as author_user 
                                FROM wsbodb.perfis_tip t, wsbodb.perfis_perfil p 
                                WHERE t.author_user_id = p.usuario_id
                                AND t.author_user_id IN ( SELECT usuario_id FROM wsbodb.perfis_perfil )
                                AND t.author_profile_id = %s
                                ORDER BY t.date DESC;""", [perfil_id])
    
    my_profile_image = Tip.objects.raw("""SELECT a.id, a.upload as upload, a.user_id
                                        FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                        ON(a.user_id = p.usuario_id)
                                        WHERE p.usuario_id = %s;""", [request.user.id])
         
    has_profile_image = Tip.objects.raw("""SELECT a.id, ifnull(a.upload,0) as upload 
                                        FROM wsbodb.perfis_avatar a
                                        WHERE a.profile_id = %s;""", [perfil_id]) 
    
    has_short_description = Tip.objects.raw("""SELECT d.id, d.description as description, 
                                ifnull(d.profile_id,0) as has_description  
                                FROM wsbodb.perfis_short_description d
                                WHERE d.profile_id = %s;""", [perfil_id])
    
    removed_count = Tip.objects.raw("""SELECT r.id, COUNT(*) as howmany 
                                        FROM wsbodb.perfis_removed r
                                        WHERE r.profile_id = %s;""", [request.user.id])
    
    accepted_count = Tip.objects.raw("""SELECT p.id, 
                                        COUNT(*) as howmany
                                        FROM wsbodb.perfis_played_cards p
                                        WHERE p.player_id = %s
                                        AND p.played = 2;""", [request.user.perfil.id])
    
    who_accepted_count = Tip.objects.raw("""SELECT p.id, p.referenced_card, p.card_id as card, 
                                        COUNT(*) as howmany
                                        FROM wsbodb.perfis_tip t,
                                        wsbodb.perfis_played_cards p
                                        WHERE p.player_id = %s
                                        AND p.played = 2
                                        AND p.referenced_card = t.id
                                        GROUP BY p.card_id;""", [request.user.perfil.id])
    
    accepted_by = Tip.objects.raw("""SELECT p.id, p.referenced_card as referenced_card 
                                        FROM wsbodb.perfis_played_cards p
                                        WHERE p.player_id = %s
                                        AND p.played = 2;""", [request.user.perfil.id])  
        
    return render(request, 'removed_cards.html', locals())


@login_required
def accepted_cards(request, perfil_id):
    perfil = Perfil.objects.get(id=perfil_id)
    perfil_logado = get_perfil_logado(request)
    ja_eh_contato = perfil in perfil_logado.contatos.all()
    
    url2 = request.build_absolute_uri()
    url = url2.split('//')[-1].split('/')[0]    
    
    accepted_cards = Tip.objects.raw("""SELECT t.id, p.nome as name, t.content, 
                                    t.author_profile_id as author, p.type as type,
                                    p.usuario_id as profile_id, t.author_name as name,
                                    t.date, ifnull(f.id,0) as isfollowing, ifnull(fav.id,0) as isfav,
                                    (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                    (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed,
                                    (t.id IN (SELECT p.card_id FROM wsbodb.perfis_played_cards p WHERE p.player_id=%s AND p.played=2)) as accepted,
                                    (t.id IN (SELECT n.referenced_card FROM wsbodb.perfis_notifications n WHERE n.card_id NOT IN (SELECT re.card_id FROM wsbodb.perfis_removed re WHERE re.profile_id=%s) AND t.author_profile_id=%s)) as notified,
                                    f.followed_id, ifnull(a.upload,0) as upload, t.outdoor
                                    FROM wsbodb.perfis_perfil p, wsbodb.perfis_follow f,
                                    wsbodb.perfis_avatar a, 
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                    ON (t.id = fav.tip_id AND fav.profile_id = %s) 
                                    WHERE p.usuario_id = %s
                                    AND f.follower_id = %s 
                                    AND t.author_profile_id = a.profile_id
                                    GROUP BY t.id
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""", 
                                    [request.user.perfil.id, request.user.id, request.user.perfil.id, request.user.id, request.user.perfil.id, request.user.id, request.user.id, request.user.id])

    
    profiletips = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date, p.usuario_id as profile_id, 
                                t.author_user_id as author_user 
                                FROM wsbodb.perfis_tip t, wsbodb.perfis_perfil p 
                                WHERE t.author_user_id = p.usuario_id
                                AND t.author_user_id IN ( SELECT usuario_id FROM wsbodb.perfis_perfil )
                                AND t.author_profile_id = %s
                                ORDER BY t.date DESC;""", [perfil_id])
    
    my_profile_image = Tip.objects.raw("""SELECT a.id, a.upload as upload, a.user_id
                                        FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                        ON(a.user_id = p.usuario_id)
                                        WHERE p.usuario_id = %s;""", [request.user.id])
         
    has_profile_image = Tip.objects.raw("""SELECT a.id, ifnull(a.upload,0) as upload 
                                        FROM wsbodb.perfis_avatar a
                                        WHERE a.profile_id = %s;""", [perfil_id]) 
    
    has_short_description = Tip.objects.raw("""SELECT d.id, d.description as description, 
                                ifnull(d.profile_id,0) as has_description  
                                FROM wsbodb.perfis_short_description d
                                WHERE d.profile_id = %s;""", [perfil_id])
    
    removed_count = Tip.objects.raw("""SELECT r.id, COUNT(*) as howmany 
                                        FROM wsbodb.perfis_removed r
                                        WHERE r.profile_id = %s;""", [request.user.id])
    
    accepted_count = Tip.objects.raw("""SELECT p.id, 
                                        COUNT(*) as howmany
                                        FROM wsbodb.perfis_played_cards p
                                        WHERE p.player_id = %s
                                        AND p.played = 2;""", [request.user.perfil.id])
    
    who_accepted_count = Tip.objects.raw("""SELECT p.id, p.referenced_card, p.card_id as card, 
                                        COUNT(*) as howmany
                                        FROM wsbodb.perfis_tip t,
                                        wsbodb.perfis_played_cards p
                                        WHERE p.player_id = %s
                                        AND p.played = 2
                                        AND p.referenced_card = t.id
                                        GROUP BY p.card_id;""", [request.user.perfil.id])
    
    accepted_by = Tip.objects.raw("""SELECT p.id, p.referenced_card as referenced_card 
                                        FROM wsbodb.perfis_played_cards p
                                        WHERE p.player_id = %s
                                        AND p.played = 2;""", [request.user.perfil.id])  
        
    return render(request, 'accepted_cards.html', locals())

@login_required
def config(request, perfil_id):
    perfil = Perfil.objects.get(id=perfil_id)
    perfil_logado = get_perfil_logado(request)
    ja_eh_contato = perfil in perfil_logado.contatos.all()
    
    url2 = request.build_absolute_uri()
    url = url2.split('//')[-1].split('/')[0]    
    
    config = Tip.objects.raw("""SELECT t.id, p.nome as name, t.content, 
                                    t.author_profile_id as author, t.type as type,
                                    p.usuario_id as profile_id, t.author_name as name,
                                    t.date, ifnull(f.id,0) as isfollowing, ifnull(fav.id,0) as isfav,
                                    (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                    (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed,
                                    (t.id IN (SELECT p.card_id FROM wsbodb.perfis_played_cards p WHERE p.player_id=%s AND p.played=2)) as accepted,
                                    (t.id IN (SELECT n.referenced_card FROM wsbodb.perfis_notifications n WHERE n.card_id NOT IN (SELECT re.card_id FROM wsbodb.perfis_removed re WHERE re.profile_id=%s) AND t.author_profile_id=%s)) as notified,
                                    f.followed_id, ifnull(a.upload,0) as upload, t.outdoor
                                    FROM wsbodb.perfis_perfil p, wsbodb.perfis_follow f,
                                    wsbodb.perfis_avatar a, 
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                    ON (t.id = fav.tip_id AND fav.profile_id = %s) 
                                    WHERE p.usuario_id = %s
                                    AND f.follower_id = %s 
                                    AND t.author_profile_id = a.profile_id
                                    GROUP BY t.id
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""", 
                                    [request.user.perfil.id, request.user.id, request.user.perfil.id, request.user.id, request.user.perfil.id, request.user.id, request.user.id, request.user.id])

    
    profiletips = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date, p.usuario_id as profile_id, 
                                t.author_user_id as author_user 
                                FROM wsbodb.perfis_tip t, wsbodb.perfis_perfil p 
                                WHERE t.author_user_id = p.usuario_id
                                AND t.author_user_id IN ( SELECT usuario_id FROM wsbodb.perfis_perfil )
                                AND t.author_profile_id = %s
                                ORDER BY t.date DESC;""", [perfil_id])
    
    my_profile_image = Tip.objects.raw("""SELECT a.id, a.upload as upload, a.user_id
                                        FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                        ON(a.user_id = p.usuario_id)
                                        WHERE p.usuario_id = %s;""", [request.user.id])
         
    has_profile_image = Tip.objects.raw("""SELECT a.id, ifnull(a.upload,0) as upload 
                                        FROM wsbodb.perfis_avatar a
                                        WHERE a.profile_id = %s;""", [perfil_id]) 
    
    has_short_description = Tip.objects.raw("""SELECT d.id, d.description as description, 
                                ifnull(d.profile_id,0) as has_description  
                                FROM wsbodb.perfis_short_description d
                                WHERE d.profile_id = %s;""", [perfil_id])
    
    removed_count = Tip.objects.raw("""SELECT r.id, COUNT(*) as howmany 
                                        FROM wsbodb.perfis_removed r
                                        WHERE r.profile_id = %s;""", [request.user.id])
    
    accepted_count = Tip.objects.raw("""SELECT p.id, 
                                        COUNT(*) as howmany
                                        FROM wsbodb.perfis_played_cards p
                                        WHERE p.player_id = %s
                                        AND p.played = 2;""", [request.user.perfil.id])
    
    who_accepted_count = Tip.objects.raw("""SELECT p.id, p.referenced_card, p.card_id as card, 
                                        COUNT(*) as howmany
                                        FROM wsbodb.perfis_tip t,
                                        wsbodb.perfis_played_cards p
                                        WHERE p.player_id = %s
                                        AND p.played = 2
                                        AND p.referenced_card = t.id
                                        GROUP BY p.card_id;""", [request.user.perfil.id])
    
    accepted_by = Tip.objects.raw("""SELECT p.id, p.referenced_card as referenced_card 
                                        FROM wsbodb.perfis_played_cards p
                                        WHERE p.player_id = %s
                                        AND p.played = 2;""", [request.user.perfil.id])  
        
    return render(request, 'configurations.html', locals())


@login_required
def stats(request, perfil_id):
    perfil = Perfil.objects.get(id=perfil_id)
    perfil_logado = get_perfil_logado(request)
    ja_eh_contato = perfil in perfil_logado.contatos.all()
    
    url2 = request.build_absolute_uri()
    url = url2.split('//')[-1].split('/')[0]    
    
    hided = Tip.objects.raw("""SELECT t.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_tip t, wsbodb.perfis_perfil p 
                                WHERE t.author_user_id = p.usuario_id
                                AND t.author_user_id IN ( SELECT usuario_id FROM wsbodb.perfis_perfil )
                                AND t.author_user_id = %s
                                AND t.hided = 1
                                ORDER BY t.date DESC;""", [request.user.id])     
    
    profiletips = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date, p.usuario_id as profile_id, 
                                t.author_user_id as author_user 
                                FROM wsbodb.perfis_tip t, wsbodb.perfis_perfil p 
                                WHERE t.author_user_id = p.usuario_id
                                AND t.author_user_id IN ( SELECT usuario_id FROM wsbodb.perfis_perfil )
                                AND t.author_profile_id = %s
                                ORDER BY t.date DESC;""", [perfil_id])
    
    published = Tip.objects.raw("""SELECT t.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_tip t, wsbodb.perfis_perfil p 
                                WHERE t.author_user_id = p.usuario_id
                                AND t.author_user_id IN ( SELECT usuario_id FROM wsbodb.perfis_perfil )
                                AND t.author_user_id = %s
                                AND t.hided = 0
                                ORDER BY t.date DESC;""", [request.user.id]) 
    
    #Menu favorite tips counting
    favorites_count = Tip.objects.raw("""SELECT t.id, COUNT(*) as howmany, t.author_profile_id as author, t.content, t.date,  
                                p.usuario_id as profile_id, p.type as type, ifnull(fav.id,0) as isfav
                                FROM wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav ON (t.id = fav.tip_id AND fav.profile_id = %s), 
                                    wsbodb.perfis_perfil p
                                WHERE p.usuario_id = %s
                                AND fav.id <> 0
                                AND t.hided = 0
                                ORDER BY t.date DESC;""", [request.user.id, request.user.id]) 
     
    #Menu followings counting
    contacts = Tip.objects.raw("""SELECT f.id, (COUNT(*)-1) as howmany
                                FROM wsbodb.perfis_follow f, wsbodb.perfis_avatar a  
                                WHERE a.profile_id = f.followed_id 
                                AND f.follower_id = %s;""", [request.user.id]) 
    
    my_profile_image = Tip.objects.raw("""SELECT a.id, a.upload as upload, a.user_id
                                        FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                        ON(a.user_id = p.usuario_id)
                                        WHERE p.usuario_id = %s;""", [request.user.id])
         
    has_profile_image = Tip.objects.raw("""SELECT a.id, ifnull(a.upload,0) as upload 
                                        FROM wsbodb.perfis_avatar a
                                        WHERE a.profile_id = %s;""", [perfil_id]) 
    
    has_short_description = Tip.objects.raw("""SELECT d.id, d.description as description, 
                                ifnull(d.profile_id,0) as has_description  
                                FROM wsbodb.perfis_short_description d
                                WHERE d.profile_id = %s;""", [perfil_id])
    
    #Followers counting
    followers_howmany = Tip.objects.raw("""SELECT f.id, (COUNT(*) -1) as howmany 
                                            FROM wsbodb.perfis_follow f, wsbodb.perfis_perfil p 
                                            WHERE f.followed_id = %s
                                            AND p.usuario_id = f.follower_id;""", [perfil_id])
    
    #Deck of cards counting
    deck_of_cards = Tip.objects.raw("""SELECT d.id, COUNT(*) as howmany 
                                            FROM wsbodb.perfis_deck d, wsbodb.perfis_perfil p 
                                            WHERE d.author_profile_id = %s
                                            AND p.usuario_id = d.author_user_id;""", [perfil_id])  
    
    removed_count =  Tip.objects.raw("""SELECT r.id, COUNT(*) as howmany 
                                        FROM wsbodb.perfis_removed r
                                        WHERE r.profile_id = %s;""", [request.user.id])
    
    accepted_count =  Tip.objects.raw("""SELECT p.id, COUNT(*) as howmany 
                                        FROM wsbodb.perfis_played_cards p
                                        WHERE p.player_id = %s
                                        AND p.played = 2;""", [request.user.perfil.id])    
        
    return render(request, 'stats.html', locals())



@login_required
def bysubject(request, perfil_id, pk):
    
    url2 = request.build_absolute_uri()
    url = url2.split('//')[-1].split('/')[0]

    perfil = Perfil.objects.get(id=perfil_id)
    perfil_logado = get_perfil_logado(request)
    ja_eh_contato = perfil in perfil_logado.contatos.all()
    
    
    bysubject = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date, p.usuario_id as profile_id,
                                t.author_user_id as author_user, t.author_name as name, p.type as type, 
                                d.deck_name,
                                (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed,
                                (t.id IN (SELECT fa.tip_id FROM wsbodb.perfis_favorites fa WHERE fa.profile_id=%s)) as isfav
                                FROM wsbodb.perfis_tip t, wsbodb.perfis_perfil p,
                                wsbodb.perfis_deck d,
                                wsbodb.perfis_folder f
                                WHERE t.author_user_id = p.usuario_id
                                AND t.author_user_id IN ( SELECT usuario_id FROM wsbodb.perfis_perfil )
                                AND t.author_profile_id = %s
                                AND t.hided = 0
                                AND d.id = f.folder_id
                                AND t.id = f.card_id
                                AND t.author_profile_id = f.profile_id
                                AND d.id = %s
                                ORDER BY ifnull(t.updated_date,t.date) DESC;""", 
                                [request.user.perfil.id, request.user.id, request.user.id, perfil_id,pk])


    bysubject_admin_view = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date, p.usuario_id as profile_id,
                                t.author_user_id as author_user, t.author_name as name, p.type as type,
                                d.deck_name, f.profile_id as deck_owner_id,
                                ifnull(a.upload,0) as upload,
                                (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed,
                                (t.id IN (SELECT fa.tip_id FROM wsbodb.perfis_favorites fa WHERE fa.profile_id=%s)) as isfav
                                FROM wsbodb.perfis_tip t, wsbodb.perfis_perfil p,
                                wsbodb.perfis_deck d,
                                wsbodb.perfis_avatar a,
                                wsbodb.perfis_folder f
                                WHERE t.author_user_id = p.usuario_id
                                AND t.hided = 0
                                AND d.id = f.folder_id
                                AND t.id = f.card_id
                                AND d.id = %s
                                AND a.profile_id = t.author_profile_id
                                ORDER BY ifnull(t.updated_date,t.date) DESC;""", 
                                [request.user.perfil.id, request.user.id, request.user.id, pk])

    
                                    
    title_subject = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date, p.usuario_id as profile_id, 
                                t.author_user_id as author_user, t.author_name as name, d.deck_name,
                                (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                (t.id IN (SELECT n.referenced_card FROM wsbodb.perfis_notifications n WHERE n.card_id NOT IN (SELECT re.card_id FROM wsbodb.perfis_removed re WHERE re.profile_id=%s) AND t.author_profile_id=%s)) as notified
                                FROM wsbodb.perfis_tip t, wsbodb.perfis_perfil p,
                                wsbodb.perfis_deck d,
                                wsbodb.perfis_folder f
                                WHERE t.author_user_id = p.usuario_id
                                AND t.author_user_id IN ( SELECT usuario_id FROM wsbodb.perfis_perfil )
                                AND t.author_profile_id = %s
                                AND t.hided = 0
                                AND d.id = f.folder_id
                                AND t.id = f.card_id
                                AND f.profile_id = %s
                                AND d.id = %s
                                GROUP BY d.id;""", 
                                [perfil_id, request.user.id, request.user.perfil.id, perfil_id, perfil_id, pk])
                                                
    followers_howmany = Tip.objects.raw("""SELECT f.id, (COUNT(*)-1) as howmany 
                                        FROM wsbodb.perfis_follow f, wsbodb.perfis_perfil p 
                                        WHERE f.followed_id = %s
                                        AND f.follower_id <> f.followed_id
                                        AND p.usuario_id = f.follower_id;""", [perfil_id]) 
        
    is_contact = Tip.objects.raw("""SELECT f.id, f.followed_id as followed, ifnull(f.followed_id,0) as isfollowing  
                                FROM wsbodb.perfis_follow f
                                WHERE f.follower_id = %s
                                AND f.followed_id = %s;""", [request.user.id, perfil_id])
    
    has_short_description = Tip.objects.raw("""SELECT d.id, d.description as description, 
                                ifnull(d.profile_id,0) as has_description  
                                FROM wsbodb.perfis_short_description d
                                WHERE d.profile_id = %s;""", [perfil_id]) 

    
    my_profile_image = Tip.objects.raw("""SELECT a.id, a.upload as upload, a.user_id
                                        FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                        ON(a.user_id = p.usuario_id)
                                        WHERE p.usuario_id = %s;""", [request.user.id])  
        
    has_profile_image = Tip.objects.raw("""SELECT a.id, a.upload as upload, a.user_id,
                                        ifnull(a.upload,0) as has_image
                                        FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                        ON(a.profile_id = p.id)
                                        WHERE p.id = %s;""", [perfil_id])    
    
    has_background_image = Tip.objects.raw("""SELECT b.id, b.bkg_upload as bkg_upload, b.user_id,
                                        ifnull(b.bkg_upload,0) as has_background
                                        FROM wsbodb.perfis_background b LEFT JOIN wsbodb.perfis_perfil p
                                        ON(b.profile_id = p.id)
                                        WHERE p.id = %s;""", [perfil_id])          
    
    company_tips = Tip.objects.raw("""SELECT c.id, c.company_profile_id, 
                                c.company_content as content, c.date, p.usuario_id as profile_id, 
                                c.company_user_id 
                                FROM wsbodb.perfis_company c, wsbodb.perfis_perfil p 
                                WHERE c.company_user_id = p.usuario_id
                                AND c.company_user_id IN ( SELECT usuario_id FROM wsbodb.perfis_perfil )
                                AND c.company_profile_id = %s
                                ORDER BY c.date DESC;""", [perfil_id])
    
    published_tips_count = Tip.objects.raw("""SELECT t.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_tip t 
                                WHERE t.author_profile_id = %s
                                AND t.hided = 0
                                ORDER BY t.date DESC;""", [perfil_id]) 
    
    company_description_count = Tip.objects.raw("""SELECT c.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_company c 
                                WHERE c.company_profile_id = %s
                                ORDER BY c.date DESC;""", [perfil_id])   
    
    company_offer_count = Tip.objects.raw("""SELECT o.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_offer o 
                                WHERE o.offer_profile_id = %s
                                ORDER BY o.date DESC;""", [perfil_id]) 
    
    company_location_count = Tip.objects.raw("""SELECT l.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_location l 
                                WHERE l.location_profile_id = %s
                                ORDER BY l.date DESC;""", [perfil_id])      
    
    person_whoami_count = Tip.objects.raw("""SELECT w.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_whoami w 
                                WHERE w.whoami_profile_id = %s
                                ORDER BY w.date DESC;""", [perfil_id]) 
    
    person_education_count = Tip.objects.raw("""SELECT e.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_education e 
                                WHERE e.education_profile_id = %s
                                ORDER BY e.date DESC;""", [perfil_id])  
    
    person_knows_count = Tip.objects.raw("""SELECT k.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_knows k 
                                WHERE k.knows_profile_id = %s
                                ORDER BY k.date DESC;""", [perfil_id]) 
    
    person_jobs_count = Tip.objects.raw("""SELECT j.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_jobs j 
                                WHERE j.jobs_profile_id = %s
                                ORDER BY j.date DESC;""", [perfil_id])
    
    person_live_count = Tip.objects.raw("""SELECT l.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_live l 
                                WHERE l.live_profile_id = %s
                                ORDER BY l.date DESC;""", [perfil_id]) 

    person_hobby_count = Tip.objects.raw("""SELECT h.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_hobby h 
                                WHERE h.hobby_profile_id = %s
                                ORDER BY h.date DESC;""", [perfil_id])

    '''card_on_deck = Tip.objects.raw("""SELECT   d.id, 
                                        t.id as tip,
                                        d.author_profile_id as fid, 
                                        d.author_user_id as user, 
                                        d.date as date,  
                                        d.author_name as name,
                                        d.deck_name as deck_name 
                                        FROM wsbodb.perfis_deck d,
                                        wsbodb.perfis_tip t,
                                        wsbodb.perfis_folder f
                                        WHERE d.id = f.folder_id
                                        AND t.id = f.card_id
                                        AND t.author_profile_id = %s;""", [perfil_id])'''
    
    card_on_deck_admin_view = Tip.objects.raw("""SELECT d.id,
                                        d.id as deck,  
                                        t.id as tip,
                                        t.author_profile_id as author,
                                        d.author_profile_id as fid, 
                                        d.author_user_id as user, 
                                        d.date as date,  
                                        d.author_name as name,
                                        d.deck_name as deck_name 
                                        FROM wsbodb.perfis_deck d,
                                        wsbodb.perfis_tip t,
                                        wsbodb.perfis_folder f
                                        WHERE d.id = f.folder_id
                                        AND t.id = f.card_id
                                        AND t.author_profile_id = f.profile_id
                                        GROUP BY t.id;""") 
    
    others_hotcard = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date, p.usuario_id as profile_id, 
                                t.author_user_id as author_user, t.author_name as name, count(fav.tip_id) hot
                                FROM wsbodb.perfis_tip t, wsbodb.perfis_perfil p, wsbodb.perfis_favorites fav 
                                WHERE t.author_user_id = p.usuario_id
                                AND t.author_user_id IN ( SELECT usuario_id FROM wsbodb.perfis_perfil )
                                AND t.author_profile_id = %s
                                AND t.hided = 0
                                AND t.id = fav.tip_id
                                GROUP BY t.id
                                ORDER BY hot DESC
                                LIMIT 1;""", [perfil_id])

    campaigns = Tip.objects.raw("""SELECT   d.id,
                                        d.id as deck,  
                                        t.id as tip,
                                        d.author_profile_id as author, 
                                        d.author_user_id as user, 
                                        d.date as date,  
                                        d.author_name as name,
                                        d.deck_name as campaign 
                                        FROM wsbodb.perfis_deck d,
                                        wsbodb.perfis_tip t,
                                        wsbodb.perfis_folder f
                                        WHERE d.id = f.folder_id
                                        AND t.id = f.card_id
                                        AND t.author_profile_id = f.profile_id
                                        AND t.author_profile_id = %s
                                        GROUP BY d.id;""", [perfil_id])    
    
    return render(request, 'bysubject.html', locals())



@login_required
@csrf_exempt
def update_type_company(request, perfil_id):
    profile = request.GET['profile']    
    cursor = connection.cursor()   
    cursor.execute("""UPDATE wsbodb.perfis_perfil
                      SET type = 'c'
                      WHERE id = %s;""",[profile])    
    row = cursor.fetchall()    
    cursor.close()           
    teste = "updatedtype"    
    response_data = { 
        'row': row, 'teste': teste
    }
    return HttpResponse(json.dumps(response_data), content_type= u'application/json')

@login_required
@csrf_exempt
def update_type_female(request, perfil_id):
    profile = request.GET['profile']    
    cursor = connection.cursor()   
    cursor.execute("""UPDATE wsbodb.perfis_perfil
                      SET type = 'f'
                      WHERE id = %s;""",[profile])    
    row = cursor.fetchall()    
    cursor.close()           
    teste = "updatedtype"    
    response_data = { 
        'row': row, 'teste': teste
    }
    return HttpResponse(json.dumps(response_data), content_type= u'application/json')

@login_required
@csrf_exempt
def update_type_male(request, perfil_id):
    profile = request.GET['profile']    
    cursor = connection.cursor()   
    cursor.execute("""UPDATE wsbodb.perfis_perfil
                      SET type = 'm'
                      WHERE id = %s;""",[profile])    
    row = cursor.fetchall()    
    cursor.close()           
    teste = "updatedtype"    
    response_data = { 
        'row': row, 'teste': teste
    }
    return HttpResponse(json.dumps(response_data), content_type= u'application/json')


@login_required
@csrf_exempt
def activate_stealth_mode(request, perfil_id):
    profile = request.GET['profile']    
    cursor = connection.cursor()   
    cursor.execute("""UPDATE wsbodb.perfis_perfil
                      SET stealth = 1
                      WHERE id = %s;""",[profile])    
    row = cursor.fetchall()    
    cursor.close()           
    teste = "stealth_activated"    
    response_data = { 
        'row': row, 'teste': teste
    }
    return HttpResponse(json.dumps(response_data), content_type= u'application/json')


@login_required
@csrf_exempt
def deactivate_stealth_mode(request, perfil_id):
    profile = request.GET['profile']    
    cursor = connection.cursor()   
    cursor.execute("""UPDATE wsbodb.perfis_perfil
                      SET stealth = 0
                      WHERE id = %s;""",[profile])    
    row = cursor.fetchall()    
    cursor.close()           
    teste = "stealth_deactivated"    
    response_data = { 
        'row': row, 'teste': teste
    }
    return HttpResponse(json.dumps(response_data), content_type= u'application/json')


@login_required
@csrf_exempt
def deactivate_account(request, perfil_id):
    profile = request.GET['profile']    
    cursor = connection.cursor()  
     
    cursor.execute("""DELETE FROM wsbodb.perfis_jobs
                      WHERE jobs_profile_id = %s;""",[profile])
    
    cursor.execute("""DELETE FROM wsbodb.perfis_knows
                      WHERE knows_profile_id = %s;""",[profile])
    
    cursor.execute("""DELETE FROM wsbodb.perfis_education
                      WHERE education_profile_id = %s;""",[profile])
    
    cursor.execute("""DELETE FROM wsbodb.perfis_whoami
                      WHERE whoami_profile_id = %s;""",[profile])   
    
    cursor.execute("""DELETE FROM wsbodb.perfis_location
                      WHERE location_profile_id = %s;""",[profile])
     
    cursor.execute("""DELETE FROM wsbodb.perfis_company
                      WHERE company_profile_id = %s;""",[profile])
   
    cursor.execute("""DELETE FROM wsbodb.perfis_short_description
                      WHERE profile_id = %s;""",[profile])
    
    cursor.execute("""DELETE FROM wsbodb.perfis_removed
                      WHERE profile_id = %s;""",[profile])
    
    cursor.execute("""DELETE FROM wsbodb.perfis_played_cards
                      WHERE player_id = %s
                      OR (referenced_card IN (SELECT t.id FROM wsbodb.perfis_tip t WHERE t.author_profile_id=%s));""",
                      [profile, profile])
    
    cursor.execute("""DELETE FROM wsbodb.perfis_held_cards
                      WHERE player_id = %s;""",[profile])
    
    cursor.execute("""DELETE FROM wsbodb.perfis_follow
                      WHERE follower_id = %s
                      OR followed_id = %s;""",[request.user.id, profile])
    
    cursor.execute("""DELETE FROM wsbodb.perfis_favorites
                      WHERE profile_id = %s
                      OR (tip_id IN (SELECT t.id FROM wsbodb.perfis_tip t WHERE t.author_profile_id=%s));""",
                      [request.user.id, profile])    

    cursor.execute("""DELETE FROM wsbodb.perfis_folder
                      WHERE profile_id = %s;""",[profile])

    cursor.execute("""DELETE FROM wsbodb.perfis_deck
                      WHERE author_profile_id = %s;""",[profile])

    cursor.execute("""DELETE FROM wsbodb.perfis_avatar
                      WHERE profile_id = %s;""",[profile])
    
    cursor.execute("""DELETE FROM wsbodb.perfis_tip
                      WHERE author_profile_id = %s;""",[profile])
    
    cursor.execute("""DELETE FROM wsbodb.perfis_perfil
                      WHERE id = %s;""",[profile])

    cursor.execute("""DELETE FROM wsbodb._usuarios_user
                      WHERE id = %s;""",[request.user.id])
 
    row = cursor.fetchall()    
    cursor.close()           
    teste = "account_deactivated"    
    response_data = { 
        'row': row, 'teste': teste
    }
    redirect('login')
    return HttpResponse(json.dumps(response_data), content_type= u'application/json')

    
@login_required
def decks(request, perfil_id):
    perfil = Perfil.objects.get(id=perfil_id)
    perfil_logado = get_perfil_logado(request)
    ja_eh_contato = perfil in perfil_logado.contatos.all()
    
    url2 = request.build_absolute_uri()
    url = url2.split('//')[-1].split('/')[0]    
    
    decks = Tip.objects.raw("""SELECT d.id, IFNULL(COUNT(f.id), 0) AS howmany,
                                d.author_profile_id as fid, 
                                d.author_user_id as user, 
                                d.date as date,  
                                d.author_name as name,
                                d.deck_name as deck
                                FROM wsbodb.perfis_deck  AS d
                                LEFT JOIN wsbodb.perfis_folder  AS f ON d.id = f.folder_id
                                GROUP BY d.id
                                ORDER BY d.date DESC;""")


    cards_inside = Tip.objects.raw("""SELECT d.id, d.deck_name, COUNT(*) as howmany
                                    FROM wsbodb.perfis_deck d, wsbodb.perfis_tip t 
                                    WHERE d.id = t.deck
                                    GROUP BY t.deck""") 
    
    
    profiletips = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date, p.usuario_id as profile_id, 
                                t.author_user_id as author_user 
                                FROM wsbodb.perfis_tip t, wsbodb.perfis_perfil p 
                                WHERE t.author_user_id = p.usuario_id
                                AND t.author_user_id IN ( SELECT usuario_id FROM wsbodb.perfis_perfil )
                                AND t.author_profile_id = %s
                                ORDER BY t.date DESC;""", [perfil_id])
        
    my_profile_image = Tip.objects.raw("""SELECT a.id, a.upload as upload, a.user_id
                                        FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                        ON(a.user_id = p.usuario_id)
                                        WHERE p.usuario_id = %s;""", [request.user.id])
         
    has_profile_image = Tip.objects.raw("""SELECT a.id, ifnull(a.upload,0) as upload 
                                        FROM wsbodb.perfis_avatar a
                                        WHERE a.profile_id = %s;""", [perfil_id]) 
    
    has_short_description = Tip.objects.raw("""SELECT d.id, d.description as description, 
                                ifnull(d.profile_id,0) as has_description  
                                FROM wsbodb.perfis_short_description d
                                WHERE d.profile_id = %s;""", [perfil_id])
    
    #Folders counting
    folders = Tip.objects.raw("""SELECT d.id, (COUNT(*)) as howmany
                                FROM wsbodb.perfis_deck d  
                                WHERE d.author_profile_id = %s;""", [perfil_id])
    
    return render(request, 'decks.html', locals())

@login_required
@csrf_exempt
def deck(request, pk):
    url2 = request.build_absolute_uri()
    url = url2.split('//')[-1].split('/')[0]
    pid = url2.split('//')[-1].split('/')[-2]
    d = get_object_or_404(Deck, pk=pk)

    perfil = Perfil.objects.get(id=request.user.perfil.id)
    perfil_logado = get_perfil_logado(request)
    ja_eh_contato = perfil in perfil_logado.contatos.all()
    
    deck = Tip.objects.raw("""SELECT t.id, p.nome as name, t.content, t.hided,
                                    t.author_profile_id as author, p.type as type,
                                    p.usuario_id as profile_id, t.author_name as name,
                                    t.date, ifnull(f.id,0) as isfollowing, ifnull(fav.id,0) as isfav,
                                    (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                    (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed,
                                    (t.id IN (SELECT n.referenced_card FROM wsbodb.perfis_notifications n WHERE t.author_profile_id=%s)) as notified,
                                    f.followed_id, ifnull(a.upload,0) as upload, t.outdoor,
                                    d.id as deck, fol.card_id as card, fol.folder_id as folder, d.deck_name as deck_name
                                    FROM wsbodb.perfis_perfil p, wsbodb.perfis_follow f,
                                    wsbodb.perfis_avatar a, 
                                    wsbodb.perfis_deck d, 
                                    wsbodb.perfis_folder fol, 
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                    ON (t.id = fav.tip_id AND fav.profile_id = %s) 
                                    WHERE p.usuario_id = %s
                                    AND f.follower_id = %s 
                                    AND t.id = fol.card_id
                                    AND d.id = fol.folder_id
                                    AND t.author_profile_id = a.profile_id
                                    AND fol.folder_id = %s
                                    AND fol.profile_id = %s
                                    GROUP BY t.id
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""", 
                                    [request.user.perfil.id, request.user.id, request.user.perfil.id, request.user.id, request.user.id, request.user.id, d.id, request.user.perfil.id])
 
    folder = Tip.objects.raw("""SELECT  d.id, 
                                        d.author_profile_id as fid, 
                                        d.author_user_id as user, 
                                        d.date as date,  
                                        d.author_name as name,
                                        d.deck_name as deck_name,
                                        fol.id, fol.card_id as card_id, fol.folder_id
                                        FROM wsbodb.perfis_deck d,
                                        wsbodb.perfis_folder fol
                                        WHERE fol.profile_id = %s
                                        AND d.id = fol.folder_id
                                        AND fol.folder_id = %s
                                        AND fol.profile_id = %s
                                        GROUP BY d.id;""", 
                                        [request.user.perfil.id, d.id, request.user.perfil.id])
                                                                                                  
    profiletips = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date, 
                                p.usuario_id as profile_id, 
                                t.author_user_id as author_user, t.author_name as name
                                FROM wsbodb.perfis_tip t, wsbodb.perfis_perfil p
                                WHERE t.author_user_id = p.usuario_id
                                AND t.author_user_id IN ( SELECT usuario_id FROM wsbodb.perfis_perfil )
                                AND t.author_profile_id = %s
                                AND t.hided = 0
                                ORDER BY ifnull(t.updated_date,t.date) DESC;""", [request.user.perfil.id])
        
    is_contact = Tip.objects.raw("""SELECT f.id, f.followed_id as followed, ifnull(f.followed_id,0) as isfollowing  
                                FROM wsbodb.perfis_follow f
                                WHERE f.follower_id = %s
                                AND f.followed_id = %s;""", [request.user.id, request.user.perfil.id])
    
    has_short_description = Tip.objects.raw("""SELECT d.id, d.description as description, 
                                ifnull(d.profile_id,0) as has_description  
                                FROM wsbodb.perfis_short_description d
                                WHERE d.profile_id = %s;""", [request.user.perfil.id]) 

    
    my_profile_image = Tip.objects.raw("""SELECT a.id, a.upload as upload, a.user_id
                                        FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                        ON(a.user_id = p.usuario_id)
                                        WHERE p.usuario_id = %s;""", [request.user.id])
         
    has_profile_image = Tip.objects.raw("""SELECT a.id, ifnull(a.upload,0) as upload 
                                        FROM wsbodb.perfis_avatar a
                                        WHERE a.profile_id = %s;""", [request.user.perfil.id])         
    
    company_tips = Tip.objects.raw("""SELECT c.id, c.company_profile_id, 
                                c.company_content as content, c.date, p.usuario_id as profile_id, 
                                c.company_user_id 
                                FROM wsbodb.perfis_company c, wsbodb.perfis_perfil p 
                                WHERE c.company_user_id = p.usuario_id
                                AND c.company_user_id IN ( SELECT usuario_id FROM wsbodb.perfis_perfil )
                                AND c.company_profile_id = %s
                                ORDER BY c.date DESC;""", [request.user.perfil.id])
    
    published_tips_count = Tip.objects.raw("""SELECT t.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_tip t 
                                WHERE t.author_profile_id = %s
                                AND t.hided = 0
                                ORDER BY t.date DESC;""", [request.user.perfil.id]) 
    
    company_description_count = Tip.objects.raw("""SELECT c.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_company c 
                                WHERE c.company_profile_id = %s
                                ORDER BY c.date DESC;""", [request.user.perfil.id])   
    
    company_offer_count = Tip.objects.raw("""SELECT o.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_offer o 
                                WHERE o.offer_profile_id = %s
                                ORDER BY o.date DESC;""", [request.user.perfil.id]) 
    
    company_location_count = Tip.objects.raw("""SELECT l.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_location l 
                                WHERE l.location_profile_id = %s
                                ORDER BY l.date DESC;""", [request.user.perfil.id])      
    
    person_whoami_count = Tip.objects.raw("""SELECT w.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_whoami w 
                                WHERE w.whoami_profile_id = %s
                                ORDER BY w.date DESC;""", [request.user.perfil.id]) 
    
    person_education_count = Tip.objects.raw("""SELECT e.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_education e 
                                WHERE e.education_profile_id = %s
                                ORDER BY e.date DESC;""", [request.user.perfil.id])  
    
    person_knows_count = Tip.objects.raw("""SELECT k.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_knows k 
                                WHERE k.knows_profile_id = %s
                                ORDER BY k.date DESC;""", [request.user.perfil.id]) 
    
    person_jobs_count = Tip.objects.raw("""SELECT j.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_jobs j 
                                WHERE j.jobs_profile_id = %s
                                ORDER BY j.date DESC;""", [request.user.perfil.id])
    
    person_live_count = Tip.objects.raw("""SELECT l.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_live l 
                                WHERE l.live_profile_id = %s
                                ORDER BY l.date DESC;""", [request.user.perfil.id]) 

    person_hobby_count = Tip.objects.raw("""SELECT h.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_hobby h 
                                WHERE h.hobby_profile_id = %s
                                ORDER BY h.date DESC;""", [request.user.perfil.id])  

    decks = Tip.objects.raw("""SELECT  d.id, 
                                        d.author_profile_id as fid, 
                                        d.author_user_id as user, 
                                        d.date as date,  
                                        d.author_name as name,
                                        d.deck_name as deck_name 
                                        FROM wsbodb.perfis_deck d
                                        WHERE d.author_user_id = %s
                                        ORDER BY d.date DESC;""", [request.user.id])

    notifications_count = Tip.objects.raw("""SELECT n.id, n.referenced_card,
                                            COUNT(*) as howmany
                                            FROM wsbodb.perfis_notifications n
                                            LEFT JOIN wsbodb.perfis_tip t
                                            ON t.id = n.referenced_card
                                            WHERE t.author_profile_id = %s;""", [request.user.perfil.id])
    
    return render(request, 'deck.html', locals())
    
@login_required
@csrf_exempt
def new_deck(request):
    form = DeckForm(request.POST)
    if request.method == 'POST':
        form = DeckForm(request.POST)
        if form.is_valid():     
            form.save() 

        return redirect('decks', request.user.perfil.id)
     
    else: 
        return render_to_response('decks.html', locals(), context_instance=RequestContext(request))


@login_required
@csrf_exempt
def update_deck(request, pk, template_name='decks.html'):
    c = get_object_or_404(Deck, pk=pk)
    form = DeckForm(request.POST or None, instance=c)
    if request.method=='POST':
        form.save()
        return redirect('decks', request.user.perfil.id)
    return render(request, template_name, {'c':c})
    

@login_required
@csrf_exempt
def delete_deck(request, pk):
    deck = request.GET['deck']
    
    cursor = connection.cursor()
    
    cursor.execute("""DELETE FROM wsbodb.perfis_deck
                      WHERE id=%s;""",[deck])
    
    cursor.execute("""DELETE FROM wsbodb.perfis_folder
                      WHERE folder_id=%s
                      AND profile_id=%s;""",[deck, request.user.perfil.id])
    
    row = cursor.fetchall()
    
    cursor.close()       
    
    teste = "removedfolder"
    
    response_data = { 
        'row': row, 'teste': teste
    }
    return HttpResponse(json.dumps(response_data), content_type= u'application/json')
   

@login_required
def new_tip(request):
    form = TipForm(request.POST)
    if request.method == 'POST':
        form = TipForm(request.POST, request.FILES)

        if form.is_valid():     
            if 'outdoor' in request.FILES:  
                newdoc = Tip(outdoor = request.FILES['outdoor'])
                
            form.save() 

        return redirect('map') 
     
    else: 
        return render_to_response('index.html', locals(), context_instance=RequestContext(request))


@login_required
@csrf_exempt
def update_card(request, pk, template_name='modal_edit_card.html'):
    tip = get_object_or_404(Tip, pk=pk)
    form = TipForm(request.POST or None,  request.FILES, instance=tip)
    if request.method=='POST':
        if 'outdoor' in request.FILES:  
            newdoc = Tip(outdoor = request.FILES['outdoor'])
        form.save()
        return redirect('index')
    return render(request, template_name, {'tip':tip})

@login_required
@csrf_exempt
def update_card_on_profile(request, pk, template_name='modal_edit_card.html'):
    tip = get_object_or_404(Tip, pk=pk)
    form = TipForm(request.POST or None,  request.FILES, instance=tip)
    if request.method=='POST':
        if 'outdoor' in request.FILES:  
            newdoc = Tip(outdoor = request.FILES['outdoor'])
        form.save()
        return redirect('exibir', request.user.perfil.id)
    return render(request, template_name, {'tip':tip})

@login_required
@csrf_exempt
def update_card_on_hided(request, pk, template_name='modal_edit_card.html'):
    tip = get_object_or_404(Tip, pk=pk)
    form = TipForm(request.POST or None,  request.FILES, instance=tip)
    if request.method=='POST':
        if 'outdoor' in request.FILES:  
            newdoc = Tip(outdoor = request.FILES['outdoor'])
        form.save()
        return redirect('hided', request.user.perfil.id)
    return render(request, template_name, {'tip':tip})

@login_required
@csrf_exempt
def update_card_on_deck(request, pk, template_name='modal_edit_card.html'):
    tip = get_object_or_404(Tip, pk=pk)
    d = request.META.get('HTTP_REFERER').split('//')[-1].split('/')[2]
    form = TipForm(request.POST or None,  request.FILES, instance=tip)
    if request.method=='POST':
        if 'outdoor' in request.FILES:  
            newdoc = Tip(outdoor = request.FILES['outdoor'])
        form.save()
        return redirect('deck', d)
    return render(request, template_name, {'tip':tip})


@login_required
@csrf_exempt
def update_card_on_card(request, pk, template_name='modal_edit_card_in_card.html'):
    tip = get_object_or_404(Tip, pk=pk)
    d = request.META.get('HTTP_REFERER').split('-')[-1]
    form = TipForm(request.POST or None,  request.FILES, instance=tip)
    if request.method=='POST':
        if 'outdoor' in request.FILES:  
            newdoc = Tip(outdoor = request.FILES['outdoor'])
        form.save()
        return redirect('show_tip', d)
    return render(request, template_name, {'tip':tip})


@login_required
@csrf_exempt
def update_card_on_search(request, pk, template_name='modal_edit_card.html'):
    tip = get_object_or_404(Tip, pk=pk)
    d = request.META.get('HTTP_REFERER').split('-')[-1]
    form = TipForm(request.POST or None,  request.FILES, instance=tip)
    if request.method=='POST':
        if 'outdoor' in request.FILES:  
            newdoc = Tip(outdoor = request.FILES['outdoor'])
        form.save()
        return redirect('search', d)
    return render(request, template_name, {'tip':tip})
     
        
@login_required
@csrf_exempt
def update_card_on_bysubject(request, pk, template_name='modal_edit_card.html'):
    tip = get_object_or_404(Tip, pk=pk)
    perfil = request.META.get('HTTP_REFERER').split('//')[-1].split('/')[2]
    folder = request.META.get('HTTP_REFERER').split('//')[-1].split('/')[3]
    form = TipForm(request.POST or None,  request.FILES, instance=tip)
    if request.method=='POST':
        if 'outdoor' in request.FILES:  
            newdoc = Tip(outdoor = request.FILES['outdoor'])
        form.save()
        return redirect('bysubject', perfil, folder)
    return render(request, template_name, {'tip':tip})


@login_required
@csrf_exempt
def delete_tip(request, pk):
    tip = request.GET['tip']
    
    cursor = connection.cursor()
    
    cursor.execute("""DELETE FROM wsbodb.perfis_removed
                      WHERE card_id=%s;""",[tip])
    
    cursor.execute("""DELETE FROM wsbodb.perfis_played_cards
                      WHERE card_id=%s;""",[tip])
    
    cursor.execute("""DELETE FROM wsbodb.perfis_held_cards
                      WHERE card_id=%s;""",[tip])
    
    cursor.execute("""DELETE FROM wsbodb.perfis_tip
                      WHERE id=%s;""",[tip])
    
    cursor.execute("""DELETE FROM wsbodb.perfis_favorites
                      WHERE tip_id=%s;""",[tip])
    
    cursor.execute("""DELETE FROM wsbodb.perfis_folder
                      WHERE card_id=%s
                      AND profile_id=%s;""",[tip, request.user.perfil.id])
    
    row = cursor.fetchall()
    
    cursor.close()       
    
    teste = "removedtip"
    
    response_data = { 
        'row': row, 'teste': teste
    }
    return HttpResponse(json.dumps(response_data), content_type= u'application/json')
    

@login_required
@csrf_exempt
def save_into_folder(request, pk):
    url2 = request.build_absolute_uri()
    url = url2.split('//')[-1].split('/')[0]
    deck = request.GET['deck']
    folder = request.GET['folder']
    tip = request.GET['tip']
    
    cursor = connection.cursor()
    
    cursor.execute('''INSERT INTO wsbodb.perfis_folder(card_id, profile_id, folder_id)
                      VALUES (%s, %s, %s);''',[tip, request.user.perfil.id, deck])
    
    row = cursor.fetchall()
    
    cursor.close()        

    teste = "folderedtip"
    
    response_data = { 
        'row': row, 'teste': teste
    }
    return HttpResponse(json.dumps(response_data), content_type= u'application/json')




@login_required
@csrf_exempt
def remove_from_folder(request, pk):
    url2 = request.build_absolute_uri()
    url = url2.split('//')[-1].split('/')[0]
    tip = request.GET['tip']
    
    cursor = connection.cursor()
    
    cursor.execute('''DELETE FROM wsbodb.perfis_folder
                      WHERE card_id=%s
                      AND profile_id=%s;''',[tip, request.user.perfil.id])
    
    row = cursor.fetchall()
    
    cursor.close()        

    teste = "removedfromfolder"
    
    response_data = { 
        'row': row, 'teste': teste
    }
    return HttpResponse(json.dumps(response_data), content_type= u'application/json')





@csrf_exempt
def show_tip(request, slug, pk):
    url2 = request.build_absolute_uri()
    url = url2.split('//')[-1].split('/')[0]
    r = url2.split('//')[-1].split('-')[-1]
    
    mail_to = Tip.objects.raw("""SELECT usr.id, usr.email as mailed                                 
                                 FROM wsbodb._usuarios_user usr, wsbodb.perfis_tip card 
                                 WHERE card.id=%s AND card.author_user_id = usr.id""",[r])
    
    mail_response = Tip.objects.raw("""SELECT usr.id, usr.email as mailed,
                                 perf.id as author_profile
                                 FROM wsbodb._usuarios_user usr,
                                 wsbodb.perfis_tip tip, 
                                 wsbodb.perfis_perfil perf, 
                                 wsbodb.perfis_played_cards play
                                 WHERE play.player_id = perf.id
                                 AND perf.usuario_id = usr.id
                                 AND tip.author_profile_id = perf.id
                                 AND tip.id = play.card_id
                                 GROUP BY perf.id;""")
    
    if request.user.is_authenticated():                               
        tips = Tip.objects.raw("""SELECT t.id, p.nome as name, t.content, t.slug,
                                    t.author_profile_id as author, p.type as type,
                                    p.usuario_id as profile_id, t.author_name as name,
                                    t.date, ifnull(f.id,0) as isfollowing, ifnull(fav.id,0) as isfav, 
                                    (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                    (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed,
                                    (t.author_profile_id IN (SELECT p.id FROM wsbodb.perfis_perfil p WHERE p.stealth=1)) as stealthed,
                                    (t.id IN (SELECT p.referenced_card FROM wsbodb.perfis_played_cards p WHERE p.played=1)) as waiting_hold,
                                    f.followed_id, ifnull(a.upload,0) as upload
                                    FROM wsbodb.perfis_perfil p, wsbodb.perfis_follow f,
                                    wsbodb.perfis_avatar a,
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                    ON (t.id = fav.tip_id AND fav.profile_id = %s)  
                                    WHERE t.id = %s
                                    AND t.author_profile_id = p.id
                                    AND t.author_profile_id = a.profile_id
                                    GROUP BY t.id
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""", 
                                    [request.user.perfil.id, request.user.id, request.user.id,  pk])
    else:
        tips = Tip.objects.raw("""SELECT t.id, p.nome as name, t.content, t.slug,
                                    t.author_profile_id as author,  p.type as type,
                                    p.usuario_id as profile_id, t.author_name as name,
                                    t.date, ifnull(f.id,0) as isfollowing,
                                    (t.author_profile_id IN (SELECT p.id FROM wsbodb.perfis_perfil p WHERE p.stealth=1)) as stealthed,
                                    (t.id IN (SELECT p.referenced_card FROM wsbodb.perfis_played_cards p WHERE p.played=1)) as waiting_hold,
                                    f.followed_id, ifnull(a.upload,0) as upload
                                    FROM wsbodb.perfis_perfil p, wsbodb.perfis_follow f,
                                    wsbodb.perfis_avatar a,
                                    wsbodb.perfis_tip t 
                                    WHERE t.id = %s
                                    AND t.author_profile_id = a.profile_id
                                    GROUP BY t.id
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""", [pk])

                                                                 
    is_contact = Tip.objects.raw("""SELECT t.id, f.followed_id as fid, p.nome as name, t.content, 
                                    t.author_profile_id as author, p.type as type,
                                    p.usuario_id as profile_id, t.author_name as name,
                                    t.date, ifnull(f.id,0) as isfollowing, ifnull(fav.id,0) as isfav, 
                                    f.followed_id
                                    FROM wsbodb.perfis_perfil p, wsbodb.perfis_follow f, 
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                    ON (t.id = fav.tip_id AND fav.profile_id = %s) 
                                    WHERE p.usuario_id = %s
                                    AND t.author_profile_id = f.followed_id 
                                    AND f.follower_id = %s 
                                    GROUP BY f.followed_id
                                    ORDER BY t.author_name ASC;""", [request.user.id, request.user.id, request.user.id])


    my_profile_image = Tip.objects.raw("""SELECT a.id, ifnull(a.upload,0) as upload, a.user_id
                                        FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                        ON(a.user_id = p.usuario_id)
                                        WHERE p.usuario_id = %s;""", [request.user.id])  

             
    has_profile_image = Tip.objects.raw("""SELECT a.id, a.user_id, p.type as type,
                                        ifnull(a.upload,0) as upload
                                        FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                        ON(a.profile_id = p.id)
                                        WHERE p.id = %s;""", [request.user.id])
        
    if request.user.is_authenticated():
        playable = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date, p.usuario_id as profile_id, 
                                    t.author_user_id as author_user, t.author_name as name,
                                    play.referenced_card as referenced_card,
                                    play.played as action,
                                    (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                    (t.id IN (SELECT play.card_id FROM wsbodb.perfis_played_cards play WHERE play.player_id=%s and play.referenced_card=%s)) as played
                                    FROM wsbodb.perfis_perfil p,
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_played_cards play
                                    ON (t.id = play.card_id and play.referenced_card = %s)
                                    WHERE t.author_user_id = p.usuario_id
                                    AND t.author_user_id IN ( SELECT usuario_id FROM wsbodb.perfis_perfil )
                                    AND t.author_profile_id = %s
                                    AND t.hided = 0
                                    GROUP BY t.id    
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""", 
                                    [request.user.perfil.id, request.user.perfil.id, r, r, request.user.perfil.id])
    else:
        playable = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date, p.usuario_id as profile_id, 
                                    t.author_user_id as author_user, t.author_name as name,
                                    play.referenced_card as referenced_card,
                                    play.played as action,
                                    (t.id IN (SELECT play.card_id FROM wsbodb.perfis_played_cards play WHERE play.referenced_card=%s)) as played
                                    FROM wsbodb.perfis_perfil p,
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_played_cards play
                                    ON (t.id = play.card_id and play.referenced_card = %s)
                                    WHERE t.author_user_id = p.usuario_id
                                    AND t.author_user_id IN ( SELECT usuario_id FROM wsbodb.perfis_perfil )
                                    AND t.hided = 0
                                    GROUP BY t.id    
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""", 
                                    [r, r])
        
    table = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date,
                                t.author_user_id as author_user, t.author_name as name,
                                (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed,
                                play.referenced_card as referenced_card,
                                ifnull(a.upload,0) as upload,
                                ifnull(fav.id,0) as isfav
                                FROM wsbodb.perfis_avatar a,
                                wsbodb.perfis_played_cards play,
                                wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                ON (t.id = fav.tip_id AND fav.profile_id = %s)                                
                                WHERE t.hided = 0
                                AND play.played <> 2
                                AND t.id = play.card_id
                                AND play.referenced_card = %s
                                AND t.author_profile_id = play.player_id
                                AND t.author_profile_id = a.profile_id
                                GROUP BY t.id    
                                ORDER BY ifnull(t.updated_date,t.date) DESC;""",
                                [request.user.id, request.user.id, r])
    
    if request.user.is_authenticated():
        upcards = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date,
                                    t.author_user_id as author_user, t.author_name as name,
                                    (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                    (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed,
                                    ifnull(a.upload,0) as upload,
                                    ifnull(fav.id,0) as isfav,
                                    p.referenced_card as referenced_card
                                    FROM wsbodb.perfis_avatar a,
                                    wsbodb.perfis_played_cards p,
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                    ON (t.id = fav.tip_id AND fav.profile_id = %s)                                
                                    WHERE  t.id = p.card_id
                                    AND p.referenced_card = %s
                                    AND p.played = 2
                                    AND t.author_profile_id = a.profile_id
                                    GROUP BY t.id    
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""",[request.user.perfil.id, request.user.id, request.user.id, r])
    else:
        upcards = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date,
                                    t.author_user_id as author_user, t.author_name as name,
                                    ifnull(a.upload,0) as upload,
                                    p.referenced_card as referenced_card
                                    FROM wsbodb.perfis_avatar a,
                                    wsbodb.perfis_played_cards p,
                                    wsbodb.perfis_tip t                                
                                    WHERE  t.id = p.card_id
                                    AND p.referenced_card = %s
                                    AND p.played = 2
                                    AND t.author_profile_id = a.profile_id
                                    GROUP BY t.id    
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""",
                                    [r])
        
    if request.user.is_authenticated():            
        myupcards = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date,
                                    t.author_user_id as author_user, t.author_name as name,  perfil.type as type,
                                    (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed,
                                    (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                    ifnull(a.upload,0) as upload,
                                    ifnull(fav.id,0) as isfav,
                                    p.referenced_card as referenced_card
                                    FROM wsbodb.perfis_avatar a,
                                    wsbodb.perfis_perfil perfil,
                                    wsbodb.perfis_played_cards p,
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                    ON (t.id = fav.tip_id AND fav.profile_id = %s)                                
                                    WHERE t.id = p.card_id
                                    AND p.referenced_card = %s
                                    AND p.played = 2
                                    AND t.author_profile_id = a.profile_id
                                    AND t.author_profile_id = perfil.id
                                    GROUP BY t.id    
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""",
                                    [request.user.id, request.user.perfil.id, request.user.id, r])    
    else:
        myupcards = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date,
                                    t.author_user_id as author_user, t.author_name as name,
                                    ifnull(a.upload,0) as upload,
                                    p.referenced_card as referenced_card
                                    FROM wsbodb.perfis_avatar a,
                                    wsbodb.perfis_played_cards p,
                                    wsbodb.perfis_tip t                                
                                    WHERE t.id = p.card_id
                                    AND p.referenced_card = %s
                                    AND p.played = 2
                                    AND t.author_profile_id = a.profile_id
                                    GROUP BY t.id    
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""",
                                    [r])    
         
    upcards_counting = Tip.objects.raw("""SELECT p.id, COUNT(*) as howmany,
                                (p.card_id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed
                                FROM wsbodb.perfis_played_cards p                                
                                WHERE p.referenced_card = %s
                                AND p.played = 2;""",[request.user.id, r])
       
        
    return render(request, 'card.html', {'perfis':Perfil.objects.all(), 
                                        'perfil_logado': get_perfil_logado(request),
                                        'url':url, 'tips':tips, 'mail_to':mail_to, 'mail_response':mail_response,
                                        'is_contact':is_contact, 'my_profile_image': my_profile_image,
                                        'playable': playable, 'upcards': upcards, 'table': table,
                                        'has_profile_image': has_profile_image,
                                        'myupcards': myupcards,
                                        'upcards_counting': upcards_counting })



@csrf_exempt
def show_connected(request, slug, pk):
    url2 = request.build_absolute_uri()
    url = url2.split('//')[-1].split('/')[0]
    r = url2.split('//')[-1].split('-')[-1]
    
    mail_to = Tip.objects.raw("""SELECT usr.id, usr.email as mailed                                 
                                 FROM wsbodb._usuarios_user usr, wsbodb.perfis_tip card 
                                 WHERE card.id=%s AND card.author_user_id = usr.id""",[r])
    
    mail_response = Tip.objects.raw("""SELECT usr.id, usr.email as mailed,
                                 perf.id as author_profile
                                 FROM wsbodb._usuarios_user usr,
                                 wsbodb.perfis_tip tip, 
                                 wsbodb.perfis_perfil perf, 
                                 wsbodb.perfis_played_cards play
                                 WHERE play.player_id = perf.id
                                 AND perf.usuario_id = usr.id
                                 AND tip.author_profile_id = perf.id
                                 AND tip.id = play.card_id
                                 GROUP BY perf.id;""")
    
    if request.user.is_authenticated():                               
        tips = Tip.objects.raw("""SELECT t.id, p.nome as name, t.content, t.slug,
                                    t.author_profile_id as author, p.type as type,
                                    p.usuario_id as profile_id, t.author_name as name,
                                    t.date, ifnull(f.id,0) as isfollowing, ifnull(fav.id,0) as isfav, 
                                    (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                    (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed,
                                    (t.author_profile_id IN (SELECT p.id FROM wsbodb.perfis_perfil p WHERE p.stealth=1)) as stealthed,
                                    (t.id IN (SELECT p.referenced_card FROM wsbodb.perfis_played_cards p WHERE p.played=1)) as waiting_hold,
                                    f.followed_id, ifnull(a.upload,0) as upload
                                    FROM wsbodb.perfis_perfil p, wsbodb.perfis_follow f,
                                    wsbodb.perfis_avatar a,
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                    ON (t.id = fav.tip_id AND fav.profile_id = %s)  
                                    WHERE t.id = %s
                                    AND t.author_profile_id = p.id
                                    AND t.author_profile_id = a.profile_id
                                    GROUP BY t.id
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""", 
                                    [request.user.perfil.id, request.user.id, request.user.id,  pk])
    else:
        tips = Tip.objects.raw("""SELECT t.id, p.nome as name, t.content, t.slug,
                                    t.author_profile_id as author,  p.type as type,
                                    p.usuario_id as profile_id, t.author_name as name,
                                    t.date, ifnull(f.id,0) as isfollowing,
                                    (t.author_profile_id IN (SELECT p.id FROM wsbodb.perfis_perfil p WHERE p.stealth=1)) as stealthed,
                                    (t.id IN (SELECT p.referenced_card FROM wsbodb.perfis_played_cards p WHERE p.played=1)) as waiting_hold,
                                    f.followed_id, ifnull(a.upload,0) as upload
                                    FROM wsbodb.perfis_perfil p, wsbodb.perfis_follow f,
                                    wsbodb.perfis_avatar a,
                                    wsbodb.perfis_tip t 
                                    WHERE t.id = %s
                                    AND t.author_profile_id = a.profile_id
                                    GROUP BY t.id
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""", [pk])

                                                                 
    is_contact = Tip.objects.raw("""SELECT t.id, f.followed_id as fid, p.nome as name, t.content, 
                                    t.author_profile_id as author, p.type as type,
                                    p.usuario_id as profile_id, t.author_name as name,
                                    t.date, ifnull(f.id,0) as isfollowing, ifnull(fav.id,0) as isfav, 
                                    f.followed_id
                                    FROM wsbodb.perfis_perfil p, wsbodb.perfis_follow f, 
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                    ON (t.id = fav.tip_id AND fav.profile_id = %s) 
                                    WHERE p.usuario_id = %s
                                    AND t.author_profile_id = f.followed_id 
                                    AND f.follower_id = %s 
                                    GROUP BY f.followed_id
                                    ORDER BY t.author_name ASC;""", [request.user.id, request.user.id, request.user.id])


    my_profile_image = Tip.objects.raw("""SELECT a.id, ifnull(a.upload,0) as upload, a.user_id
                                        FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                        ON(a.user_id = p.usuario_id)
                                        WHERE p.usuario_id = %s;""", [request.user.id])  

             
    has_profile_image = Tip.objects.raw("""SELECT a.id, a.user_id, p.type as type,
                                        ifnull(a.upload,0) as upload
                                        FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                        ON(a.profile_id = p.id)
                                        WHERE p.id = %s;""", [request.user.id])
        
    if request.user.is_authenticated():
        playable = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date, p.usuario_id as profile_id, 
                                    t.author_user_id as author_user, t.author_name as name,
                                    play.referenced_card as referenced_card,
                                    play.played as action,
                                    (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                    (t.id IN (SELECT play.card_id FROM wsbodb.perfis_played_cards play WHERE play.player_id=%s and play.referenced_card=%s)) as played
                                    FROM wsbodb.perfis_perfil p,
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_played_cards play
                                    ON (t.id = play.card_id and play.referenced_card = %s)
                                    WHERE t.author_user_id = p.usuario_id
                                    AND t.author_user_id IN ( SELECT usuario_id FROM wsbodb.perfis_perfil )
                                    AND t.author_profile_id = %s
                                    AND t.hided = 0
                                    GROUP BY t.id    
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""", 
                                    [request.user.perfil.id, request.user.perfil.id, r, r, request.user.perfil.id])
    else:
        playable = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date, p.usuario_id as profile_id, 
                                    t.author_user_id as author_user, t.author_name as name,
                                    play.referenced_card as referenced_card,
                                    play.played as action,
                                    (t.id IN (SELECT play.card_id FROM wsbodb.perfis_played_cards play WHERE play.referenced_card=%s)) as played
                                    FROM wsbodb.perfis_perfil p,
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_played_cards play
                                    ON (t.id = play.card_id and play.referenced_card = %s)
                                    WHERE t.author_user_id = p.usuario_id
                                    AND t.author_user_id IN ( SELECT usuario_id FROM wsbodb.perfis_perfil )
                                    AND t.hided = 0
                                    GROUP BY t.id    
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""", 
                                    [r, r])
        
    table = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date,
                                t.author_user_id as author_user, t.author_name as name,
                                (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed,
                                play.referenced_card as referenced_card,
                                ifnull(a.upload,0) as upload,
                                ifnull(fav.id,0) as isfav
                                FROM wsbodb.perfis_avatar a,
                                wsbodb.perfis_played_cards play,
                                wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                ON (t.id = fav.tip_id AND fav.profile_id = %s)                                
                                WHERE t.hided = 0
                                AND play.played <> 2
                                AND t.id = play.card_id
                                AND play.referenced_card = %s
                                AND t.author_profile_id = play.player_id
                                AND t.author_profile_id = a.profile_id
                                GROUP BY t.id    
                                ORDER BY ifnull(t.updated_date,t.date) DESC;""",
                                [request.user.id, request.user.id, r])
    
    if request.user.is_authenticated():
        upcards = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date,
                                    t.author_user_id as author_user, t.author_name as name,
                                    (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                    (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed,
                                    ifnull(a.upload,0) as upload,
                                    ifnull(fav.id,0) as isfav,
                                    p.referenced_card as referenced_card
                                    FROM wsbodb.perfis_avatar a,
                                    wsbodb.perfis_played_cards p,
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                    ON (t.id = fav.tip_id AND fav.profile_id = %s)                                
                                    WHERE  t.id = p.card_id
                                    AND p.referenced_card = %s
                                    AND p.played = 2
                                    AND t.author_profile_id = a.profile_id
                                    GROUP BY t.id    
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""",[request.user.perfil.id, request.user.id, request.user.id, r])
    else:
        upcards = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date,
                                    t.author_user_id as author_user, t.author_name as name,
                                    ifnull(a.upload,0) as upload,
                                    p.referenced_card as referenced_card
                                    FROM wsbodb.perfis_avatar a,
                                    wsbodb.perfis_played_cards p,
                                    wsbodb.perfis_tip t                                
                                    WHERE  t.id = p.card_id
                                    AND p.referenced_card = %s
                                    AND p.played = 2
                                    AND t.author_profile_id = a.profile_id
                                    GROUP BY t.id    
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""",
                                    [r])
        
    if request.user.is_authenticated():            
        myupcards = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date,
                                    t.author_user_id as author_user, t.author_name as name,  perfil.type as type,
                                    (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed,
                                    (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                    ifnull(a.upload,0) as upload,
                                    ifnull(fav.id,0) as isfav,
                                    p.referenced_card as referenced_card
                                    FROM wsbodb.perfis_avatar a,
                                    wsbodb.perfis_perfil perfil,
                                    wsbodb.perfis_played_cards p,
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                    ON (t.id = fav.tip_id AND fav.profile_id = %s)                                
                                    WHERE t.id = p.card_id
                                    AND p.referenced_card = %s
                                    AND p.played = 2
                                    AND t.author_profile_id = a.profile_id
                                    AND t.author_profile_id = perfil.id
                                    GROUP BY t.id    
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""",
                                    [request.user.id, request.user.perfil.id, request.user.id, r])    
    else:
        myupcards = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date,
                                    t.author_user_id as author_user, t.author_name as name,
                                    ifnull(a.upload,0) as upload,
                                    p.referenced_card as referenced_card
                                    FROM wsbodb.perfis_avatar a,
                                    wsbodb.perfis_played_cards p,
                                    wsbodb.perfis_tip t                                
                                    WHERE t.id = p.card_id
                                    AND p.referenced_card = %s
                                    AND p.played = 2
                                    AND t.author_profile_id = a.profile_id
                                    GROUP BY t.id    
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""",
                                    [r])    
         
    upcards_counting = Tip.objects.raw("""SELECT p.id, COUNT(*) as howmany,
                                (p.card_id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed
                                FROM wsbodb.perfis_played_cards p                                
                                WHERE p.referenced_card = %s
                                AND p.played = 2;""",[request.user.id, r])
       
        
    return render(request, 'connected.html', {'perfis':Perfil.objects.all(), 
                                        'perfil_logado': get_perfil_logado(request),
                                        'url':url, 'tips':tips, 'mail_to':mail_to, 'mail_response':mail_response,
                                        'is_contact':is_contact, 'my_profile_image': my_profile_image,
                                        'playable': playable, 'upcards': upcards, 'table': table,
                                        'has_profile_image': has_profile_image,
                                        'myupcards': myupcards,
                                        'upcards_counting': upcards_counting })
    
    

@login_required
@csrf_exempt
def remove_upload(request, pk):
    tip = request.GET['tip']
    
    cursor = connection.cursor()
    
    cursor.execute("""DELETE outdoor FROM wsbodb.perfis_tip
                      WHERE id = %s;""",[tip])
    
    row = cursor.fetchall()
    
    cursor.close()       
    
    teste = "removeupload"
    
    response_data = { 
        'row': row, 'teste': teste
    }
    return HttpResponse(json.dumps(response_data), content_type= u'application/json')


@login_required
@csrf_exempt
def delete_notification(request, pk):
    tip = request.GET['tip']
    
    cursor = connection.cursor()
    
    cursor.execute("""DELETE FROM wsbodb.perfis_notifications
                      WHERE referenced_card=%s;""",[tip])
    
    row = cursor.fetchall()
    
    cursor.close()       
    
    teste = "removednotification"
    
    response_data = { 
        'row': row, 'teste': teste
    }
    return HttpResponse(json.dumps(response_data), content_type= u'application/json')


@login_required
@csrf_exempt
def play_card(request, pk):
    card = request.GET['card']
    mail = request.GET['mail']
    r = request.META.get('HTTP_REFERER').split('//')[-1].split('-')[-1]
    from_email = settings.DEFAULT_FROM_EMAIL

    subject = u"Wasaboo - An outdoor was advertised to you!"
    message = u"See if you enjoy it at www.wasaboo.com/notifications"    
    send_mail(subject, message, from_email, [mail], fail_silently=False)    
    
    
    cursor = connection.cursor()
    
    cursor.execute('''INSERT INTO wsbodb.perfis_played_cards(card_id, player_id, referenced_card, played)
                      VALUES (%s, %s, %s, %s);''',[card, request.user.perfil.id, r, 1])
    
    cursor.execute('''INSERT INTO wsbodb.perfis_notifications(card_id, referenced_card)
                      VALUES (%s, %s);''',[card, r])
    
    row = cursor.fetchall()
    
    cursor.close()        

    teste = "played"
    
    response_data = { 
        'row': row, 'teste': teste
    }
    return HttpResponse(json.dumps(response_data), content_type= u'application/json')


def play_to(request, slug, pk):
    url2 = request.build_absolute_uri()
    url = url2.split('//')[-1].split('/')[0]
    r = url2.split('//')[-1].split('-')[-1]
    
    mail_to = Tip.objects.raw("""SELECT usr.id, usr.email as mailed                                 
                                 FROM wsbodb._usuarios_user usr, wsbodb.perfis_tip card 
                                 WHERE card.id=%s AND card.author_user_id = usr.id""",[r])
    
    mail_response = Tip.objects.raw("""SELECT usr.id, usr.email as mailed,
                                 perf.id as author_profile
                                 FROM wsbodb._usuarios_user usr,
                                 wsbodb.perfis_tip tip, 
                                 wsbodb.perfis_perfil perf, 
                                 wsbodb.perfis_played_cards play
                                 WHERE play.player_id = perf.id
                                 AND perf.usuario_id = usr.id
                                 AND tip.author_profile_id = perf.id
                                 AND tip.id = play.card_id
                                 GROUP BY perf.id;""")
    
    if request.user.is_authenticated():                               
        tips = Tip.objects.raw("""SELECT t.id, p.nome as name, t.content, t.slug,
                                    t.author_profile_id as author, p.type as type,
                                    p.usuario_id as profile_id, t.author_name as name,
                                    t.date, ifnull(f.id,0) as isfollowing, ifnull(fav.id,0) as isfav, 
                                    (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                    (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed,
                                    (t.author_profile_id IN (SELECT p.id FROM wsbodb.perfis_perfil p WHERE p.stealth=1)) as stealthed,
                                    (t.id IN (SELECT p.referenced_card FROM wsbodb.perfis_played_cards p WHERE p.played=1)) as waiting_hold,
                                    f.followed_id, ifnull(a.upload,0) as upload
                                    FROM wsbodb.perfis_perfil p, wsbodb.perfis_follow f,
                                    wsbodb.perfis_avatar a,
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                    ON (t.id = fav.tip_id AND fav.profile_id = %s)  
                                    WHERE t.id = %s
                                    AND t.author_profile_id = p.id
                                    AND t.author_profile_id = a.profile_id
                                    GROUP BY t.id
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""", 
                                    [request.user.perfil.id, request.user.id, request.user.id,  pk])
    else:
        tips = Tip.objects.raw("""SELECT t.id, p.nome as name, t.content, t.slug,
                                    t.author_profile_id as author,  p.type as type,
                                    p.usuario_id as profile_id, t.author_name as name,
                                    t.date, ifnull(f.id,0) as isfollowing,
                                    (t.author_profile_id IN (SELECT p.id FROM wsbodb.perfis_perfil p WHERE p.stealth=1)) as stealthed,
                                    (t.id IN (SELECT p.referenced_card FROM wsbodb.perfis_played_cards p WHERE p.played=1)) as waiting_hold,
                                    f.followed_id, ifnull(a.upload,0) as upload
                                    FROM wsbodb.perfis_perfil p, wsbodb.perfis_follow f,
                                    wsbodb.perfis_avatar a,
                                    wsbodb.perfis_tip t 
                                    WHERE t.id = %s
                                    AND t.author_profile_id = a.profile_id
                                    GROUP BY t.id
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""", [pk])

                                                                 
    is_contact = Tip.objects.raw("""SELECT t.id, f.followed_id as fid, p.nome as name, t.content, 
                                    t.author_profile_id as author, p.type as type,
                                    p.usuario_id as profile_id, t.author_name as name,
                                    t.date, ifnull(f.id,0) as isfollowing, ifnull(fav.id,0) as isfav, 
                                    f.followed_id
                                    FROM wsbodb.perfis_perfil p, wsbodb.perfis_follow f, 
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                    ON (t.id = fav.tip_id AND fav.profile_id = %s) 
                                    WHERE p.usuario_id = %s
                                    AND t.author_profile_id = f.followed_id 
                                    AND f.follower_id = %s 
                                    GROUP BY f.followed_id
                                    ORDER BY t.author_name ASC;""", [request.user.id, request.user.id, request.user.id])


    my_profile_image = Tip.objects.raw("""SELECT a.id, ifnull(a.upload,0) as upload, a.user_id
                                        FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                        ON(a.user_id = p.usuario_id)
                                        WHERE p.usuario_id = %s;""", [request.user.id])  

             
    has_profile_image = Tip.objects.raw("""SELECT a.id, a.user_id, p.type as type,
                                        ifnull(a.upload,0) as upload
                                        FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                        ON(a.profile_id = p.id)
                                        WHERE p.id = %s;""", [request.user.id])
        
    if request.user.is_authenticated():
        playable = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date, p.usuario_id as profile_id, 
                                    t.author_user_id as author_user, t.author_name as name,
                                    play.referenced_card as referenced_card,
                                    play.played as action,
                                    (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                    (t.id IN (SELECT play.card_id FROM wsbodb.perfis_played_cards play WHERE play.player_id=%s and play.referenced_card=%s)) as played
                                    FROM wsbodb.perfis_perfil p,
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_played_cards play
                                    ON (t.id = play.card_id and play.referenced_card = %s)
                                    WHERE t.author_user_id = p.usuario_id
                                    AND t.author_user_id IN ( SELECT usuario_id FROM wsbodb.perfis_perfil )
                                    AND t.author_profile_id = %s
                                    AND t.hided = 0
                                    GROUP BY t.id    
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""", 
                                    [request.user.perfil.id, request.user.perfil.id, r, r, request.user.perfil.id])
    else:
        playable = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date, p.usuario_id as profile_id, 
                                    t.author_user_id as author_user, t.author_name as name,
                                    play.referenced_card as referenced_card,
                                    play.played as action,
                                    (t.id IN (SELECT play.card_id FROM wsbodb.perfis_played_cards play WHERE play.referenced_card=%s)) as played
                                    FROM wsbodb.perfis_perfil p,
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_played_cards play
                                    ON (t.id = play.card_id and play.referenced_card = %s)
                                    WHERE t.author_user_id = p.usuario_id
                                    AND t.author_user_id IN ( SELECT usuario_id FROM wsbodb.perfis_perfil )
                                    AND t.hided = 0
                                    GROUP BY t.id    
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""", 
                                    [r, r])
        
    table = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date,
                                t.author_user_id as author_user, t.author_name as name,
                                (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed,
                                play.referenced_card as referenced_card,
                                ifnull(a.upload,0) as upload,
                                ifnull(fav.id,0) as isfav
                                FROM wsbodb.perfis_avatar a,
                                wsbodb.perfis_played_cards play,
                                wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                ON (t.id = fav.tip_id AND fav.profile_id = %s)                                
                                WHERE t.hided = 0
                                AND play.played <> 2
                                AND t.id = play.card_id
                                AND play.referenced_card = %s
                                AND t.author_profile_id = play.player_id
                                AND t.author_profile_id = a.profile_id
                                GROUP BY t.id    
                                ORDER BY ifnull(t.updated_date,t.date) DESC;""",
                                [request.user.id, request.user.id, r])
    
    if request.user.is_authenticated():
        upcards = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date,
                                    t.author_user_id as author_user, t.author_name as name,
                                    (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                    (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed,
                                    ifnull(a.upload,0) as upload,
                                    ifnull(fav.id,0) as isfav,
                                    p.referenced_card as referenced_card
                                    FROM wsbodb.perfis_avatar a,
                                    wsbodb.perfis_played_cards p,
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                    ON (t.id = fav.tip_id AND fav.profile_id = %s)                                
                                    WHERE  t.id = p.card_id
                                    AND p.referenced_card = %s
                                    AND p.played = 2
                                    AND t.author_profile_id = a.profile_id
                                    GROUP BY t.id    
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""",[request.user.perfil.id, request.user.id, request.user.id, r])
    else:
        upcards = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date,
                                    t.author_user_id as author_user, t.author_name as name,
                                    ifnull(a.upload,0) as upload,
                                    p.referenced_card as referenced_card
                                    FROM wsbodb.perfis_avatar a,
                                    wsbodb.perfis_played_cards p,
                                    wsbodb.perfis_tip t                                
                                    WHERE  t.id = p.card_id
                                    AND p.referenced_card = %s
                                    AND p.played = 2
                                    AND t.author_profile_id = a.profile_id
                                    GROUP BY t.id    
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""",
                                    [r])
        
    if request.user.is_authenticated():            
        myupcards = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date,
                                    t.author_user_id as author_user, t.author_name as name,  perfil.type as type,
                                    (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed,
                                    (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                    ifnull(a.upload,0) as upload,
                                    ifnull(fav.id,0) as isfav,
                                    p.referenced_card as referenced_card
                                    FROM wsbodb.perfis_avatar a,
                                    wsbodb.perfis_perfil perfil,
                                    wsbodb.perfis_played_cards p,
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                    ON (t.id = fav.tip_id AND fav.profile_id = %s)                                
                                    WHERE t.id = p.card_id
                                    AND p.referenced_card = %s
                                    AND p.played = 2
                                    AND t.author_profile_id = a.profile_id
                                    AND t.author_profile_id = perfil.id
                                    GROUP BY t.id    
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""",
                                    [request.user.id, request.user.perfil.id, request.user.id, r])    
    else:
        myupcards = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date,
                                    t.author_user_id as author_user, t.author_name as name,
                                    ifnull(a.upload,0) as upload,
                                    p.referenced_card as referenced_card
                                    FROM wsbodb.perfis_avatar a,
                                    wsbodb.perfis_played_cards p,
                                    wsbodb.perfis_tip t                                
                                    WHERE t.id = p.card_id
                                    AND p.referenced_card = %s
                                    AND p.played = 2
                                    AND t.author_profile_id = a.profile_id
                                    GROUP BY t.id    
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""",
                                    [r])    
         
    upcards_counting = Tip.objects.raw("""SELECT p.id, COUNT(*) as howmany,
                                (p.card_id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed
                                FROM wsbodb.perfis_played_cards p                                
                                WHERE p.referenced_card = %s
                                AND p.played = 2;""",[request.user.id, r])
       
        
    return render(request, 'play_card.html', {'perfis':Perfil.objects.all(), 
                                        'perfil_logado': get_perfil_logado(request),
                                        'url':url, 'tips':tips, 'mail_to':mail_to, 'mail_response':mail_response,
                                        'is_contact':is_contact, 'my_profile_image': my_profile_image,
                                        'playable': playable, 'upcards': upcards, 'table': table,
                                        'has_profile_image': has_profile_image,
                                        'myupcards': myupcards,
                                        'upcards_counting': upcards_counting })
    
    
@login_required
@csrf_exempt
def hold_card(request, pk):
    card = request.GET['card']
    mail = request.GET['mail']
    profile = request.GET['profile']
    r = request.META.get('HTTP_REFERER').split('//')[-1].split('-')[-1]
    from_email = settings.DEFAULT_FROM_EMAIL    
    
    subject = u"Wasaboo - An outdoor that you advertised was enjoyed!"
    message = u"See here at www.wasaboo.com/accepted_cards/"+profile
    
    send_mail(subject, message, from_email, [mail], fail_silently=False)
        
    cursor = connection.cursor()
    
    cursor.execute('''INSERT INTO wsbodb.perfis_held_cards(card_id, player_id, referenced_card, held)
                      VALUES (%s, %s, %s, %s);''',[card, request.user.perfil.id, r, 1])
    
    cursor.execute('''INSERT INTO wsbodb.perfis_held_cards(card_id, player_id, referenced_card, held)
                      VALUES (%s, %s, %s, %s);''',[r, request.user.perfil.id, card, 1])
    
    cursor.execute('''UPDATE wsbodb.perfis_played_cards
                      SET played = 2
                      WHERE card_id = %s
                      AND referenced_card = %s;''',[card, r])
    
    cursor.execute('''INSERT INTO wsbodb.perfis_played_cards(card_id, player_id, referenced_card, played)
                      VALUES (%s, %s, %s, %s);''',[r, request.user.perfil.id, card, 2])
    
    cursor.execute("""DELETE FROM wsbodb.perfis_notifications
                      WHERE referenced_card=%s;""",[r])
    
    row = cursor.fetchall()
    
    cursor.close()        

    teste = "held"
    
    response_data = { 
        'row': row, 'teste': teste
    }
    return HttpResponse(json.dumps(response_data), content_type= u'application/json')



def hold_to(request, slug, pk):
    url2 = request.build_absolute_uri()
    url = url2.split('//')[-1].split('/')[0]
    r = url2.split('//')[-1].split('-')[-1]
    
    mail_to = Tip.objects.raw("""SELECT usr.id, usr.email as mailed                                 
                                 FROM wsbodb._usuarios_user usr, wsbodb.perfis_tip card 
                                 WHERE card.id=%s AND card.author_user_id = usr.id""",[r])
    
    mail_response = Tip.objects.raw("""SELECT usr.id, usr.email as mailed,
                                 perf.id as author_profile
                                 FROM wsbodb._usuarios_user usr,
                                 wsbodb.perfis_tip tip, 
                                 wsbodb.perfis_perfil perf, 
                                 wsbodb.perfis_played_cards play
                                 WHERE play.player_id = perf.id
                                 AND perf.usuario_id = usr.id
                                 AND tip.author_profile_id = perf.id
                                 AND tip.id = play.card_id
                                 GROUP BY perf.id;""")
    
    if request.user.is_authenticated():                               
        tips = Tip.objects.raw("""SELECT t.id, p.nome as name, t.content, t.slug,
                                    t.author_profile_id as author, p.type as type,
                                    p.usuario_id as profile_id, t.author_name as name,
                                    t.date, ifnull(f.id,0) as isfollowing, ifnull(fav.id,0) as isfav, 
                                    (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                    (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed,
                                    (t.author_profile_id IN (SELECT p.id FROM wsbodb.perfis_perfil p WHERE p.stealth=1)) as stealthed,
                                    (t.id IN (SELECT p.referenced_card FROM wsbodb.perfis_played_cards p WHERE p.played=1)) as waiting_hold,
                                    f.followed_id, ifnull(a.upload,0) as upload
                                    FROM wsbodb.perfis_perfil p, wsbodb.perfis_follow f,
                                    wsbodb.perfis_avatar a,
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                    ON (t.id = fav.tip_id AND fav.profile_id = %s)  
                                    WHERE t.id = %s
                                    AND t.author_profile_id = p.id
                                    AND t.author_profile_id = a.profile_id
                                    GROUP BY t.id
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""", 
                                    [request.user.perfil.id, request.user.id, request.user.id,  pk])
    else:
        tips = Tip.objects.raw("""SELECT t.id, p.nome as name, t.content, t.slug,
                                    t.author_profile_id as author,  p.type as type,
                                    p.usuario_id as profile_id, t.author_name as name,
                                    t.date, ifnull(f.id,0) as isfollowing,
                                    (t.author_profile_id IN (SELECT p.id FROM wsbodb.perfis_perfil p WHERE p.stealth=1)) as stealthed,
                                    (t.id IN (SELECT p.referenced_card FROM wsbodb.perfis_played_cards p WHERE p.played=1)) as waiting_hold,
                                    f.followed_id, ifnull(a.upload,0) as upload
                                    FROM wsbodb.perfis_perfil p, wsbodb.perfis_follow f,
                                    wsbodb.perfis_avatar a,
                                    wsbodb.perfis_tip t 
                                    WHERE t.id = %s
                                    AND t.author_profile_id = a.profile_id
                                    GROUP BY t.id
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""", [pk])

                                                                 
    is_contact = Tip.objects.raw("""SELECT t.id, f.followed_id as fid, p.nome as name, t.content, 
                                    t.author_profile_id as author, p.type as type,
                                    p.usuario_id as profile_id, t.author_name as name,
                                    t.date, ifnull(f.id,0) as isfollowing, ifnull(fav.id,0) as isfav, 
                                    f.followed_id
                                    FROM wsbodb.perfis_perfil p, wsbodb.perfis_follow f, 
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                    ON (t.id = fav.tip_id AND fav.profile_id = %s) 
                                    WHERE p.usuario_id = %s
                                    AND t.author_profile_id = f.followed_id 
                                    AND f.follower_id = %s 
                                    GROUP BY f.followed_id
                                    ORDER BY t.author_name ASC;""", [request.user.id, request.user.id, request.user.id])


    my_profile_image = Tip.objects.raw("""SELECT a.id, ifnull(a.upload,0) as upload, a.user_id
                                        FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                        ON(a.user_id = p.usuario_id)
                                        WHERE p.usuario_id = %s;""", [request.user.id])  

             
    has_profile_image = Tip.objects.raw("""SELECT a.id, a.user_id, p.type as type,
                                        ifnull(a.upload,0) as upload
                                        FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                        ON(a.profile_id = p.id)
                                        WHERE p.id = %s;""", [request.user.id])
        
    if request.user.is_authenticated():
        playable = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date, p.usuario_id as profile_id, 
                                    t.author_user_id as author_user, t.author_name as name,
                                    play.referenced_card as referenced_card,
                                    play.played as action,
                                    (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                    (t.id IN (SELECT play.card_id FROM wsbodb.perfis_played_cards play WHERE play.player_id=%s and play.referenced_card=%s)) as played
                                    FROM wsbodb.perfis_perfil p,
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_played_cards play
                                    ON (t.id = play.card_id and play.referenced_card = %s)
                                    WHERE t.author_user_id = p.usuario_id
                                    AND t.author_user_id IN ( SELECT usuario_id FROM wsbodb.perfis_perfil )
                                    AND t.author_profile_id = %s
                                    AND t.hided = 0
                                    GROUP BY t.id    
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""", 
                                    [request.user.perfil.id, request.user.perfil.id, r, r, request.user.perfil.id])
    else:
        playable = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date, p.usuario_id as profile_id, 
                                    t.author_user_id as author_user, t.author_name as name,
                                    play.referenced_card as referenced_card,
                                    play.played as action,
                                    (t.id IN (SELECT play.card_id FROM wsbodb.perfis_played_cards play WHERE play.referenced_card=%s)) as played
                                    FROM wsbodb.perfis_perfil p,
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_played_cards play
                                    ON (t.id = play.card_id and play.referenced_card = %s)
                                    WHERE t.author_user_id = p.usuario_id
                                    AND t.author_user_id IN ( SELECT usuario_id FROM wsbodb.perfis_perfil )
                                    AND t.hided = 0
                                    GROUP BY t.id    
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""", 
                                    [r, r])
        
    table = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date,
                                t.author_user_id as author_user, t.author_name as name,
                                (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed,
                                play.referenced_card as referenced_card,
                                ifnull(a.upload,0) as upload,
                                ifnull(fav.id,0) as isfav
                                FROM wsbodb.perfis_avatar a,
                                wsbodb.perfis_played_cards play,
                                wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                ON (t.id = fav.tip_id AND fav.profile_id = %s)                                
                                WHERE t.hided = 0
                                AND play.played <> 2
                                AND t.id = play.card_id
                                AND play.referenced_card = %s
                                AND t.author_profile_id = play.player_id
                                AND t.author_profile_id = a.profile_id
                                GROUP BY t.id    
                                ORDER BY ifnull(t.updated_date,t.date) DESC;""",
                                [request.user.id, request.user.id, r])
    
    if request.user.is_authenticated():
        upcards = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date,
                                    t.author_user_id as author_user, t.author_name as name,
                                    (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                    (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed,
                                    ifnull(a.upload,0) as upload,
                                    ifnull(fav.id,0) as isfav,
                                    p.referenced_card as referenced_card
                                    FROM wsbodb.perfis_avatar a,
                                    wsbodb.perfis_played_cards p,
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                    ON (t.id = fav.tip_id AND fav.profile_id = %s)                                
                                    WHERE  t.id = p.card_id
                                    AND p.referenced_card = %s
                                    AND p.played = 2
                                    AND t.author_profile_id = a.profile_id
                                    GROUP BY t.id    
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""",[request.user.perfil.id, request.user.id, request.user.id, r])
    else:
        upcards = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date,
                                    t.author_user_id as author_user, t.author_name as name,
                                    ifnull(a.upload,0) as upload,
                                    p.referenced_card as referenced_card
                                    FROM wsbodb.perfis_avatar a,
                                    wsbodb.perfis_played_cards p,
                                    wsbodb.perfis_tip t                                
                                    WHERE  t.id = p.card_id
                                    AND p.referenced_card = %s
                                    AND p.played = 2
                                    AND t.author_profile_id = a.profile_id
                                    GROUP BY t.id    
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""",
                                    [r])
        
    if request.user.is_authenticated():            
        myupcards = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date,
                                    t.author_user_id as author_user, t.author_name as name,  perfil.type as type,
                                    (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed,
                                    (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                    ifnull(a.upload,0) as upload,
                                    ifnull(fav.id,0) as isfav,
                                    p.referenced_card as referenced_card
                                    FROM wsbodb.perfis_avatar a,
                                    wsbodb.perfis_perfil perfil,
                                    wsbodb.perfis_played_cards p,
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                    ON (t.id = fav.tip_id AND fav.profile_id = %s)                                
                                    WHERE t.id = p.card_id
                                    AND p.referenced_card = %s
                                    AND p.played = 2
                                    AND t.author_profile_id = a.profile_id
                                    AND t.author_profile_id = perfil.id
                                    GROUP BY t.id    
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""",
                                    [request.user.id, request.user.perfil.id, request.user.id, r])    
    else:
        myupcards = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date,
                                    t.author_user_id as author_user, t.author_name as name,
                                    ifnull(a.upload,0) as upload,
                                    p.referenced_card as referenced_card
                                    FROM wsbodb.perfis_avatar a,
                                    wsbodb.perfis_played_cards p,
                                    wsbodb.perfis_tip t                                
                                    WHERE t.id = p.card_id
                                    AND p.referenced_card = %s
                                    AND p.played = 2
                                    AND t.author_profile_id = a.profile_id
                                    GROUP BY t.id    
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""",
                                    [r])    
         
    upcards_counting = Tip.objects.raw("""SELECT p.id, COUNT(*) as howmany,
                                (p.card_id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed
                                FROM wsbodb.perfis_played_cards p                                
                                WHERE p.referenced_card = %s
                                AND p.played = 2;""",[request.user.id, r])
       
        
    return render(request, 'table.html', {'perfis':Perfil.objects.all(), 
                                        'perfil_logado': get_perfil_logado(request),
                                        'url':url, 'tips':tips, 'mail_to':mail_to, 'mail_response':mail_response,
                                        'is_contact':is_contact, 'my_profile_image': my_profile_image,
                                        'playable': playable, 'upcards': upcards, 'table': table,
                                        'has_profile_image': has_profile_image,
                                        'myupcards': myupcards,
                                        'upcards_counting': upcards_counting })


@login_required
@csrf_exempt
def buy(request, pk):
    card = request.GET['card']
    mail = request.GET['mail']
    r = request.META.get('HTTP_REFERER').split('//')[-1].split('-')[-1]
    from_email = settings.DEFAULT_FROM_EMAIL

    subject = u"Wasaboo - A CREDIT CARD OUTDOOR was sent to you! Someone bought your product!"
    message = u"Congratulations! Confirm at www.wasaboo.com/notifications"    
    send_mail(subject, message, from_email, [mail], fail_silently=False)    
    
    
    cursor = connection.cursor()
    
    cursor.execute('''INSERT INTO wsbodb.perfis_played_cards(card_id, player_id, referenced_card, played)
                      VALUES (%s, %s, %s, %s);''',[card, request.user.perfil.id, r, 1])
    
    cursor.execute('''INSERT INTO wsbodb.perfis_notifications(card_id, referenced_card)
                      VALUES (%s, %s);''',[card, r])
    
    row = cursor.fetchall()
    
    cursor.close()        

    teste = "buy"
    
    response_data = { 
        'row': row, 'teste': teste
    }
    return HttpResponse(json.dumps(response_data), content_type= u'application/json')


def buy_action(request, slug, pk):
    url2 = request.build_absolute_uri()
    url = url2.split('//')[-1].split('/')[0]
    r = url2.split('//')[-1].split('-')[-1]
    
    mail_to = Tip.objects.raw("""SELECT usr.id, usr.email as mailed                                 
                                 FROM wsbodb._usuarios_user usr, wsbodb.perfis_tip card 
                                 WHERE card.id=%s AND card.author_user_id = usr.id""",[r])
    
    mail_response = Tip.objects.raw("""SELECT usr.id, usr.email as mailed,
                                 perf.id as author_profile
                                 FROM wsbodb._usuarios_user usr,
                                 wsbodb.perfis_tip tip, 
                                 wsbodb.perfis_perfil perf, 
                                 wsbodb.perfis_played_cards play
                                 WHERE play.player_id = perf.id
                                 AND perf.usuario_id = usr.id
                                 AND tip.author_profile_id = perf.id
                                 AND tip.id = play.card_id
                                 GROUP BY perf.id;""")
    
    if request.user.is_authenticated():                               
        tips = Tip.objects.raw("""SELECT t.id, p.nome as name, t.content, t.slug,
                                    t.author_profile_id as author, p.type as type,
                                    p.usuario_id as profile_id, t.author_name as name,
                                    t.date, ifnull(f.id,0) as isfollowing, ifnull(fav.id,0) as isfav, 
                                    (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                    (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed,
                                    (t.author_profile_id IN (SELECT p.id FROM wsbodb.perfis_perfil p WHERE p.stealth=1)) as stealthed,
                                    (t.id IN (SELECT p.referenced_card FROM wsbodb.perfis_played_cards p WHERE p.played=1)) as waiting_hold,
                                    f.followed_id, ifnull(a.upload,0) as upload
                                    FROM wsbodb.perfis_perfil p, wsbodb.perfis_follow f,
                                    wsbodb.perfis_avatar a,
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                    ON (t.id = fav.tip_id AND fav.profile_id = %s)  
                                    WHERE t.id = %s
                                    AND t.author_profile_id = p.id
                                    AND t.author_profile_id = a.profile_id
                                    GROUP BY t.id
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""", 
                                    [request.user.perfil.id, request.user.id, request.user.id,  pk])
    else:
        tips = Tip.objects.raw("""SELECT t.id, p.nome as name, t.content, t.slug,
                                    t.author_profile_id as author,  p.type as type,
                                    p.usuario_id as profile_id, t.author_name as name,
                                    t.date, ifnull(f.id,0) as isfollowing,
                                    (t.author_profile_id IN (SELECT p.id FROM wsbodb.perfis_perfil p WHERE p.stealth=1)) as stealthed,
                                    (t.id IN (SELECT p.referenced_card FROM wsbodb.perfis_played_cards p WHERE p.played=1)) as waiting_hold,
                                    f.followed_id, ifnull(a.upload,0) as upload
                                    FROM wsbodb.perfis_perfil p, wsbodb.perfis_follow f,
                                    wsbodb.perfis_avatar a,
                                    wsbodb.perfis_tip t 
                                    WHERE t.id = %s
                                    AND t.author_profile_id = a.profile_id
                                    GROUP BY t.id
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""", [pk])

                                                                 
    is_contact = Tip.objects.raw("""SELECT t.id, f.followed_id as fid, p.nome as name, t.content, 
                                    t.author_profile_id as author, p.type as type,
                                    p.usuario_id as profile_id, t.author_name as name,
                                    t.date, ifnull(f.id,0) as isfollowing, ifnull(fav.id,0) as isfav, 
                                    f.followed_id
                                    FROM wsbodb.perfis_perfil p, wsbodb.perfis_follow f, 
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                    ON (t.id = fav.tip_id AND fav.profile_id = %s) 
                                    WHERE p.usuario_id = %s
                                    AND t.author_profile_id = f.followed_id 
                                    AND f.follower_id = %s 
                                    GROUP BY f.followed_id
                                    ORDER BY t.author_name ASC;""", [request.user.id, request.user.id, request.user.id])


    my_profile_image = Tip.objects.raw("""SELECT a.id, ifnull(a.upload,0) as upload, a.user_id
                                        FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                        ON(a.user_id = p.usuario_id)
                                        WHERE p.usuario_id = %s;""", [request.user.id])  

             
    has_profile_image = Tip.objects.raw("""SELECT a.id, a.user_id, p.type as type,
                                        ifnull(a.upload,0) as upload
                                        FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                        ON(a.profile_id = p.id)
                                        WHERE p.id = %s;""", [request.user.id])
        
    if request.user.is_authenticated():
        playable = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date, p.usuario_id as profile_id, 
                                    t.author_user_id as author_user, t.author_name as name,
                                    play.referenced_card as referenced_card,
                                    play.played as action,
                                    (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                    (t.id IN (SELECT play.card_id FROM wsbodb.perfis_played_cards play WHERE play.player_id=%s and play.referenced_card=%s)) as played
                                    FROM wsbodb.perfis_perfil p,
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_played_cards play
                                    ON (t.id = play.card_id and play.referenced_card = %s)
                                    WHERE t.author_user_id = p.usuario_id
                                    AND t.author_user_id IN ( SELECT usuario_id FROM wsbodb.perfis_perfil )
                                    AND t.author_profile_id = %s
                                    AND t.hided = 0
                                    GROUP BY t.id    
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""", 
                                    [request.user.perfil.id, request.user.perfil.id, r, r, request.user.perfil.id])
    else:
        playable = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date, p.usuario_id as profile_id, 
                                    t.author_user_id as author_user, t.author_name as name,
                                    play.referenced_card as referenced_card,
                                    play.played as action,
                                    (t.id IN (SELECT play.card_id FROM wsbodb.perfis_played_cards play WHERE play.referenced_card=%s)) as played
                                    FROM wsbodb.perfis_perfil p,
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_played_cards play
                                    ON (t.id = play.card_id and play.referenced_card = %s)
                                    WHERE t.author_user_id = p.usuario_id
                                    AND t.author_user_id IN ( SELECT usuario_id FROM wsbodb.perfis_perfil )
                                    AND t.hided = 0
                                    GROUP BY t.id    
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""", 
                                    [r, r])
        
    table = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date,
                                t.author_user_id as author_user, t.author_name as name,
                                (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed,
                                play.referenced_card as referenced_card,
                                ifnull(a.upload,0) as upload,
                                ifnull(fav.id,0) as isfav
                                FROM wsbodb.perfis_avatar a,
                                wsbodb.perfis_played_cards play,
                                wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                ON (t.id = fav.tip_id AND fav.profile_id = %s)                                
                                WHERE t.hided = 0
                                AND play.played <> 2
                                AND t.id = play.card_id
                                AND play.referenced_card = %s
                                AND t.author_profile_id = play.player_id
                                AND t.author_profile_id = a.profile_id
                                GROUP BY t.id    
                                ORDER BY ifnull(t.updated_date,t.date) DESC;""",
                                [request.user.id, request.user.id, r])
    
    if request.user.is_authenticated():
        upcards = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date,
                                    t.author_user_id as author_user, t.author_name as name,
                                    (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                    (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed,
                                    ifnull(a.upload,0) as upload,
                                    ifnull(fav.id,0) as isfav,
                                    p.referenced_card as referenced_card
                                    FROM wsbodb.perfis_avatar a,
                                    wsbodb.perfis_played_cards p,
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                    ON (t.id = fav.tip_id AND fav.profile_id = %s)                                
                                    WHERE  t.id = p.card_id
                                    AND p.referenced_card = %s
                                    AND p.played = 2
                                    AND t.author_profile_id = a.profile_id
                                    GROUP BY t.id    
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""",[request.user.perfil.id, request.user.id, request.user.id, r])
    else:
        upcards = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date,
                                    t.author_user_id as author_user, t.author_name as name,
                                    ifnull(a.upload,0) as upload,
                                    p.referenced_card as referenced_card
                                    FROM wsbodb.perfis_avatar a,
                                    wsbodb.perfis_played_cards p,
                                    wsbodb.perfis_tip t                                
                                    WHERE  t.id = p.card_id
                                    AND p.referenced_card = %s
                                    AND p.played = 2
                                    AND t.author_profile_id = a.profile_id
                                    GROUP BY t.id    
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""",
                                    [r])
        
    if request.user.is_authenticated():            
        myupcards = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date,
                                    t.author_user_id as author_user, t.author_name as name,  perfil.type as type,
                                    (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed,
                                    (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                    ifnull(a.upload,0) as upload,
                                    ifnull(fav.id,0) as isfav,
                                    p.referenced_card as referenced_card
                                    FROM wsbodb.perfis_avatar a,
                                    wsbodb.perfis_perfil perfil,
                                    wsbodb.perfis_played_cards p,
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                    ON (t.id = fav.tip_id AND fav.profile_id = %s)                                
                                    WHERE t.id = p.card_id
                                    AND p.referenced_card = %s
                                    AND p.played = 2
                                    AND t.author_profile_id = a.profile_id
                                    AND t.author_profile_id = perfil.id
                                    GROUP BY t.id    
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""",
                                    [request.user.id, request.user.perfil.id, request.user.id, r])    
    else:
        myupcards = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date,
                                    t.author_user_id as author_user, t.author_name as name,
                                    ifnull(a.upload,0) as upload,
                                    p.referenced_card as referenced_card
                                    FROM wsbodb.perfis_avatar a,
                                    wsbodb.perfis_played_cards p,
                                    wsbodb.perfis_tip t                                
                                    WHERE t.id = p.card_id
                                    AND p.referenced_card = %s
                                    AND p.played = 2
                                    AND t.author_profile_id = a.profile_id
                                    GROUP BY t.id    
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""",
                                    [r])    
         
    upcards_counting = Tip.objects.raw("""SELECT p.id, COUNT(*) as howmany,
                                (p.card_id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed
                                FROM wsbodb.perfis_played_cards p                                
                                WHERE p.referenced_card = %s
                                AND p.played = 2;""",[request.user.id, r])
       
        
    return render(request, 'credit_cards.html', {'perfis':Perfil.objects.all(), 
                                        'perfil_logado': get_perfil_logado(request),
                                        'url':url, 'tips':tips, 'mail_to':mail_to, 'mail_response':mail_response,
                                        'is_contact':is_contact, 'my_profile_image': my_profile_image,
                                        'playable': playable, 'upcards': upcards, 'table': table,
                                        'has_profile_image': has_profile_image,
                                        'myupcards': myupcards,
                                        'upcards_counting': upcards_counting })
      
    
@login_required
@csrf_exempt
def remove_discard(request, pk):
        card_id = request.GET['card']
        r = request.META.get('HTTP_REFERER').split('//')[-1].split('-')[-1]
        cursor = connection.cursor()
        cursor.execute("""UPDATE wsbodb.perfis_played_cards
                      SET played=1
                      WHERE card_id=%s
                      AND referenced_card=%s;""",[card_id, r]) 
        
        cursor.execute("""DELETE FROM wsbodb.perfis_played_cards
                      WHERE card_id=%s
                      AND player_id=%s
                      AND referenced_card=%s;""",[r, request.user.perfil.id, card_id]) 
        
        cursor.execute("""DELETE FROM wsbodb.perfis_held_cards
                      WHERE card_id=%s
                      AND player_id=%s
                      AND referenced_card=%s;""",[card_id, request.user.perfil.id, r]) 
        
        cursor.execute("""DELETE FROM wsbodb.perfis_held_cards
                      WHERE card_id=%s
                      AND player_id=%s
                      AND referenced_card=%s;""",[r, request.user.perfil.id, card_id])      
        remove_cards = cursor.fetchall()
        cursor.close()        
        teste = "discard"
        response_data = { 
            'removed': remove_cards, 'teste': teste
        }
        return HttpResponse(json.dumps(response_data), content_type= u'application/json')
    
    
@login_required
@csrf_exempt
def remove_harassment(request, pk):
        card_id = request.GET['card']
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO wsbodb.perfis_removed (card_id, profile_id, removed_by) 
                          VALUES (%s,%s,%s);''',[card_id, request.user.id, 1])
        cursor.execute('''DELETE FROM wsbodb.perfis_favorites 
                          WHERE tip_id=%s
                          AND profile_id=%s;''',[card_id, request.user.id])
        cursor.execute('''DELETE FROM wsbodb.perfis_folder
                      WHERE card_id=%s
                      AND profile_id=%s;''',[card_id, request.user.perfil.id])
        cursor.execute("""DELETE FROM wsbodb.perfis_played_cards
                      WHERE card_id=%s
                      AND player_id=%s;""",[card_id, request.user.perfil.id])  
        cursor.execute("""DELETE FROM wsbodb.perfis_held_cards
                      WHERE card_id=%s
                      AND player_id=%s;""",[card_id, request.user.perfil.id])        
        remove_cards = cursor.fetchall()
        cursor.close()        
        teste = "harassment"
        response_data = { 
            'removed': remove_cards, 'teste': teste
        }
        return HttpResponse(json.dumps(response_data), content_type= u'application/json')
    
@login_required
@csrf_exempt
def remove_spam(request, pk):
        card_id = request.GET['card']
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO wsbodb.perfis_removed (card_id, profile_id, removed_by) 
                          VALUES (%s,%s,%s);''',[card_id, request.user.id, 2])
        cursor.execute('''DELETE FROM wsbodb.perfis_favorites 
                          WHERE tip_id=%s
                          AND profile_id=%s;''',[card_id, request.user.id])
        cursor.execute('''DELETE FROM wsbodb.perfis_folder
                      WHERE card_id=%s
                      AND profile_id=%s;''',[card_id, request.user.perfil.id])
        cursor.execute("""DELETE FROM wsbodb.perfis_played_cards
                      WHERE card_id=%s                      
                      AND player_id=%s;""",[card_id, request.user.perfil.id])  
        cursor.execute("""DELETE FROM wsbodb.perfis_held_cards
                      WHERE card_id=%s
                      AND player_id=%s;""",[card_id, request.user.perfil.id])                         
        remove_cards = cursor.fetchall()
        cursor.close()        
        teste = "spam"
        response_data = { 
            'removed': remove_cards, 'teste': teste
        }
        return HttpResponse(json.dumps(response_data), content_type= u'application/json')  
    
    
@login_required
@csrf_exempt
def remove_plagiarism(request, pk):
        card_id = request.GET['card']
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO wsbodb.perfis_removed (card_id, profile_id, removed_by) 
                          VALUES (%s,%s,%s);''',[card_id, request.user.id, 3])
        cursor.execute('''DELETE FROM wsbodb.perfis_favorites 
                          WHERE tip_id=%s
                          AND profile_id=%s;''',[card_id, request.user.id])
        cursor.execute('''DELETE FROM wsbodb.perfis_folder
                      WHERE card_id=%s
                      AND profile_id=%s;''',[card_id, request.user.perfil.id]) 
        cursor.execute("""DELETE FROM wsbodb.perfis_played_cards
                      WHERE card_id=%s
                      AND player_id=%s;""",[card_id, request.user.perfil.id])  
        cursor.execute("""DELETE FROM wsbodb.perfis_held_cards
                      WHERE card_id=%s
                      AND player_id=%s;""",[card_id, request.user.perfil.id])                        
        remove_cards = cursor.fetchall()
        cursor.close()        
        teste = "plagiarism"
        response_data = { 
            'removed': remove_cards, 'teste': teste
        }
        return HttpResponse(json.dumps(response_data), content_type= u'application/json')
    
    
@login_required
@csrf_exempt
def remove_joke(request, pk):
        card_id = request.GET['card']
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO wsbodb.perfis_removed (card_id, profile_id, removed_by) 
                          VALUES (%s,%s,%s);''',[card_id, request.user.id, 4])
        cursor.execute('''DELETE FROM wsbodb.perfis_favorites 
                          WHERE tip_id=%s
                          AND profile_id=%s;''',[card_id, request.user.id])
        cursor.execute('''DELETE FROM wsbodb.perfis_folder
                      WHERE card_id=%s
                      AND profile_id=%s;''',[card_id, request.user.perfil.id]) 
        
        cursor.execute("""DELETE FROM wsbodb.perfis_played_cards
                      WHERE card_id=%s
                      AND player_id=%s;""",[card_id, request.user.perfil.id])  
        cursor.execute("""DELETE FROM wsbodb.perfis_held_cards
                      WHERE card_id=%s
                      AND player_id=%s;""",[card_id, request.user.perfil.id])                        
        remove_cards = cursor.fetchall()
        cursor.close()        
        teste = "joke"
        response_data = { 
            'removed': remove_cards, 'teste': teste
        }
        return HttpResponse(json.dumps(response_data), content_type= u'application/json')
    
    
@login_required
@csrf_exempt
def remove_out(request, pk):
        card_id = request.GET['card']
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO wsbodb.perfis_removed (card_id, profile_id, removed_by) 
                          VALUES (%s,%s,%s);''',[card_id, request.user.id, 5])
        cursor.execute('''DELETE FROM wsbodb.perfis_favorites 
                          WHERE tip_id=%s
                          AND profile_id=%s;''',[card_id, request.user.id])
        cursor.execute('''DELETE FROM wsbodb.perfis_folder
                      WHERE card_id=%s
                      AND profile_id=%s;''',[card_id, request.user.perfil.id])   
        cursor.execute("""DELETE FROM wsbodb.perfis_played_cards
                      WHERE card_id=%s
                      AND player_id=%s;""",[card_id, request.user.perfil.id])  
        cursor.execute("""DELETE FROM wsbodb.perfis_held_cards
                      WHERE card_id=%s
                      AND player_id=%s;""",[card_id, request.user.perfil.id])                    
        remove_cards = cursor.fetchall()
        cursor.close()        
        teste = "out"
        response_data = { 
            'removed': remove_cards, 'teste': teste
        }
        return HttpResponse(json.dumps(response_data), content_type= u'application/json') 
    
    
@login_required
@csrf_exempt
def remove_written(request, pk):
        card_id = request.GET['card']
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO wsbodb.perfis_removed (card_id, profile_id, removed_by) 
                          VALUES (%s,%s,%s);''',[card_id, request.user.id, 6])
        cursor.execute('''DELETE FROM wsbodb.perfis_favorites 
                          WHERE tip_id=%s
                          AND profile_id=%s;''',[card_id, request.user.id])
        cursor.execute('''DELETE FROM wsbodb.perfis_folder
                      WHERE card_id=%s
                      AND profile_id=%s;''',[card_id, request.user.perfil.id])  
        cursor.execute("""DELETE FROM wsbodb.perfis_played_cards
                      WHERE card_id=%s
                      AND player_id=%s;""",[card_id, request.user.perfil.id])  
        cursor.execute("""DELETE FROM wsbodb.perfis_held_cards
                      WHERE card_id=%s
                      AND player_id=%s;""",[card_id, request.user.perfil.id])                       
        remove_cards = cursor.fetchall()
        cursor.close()        
        teste = "written"
        response_data = { 
            'removed': remove_cards, 'teste': teste
        }
        return HttpResponse(json.dumps(response_data), content_type= u'application/json') 
    
@login_required
@csrf_exempt
def remove_fake(request, pk):
        card_id = request.GET['card']
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO wsbodb.perfis_removed (card_id, profile_id, removed_by) 
                          VALUES (%s,%s,%s);''',[card_id, request.user.id, 7])
        cursor.execute('''DELETE FROM wsbodb.perfis_favorites 
                          WHERE tip_id=%s
                          AND profile_id=%s;''',[card_id, request.user.id])
        cursor.execute('''DELETE FROM wsbodb.perfis_folder
                      WHERE card_id=%s
                      AND profile_id=%s;''',[card_id, request.user.perfil.id])  
        cursor.execute("""DELETE FROM wsbodb.perfis_played_cards
                      WHERE card_id=%s
                      AND player_id=%s;""",[card_id, request.user.perfil.id])  
        cursor.execute("""DELETE FROM wsbodb.perfis_held_cards
                      WHERE card_id=%s
                      AND player_id=%s;""",[card_id, request.user.perfil.id])                       
        remove_cards = cursor.fetchall()
        cursor.close()        
        teste = "fake"
        response_data = { 
            'removed': remove_cards, 'teste': teste
        }
        return HttpResponse(json.dumps(response_data), content_type= u'application/json') 
    
    
@login_required
@csrf_exempt
def remove_image(request, pk):
        card_id = request.GET['card']
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO wsbodb.perfis_removed (card_id, profile_id, removed_by) 
                          VALUES (%s,%s,%s);''',[card_id, request.user.id, 8])
        cursor.execute('''DELETE FROM wsbodb.perfis_favorites 
                          WHERE tip_id=%s
                          AND profile_id=%s;''',[card_id, request.user.id])
        cursor.execute('''DELETE FROM wsbodb.perfis_folder
                      WHERE card_id=%s
                      AND profile_id=%s;''',[card_id, request.user.perfil.id])    
        cursor.execute("""DELETE FROM wsbodb.perfis_played_cards
                      WHERE card_id=%s
                      AND player_id=%s;""",[card_id, request.user.perfil.id])  
        cursor.execute("""DELETE FROM wsbodb.perfis_held_cards
                      WHERE card_id=%s
                      AND player_id=%s;""",[card_id, request.user.perfil.id])                     
        remove_cards = cursor.fetchall()
        cursor.close()        
        teste = "image"
        response_data = { 
            'removed': remove_cards, 'teste': teste
        }
        return HttpResponse(json.dumps(response_data), content_type= u'application/json')  
    
    
@login_required
@csrf_exempt
def remove_incorrect(request, pk):
        card_id = request.GET['card']
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO wsbodb.perfis_removed (card_id, profile_id, removed_by) 
                          VALUES (%s,%s,%s);''',[card_id, request.user.id, 9])
        cursor.execute('''DELETE FROM wsbodb.perfis_favorites 
                          WHERE tip_id=%s
                          AND profile_id=%s;''',[card_id, request.user.id])
        cursor.execute('''DELETE FROM wsbodb.perfis_folder
                      WHERE card_id=%s
                      AND profile_id=%s;''',[card_id, request.user.perfil.id])    
        cursor.execute("""DELETE FROM wsbodb.perfis_played_cards
                      WHERE card_id=%s
                      AND player_id=%s;""",[card_id, request.user.perfil.id])  
        cursor.execute("""DELETE FROM wsbodb.perfis_held_cards
                      WHERE card_id=%s
                      AND player_id=%s;""",[card_id, request.user.perfil.id])                     
        remove_cards = cursor.fetchall()
        cursor.close()        
        teste = "incorrect"
        response_data = { 
            'removed': remove_cards, 'teste': teste
        }
        return HttpResponse(json.dumps(response_data), content_type= u'application/json')   
    
    
@login_required
@csrf_exempt
def restore(request, pk):
        card_id = request.GET['card']
        cursor = connection.cursor()
        cursor.execute('''DELETE FROM wsbodb.perfis_removed 
                          WHERE card_id = %s
                          AND profile_id = %s;''',[card_id, request.user.id])
        restored_cards = cursor.fetchall()
        cursor.close()        
        teste = "restored"
        response_data = { 
            'restored': restored_cards, 'teste': teste
        }
        return HttpResponse(json.dumps(response_data), content_type= u'application/json')                               
                                

@login_required
@csrf_exempt
def who_accepted(request, pk):
    perfil = Perfil.objects.get(id=request.user.perfil.id)
    perfil_logado = get_perfil_logado(request)
    
    url2 = request.build_absolute_uri()
    url = url2.split('//')[-1].split('/')[0]
    pid = url2.split('//')[-1].split('/')[-2]
    
    who = Tip.objects.raw("""SELECT t.id, p.nome as name, t.content, 
                                    t.author_profile_id as author, p.type as type,
                                    p.usuario_id as profile_id, t.author_name as name,
                                    j.jobs_profile_id, j.company,
                                    t.date, ifnull(f.id,0) as isfollowing, ifnull(fav.id,0) as isfav,
                                    (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                    (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed,
                                    (t.author_profile_id IN (SELECT p.id FROM wsbodb.perfis_perfil p WHERE p.stealth=1 AND t.author_profile_id=%s)) as stealthed,
                                    (t.id IN (SELECT n.referenced_card FROM wsbodb.perfis_notifications n WHERE n.card_id NOT IN (SELECT re.card_id FROM wsbodb.perfis_removed re) AND t.author_profile_id=%s)) as notified,
                                    (t.id IN (SELECT p.referenced_card FROM wsbodb.perfis_played_cards p WHERE p.player_id = %s AND p.played = 2)) as accepted_by,
                                    f.followed_id, ifnull(a.upload,0) as upload, t.outdoor
                                    FROM wsbodb.perfis_perfil p, wsbodb.perfis_follow f,
                                    wsbodb.perfis_jobs j,
                                    wsbodb.perfis_avatar a, wsbodb.perfis_played_cards play,
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                    ON (t.id = fav.tip_id AND fav.profile_id = %s) 
                                    WHERE p.usuario_id = %s
                                    AND f.follower_id = %s 
                                    AND t.author_profile_id = a.profile_id
                                    AND t.id = play.referenced_card
                                    AND play.card_id = %s
                                    AND j.jobs_profile_id = t.author_profile_id
                                    GROUP BY play.referenced_card
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""", 
                                    [request.user.perfil.id, request.user.id, request.user.perfil.id, request.user.perfil.id, request.user.perfil.id, request.user.id, request.user.id, request.user.id, pid])
                                                              
    is_contact = Tip.objects.raw("""SELECT t.id, f.followed_id as fid, p.nome as name, t.content, 
                                    t.author_profile_id as author, p.type as type,
                                    p.usuario_id as profile_id, t.author_name as name,
                                    t.date, ifnull(f.id,0) as isfollowing, ifnull(fav.id,0) as isfav, 
                                    f.followed_id
                                    FROM wsbodb.perfis_perfil p, wsbodb.perfis_follow f, 
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                    ON (t.id = fav.tip_id AND fav.profile_id = %s) 
                                    WHERE p.usuario_id = %s
                                    AND t.author_profile_id = f.followed_id 
                                    AND f.follower_id = %s 
                                    GROUP BY f.followed_id
                                    ORDER BY t.author_name ASC;""", [request.user.id, request.user.id, request.user.id])

    
    my_profile_image = Tip.objects.raw("""SELECT a.id, a.upload as upload, a.user_id
                                        FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                        ON(a.user_id = p.usuario_id)
                                        WHERE p.usuario_id = %s;""", [request.user.id])  
    
    
    notifications_count = Tip.objects.raw("""SELECT n.id, n.referenced_card,
                                            COUNT(*) as howmany
                                            FROM wsbodb.perfis_notifications n
                                            LEFT JOIN wsbodb.perfis_tip t
                                            ON t.id = n.referenced_card
                                            WHERE n.card_id NOT IN (SELECT re.card_id FROM wsbodb.perfis_removed re) 
                                            AND t.author_profile_id = %s
                                            GROUP BY n.referenced_card;""", [request.user.perfil.id])
                 
    notifications_all = Tip.objects.raw("""SELECT n.id, n.referenced_card,
                                            COUNT(*) as howmany
                                            FROM wsbodb.perfis_notifications n
                                            LEFT JOIN wsbodb.perfis_tip t
                                            ON t.id = n.referenced_card
                                            WHERE n.card_id NOT IN (SELECT re.card_id FROM wsbodb.perfis_removed re) 
                                            AND t.author_profile_id = %s;""", [request.user.perfil.id])
        
    return render(request, 'who_accepted.html', locals())


@login_required
@csrf_exempt
def favorite_tips(request, pk):
        #tip_id = request.GET.get("favoriteTip", pk)
        tip_id = request.GET['tip']
        author = request.GET['author']
        
        cursor = connection.cursor()
        
        cursor.execute('''INSERT INTO wsbodb.perfis_favorites (tip_id, profile_id, favorite) 
                          VALUES (%s,%s,%s);''',[tip_id, request.user.id, author])

        
        favorite_tips = cursor.fetchall()
        
        cursor.close()        

        teste = "yes"
        
        response_data = { 
            'favorites': favorite_tips, 'teste': teste
        }
        return HttpResponse(json.dumps(response_data), content_type= u'application/json')


@login_required
@csrf_exempt
def desfavorite_tips(request, pk):
        #tip_id = request.GET.get("favoriteTip", pk)
        tip_id = request.GET['tip']
        
        cursor = connection.cursor()
        
        cursor.execute('''DELETE FROM wsbodb.perfis_favorites 
                          WHERE tip_id=%s
                          AND profile_id=%s;''',[tip_id, request.user.id])
        
        favorite_tips = cursor.fetchall()
        
        cursor.close()   
        
        teste = "no"
        
        response_data = { 
            'favorites': favorite_tips, 'teste': teste
        }
        return HttpResponse(json.dumps(response_data), content_type= u'application/json')    


   
    
@login_required
@csrf_exempt
def hide_tips(request, pk):
        hided_tip_id = request.GET.get("hiddenTip", pk)
        
        cursor = connection.cursor()
        
        cursor.execute("""UPDATE wsbodb.perfis_tip t
                          SET t.hided = 1
                          WHERE t.id="""+hided_tip_id+"""
                          AND t.author_user_id=%s;""",[request.user.id])
        
        hided_tips = cursor.fetchall()
        teste = "hide"
        
        response_data = { 
            'hided': hided_tips, 'teste': teste
        }

        return HttpResponse(json.dumps(response_data), content_type= u'application/json')
    

@login_required
@csrf_exempt
def show_tips(request, pk):
        hided_tip_id = request.GET.get("pbhiddenTip", pk)
        
        cursor = connection.cursor()
        
        cursor.execute("""UPDATE wsbodb.perfis_tip t
                          SET t.hided = 0
                          WHERE t.id="""+hided_tip_id+"""
                          AND t.author_user_id=%s;""",[request.user.id])
        
        show_tips = cursor.fetchall()
        teste = "show"
        
        response_data = { 
            'show': show_tips, 'teste': teste
        }

        return HttpResponse(json.dumps(response_data), content_type= u'application/json')
      

@login_required
@csrf_exempt
def like_tips(request,pk):
        tip_id = request.GET.get("favoriteTip", pk)
        
        cursor = connection.cursor()
        
        cursor.execute("""SELECT   COUNT(tip_id) as likes 
                                   FROM wsbodb.perfis_favorites f, wsbodb.perfis_tip t
                                   WHERE f.tip_id = t.id
                                   AND f.tip_id = """+ str(tip_id) +"""
                                   AND t.author_user_id = %s;""", [request.user.id])
        
        like_tips = cursor.fetchall()
        

        
        cursor.close()        

        teste = "yes"
        
        response_data = { 
            'likes': like_tips, 'teste': teste
        }
        #print >>sys.stderr, teste
        return HttpResponse(json.dumps(response_data), content_type= u'application/json')


@login_required
@csrf_exempt
def myfeed_on(request, pk):
        profile_id = request.GET['profile']
        
        cursor = connection.cursor()
        
        cursor.execute('''UPDATE wsbodb.perfis_perfil 
                          SET map=0
                          WHERE id=%s;''',[profile_id])
                
        map_on = cursor.fetchall()
        
        cursor.close()        

        teste = "on"
        
        
        response_data = { 
            'teste': teste
        }
        return HttpResponse(json.dumps(response_data), content_type= u'application/json')
        return redirect('index')
    

@login_required
@csrf_exempt
def world_on(request, pk):
        profile_id = request.GET['profile']
        
        cursor = connection.cursor()
        
        cursor.execute('''UPDATE wsbodb.perfis_perfil 
                          SET map=0
                          WHERE id=%s;''',[profile_id])
                
        map_on = cursor.fetchall()
        
        cursor.close()        

        teste = "on"
        
        response_data = { 
            'teste': teste
        }
        return HttpResponse(json.dumps(response_data), content_type= u'application/json')
       
@login_required
@csrf_exempt
def world_off(request, pk):
        profile_id = request.GET['profile']
        
        cursor = connection.cursor()
        
        cursor.execute('''UPDATE wsbodb.perfis_perfil 
                          SET map=9
                          WHERE id=%s;''',[profile_id])
                
        map_on = cursor.fetchall()
        
        cursor.close()        

        teste = "off"
        
        response_data = { 
            'teste': teste
        }
        return HttpResponse(json.dumps(response_data), content_type= u'application/json')
    
    
@csrf_exempt
def map_init(request):
    perfil = Perfil.objects.get(id=request.user.perfil.id)
    
    url2 = request.build_absolute_uri()
    url = url2.split('//')[-1].split('/')[0]
    
   
    tips = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date, c.to_perfil_id as destiny, 
                            c.from_perfil_id as origin, p.usuario_id as profile_id, p.type as type, ifnull(f.id,0) as isfav
                            FROM wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites f ON (t.id = f.tip_id AND f.profile_id = %s), 
                            wsbodb.perfis_perfil_contatos c, wsbodb.perfis_perfil p
                            WHERE c.from_perfil_id = t.author_profile_id
                            AND c.to_perfil_id = p.id
                            AND p.usuario_id = %s
                            ORDER BY t.date DESC;""", [request.user.id, request.user.id])

                                    
    following = Tip.objects.raw("""SELECT t.id, p.nome as name, t.content,
                                    t.author_profile_id as author, p.type as type,
                                    p.usuario_id as profile_id, t.author_name as name,
                                    t.date, ifnull(f.id,0) as isfollowing, ifnull(fav.id,0) as isfav,
                                    (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                    (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed,
                                    (t.author_profile_id IN (SELECT p.id FROM wsbodb.perfis_perfil p WHERE p.stealth=1 AND t.author_profile_id=%s)) as stealthed,
                                    (t.id IN (SELECT n.referenced_card FROM wsbodb.perfis_notifications n WHERE n.card_id NOT IN (SELECT re.card_id FROM wsbodb.perfis_removed re WHERE re.profile_id=%s) AND t.author_profile_id=%s)) as notified,
                                    f.followed_id, ifnull(a.upload,0) as upload, t.outdoor
                                    FROM wsbodb.perfis_perfil p, wsbodb.perfis_follow f,
                                    wsbodb.perfis_avatar a, 
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                    ON (t.id = fav.tip_id AND fav.profile_id = %s) 
                                    WHERE p.usuario_id = %s
                                    AND t.author_profile_id = f.followed_id
                                    AND f.follower_id = %s 
                                    AND t.hided = 0
                                    AND f.followed_id = a.profile_id
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""", 
                                    [request.user.perfil.id, request.user.id, request.user.perfil.id, request.user.id, request.user.perfil.id, request.user.id, request.user.id, request.user.id])
                                                              
    is_contact = Tip.objects.raw("""SELECT t.id, f.followed_id as fid, p.nome as name, t.content, 
                                    t.author_profile_id as author, p.type as type,
                                    p.usuario_id as profile_id, t.author_name as name,
                                    t.date, ifnull(f.id,0) as isfollowing, ifnull(fav.id,0) as isfav, 
                                    f.followed_id
                                    FROM wsbodb.perfis_perfil p, wsbodb.perfis_follow f, 
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                    ON (t.id = fav.tip_id AND fav.profile_id = %s) 
                                    WHERE p.usuario_id = %s
                                    AND t.author_profile_id = f.followed_id 
                                    AND f.follower_id = %s 
                                    GROUP BY f.followed_id
                                    ORDER BY t.author_name ASC;""", [request.user.id, request.user.id, request.user.id])

    
    my_profile_image = Tip.objects.raw("""SELECT a.id, a.upload as upload, a.user_id
                                        FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                        ON(a.user_id = p.usuario_id)
                                        WHERE p.usuario_id = %s;""", [request.user.id])  
    
    
    return render(request, 'index.html', {'perfil':perfil, 'perfis':Perfil.objects.all(), 
                                          'perfil_logado': get_perfil_logado(request), 'tips': tips,
                                          'url':url, 'following':following,
                                          'is_contact':is_contact, 'my_profile_image': my_profile_image })


@csrf_exempt
def mapping(request, pk):
        tip = request.GET['tip']
        
        cursor = connection.cursor()
        
        cursor.execute("""SELECT COUNT(t.id) as mappedcards 
                                 FROM wsbodb.perfis_tip t
                                 WHERE t.author_user_id=%s;""",[request.user.id])
        mappedcards = cursor.fetchall()
        
        
        cursor.execute('''SELECT t.lat as lat
                        FROM wsbodb.perfis_tip t
                        WHERE t.id=%s;''',[tip])
        lat = cursor.fetchall()
        
        
        cursor.execute('''SELECT t.lng as lng
                        FROM wsbodb.perfis_tip t
                        WHERE t.id=%s;''',[tip])
        lng = cursor.fetchall()
        
        
        cursor.execute('''SELECT t.content as cnt
                        FROM wsbodb.perfis_tip t
                        WHERE t.id=%s;''',[tip])
        cnt = cursor.fetchall()
        
        
        cursor.execute('''SELECT t.reference as ref
                        FROM wsbodb.perfis_tip t
                        WHERE t.id=%s;''',[tip])
        ref = cursor.fetchall()
        
        
        cursor.execute('''SELECT t.slug as slg
                        FROM wsbodb.perfis_tip t
                        WHERE t.id=%s;''',[tip])
        slg = cursor.fetchall()
        
        
        cursor.execute('''SELECT t.id as idc
                        FROM wsbodb.perfis_tip t
                        WHERE t.id=%s;''',[tip])
        idc = cursor.fetchall()
        
        
        cursor.execute('''SELECT t.outdoor as img
                        FROM wsbodb.perfis_tip t
                        WHERE t.id=%s;''',[tip])
        img = cursor.fetchall()
        
        
        cursor.execute('''SELECT a.upload as ava
                        FROM wsbodb.perfis_tip t,
                        wsbodb.perfis_avatar a
                        WHERE t.id=%s
                        AND a.profile_id=t.author_profile_id;''',[tip])
        ava = cursor.fetchall()
        
        
        cursor.execute('''SELECT t.author_name as nme
                        FROM wsbodb.perfis_tip t
                        WHERE t.id=%s;''',[tip])
        nme = cursor.fetchall()
        
        
        cursor.close()        

        teste = "yes"
        
        response_data = { 
            'mappedcards': mappedcards, 'teste': teste, 'lat':lat, 'lng':lng,
            'cnt': cnt, 'slg': slg, 'idc': idc, 'img': img, 'ava': ava, 'nme': nme, 'ref': ref
        }

        return HttpResponse(json.dumps(response_data), content_type= u'application/json')
        


@login_required
@csrf_exempt
def map_on(request, pk):
        profile_id = request.GET['profile']
        
        cursor = connection.cursor()
        
        cursor.execute('''UPDATE wsbodb.perfis_perfil 
                          SET map=1
                          WHERE id=%s;''',[profile_id])
                
        map_on = cursor.fetchall()
        
        cursor.close()        

        teste = "on"
        
        
        response_data = { 
            'teste': teste
        }
        return HttpResponse(json.dumps(response_data), content_type= u'application/json')
        return redirect('index')
    
      
@login_required
@csrf_exempt
def map_off(request, pk):
        profile_id = request.GET['profile']
        
        cursor = connection.cursor()
        
        cursor.execute('''UPDATE wsbodb.perfis_perfil 
                          SET map=0
                          WHERE id=%s;''',[profile_id])

        map_on = cursor.fetchall()
        
        cursor.close()        

        teste = "off"
        
        response_data = { 
            'teste': teste
        }
        return HttpResponse(json.dumps(response_data), content_type= u'application/json')
        

@login_required
@csrf_exempt
def fys_on(request, pk):
        profile_id = request.GET['profile']
        
        cursor = connection.cursor()
        
        cursor.execute('''UPDATE wsbodb.perfis_perfil 
                          SET map=2
                          WHERE id=%s;''',[profile_id])
                
        map_on = cursor.fetchall()
        
        cursor.close()        

        teste = "on"
        
        
        response_data = { 
            'teste': teste
        }
        return HttpResponse(json.dumps(response_data), content_type= u'application/json')
        return redirect('index')
    
    
@login_required
@csrf_exempt
def adidas_on(request, pk):
        profile_id = request.GET['profile']
        
        cursor = connection.cursor()
        
        cursor.execute('''UPDATE wsbodb.perfis_perfil 
                          SET map=3
                          WHERE id=%s;''',[profile_id])
                
        map_on = cursor.fetchall()
        
        cursor.close()        

        teste = "on"
        
        
        response_data = { 
            'teste': teste
        }
        return HttpResponse(json.dumps(response_data), content_type= u'application/json') 
        return redirect('index')   
     


@csrf_exempt
def upcards_cards(request,pk):
        card_id = request.GET['card']
        
        cursor = connection.cursor()
        
        cursor.execute("""SELECT   COUNT(card_id) as upcards 
                                   FROM wsbodb.perfis_played_cards p, wsbodb.perfis_tip t
                                   WHERE p.referenced_card = t.id
                                   AND p.referenced_card = %s
                                   AND p.played = 2;""", [card_id])
        
        upcarded = cursor.fetchall()
                
        cursor.close()        

        teste = "upcard"
        
        response_data = { 
            'upcards': upcarded, 'teste': teste
        }
        #print >>sys.stderr, teste
        return HttpResponse(json.dumps(response_data), content_type= u'application/json') 


@login_required
@csrf_exempt
def follow_tips(request, pk):
        followed_user = request.GET.get("following", pk)
        
        cursor = connection.cursor()
        
        cursor.execute('''INSERT INTO wsbodb.perfis_follow (follower_id, followed_id) 
                  VALUES (%s, %s);''',[request.user.id, followed_user])

        
        followed_tips = cursor.fetchall()
        teste = "follow"
        
        response_data = { 
            'followed': followed_tips, 'teste': teste
        }

        return HttpResponse(json.dumps(response_data), content_type= u'application/json')
    
    
@login_required
@csrf_exempt
def no_follow_tips(request, pk):
        nofollowed_user = request.GET.get("nofollowing", pk)
        
        cursor = connection.cursor()
        
        cursor.execute('''DELETE FROM wsbodb.perfis_follow 
                          WHERE follower_id = %s
                          AND followed_id = %s;''',[request.user.id, nofollowed_user])

        
        no_followed_tips = cursor.fetchall()
        
        cursor.close()
        
        teste = "nofollow"
        
        response_data = { 
            'nofollowed': no_followed_tips, 'teste': teste
        }

        return HttpResponse(json.dumps(response_data), content_type= u'application/json')   
    

@login_required
@csrf_exempt
def show_references(request, pk):
    tip = request.POST.get('tip')

    cursor = connection.cursor()
    cursor.execute('''SELECT  t.reference 
					  FROM wsbodb.perfis_tip t
					  WHERE t.id = %s;''', tip)
    editable = cursor.fetchall()
    cursor.close()        
    teste = "showreferences"
    response_data = { 
        'editable': editable, 'teste': teste
    }
    return HttpResponse(json.dumps(response_data), content_type= u'application/json')
   
@login_required
@csrf_exempt
def show_content(request, pk):
    tip = request.GET['tip']

    cursor = connection.cursor()
    cursor.execute('''SELECT  t.content 
					  FROM wsbodb.perfis_tip t
					  WHERE t.id = %s;''', tip)
    editable = cursor.fetchall()
    cursor.close()        
    teste = "showcontent"
    response_data = { 
        'editable': editable, 'teste': teste
    }
    return HttpResponse(json.dumps(response_data), content_type= u'application/json')

@login_required
@csrf_exempt
def who_favorited(request, pk):
    url2 = request.build_absolute_uri()
    url = url2.split('//')[-1].split('/')[0]
    tip = request.GET.get("favoritings", pk)   
    
    cursor = connection.cursor()
    
    who_favorited = cursor.execute('''SELECT COUNT(a.id) as c
                        FROM wsbodb.perfis_perfil p, wsbodb.perfis_favorites fav,
                        wsbodb.perfis_avatar a 
                        WHERE p.usuario_id = fav.profile_id
                        AND a.profile_id = p.id
                        AND fav.tip_id = %s;''', [tip])
    who_favorited = cursor.fetchall()
    
    
    who_id = cursor.execute('''SELECT p.id as id
                        FROM wsbodb.perfis_perfil p, wsbodb.perfis_favorites fav,
                        wsbodb.perfis_avatar a 
                        WHERE p.usuario_id = fav.profile_id
                        AND a.profile_id = p.id
                        AND fav.tip_id = %s;''', [tip])
    who_id = cursor.fetchall()
    
    who_name = cursor.execute('''SELECT p.nome as name
                        FROM wsbodb.perfis_perfil p, wsbodb.perfis_favorites fav,
                        wsbodb.perfis_avatar a 
                        WHERE p.usuario_id = fav.profile_id
                        AND a.profile_id = p.id
                        AND fav.tip_id = %s;''', [tip])
    who_name = cursor.fetchall()    

    who_image = cursor.execute('''SELECT a.upload as upload
                        FROM wsbodb.perfis_perfil p, wsbodb.perfis_favorites fav,
                        wsbodb.perfis_avatar a 
                        WHERE p.usuario_id = fav.profile_id
                        AND a.profile_id = p.id
                        AND fav.tip_id = %s;''', [tip])
    who_image = cursor.fetchall() 

    who_type = cursor.execute('''SELECT p.type as type
                        FROM wsbodb.perfis_perfil p, wsbodb.perfis_favorites fav,
                        wsbodb.perfis_avatar a 
                        WHERE p.usuario_id = fav.profile_id
                        AND a.profile_id = p.id
                        AND fav.tip_id = %s;''', [tip])
    who_type = cursor.fetchall() 

    who_following = cursor.execute("""SELECT f.id, f.followed_id
                                    FROM wsbodb.perfis_avatar a,
                                    wsbodb.perfis_perfil p, wsbodb.perfis_follow f 
                                    WHERE p.id = f.followed_id
                                     AND a.profile_id = f.followed_id 
                                    AND f.follower_id = %s 
                                    GROUP BY f.followed_id
                                    ORDER BY p.nome;""", [request.user.id])
    who_following = cursor.fetchall()
                
    cursor.close()
        
    teste = "whofavorited" 
    
    response_data = { 
        'who_favorited': who_favorited,  'teste': teste, 'id': who_id, 'name': who_name, 
        'upload': who_image, 'type': who_type, 'following': who_following
    }

    return HttpResponse(json.dumps(response_data), content_type= u'application/json')

	
@login_required
@csrf_exempt
def who_favorited_list(request, pk):
    tip = request.GET.get("favoritings", pk)
    who_name = Tip.objects.raw('''SELECT p.id, p.nome as name, p.type as type,
                        a.upload as upload
                        FROM wsbodb.perfis_perfil p, wsbodb.perfis_favorites fav,
                        wsbodb.perfis_avatar a 
                        WHERE p.usuario_id = fav.profile_id
                        AND a.profile_id = p.id
                        AND fav.tip_id = %s;''', [tip])

    return render(request, 'who_favorited_list.html', {'who_name':who_name})
	

@login_required
@csrf_exempt
def update_profile_name(request, pk):
        perfil = request.GET.get("profileID", pk)   
        nome = request.GET['profilename'] 
    
        cursor = connection.cursor()
        
        cursor.execute("""UPDATE wsbodb.perfis_perfil p
                          SET p.nome = %s   
                          WHERE p.id = %s;""",[nome, perfil])
        
        cursor.execute("""UPDATE wsbodb.perfis_tip t
                          SET t.author_name = %s   
                          WHERE t.author_profile_id = %s;""",[nome, perfil])
        
        row = cursor.fetchall()
        
        cursor.close()
        
        teste = "update"
        
        response_data = { 
            'row': row, 'teste': teste
        }
        return HttpResponse(json.dumps(response_data), content_type= u'application/json')


@login_required
def publish_short_description(request, pk):
        perfil = request.GET.get("profileID", pk)   
        description = request.GET['text'] 
    
        cursor = connection.cursor()
        
        cursor.execute("""INSERT INTO wsbodb.perfis_short_description (profile_id, description) 
                          VALUES(%s, %s);""",[perfil, description])
        
        row = cursor.fetchall()
        
        cursor.close()       
        
        teste = "description"
        
        response_data = { 
            'row': row, 'teste': teste
        }
        return HttpResponse(json.dumps(response_data), content_type= u'application/json')
    

@login_required
def update_short_description(request, pk):
        perfil = request.GET.get("profileID", pk)   
        description = request.GET['text'] 
    
        cursor = connection.cursor()
        
        cursor.execute("""UPDATE wsbodb.perfis_short_description 
                          SET description = %s
                          WHERE profile_id = %s;""",[description, perfil])
        
        row = cursor.fetchall()
        
        cursor.close()       
        
        teste = "description"
        
        response_data = { 
            'row': row, 'teste': teste
        }
        return HttpResponse(json.dumps(response_data), content_type= u'application/json')
    

@login_required
@csrf_exempt
def delete_short_description(request, pk):
        perfil = request.GET['profileid']    
        
        cursor = connection.cursor()
        
        cursor.execute("""DELETE FROM wsbodb.perfis_short_description
                          WHERE profile_id=%s;""",[perfil])
        
        
        row = cursor.fetchall()
        
        cursor.close()       
        
        teste = "delete"
        
        response_data = { 
            'row': row, 'teste': teste
        }
        return HttpResponse(json.dumps(response_data), content_type= u'application/json')    



@login_required
@csrf_exempt
def new_profile_picture(request, pk, template_name='modal_edit_picture.html'):
    a = get_object_or_404(Avatar, pk=pk)
    form = AvatarForm(request.POST or None,  request.FILES, instance=a)
    if request.method=='POST':
        form.save()
        return redirect(request.META['HTTP_REFERER'])
    return render(request, template_name, {'a':a})


@login_required
@csrf_exempt
def new_background_picture(request, pk, template_name='modal_edit_background.html'):
    b = get_object_or_404(Background, pk=pk)
    form = BackgroundForm(request.POST or None,  request.FILES, instance=b)
    if request.method=='POST':
        if 'bkg_upload' in request.FILES:  
            newdoc = Background(bkg_upload = request.FILES['bkg_upload'])
        form.save()
        return redirect('index')
    return render(request, template_name, {'b':b})
    
    """
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():     
            if 'upload' in request.FILES:  
                newimg = Avatar(upload = request.FILES['upload'])
            form.save()
            
        return redirect('exibir', perfil)      
    else: 
        form = AvatarForm() 
    return render_to_response('perfil.html', locals(), context_instance=RequestContext(request)) """


#CHANGE PROFILE MENU BACKGROUND
@login_required
def change_background_default(request, pk):
    background = request.GET['background']
    
    cursor = connection.cursor()
        
    cursor.execute("""UPDATE wsbodb.perfis_background
                      SET bkg_upload = %s
                      WHERE id = %s;""",[0, background])        
   
    row = cursor.fetchall()
    cursor.close()                    

    teste = "default-background"
    
    response_data = { 
        'row': row, 'teste': teste
    }
    return HttpResponse(json.dumps(response_data), content_type= u'application/json')


#CHANGE PROFILE MENU TEXT TO WHITE
@login_required
def change_white_text(request, pk):
    background = request.GET['background']
    user = request.GET['user']
    profile = request.GET['profile']
    
    cursor = connection.cursor()
        
    cursor.execute("""UPDATE wsbodb.perfis_perfil
                      SET color = 1
                      WHERE usuario_id = %s;""",[user])  
    
    cursor.execute("""UPDATE wsbodb.perfis_short_description
                      SET color = 1
                      WHERE profile_id = %s;""",[profile])        
   
    row = cursor.fetchall()
    cursor.close()                    

    teste = "white-text"
    
    response_data = { 
        'row': row, 'teste': teste
    }
    return HttpResponse(json.dumps(response_data), content_type= u'application/json')  

#CHANGE PROFILE MENU TEXT TO BLACK
@login_required
def change_black_text(request, pk):
    background = request.GET['background']
    user = request.GET['user']
    profile = request.GET['profile']
    
    cursor = connection.cursor()
        
    cursor.execute("""UPDATE wsbodb.perfis_perfil
                      SET color = 0
                      WHERE usuario_id = %s;""",[user])   
    
    cursor.execute("""UPDATE wsbodb.perfis_short_description
                      SET color = 0
                      WHERE profile_id = %s;""",[profile])        
         
   
    row = cursor.fetchall()
    cursor.close()                    

    teste = "black-text"
    
    response_data = { 
        'row': row, 'teste': teste
    }
    return HttpResponse(json.dumps(response_data), content_type= u'application/json')
    
    
#WHO AM I - PROFILE SECTION
@login_required
def whoami(request, perfil_id): 
    
    perfil = Perfil.objects.get(id=perfil_id)
    perfil_logado = get_perfil_logado(request)
       
    url2 = request.build_absolute_uri()
    url = url2.split('//')[-1].split('/')[0]

    content = Tip.objects.raw("""SELECT * 
                                 FROM wsbodb.perfis_whoami
                                 WHERE whoami_profile_id = %s
                                 ORDER BY date DESC;""", [perfil_id])
    
     
    is_contact = Tip.objects.raw("""SELECT f.id, f.followed_id as followed, ifnull(f.followed_id,0) as isfollowing  
                                FROM wsbodb.perfis_follow f
                                WHERE f.follower_id = %s
                                AND f.followed_id = %s;""", [request.user.id, perfil_id])
                                            
    my_profile_image = Tip.objects.raw("""SELECT a.id, a.upload as upload, a.user_id
                                        FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                        ON(a.user_id = p.usuario_id)
                                        WHERE p.usuario_id = %s;""", [request.user.id])
         
    has_profile_image = Tip.objects.raw("""SELECT a.id, ifnull(a.upload,0) as upload 
                                        FROM wsbodb.perfis_avatar a
                                        WHERE a.profile_id = %s;""", [perfil_id])  
    
    has_background_image = Tip.objects.raw("""SELECT b.id, b.bkg_upload as bkg_upload, b.user_id,
                                        ifnull(b.bkg_upload,0) as has_background
                                        FROM wsbodb.perfis_background b LEFT JOIN wsbodb.perfis_perfil p
                                        ON(b.profile_id = p.id)
                                        WHERE p.id = %s;""", [perfil_id])          
     
     
    has_short_description = Tip.objects.raw("""SELECT d.id, d.description as description, 
                                ifnull(d.profile_id,0) as has_description  
                                FROM wsbodb.perfis_short_description d
                                WHERE d.profile_id = %s;""", [perfil_id]) 

    published_tips_count = Tip.objects.raw("""SELECT t.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_tip t 
                                WHERE t.author_profile_id = %s
                                AND t.hided = 0
                                ORDER BY t.date DESC;""", [perfil_id]) 
    
    company_description_count = Tip.objects.raw("""SELECT c.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_company c 
                                WHERE c.company_profile_id = %s
                                ORDER BY c.date DESC;""", [perfil_id])   
    
    company_offer_count = Tip.objects.raw("""SELECT o.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_offer o 
                                WHERE o.offer_profile_id = %s
                                ORDER BY o.date DESC;""", [perfil_id]) 
    
    company_location_count = Tip.objects.raw("""SELECT l.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_location l 
                                WHERE l.location_profile_id = %s
                                ORDER BY l.date DESC;""", [perfil_id])      
    
    person_whoami_count = Tip.objects.raw("""SELECT w.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_whoami w 
                                WHERE w.whoami_profile_id = %s
                                ORDER BY w.date DESC;""", [perfil_id]) 
    
    person_education_count = Tip.objects.raw("""SELECT e.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_education e 
                                WHERE e.education_profile_id = %s
                                ORDER BY e.date DESC;""", [perfil_id])  
    
    person_knows_count = Tip.objects.raw("""SELECT k.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_knows k 
                                WHERE k.knows_profile_id = %s
                                ORDER BY k.date DESC;""", [perfil_id]) 
    
    person_jobs_count = Tip.objects.raw("""SELECT j.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_jobs j 
                                WHERE j.jobs_profile_id = %s
                                ORDER BY j.date DESC;""", [perfil_id])
    
    person_live_count = Tip.objects.raw("""SELECT l.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_live l 
                                WHERE l.live_profile_id = %s
                                ORDER BY l.date DESC;""", [perfil_id]) 

    person_hobby_count = Tip.objects.raw("""SELECT h.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_hobby h 
                                WHERE h.hobby_profile_id = %s
                                ORDER BY h.date DESC;""", [perfil_id]) 

            
    return render(request, 'whoami.html', locals())


@login_required
def new_whoami(request, perfil_id):
    form = WhoamiForm(request.POST)
          
    if request.method == 'POST':
        if form.is_valid():     
            form.save() 

        return redirect('whoami', perfil_id) 
     
    else: 
        return render_to_response('admin/tips/tip_error.html', locals(), context_instance=RequestContext(request))


@login_required
@csrf_exempt
def update_whoami(request, pk, template_name='whoami.html'):
    c = get_object_or_404(Whoami, pk=pk)
    form = WhoamiForm(request.POST or None, instance=c)
    if request.method=='POST':
        form.save()
        return redirect('whoami', request.user.perfil.id)
    return render(request, template_name, {'c':c})


@login_required
@csrf_exempt
def delete_whoami(request, pk):
    tip = request.GET['tip']
    
    cursor = connection.cursor()
    
    cursor.execute("""DELETE FROM wsbodb.perfis_whoami
                      WHERE id=%s;""",[tip])
    
    row = cursor.fetchall()
    
    cursor.close()       
    
    teste = "removedwhoami"
    
    response_data = { 
        'row': row, 'teste': teste
    }
    return HttpResponse(json.dumps(response_data), content_type= u'application/json')



#EDUCATION - PROFILE SECTION  
@login_required
def education(request, perfil_id):    

    perfil = Perfil.objects.get(id=perfil_id)
    perfil_logado = get_perfil_logado(request)
       
    url2 = request.build_absolute_uri()
    url = url2.split('//')[-1].split('/')[0]

    content = Tip.objects.raw("""SELECT *
                                 FROM wsbodb.perfis_education
                                 WHERE education_profile_id = %s
                                 ORDER BY date DESC;""", [perfil_id])
                                        
    
     

    is_contact = Tip.objects.raw("""SELECT f.id, f.followed_id as followed, ifnull(f.followed_id,0) as isfollowing  
                                FROM wsbodb.perfis_follow f
                                WHERE f.follower_id = %s
                                AND f.followed_id = %s;""", [request.user.id, perfil_id])
                                             
    my_profile_image = Tip.objects.raw("""SELECT a.id, a.upload as upload, a.user_id
                                        FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                        ON(a.user_id = p.usuario_id)
                                        WHERE p.usuario_id = %s;""", [request.user.id])
         
    has_profile_image = Tip.objects.raw("""SELECT a.id, ifnull(a.upload,0) as upload 
                                        FROM wsbodb.perfis_avatar a
                                        WHERE a.profile_id = %s;""", [perfil_id])   
    
    has_background_image = Tip.objects.raw("""SELECT b.id, b.bkg_upload as bkg_upload, b.user_id,
                                        ifnull(b.bkg_upload,0) as has_background
                                        FROM wsbodb.perfis_background b LEFT JOIN wsbodb.perfis_perfil p
                                        ON(b.profile_id = p.id)
                                        WHERE p.id = %s;""", [perfil_id])              
     
    has_short_description = Tip.objects.raw("""SELECT d.id, d.description as description, 
                                ifnull(d.profile_id,0) as has_description  
                                FROM wsbodb.perfis_short_description d
                                WHERE d.profile_id = %s;""", [perfil_id])  

    published_tips_count = Tip.objects.raw("""SELECT t.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_tip t 
                                WHERE t.author_profile_id = %s
                                AND t.hided = 0
                                ORDER BY t.date DESC;""", [perfil_id]) 
    
    company_description_count = Tip.objects.raw("""SELECT c.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_company c 
                                WHERE c.company_profile_id = %s
                                ORDER BY c.date DESC;""", [perfil_id])   
    
    company_offer_count = Tip.objects.raw("""SELECT o.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_offer o 
                                WHERE o.offer_profile_id = %s
                                ORDER BY o.date DESC;""", [perfil_id]) 
    
    company_location_count = Tip.objects.raw("""SELECT l.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_location l 
                                WHERE l.location_profile_id = %s
                                ORDER BY l.date DESC;""", [perfil_id])      
    
    person_whoami_count = Tip.objects.raw("""SELECT w.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_whoami w 
                                WHERE w.whoami_profile_id = %s
                                ORDER BY w.date DESC;""", [perfil_id]) 
    
    person_education_count = Tip.objects.raw("""SELECT e.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_education e 
                                WHERE e.education_profile_id = %s
                                ORDER BY e.date DESC;""", [perfil_id])  
    
    person_knows_count = Tip.objects.raw("""SELECT k.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_knows k 
                                WHERE k.knows_profile_id = %s
                                ORDER BY k.date DESC;""", [perfil_id]) 
    
    person_jobs_count = Tip.objects.raw("""SELECT j.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_jobs j 
                                WHERE j.jobs_profile_id = %s
                                ORDER BY j.date DESC;""", [perfil_id])
    
    person_live_count = Tip.objects.raw("""SELECT l.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_live l 
                                WHERE l.live_profile_id = %s
                                ORDER BY l.date DESC;""", [perfil_id]) 

    person_hobby_count = Tip.objects.raw("""SELECT h.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_hobby h 
                                WHERE h.hobby_profile_id = %s
                                ORDER BY h.date DESC;""", [perfil_id]) 
                
    return render(request, 'education.html', locals()) 


@login_required
@csrf_exempt
def new_education(request, perfil_id):
    form = EducationForm(request.POST)

    if request.method == 'POST':
        if form.is_valid(): 
            form.save() 

        return redirect('education', perfil_id) 
     
    else: 
        return render_to_response('admin/tips/tip_error.html', locals(), context_instance=RequestContext(request))
    
    
@login_required
@csrf_exempt
def update_education(request, pk, template_name='education.html'):
    c = get_object_or_404(Education, pk=pk)
    form = EducationForm(request.POST or None, instance=c)
    if request.method=='POST':
        form.save()
        return redirect('education', request.user.perfil.id)
    return render(request, template_name, {'c':c})
             

@login_required
@csrf_exempt
def delete_education(request, pk):
    tip = request.GET['tip']
    
    cursor = connection.cursor()
    
    cursor.execute("""DELETE FROM wsbodb.perfis_education
                      WHERE id=%s;""",[tip])
    
    row = cursor.fetchall()
    
    cursor.close()       
    
    teste = "removededucation"
    
    response_data = { 
        'row': row, 'teste': teste
    }
    return HttpResponse(json.dumps(response_data), content_type= u'application/json')



#KNOWS ABOUT - PROFILE SECTION
@login_required
def knows(request, perfil_id):    

    perfil = Perfil.objects.get(id=perfil_id)
    perfil_logado = get_perfil_logado(request)
       
    url2 = request.build_absolute_uri()
    url = url2.split('//')[-1].split('/')[0]

    content = Tip.objects.raw("""SELECT *
                                 FROM wsbodb.perfis_knows
                                 WHERE knows_profile_id = %s
                                 ORDER BY date DESC;""", [perfil_id])
                                        
    is_contact = Tip.objects.raw("""SELECT f.id, f.followed_id as followed, ifnull(f.followed_id,0) as isfollowing  
                                FROM wsbodb.perfis_follow f
                                WHERE f.follower_id = %s
                                AND f.followed_id = %s;""", [request.user.id, perfil_id])
         
                                    
    my_profile_image = Tip.objects.raw("""SELECT a.id, a.upload as upload, a.user_id
                                        FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                        ON(a.user_id = p.usuario_id)
                                        WHERE p.usuario_id = %s;""", [request.user.id])
         
    has_profile_image = Tip.objects.raw("""SELECT a.id, ifnull(a.upload,0) as upload 
                                        FROM wsbodb.perfis_avatar a
                                        WHERE a.profile_id = %s;""", [perfil_id])   
    
    has_background_image = Tip.objects.raw("""SELECT b.id, b.bkg_upload as bkg_upload, b.user_id,
                                        ifnull(b.bkg_upload,0) as has_background
                                        FROM wsbodb.perfis_background b LEFT JOIN wsbodb.perfis_perfil p
                                        ON(b.profile_id = p.id)
                                        WHERE p.id = %s;""", [perfil_id])              
     
    has_short_description = Tip.objects.raw("""SELECT d.id, d.description as description, 
                                ifnull(d.profile_id,0) as has_description  
                                FROM wsbodb.perfis_short_description d
                                WHERE d.profile_id = %s;""", [perfil_id])  

    published_tips_count = Tip.objects.raw("""SELECT t.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_tip t 
                                WHERE t.author_profile_id = %s
                                AND t.hided = 0
                                ORDER BY t.date DESC;""", [perfil_id]) 
    
    company_description_count = Tip.objects.raw("""SELECT c.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_company c 
                                WHERE c.company_profile_id = %s
                                ORDER BY c.date DESC;""", [perfil_id])   
    
    company_offer_count = Tip.objects.raw("""SELECT o.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_offer o 
                                WHERE o.offer_profile_id = %s
                                ORDER BY o.date DESC;""", [perfil_id]) 
    
    company_location_count = Tip.objects.raw("""SELECT l.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_location l 
                                WHERE l.location_profile_id = %s
                                ORDER BY l.date DESC;""", [perfil_id])      
    
    person_whoami_count = Tip.objects.raw("""SELECT w.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_whoami w 
                                WHERE w.whoami_profile_id = %s
                                ORDER BY w.date DESC;""", [perfil_id]) 
    
    person_education_count = Tip.objects.raw("""SELECT e.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_education e 
                                WHERE e.education_profile_id = %s
                                ORDER BY e.date DESC;""", [perfil_id])  
    
    person_knows_count = Tip.objects.raw("""SELECT k.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_knows k 
                                WHERE k.knows_profile_id = %s
                                ORDER BY k.date DESC;""", [perfil_id]) 
    
    person_jobs_count = Tip.objects.raw("""SELECT j.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_jobs j 
                                WHERE j.jobs_profile_id = %s
                                ORDER BY j.date DESC;""", [perfil_id])
    
    person_live_count = Tip.objects.raw("""SELECT l.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_live l 
                                WHERE l.live_profile_id = %s
                                ORDER BY l.date DESC;""", [perfil_id]) 

    person_hobby_count = Tip.objects.raw("""SELECT h.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_hobby h 
                                WHERE h.hobby_profile_id = %s
                                ORDER BY h.date DESC;""", [perfil_id]) 
               
    return render(request, 'knows.html', locals()) 

@login_required
def new_knows(request, perfil_id):
    form = KnowsForm(request.POST)

    if request.method == 'POST':
        if form.is_valid(): 
            form.save() 

        return redirect('knows', perfil_id) 
     
    else: 
        return render_to_response('admin/tips/tip_error.html', locals(), context_instance=RequestContext(request))


@login_required
@csrf_exempt
def update_knows(request, pk, template_name='knows.html'):
    c = get_object_or_404(Knows, pk=pk)
    form = KnowsForm(request.POST or None, instance=c)
    if request.method=='POST':
        form.save()
        return redirect('knows', request.user.perfil.id)
    return render(request, template_name, {'c':c})


@login_required
@csrf_exempt
def delete_knows(request, pk):
    tip = request.GET['tip']
    
    cursor = connection.cursor()
    
    cursor.execute("""DELETE FROM wsbodb.perfis_knows
                      WHERE id=%s;""",[tip])
    
    row = cursor.fetchall()
    
    cursor.close()       
    
    teste = "removedknows"
    
    response_data = { 
        'row': row, 'teste': teste
    }
    return HttpResponse(json.dumps(response_data), content_type= u'application/json')


#JOBS - PROFILE SECTION
@login_required
def jobs(request, perfil_id):    

    perfil = Perfil.objects.get(id=perfil_id)
    perfil_logado = get_perfil_logado(request)
       
    url2 = request.build_absolute_uri()
    url = url2.split('//')[-1].split('/')[0]

    content = Tip.objects.raw("""SELECT *
                                 FROM wsbodb.perfis_jobs
                                 WHERE jobs_profile_id = %s
                                 ORDER BY date DESC;""", [perfil_id])
    

    is_contact = Tip.objects.raw("""SELECT f.id, f.followed_id as followed, ifnull(f.followed_id,0) as isfollowing  
                                FROM wsbodb.perfis_follow f
                                WHERE f.follower_id = %s
                                AND f.followed_id = %s;""", [request.user.id, perfil_id])
         
                                    
    my_profile_image = Tip.objects.raw("""SELECT a.id, a.upload as upload, a.user_id
                                        FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                        ON(a.user_id = p.usuario_id)
                                        WHERE p.usuario_id = %s;""", [request.user.id])
         
    has_profile_image = Tip.objects.raw("""SELECT a.id, ifnull(a.upload,0) as upload 
                                        FROM wsbodb.perfis_avatar a
                                        WHERE a.profile_id = %s;""", [perfil_id])  
    
    has_background_image = Tip.objects.raw("""SELECT b.id, b.bkg_upload as bkg_upload, b.user_id,
                                        ifnull(b.bkg_upload,0) as has_background
                                        FROM wsbodb.perfis_background b LEFT JOIN wsbodb.perfis_perfil p
                                        ON(b.profile_id = p.id)
                                        WHERE p.id = %s;""", [perfil_id])               
     
    has_short_description = Tip.objects.raw("""SELECT d.id, d.description as description, 
                                ifnull(d.profile_id,0) as has_description  
                                FROM wsbodb.perfis_short_description d
                                WHERE d.profile_id = %s;""", [perfil_id])  

    published_tips_count = Tip.objects.raw("""SELECT t.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_tip t 
                                WHERE t.author_profile_id = %s
                                AND t.hided = 0
                                ORDER BY t.date DESC;""", [perfil_id]) 
    
    company_description_count = Tip.objects.raw("""SELECT c.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_company c 
                                WHERE c.company_profile_id = %s
                                ORDER BY c.date DESC;""", [perfil_id])   
    
    company_offer_count = Tip.objects.raw("""SELECT o.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_offer o 
                                WHERE o.offer_profile_id = %s
                                ORDER BY o.date DESC;""", [perfil_id]) 
    
    company_location_count = Tip.objects.raw("""SELECT l.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_location l 
                                WHERE l.location_profile_id = %s
                                ORDER BY l.date DESC;""", [perfil_id])      
    
    person_whoami_count = Tip.objects.raw("""SELECT w.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_whoami w 
                                WHERE w.whoami_profile_id = %s
                                ORDER BY w.date DESC;""", [perfil_id]) 
    
    person_education_count = Tip.objects.raw("""SELECT e.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_education e 
                                WHERE e.education_profile_id = %s
                                ORDER BY e.date DESC;""", [perfil_id])  
    
    person_knows_count = Tip.objects.raw("""SELECT k.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_knows k 
                                WHERE k.knows_profile_id = %s
                                ORDER BY k.date DESC;""", [perfil_id]) 
    
    person_jobs_count = Tip.objects.raw("""SELECT j.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_jobs j 
                                WHERE j.jobs_profile_id = %s
                                ORDER BY j.date DESC;""", [perfil_id])
    
    person_live_count = Tip.objects.raw("""SELECT l.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_live l 
                                WHERE l.live_profile_id = %s
                                ORDER BY l.date DESC;""", [perfil_id]) 

    person_hobby_count = Tip.objects.raw("""SELECT h.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_hobby h 
                                WHERE h.hobby_profile_id = %s
                                ORDER BY h.date DESC;""", [perfil_id]) 
                
    return render(request, 'jobs.html', locals()) 

@login_required
def new_jobs(request, perfil_id):
    form = JobsForm(request.POST)

    if request.method == 'POST':
        if form.is_valid(): 
            form.save() 

        return redirect('jobs', perfil_id) 
     
    else: 
        return render_to_response('admin/tips/tip_error.html', locals(), context_instance=RequestContext(request))
    

@login_required
@csrf_exempt
def update_jobs(request, pk, template_name='jobs.html'):
    c = get_object_or_404(Jobs, pk=pk)
    form = JobsForm(request.POST or None, instance=c)
    if request.method=='POST':
        form.save()
        return redirect('jobs', request.user.perfil.id)
    return render(request, template_name, {'c':c})
 

@login_required
@csrf_exempt
def delete_jobs(request, pk):
    tip = request.GET['tip']
    
    cursor = connection.cursor()
    
    cursor.execute("""DELETE FROM wsbodb.perfis_jobs
                      WHERE id=%s;""",[tip])
    
    row = cursor.fetchall()
    
    cursor.close()       
    
    teste = "removedjobs"
    
    response_data = { 
        'row': row, 'teste': teste
    }
    return HttpResponse(json.dumps(response_data), content_type= u'application/json')


#COMPANY - PROFILE SECTION
@login_required
@csrf_exempt
def company(request, perfil_id): 
    
    perfil = Perfil.objects.get(id=perfil_id)
    perfil_logado = get_perfil_logado(request)
       
    url2 = request.build_absolute_uri()
    url = url2.split('//')[-1].split('/')[0]

    content = Tip.objects.raw("""SELECT *
                                 FROM wsbodb.perfis_company
                                 WHERE company_profile_id = %s
                                 ORDER BY date DESC;""", [perfil_id])

    is_contact = Tip.objects.raw("""SELECT f.id, f.followed_id as followed, ifnull(f.followed_id,0) as isfollowing  
                                FROM wsbodb.perfis_follow f
                                WHERE f.follower_id = %s
                                AND f.followed_id = %s;""", [request.user.id, perfil_id])
                                             
    my_profile_image = Tip.objects.raw("""SELECT a.id, a.upload as upload, a.user_id
                                        FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                        ON(a.user_id = p.usuario_id)
                                        WHERE p.usuario_id = %s;""", [request.user.id])
         
    has_profile_image = Tip.objects.raw("""SELECT a.id, ifnull(a.upload,0) as upload 
                                        FROM wsbodb.perfis_avatar a
                                        WHERE a.profile_id = %s;""", [perfil_id])
    
    has_background_image = Tip.objects.raw("""SELECT b.id, b.bkg_upload as bkg_upload, b.user_id,
                                        ifnull(b.bkg_upload,0) as has_background
                                        FROM wsbodb.perfis_background b LEFT JOIN wsbodb.perfis_perfil p
                                        ON(b.profile_id = p.id)
                                        WHERE p.id = %s;""", [perfil_id])                 
     
    has_short_description = Tip.objects.raw("""SELECT d.id, d.description as description, 
                                ifnull(d.profile_id,0) as has_description  
                                FROM wsbodb.perfis_short_description d
                                WHERE d.profile_id = %s;""", [perfil_id]) 

    published_tips_count = Tip.objects.raw("""SELECT t.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_tip t 
                                WHERE t.author_profile_id = %s
                                AND t.hided = 0
                                ORDER BY t.date DESC;""", [perfil_id]) 
    
    company_description_count = Tip.objects.raw("""SELECT c.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_company c 
                                WHERE c.company_profile_id = %s
                                ORDER BY c.date DESC;""", [perfil_id])   
    
    company_offer_count = Tip.objects.raw("""SELECT o.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_offer o 
                                WHERE o.offer_profile_id = %s
                                ORDER BY o.date DESC;""", [perfil_id]) 
    
    company_location_count = Tip.objects.raw("""SELECT l.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_location l 
                                WHERE l.location_profile_id = %s
                                ORDER BY l.date DESC;""", [perfil_id])      
    
    #Followers counting
    followers_howmany = Tip.objects.raw("""SELECT f.id, (COUNT(*) -1) as howmany 
                                            FROM wsbodb.perfis_follow f, wsbodb.perfis_perfil p 
                                            WHERE f.followed_id = %s
                                            AND p.usuario_id = f.follower_id;""", [perfil_id])
            
    return render(request, 'company.html', locals())

@login_required
@csrf_exempt
def new_company(request, perfil_id):
    form = CompanyForm(request.POST)
    if request.method == 'POST':
        if form.is_valid(): 
            form.save() 

        return redirect('company', perfil_id) 
     
    else: 
        return render_to_response('admin/tips/tip_error.html', locals(), context_instance=RequestContext(request))
    

@login_required
@csrf_exempt
def update_company(request, pk, template_name='company.html'):
    c = get_object_or_404(Company, pk=pk)
    form = CompanyForm(request.POST or None, instance=c)
    if request.method=='POST':
        form.save()
        return redirect('company', request.user.perfil.id)
    return render(request, template_name, {'c':c})


@login_required
@csrf_exempt
def delete_company(request, pk):
    tip = request.GET['tip']
    
    cursor = connection.cursor()
    
    cursor.execute("""DELETE FROM wsbodb.perfis_company
                      WHERE id=%s;""",[tip])
    
    row = cursor.fetchall()
    
    cursor.close()       
    
    teste = "removedcompany"
    
    response_data = { 
        'row': row, 'teste': teste
    }
    return HttpResponse(json.dumps(response_data), content_type= u'application/json')    



#LOCATION - COMPANY PROFILE SECTION
@login_required
@csrf_exempt
def location(request, perfil_id): 
    
    perfil = Perfil.objects.get(id=perfil_id)
    perfil_logado = get_perfil_logado(request)
       
    url2 = request.build_absolute_uri()
    url = url2.split('//')[-1].split('/')[0]

    content = Tip.objects.raw("""SELECT *
                                 FROM wsbodb.perfis_location
                                 WHERE location_profile_id = %s
                                 ORDER BY date DESC;""", [perfil_id])

    is_contact = Tip.objects.raw("""SELECT f.id, f.followed_id as followed, ifnull(f.followed_id,0) as isfollowing  
                                FROM wsbodb.perfis_follow f
                                WHERE f.follower_id = %s
                                AND f.followed_id = %s;""", [request.user.id, perfil_id])
         
                                    
    my_profile_image = Tip.objects.raw("""SELECT a.id, a.upload as upload, a.user_id
                                        FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                        ON(a.user_id = p.usuario_id)
                                        WHERE p.usuario_id = %s;""", [request.user.id])
         
    has_profile_image = Tip.objects.raw("""SELECT a.id, ifnull(a.upload,0) as upload 
                                        FROM wsbodb.perfis_avatar a
                                        WHERE a.profile_id = %s;""", [perfil_id])  
    
    has_background_image = Tip.objects.raw("""SELECT b.id, b.bkg_upload as bkg_upload, b.user_id,
                                        ifnull(b.bkg_upload,0) as has_background
                                        FROM wsbodb.perfis_background b LEFT JOIN wsbodb.perfis_perfil p
                                        ON(b.profile_id = p.id)
                                        WHERE p.id = %s;""", [perfil_id])               
     
    has_short_description = Tip.objects.raw("""SELECT d.id, d.description as description, 
                                ifnull(d.profile_id,0) as has_description  
                                FROM wsbodb.perfis_short_description d
                                WHERE d.profile_id = %s;""", [perfil_id]) 

    company_description_count = Tip.objects.raw("""SELECT c.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_company c 
                                WHERE c.company_profile_id = %s
                                ORDER BY c.date DESC;""", [perfil_id])   

    published_tips_count = Tip.objects.raw("""SELECT t.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_tip t 
                                WHERE t.author_profile_id = %s
                                AND t.hided = 0
                                ORDER BY t.date DESC;""", [perfil_id]) 
        
    company_offer_count = Tip.objects.raw("""SELECT o.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_offer o 
                                WHERE o.offer_profile_id = %s
                                ORDER BY o.date DESC;""", [perfil_id]) 
    
    company_location_count = Tip.objects.raw("""SELECT l.id, COUNT(*) as howmany
                                FROM wsbodb.perfis_location l 
                                WHERE l.location_profile_id = %s
                                ORDER BY l.date DESC;""", [perfil_id]) 
 
     #Followers counting
    followers_howmany = Tip.objects.raw("""SELECT f.id, (COUNT(*) -1) as howmany 
                                            FROM wsbodb.perfis_follow f, wsbodb.perfis_perfil p 
                                            WHERE f.followed_id = %s
                                            AND p.usuario_id = f.follower_id;""", [perfil_id])
                   
    return render(request, 'location.html', locals())  

@login_required
@csrf_exempt
def new_location(request, perfil_id):
    form = LocationForm(request.POST)
    if request.method == 'POST':
        if form.is_valid(): 
            form.save() 

        return redirect('location', perfil_id) 
     
    else: 
        return render_to_response('admin/tips/tip_error.html', locals(), context_instance=RequestContext(request))
    

@login_required
@csrf_exempt
def update_location(request, pk, template_name='location.html'):
    c = get_object_or_404(Location, pk=pk)
    form = LocationForm(request.POST or None, instance=c)
    if request.method=='POST':
        form.save()
        return redirect('location', request.user.perfil.id)
    return render(request, template_name, {'c':c})

@login_required
@csrf_exempt
def delete_location(request, pk):
    tip = request.GET['tip']
    
    cursor = connection.cursor()
    
    cursor.execute("""DELETE FROM wsbodb.perfis_location
                      WHERE id=%s;""",[tip])
    
    row = cursor.fetchall()
    
    cursor.close()       
    
    teste = "removedlocation"
    
    response_data = { 
        'row': row, 'teste': teste
    }
    return HttpResponse(json.dumps(response_data), content_type= u'application/json')     



@login_required
def search(request):
    query = str(request.GET.get('q', ''))
        
    url2 = request.build_absolute_uri()
    url = url2.split('//')[-1].split('/')[0]
    
    perfil = Perfil.objects.get(id=request.user.perfil.id)

    results =  Tip.objects.raw("""SELECT t.id, p.nome as name, t.content, 
                                t.author_profile_id as author, t.type as type,
                                (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed,
                                (t.author_profile_id IN (SELECT p.id FROM wsbodb.perfis_perfil p WHERE p.stealth=1)) as stealthed,
                                p.usuario_id as profile_id, t.author_name as name,
                                t.date, ifnull(f.id,0) as isfollowing, ifnull(fav.id,0) as isfav, 
                                f.followed_id, ifnull(a.upload,0) as upload, t.outdoor
                                FROM wsbodb.perfis_perfil p, wsbodb.perfis_follow f,
                                wsbodb.perfis_avatar a,
                                wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                ON (t.id = fav.tip_id AND fav.profile_id = %s)  
                                WHERE (t.content LIKE trim(%s) OR REPLACE(t.content, ' ', '') = REPLACE(trim(%s), ' ', '')
                                OR t.author_name LIKE trim(%s) OR REPLACE(t.author_name, ' ', '') = REPLACE(trim(%s), ' ', ''))
                                AND p.usuario_id = %s                               
                                AND t.hided = 0
                                AND t.author_profile_id = a.profile_id
                                GROUP BY t.id
                                ORDER BY ifnull(t.updated_date,t.date) DESC;""", 
                                [request.user.perfil.id, request.user.id, request.user.id, '%%'+query+'%%', query, '%%'+query+'%%', query, request.user.id]),
 
                                                            
    is_contact = Tip.objects.raw("""SELECT t.id, f.followed_id as fid, p.nome as name, t.content, 
                                    t.author_profile_id as author, p.type as type,
                                    p.usuario_id as profile_id, t.author_name as name,
                                    t.date, ifnull(f.id,0) as isfollowing, ifnull(fav.id,0) as isfav, 
                                    f.followed_id
                                    FROM wsbodb.perfis_perfil p, wsbodb.perfis_follow f, 
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                    ON (t.id = fav.tip_id AND fav.profile_id = %s) 
                                    WHERE p.usuario_id = %s
                                    AND t.author_profile_id = f.followed_id 
                                    AND f.follower_id = %s 
                                    GROUP BY f.followed_id
                                    ORDER BY t.date DESC;""", [request.user.id, request.user.id, request.user.id])
        
    my_profile_image = Tip.objects.raw("""SELECT a.id, a.upload as upload, a.user_id
                                        FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                        ON(a.user_id = p.usuario_id)
                                        WHERE p.usuario_id = %s;""", [request.user.id])
         
    has_profile_image = Tip.objects.raw("""SELECT a.id, ifnull(a.upload,0) as upload 
                                        FROM wsbodb.perfis_avatar a
                                        WHERE a.profile_id = %s;""", [request.user.perfil.id])    
            
    return render(request, 'search/search.html', {'perfis':Perfil.objects.all(),
                                                  'perfil': perfil, 
                                                  'perfil_logado': get_perfil_logado(request), 
                                                  'is_contact':is_contact, 
                                                  'my_profile_image': my_profile_image,
                                                  'has_profile_image': has_profile_image, 
                                                  'results': results,
                                                  'url': url })    

    
def autocomplete(request):
    sqs = SearchQuerySet().filter(content=AutoQuery(request.GET['q'])).order_by('-date')[:5]
    sqs2 = SearchQuerySet().filter(deck_name=AutoQuery(request.GET['q']))[:5]
    sqs3 = SearchQuerySet().filter(upload=AutoQuery(request.GET['q']))[:5]
    
    suggestions = [result.content for result in sqs] 
    suggestionso = [result.outdoor for result in sqs] 
    suggestionsa = [result.author_name for result in sqs]
    suggestions_profile_id = [result.author_profile_id for result in sqs]
    suggestions_slug = [result.slug for result in sqs]
    suggestions_id = [result.pk for result in sqs]
    
    suggestionsd = [result.deck_name for result in sqs2]
    
    suggestionsu = [result.upload for result in sqs3]

    the_data = json.dumps({
        'results': suggestions,
        'authors': suggestionsa,
        'profile_id': suggestions_profile_id,
        'slug': suggestions_slug,
        'id': suggestions_id,
        'campaigns': suggestionsd,
        'uploads': suggestionsu,
        'outdoors': suggestionso
    })
    return HttpResponse(the_data, content_type='application/json')


@login_required
def mobile_menu(request, perfil_id):
    
    url2 = request.build_absolute_uri()
    url = url2.split('//')[-1].split('/')[0]

    perfil = Perfil.objects.get(id=perfil_id)
    perfil_logado = get_perfil_logado(request)
    ja_eh_contato = perfil in perfil_logado.contatos.all()
    
    return render(request, 'mobile_menu.html', locals())



@login_required
def mobile_new_card(request, perfil_id):
    
    url2 = request.build_absolute_uri()
    url = url2.split('//')[-1].split('/')[0]

    perfil = Perfil.objects.get(id=perfil_id)
    perfil_logado = get_perfil_logado(request)
    ja_eh_contato = perfil in perfil_logado.contatos.all()

    my_profile_image = Tip.objects.raw("""SELECT a.id, a.upload as upload, a.user_id
                                    FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                    ON(a.user_id = p.usuario_id)
                                    WHERE p.usuario_id = %s;""", [request.user.id])
    
    return render(request, 'mobile_new_card.html', locals())



@login_required
@csrf_exempt
def chat(request, pk):
    tip = request.GET['tip']
    destino = request.GET['destino']
    origem = request.GET['origem']
    status = request.GET['status']
    corpo = request.GET['corpo']
    criacao = request.GET['criacao']
    
    cursor = connection.cursor()
    
    cursor.execute("""INSERT INTO wsbodb.mensagens_mensagem (outdoor, destino, origem, status, corpo, criacao)
                      VALUES (%s, %s, %s, %s, %s, %s);""", [tip, destino, origem, status, corpo, criacao])
    
    chat = cursor.execute('''SELECT COUNT(m.id) as total
                        FROM wsbodb.mensagens_mensagem m
                        WHERE m.outdoor = %s;''', [tip])
    
    row = cursor.fetchall()
    
    cursor.close()       
    
    teste = "sent"
    
    response_data = { 
        'row': row, 'teste': teste, 'chat': chat
    }
    return HttpResponse(json.dumps(response_data), content_type= u'application/json') 



@login_required
@csrf_exempt
def chat_room(request, perfil_id, pk):
    
    url2 = request.build_absolute_uri()
    url = url2.split('//')[-1].split('/')[0]

    perfil = Perfil.objects.get(id=perfil_id)
    perfil_logado = get_perfil_logado(request)
    ja_eh_contato = perfil in perfil_logado.contatos.all()
    
    my_profile_image = Tip.objects.raw("""SELECT a.id, a.upload as upload, a.user_id
                                        FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                        ON(a.user_id = p.usuario_id)
                                        WHERE p.usuario_id = %s;""", [request.user.id])
         
    has_profile_image = Tip.objects.raw("""SELECT a.id, ifnull(a.upload,0) as upload 
                                        FROM wsbodb.perfis_avatar a
                                        WHERE a.profile_id = %s;""", [request.user.perfil.id]) 
    
    chat_room = Tip.objects.raw("""SELECT m.id, m.outdoor, m.corpo, m.origem,
                                    p.nome, p.type, p.id as profileID,
                                    a.upload,
                                    t.outdoor as imagem, t.outdoor2 as imagem2,
                                    t.outdoor3 as imagem3, t.outdoor4 as imagem4, 
                                    t.hide_image as hide_image, t.hide_image2 as hide_image2,
                                    t.hide_image3 as hide_image3, t.hide_image4 as hide_image4, 
                                    t.slug, t.content, t.id as outdoorID,
                                    t.direction, t.price, t.reference
                                    FROM wsbodb.perfis_perfil p,
                                    wsbodb.perfis_avatar a,
                                    wsbodb.mensagens_mensagem m
                                    LEFT JOIN wsbodb.perfis_tip t
                                    ON t.id = m.outdoor
                                    WHERE m.outdoor NOT IN (SELECT re.card_id FROM wsbodb.perfis_removed re WHERE re.profile_id=%s) 
                                    AND m.destino = %s
                                    AND m.origem = p.id
                                    AND p.id = a.profile_id
                                    and t.id = %s
                                    GROUP BY p.id;""", [request.user.id, request.user.perfil.id, pk])         
    
    chat_in_room = Mensagem.objects.raw("""SELECT *,
                                  p.id as profileID,
                                  a.upload
                                  FROM wsbodb.mensagens_mensagem m,
                                  wsbodb.perfis_perfil p,
                                  wsbodb.perfis_avatar a,
                                  wsbodb.perfis_tip t
                                  WHERE m.origem = p.id
                                  AND p.id = a.profile_id
                                  AND (p.usuario_id = %s or m.destino = %s)
                                  AND t.id = m.outdoor
                                  AND t.id = %s
                                  ORDER BY m.id DESC;""",[request.user.id, request.user.perfil.id, pk])
    
    
    return render(request, 'chat_room.html', locals())


def upload_file(request):
    try:
        response = File.upload(DjangoAdapter(request), '/media/documents/')
    except Exception:
        response = {'error': str(sys.exc_info()[1])}
    return HttpResponse(json.dumps(response), content_type="application/json")


def windy(request):
    perfil = Perfil.objects.get(id=request.user.perfil.id)
    
    url2 = request.build_absolute_uri()
    url = url2.split('//')[-1].split('/')[0]
    
   
    tips = Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date, c.to_perfil_id as destiny, 
                            c.from_perfil_id as origin, p.usuario_id as profile_id, p.type as type, ifnull(f.id,0) as isfav
                            FROM wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites f ON (t.id = f.tip_id AND f.profile_id = %s), 
                            wsbodb.perfis_perfil_contatos c, wsbodb.perfis_perfil p
                            WHERE c.from_perfil_id = t.author_profile_id
                            AND c.to_perfil_id = p.id
                            AND p.usuario_id = %s
                            ORDER BY t.date DESC;""", [request.user.id, request.user.id])

                                    
    following = Tip.objects.raw("""SELECT t.id, p.nome as name, t.content,
                                    t.author_profile_id as author, p.type as type,
                                    p.usuario_id as profile_id, t.author_name as name,
                                    t.date, ifnull(f.id,0) as isfollowing, ifnull(fav.id,0) as isfav,
                                    (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                    (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed,
                                    (t.author_profile_id IN (SELECT p.id FROM wsbodb.perfis_perfil p WHERE p.stealth=1 AND t.author_profile_id=%s)) as stealthed,
                                    (t.id IN (SELECT n.referenced_card FROM wsbodb.perfis_notifications n WHERE n.card_id NOT IN (SELECT re.card_id FROM wsbodb.perfis_removed re WHERE re.profile_id=%s) AND t.author_profile_id=%s)) as notified,
                                    f.followed_id, ifnull(a.upload,0) as upload, t.outdoor
                                    FROM wsbodb.perfis_perfil p, wsbodb.perfis_follow f,
                                    wsbodb.perfis_avatar a, 
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                    ON (t.id = fav.tip_id AND fav.profile_id = %s) 
                                    WHERE p.usuario_id = %s
                                    AND t.author_profile_id = f.followed_id
                                    AND f.follower_id = %s 
                                    AND t.hided = 0
                                    AND f.followed_id = a.profile_id
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""", 
                                    [request.user.perfil.id, request.user.id, request.user.perfil.id, request.user.id, request.user.perfil.id, request.user.id, request.user.id, request.user.id])
                                                              
    is_contact = Tip.objects.raw("""SELECT t.id, f.followed_id as fid, p.nome as name, t.content, 
                                    t.author_profile_id as author, p.type as type,
                                    p.usuario_id as profile_id, t.author_name as name,
                                    t.date, ifnull(f.id,0) as isfollowing, ifnull(fav.id,0) as isfav, 
                                    f.followed_id
                                    FROM wsbodb.perfis_perfil p, wsbodb.perfis_follow f, 
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                    ON (t.id = fav.tip_id AND fav.profile_id = %s) 
                                    WHERE p.usuario_id = %s
                                    AND t.author_profile_id = f.followed_id 
                                    AND f.follower_id = %s 
                                    GROUP BY f.followed_id
                                    ORDER BY t.author_name ASC;""", [request.user.id, request.user.id, request.user.id])

    
    my_profile_image = Tip.objects.raw("""SELECT a.id, a.upload as upload, a.user_id
                                        FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                        ON(a.user_id = p.usuario_id)
                                        WHERE p.usuario_id = %s;""", [request.user.id])  
    
    
    maps = Tip.objects.raw("""SELECT t.id, p.nome as name, t.content, 
                                    t.author_profile_id as author, p.type as type,
                                    p.usuario_id as profile_id, t.author_name as name,
                                    ifnull(a.upload,0) as upload, t.outdoor
                                    FROM wsbodb.perfis_perfil p,
                                    wsbodb.perfis_avatar a, 
                                    wsbodb.perfis_tip t 
                                    WHERE t.author_profile_id = p.id
                                    AND t.author_profile_id = a.profile_id
                                    AND t.hided = 0
                                    AND t.world = 1
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""")
    
    return render(request, 'windy.html', {'perfil':perfil, 'perfis':Perfil.objects.all(), 
                                          'perfil_logado': get_perfil_logado(request), 'tips': tips,
                                          'url':url, 'following':following, 'maps':maps,
                                          'is_contact':is_contact, 'my_profile_image': my_profile_image })
