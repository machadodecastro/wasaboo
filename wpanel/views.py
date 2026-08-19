from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from perfis.models import Tip
from perfis.views import get_perfil_logado


#Wasaboo Control Panel Dashboard
@login_required
def home(request):
    users_count = Tip.objects.raw("""SELECT p.id, COUNT(*) as amount
                                    FROM wsbodb._usuarios_user u,
                                    wsbodb.perfis_perfil p
                                    WHERE u.id = p.usuario_id;""") 
    
    superusers_count = Tip.objects.raw("""SELECT p.id, COUNT(*) as amount
                                        FROM wsbodb._usuarios_user u,
                                        wsbodb.perfis_perfil p
                                        WHERE u.id = p.usuario_id
                                        AND u.is_superuser = 1;""")    
    
    users_stealth_count = Tip.objects.raw("""SELECT p.id, COUNT(*) as amount
                                            FROM wsbodb._usuarios_user u,
                                            wsbodb.perfis_perfil p
                                            WHERE u.id = p.usuario_id
                                            AND p.stealth = 1;""") 
    
    users_masculine_count = Tip.objects.raw("""SELECT p.id, COUNT(*) as amount
                                            FROM wsbodb._usuarios_user u,
                                            wsbodb.perfis_perfil p
                                            WHERE u.id = p.usuario_id
                                            AND p.type = 'm';""")
    
    users_feminine_count = Tip.objects.raw("""SELECT p.id, COUNT(*) as amount
                                            FROM wsbodb._usuarios_user u,
                                            wsbodb.perfis_perfil p
                                            WHERE u.id = p.usuario_id
                                            AND p.type = 'f';""")
    
    users_company_count = Tip.objects.raw("""SELECT p.id, COUNT(*) as amount
                                            FROM wsbodb._usuarios_user u,
                                            wsbodb.perfis_perfil p
                                            WHERE u.id = p.usuario_id
                                            AND p.type = 'c';""") 
    
    users_short_description_count = Tip.objects.raw("""SELECT s.id, COUNT(*) as amount
                                                    FROM wsbodb.perfis_short_description s,
                                                    wsbodb.perfis_perfil p
                                                    WHERE s.profile_id = p.id;""") 
    
    cards_count = Tip.objects.raw("""SELECT t.id, COUNT(*) as amount, 
                            t.author_name, t.content, t.date, t.hided, 
                            t.reference, t.link, t.updated_date, t.outdoor
                            FROM wsbodb.perfis_tip t;""")
    
    played_cards_count = Tip.objects.raw("""SELECT play.id, COUNT(*) as amount
                            FROM wsbodb.perfis_played_cards play;""")
    
    removed_cards_count = Tip.objects.raw("""SELECT r.id, COUNT(*) as amount
                            FROM wsbodb.perfis_removed r;""")
    
    favorites_count = Tip.objects.raw("""SELECT fav.id, COUNT(*) as amount
                            FROM wsbodb.perfis_favorites fav,
                            wsbodb.perfis_tip t
                            WHERE t.id = fav.tip_id;""") 
    
    followers_count = Tip.objects.raw("""SELECT f.id, COUNT(*) as amount
                            FROM wsbodb.perfis_follow f,
                            wsbodb._usuarios_user u
                            WHERE f.follower_id = u.id;""")
    
    decks_count = Tip.objects.raw("""SELECT d.id, COUNT(*) as amount
                            FROM wsbodb.perfis_deck d;""") 
      
    whoami_count = Tip.objects.raw("""SELECT w.id, COUNT(*) as amount,
                                    w.whoami_profile_id, w.whoami_content,
                                    p.id as profile_id, p.nome, p.usuario_id, p.type
                                    FROM wsbodb.perfis_whoami w,
                                    wsbodb.perfis_perfil p
                                    WHERE w.whoami_profile_id = p.id;""") 
    
    education_count = Tip.objects.raw("""SELECT e.id, COUNT(*) as amount,
                                        e.education_profile_id, e.school, e.course, e.degree, e.graduation,
                                        p.id as profile_id, p.nome, p.usuario_id, p.type
                                        FROM wsbodb.perfis_education e,
                                        wsbodb.perfis_perfil p
                                        WHERE e.education_profile_id = p.id;""") 
    
    knows_count = Tip.objects.raw("""SELECT k.id, COUNT(*) as amount,
                                    k.knows_profile_id, k.topic,
                                    p.id as profile_id, p.nome, p.usuario_id, p.type
                                    FROM wsbodb.perfis_knows k,
                                    wsbodb.perfis_perfil p
                                    WHERE k.knows_profile_id = p.id;""") 
    
    jobs_count = Tip.objects.raw("""SELECT j.id, COUNT(*) as amount,
                                    j.jobs_profile_id, j.company, j.position, j.start_year, j.end_year,
                                    p.id as profile_id, p.nome, p.usuario_id, p.type
                                    FROM wsbodb.perfis_jobs j,
                                    wsbodb.perfis_perfil p
                                    WHERE j.jobs_profile_id = p.id;""")
    
    company_count = Tip.objects.raw("""SELECT c.id, COUNT(*) as amount,
                                        c.company_profile_id, c.company_content,
                                        p.id as profile_id, p.nome, p.usuario_id, p.type
                                        FROM wsbodb.perfis_company c,
                                        wsbodb.perfis_perfil p
                                        WHERE c.company_profile_id = p.id;""")
    
    location_count = Tip.objects.raw("""SELECT l.id, COUNT(*) as amount,
                                        l.location_profile_id, l.address,
                                        p.id as profile_id, p.nome, p.usuario_id, p.type
                                        FROM wsbodb.perfis_location l,
                                        wsbodb.perfis_perfil p
                                        WHERE l.location_profile_id = p.id;""") 
      
    return render(request, 'dashboard.html',  locals())


#All Users
@login_required
def users(request):
    users = Tip.objects.raw("""SELECT p.id, u.email, u.date_joined,
                            p.nome, p.type, p.stealth, p.usuario_id,
                            ifnull(a.upload,0) as upload,
                            b.bkg_upload, b.profile_id
                            FROM wsbodb._usuarios_user u,
                            wsbodb.perfis_perfil p,
                            wsbodb.perfis_avatar a,
                            wsbodb.perfis_background b
                            WHERE u.id = p.usuario_id
                            AND a.profile_id = p.id
                            AND b.profile_id = p.id;""")  
    
    return render(request, 'users.html',  locals())

#All SuperUsers
@login_required
def superusers(request):
    superusers = Tip.objects.raw("""SELECT p.id, u.email, u.date_joined,
                            p.nome, p.type, p.stealth, p.usuario_id,
                            ifnull(a.upload,0) as upload
                            FROM wsbodb._usuarios_user u,
                            wsbodb.perfis_perfil p,
                            wsbodb.perfis_avatar a
                            WHERE u.id = p.usuario_id
                            AND a.profile_id = p.id
                            AND u.is_superuser = 1;""")  
    
    return render(request, 'superusers.html',  locals()) 

#All Users in Stealth Mode
@login_required
def users_in_stealth(request):
    users_in_stealth = Tip.objects.raw("""SELECT p.id, u.email, u.date_joined,
                            p.nome, p.type, p.stealth, p.usuario_id,
                            ifnull(a.upload,0) as upload
                            FROM wsbodb._usuarios_user u,
                            wsbodb.perfis_perfil p,
                            wsbodb.perfis_avatar a
                            WHERE u.id = p.usuario_id
                            AND a.profile_id = p.id
                            AND p.stealth = 1;""")  
    
    return render(request, 'users_stealth.html',  locals())

#All Masculines Profiles
@login_required
def users_masculine(request):
    users_masculine = Tip.objects.raw("""SELECT p.id, u.email, u.date_joined,
                            p.nome, p.type, p.stealth, p.usuario_id,
                            ifnull(a.upload,0) as upload
                            FROM wsbodb._usuarios_user u,
                            wsbodb.perfis_perfil p,
                            wsbodb.perfis_avatar a
                            WHERE u.id = p.usuario_id
                            AND a.profile_id = p.id
                            AND p.type = 'm';""")  
    
    return render(request, 'users_masculine.html',  locals())

#All Feminine Profiles
@login_required
def users_feminine(request):
    users_feminine = Tip.objects.raw("""SELECT p.id, u.email, u.date_joined,
                            p.nome, p.type, p.stealth, p.usuario_id,
                            ifnull(a.upload,0) as upload
                            FROM wsbodb._usuarios_user u,
                            wsbodb.perfis_perfil p,
                            wsbodb.perfis_avatar a
                            WHERE u.id = p.usuario_id
                            AND a.profile_id = p.id
                            AND p.type = 'f';""")  
    
    return render(request, 'users_feminine.html',  locals())

#All Company Profiles
@login_required
def users_company(request):
    users_company = Tip.objects.raw("""SELECT p.id, u.email, u.date_joined,
                            p.nome, p.type, p.stealth, p.usuario_id,
                            ifnull(a.upload,0) as upload
                            FROM wsbodb._usuarios_user u,
                            wsbodb.perfis_perfil p,
                            wsbodb.perfis_avatar a
                            WHERE u.id = p.usuario_id
                            AND a.profile_id = p.id
                            AND p.type = 'c';""")  
    
    return render(request, 'users_company.html',  locals())

#All Users Short Descriptions
@login_required
def users_short_description(request):
    users_short_description = Tip.objects.raw("""SELECT s.id, s.description,
                            p.id as profile_id, p.nome, p.type, p.stealth, p.usuario_id,
                            ifnull(a.upload,0) as upload
                            FROM wsbodb.perfis_short_description s,
                            wsbodb.perfis_perfil p,
                            wsbodb.perfis_avatar a
                            WHERE s.profile_id = p.id
                            AND a.profile_id = p.id;""")  
    
    return render(request, 'users_short_description.html',  locals())


#All Cards
@login_required
def cards(request):
    cards = Tip.objects.raw("""SELECT t.id, t.author_profile_id,
                            t.author_name, t.content, t.date, t.hided, 
                            t.reference, t.link, t.updated_date, t.outdoor,
                            p.id as profile_id, p.nome, p.type, p.stealth, p.usuario_id,
                            ifnull(a.upload,0) as upload
                            FROM wsbodb.perfis_tip t,
                            wsbodb.perfis_perfil p,
                            wsbodb.perfis_avatar a
                            WHERE a.profile_id = t.author_profile_id
                            AND a.profile_id = p.id;""")  
    
    return render(request, 'cards.html',  locals())


#Played Cards
@login_required
def played_cards(request):    
    played_cards = Tip.objects.raw("""SELECT play.id, play.card_id, play.player_id, play.referenced_card,
                            p.id as profile_id, p.nome, p.usuario_id, p.type,
                            ifnull(a.upload,0) as upload,
                            t.slug as slug
                            FROM wsbodb.perfis_played_cards play,
                            wsbodb.perfis_perfil p,
                            wsbodb.perfis_avatar a,
                            wsbodb.perfis_tip t
                            WHERE play.player_id = p.id
                            AND a.profile_id = p.id
                            AND t.id = play.referenced_card
                            GROUP BY play.card_id;""")
    
    cards_played = Tip.objects.raw("""SELECT play.id, play.card_id, play.player_id, play.referenced_card,
                            p.id as profile_id, p.nome, p.usuario_id, p.type,
                            t.slug as slug                            
                            FROM wsbodb.perfis_played_cards play,
                            wsbodb.perfis_perfil p,
                            wsbodb.perfis_tip t                            
                            WHERE play.player_id = p.id
                            AND t.id = play.referenced_card;""")
    
    cards_accepted = Tip.objects.raw("""SELECT play.id, play.card_id, play.player_id, play.referenced_card,
                            p.id as profile_id, p.nome, p.usuario_id,
                            t.slug as slug
                            FROM wsbodb.perfis_played_cards play,
                            wsbodb.perfis_perfil p,
                            wsbodb.perfis_tip t
                            WHERE play.player_id = p.id
                            AND play.played = 2
                            AND t.id = play.referenced_card;""")  
    
    return render(request, 'users_played_cards.html',  locals())


#Removed Cards
@login_required
def removed_cards(request):    
    removed_cards = Tip.objects.raw("""SELECT r.id, r.card_id, r.profile_id, r.removed_by,
                            p.id as profile_id, p.nome, p.usuario_id, p.type,
                            t.slug as slug                            
                            FROM wsbodb.perfis_removed r,
                            wsbodb.perfis_perfil p,                            
                            wsbodb._usuarios_user u,
                            wsbodb.perfis_tip t
                            WHERE r.profile_id = p.usuario_id
                            AND u.id = p.usuario_id                            
                            GROUP BY r.card_id;""")
    
    cards_removed = Tip.objects.raw("""SELECT r.id, r.card_id, r.profile_id, r.removed_by,
                            p.id as profile_id, p.nome, p.usuario_id, p.type,
                            ifnull(a.upload,0) as upload
                            FROM wsbodb.perfis_removed r,
                            wsbodb.perfis_perfil p,
                            wsbodb.perfis_avatar a,
                            wsbodb._usuarios_user u
                            WHERE r.profile_id = p.usuario_id
                            AND a.profile_id = p.id
                            AND u.id = p.usuario_id;""")
        
    return render(request, 'users_removed_cards.html',  locals())

#Favorites by Users
@login_required
def users_favorites(request):    
    users_favorites = Tip.objects.raw("""SELECT fav.id, 
                            p.usuario_id, p.nome, p.id as profile_id, p.type,
                            ifnull(a.upload,0) as upload,
                            fav.favorite, fav.tip_id
                            FROM wsbodb.perfis_favorites fav,
                            wsbodb.perfis_perfil p,
                            wsbodb.perfis_avatar a,
                            wsbodb._usuarios_user u,
                            wsbodb.perfis_tip t
                            WHERE u.id = p.usuario_id
                            AND a.profile_id = p.id
                            AND fav.profile_id = u.id
                            AND t.id = fav.tip_id
                            GROUP BY p.id;""")
    
    favoriteds = Tip.objects.raw("""SELECT fav.id, t.slug as slug,
                            p.id as profile_id, p.usuario_id, p.nome, p.type,
                            ifnull(a.upload,0) as upload,
                            fav.favorite, fav.tip_id
                            FROM wsbodb.perfis_favorites fav,
                            wsbodb.perfis_perfil p,
                            wsbodb.perfis_avatar a,
                            wsbodb._usuarios_user u,
                            wsbodb.perfis_tip t
                            WHERE u.id = p.usuario_id
                            AND a.profile_id = t.author_profile_id
                            AND fav.profile_id = u.id
                            AND t.id = fav.tip_id;""")  
    
    return render(request, 'users_favorites.html',  locals())


#Followers
@login_required
def users_followers(request):    
    users_followers = Tip.objects.raw("""SELECT f.id, f.follower_id, f.followed_id,
                            p.id as profile_id, p.nome, p.usuario_id, p.type,
                            ifnull(a.upload,0) as upload
                            FROM wsbodb.perfis_follow f,
                            wsbodb._usuarios_user u,
                            wsbodb.perfis_avatar a,
                            wsbodb.perfis_perfil p
                            WHERE f.follower_id = u.id
                            AND u.id = p.usuario_id
                            AND a.profile_id = p.id
                            GROUP BY p.id;""")
    
    users_followeds = Tip.objects.raw("""SELECT f.id, f.follower_id, f.followed_id,
                            p.id as perfil, p.nome, p.usuario_id, p.type,
                            ifnull(a.upload,0) as upload
                            FROM wsbodb._usuarios_user u,
                            wsbodb.perfis_avatar a,
                            wsbodb.perfis_follow f
                            LEFT JOIN wsbodb.perfis_perfil p
                            ON f.followed_id = p.id                                                       
                            WHERE u.id = p.usuario_id
                            AND a.profile_id = p.id
                            AND f.follower_id <> u.id;""")  
    
    return render(request, 'users_followers.html',  locals())


#Followed
@login_required
def users_followed(request):    
    users_followed = Tip.objects.raw("""SELECT f.id, f.follower_id, f.followed_id,
                            p.id as profile_id, p.nome, p.usuario_id, p.type,
                            ifnull(a.upload,0) as upload
                            FROM wsbodb.perfis_follow f,
                            wsbodb._usuarios_user u,
                            wsbodb.perfis_avatar a,
                            wsbodb.perfis_perfil p
                            WHERE f.followed_id = p.id
                            AND a.profile_id = p.id
                            AND u.id = p.usuario_id
                            GROUP BY p.id;""")
    
    users_followers = Tip.objects.raw("""SELECT f.id, f.follower_id, f.followed_id,
                            p.id as profile_id, p.nome, p.usuario_id, p.type,
                            ifnull(a.upload,0) as upload
                            FROM wsbodb._usuarios_user u,
                            wsbodb.perfis_avatar a,
                            wsbodb.perfis_follow f
                            LEFT JOIN wsbodb.perfis_perfil p
                            ON f.follower_id = p.usuario_id                                                       
                            WHERE u.id = p.usuario_id
                            AND a.profile_id = p.id
                            AND f.followed_id <> p.id;""")  
    
    return render(request, 'users_followed.html',  locals())


#Decks
@login_required
def users_decks(request):    
    users_decks = Tip.objects.raw("""SELECT d.id, d.author_user_id, d.author_profile_id,
                            d.author_name, d.deck_name, d.date,
                            p.id as profile_id, p.nome, p.usuario_id, p.type,
                            ifnull(a.upload,0) as upload
                            FROM wsbodb.perfis_deck d,
                            wsbodb._usuarios_user u,
                            wsbodb.perfis_perfil p,
                            wsbodb.perfis_avatar a
                            WHERE d.author_profile_id = p.id
                            AND u.id = p.usuario_id
                            AND a.profile_id = p.id
                            GROUP BY d.author_profile_id;""")
    
    decks_created = Tip.objects.raw("""SELECT d.id, d.author_user_id, d.author_profile_id,
                            d.author_name, d.deck_name, d.date,
                            p.id as profile_id, p.nome, p.usuario_id
                            FROM wsbodb.perfis_deck d,
                            wsbodb._usuarios_user u,
                            wsbodb.perfis_perfil p
                            WHERE d.author_profile_id = p.id
                            AND u.id = p.usuario_id;""")  
    
    cards_in_deck = Tip.objects.raw("""SELECT f.id, f.folder_id, 
                            COUNT(*) as amount
                            FROM wsbodb.perfis_folder f
                            GROUP BY f.folder_id;""") 
    
    return render(request, 'users_decks.html',  locals())  


#Who Am I
@login_required
def users_whoami(request):    
    users_whoami = Tip.objects.raw("""SELECT w.id,
                                    w.whoami_profile_id, w.whoami_content,
                                    p.id as profile_id, p.nome, p.usuario_id, p.type,
                                    ifnull(a.upload,0) as upload
                                    FROM wsbodb.perfis_whoami w,
                                    wsbodb.perfis_perfil p,
                                    wsbodb.perfis_avatar a
                                    WHERE w.whoami_profile_id = p.id
                                    AND a.profile_id = p.id
                                    GROUP BY w.whoami_profile_id;""")
    
    whoami_cards = Tip.objects.raw("""SELECT w.id,
                                    w.whoami_profile_id, w.whoami_content,
                                    p.id as profile_id, p.nome, p.usuario_id, p.type
                                    FROM wsbodb.perfis_whoami w,
                                    wsbodb.perfis_perfil p
                                    WHERE w.whoami_profile_id = p.id;""")  
    
    return render(request, 'users_whoami.html',  locals())

#Education
@login_required
def users_education(request):    
    users_education = Tip.objects.raw("""SELECT e.id,
                                        e.education_profile_id, e.school, e.course, e.degree, e.graduation,
                                        p.id as profile_id, p.nome, p.usuario_id, p.type,
                                        ifnull(a.upload,0) as upload
                                        FROM wsbodb.perfis_education e,
                                        wsbodb.perfis_perfil p,
                                        wsbodb.perfis_avatar a
                                        WHERE e.education_profile_id = p.id
                                        AND a.profile_id = p.id
                                        GROUP BY e.education_profile_id;""")
    
    education_cards = Tip.objects.raw("""SELECT e.id,
                                        e.education_profile_id, e.school, e.course, e.degree, e.graduation,
                                        p.id as profile_id, p.nome, p.usuario_id, p.type
                                        FROM wsbodb.perfis_education e,
                                        wsbodb.perfis_perfil p
                                        WHERE e.education_profile_id = p.id;""")  
    
    return render(request, 'users_education.html',  locals())

#Knows
@login_required
def users_knows(request):    
    users_knows = Tip.objects.raw("""SELECT k.id,
                                    k.knows_profile_id, k.topic,
                                    p.id as profile_id, p.nome, p.usuario_id, p.type,
                                    ifnull(a.upload,0) as upload
                                    FROM wsbodb.perfis_knows k,
                                    wsbodb.perfis_perfil p,
                                    wsbodb.perfis_avatar a
                                    WHERE k.knows_profile_id = p.id
                                    AND a.profile_id = p.id
                                    GROUP BY k.knows_profile_id;""")
    
    knows_cards = Tip.objects.raw("""SELECT k.id,
                                        k.knows_profile_id, k.topic,
                                        p.id as profile_id, p.nome, p.usuario_id, p.type
                                        FROM wsbodb.perfis_knows k,
                                        wsbodb.perfis_perfil p
                                        WHERE k.knows_profile_id = p.id;""")  
    
    return render(request, 'users_knows.html',  locals())

#Jobs
@login_required
def users_jobs(request):    
    users_jobs = Tip.objects.raw("""SELECT j.id,
                                    j.jobs_profile_id, j.company, j.position, j.start_year, j.end_year,
                                    p.id as profile_id, p.nome, p.usuario_id, p.type,
                                    ifnull(a.upload,0) as upload
                                    FROM wsbodb.perfis_jobs j,
                                    wsbodb.perfis_perfil p,
                                    wsbodb.perfis_avatar a
                                    WHERE j.jobs_profile_id = p.id
                                    AND a.profile_id = p.id
                                    GROUP BY j.jobs_profile_id;""")
    
    jobs_cards = Tip.objects.raw("""SELECT j.id,
                                    j.jobs_profile_id, j.company, j.position, j.start_year, j.end_year,
                                    p.id as profile_id, p.nome, p.usuario_id, p.type
                                    FROM wsbodb.perfis_jobs j,
                                    wsbodb.perfis_perfil p
                                    WHERE j.jobs_profile_id = p.id;""")  
    
    return render(request, 'users_jobs.html',  locals())

#Company About
@login_required
def users_company_about(request):    
    users_company_about = Tip.objects.raw("""SELECT c.id,
                                        c.company_profile_id, c.company_content,
                                        p.id as profile_id, p.nome, p.usuario_id, p.type,
                                        ifnull(a.upload,0) as upload
                                        FROM wsbodb.perfis_company c,
                                        wsbodb.perfis_perfil p,
                                        wsbodb.perfis_avatar a
                                        WHERE c.company_profile_id = p.id
                                        AND a.profile_id = p.id
                                        GROUP BY c.company_profile_id;""")
    
    company_cards = Tip.objects.raw("""SELECT c.id,
                                        c.company_profile_id, c.company_content,
                                        p.id as profile_id, p.nome, p.usuario_id, p.type
                                        FROM wsbodb.perfis_company c,
                                        wsbodb.perfis_perfil p
                                        WHERE c.company_profile_id = p.id;""")  
    
    return render(request, 'users_company_about.html',  locals())

#Location
@login_required
def users_location(request):    
    users_location = Tip.objects.raw("""SELECT l.id,
                                        l.location_profile_id, l.address,
                                        p.id as profile_id, p.nome, p.usuario_id, p.type,
                                        ifnull(a.upload,0) as upload
                                        FROM wsbodb.perfis_location l,
                                        wsbodb.perfis_perfil p,
                                        wsbodb.perfis_avatar a
                                        WHERE l.location_profile_id = p.id
                                        AND a.profile_id = p.id
                                        GROUP BY l.location_profile_id;""")
    
    location_cards = Tip.objects.raw("""SELECT l.id,
                                        l.location_profile_id, l.address,
                                        p.id as profile_id, p.nome, p.usuario_id, p.type
                                        FROM wsbodb.perfis_location l,
                                        wsbodb.perfis_perfil p
                                        WHERE l.location_profile_id = p.id;""")  
    
    return render(request, 'users_location.html',  locals())