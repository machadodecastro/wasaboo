from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from requests.models import Request

from perfis import views
import perfis
from perfis.forms import PerfilForm
from perfis.models import Tip, Perfil, Mensagem, Jobs


@login_required
def settings(request):
    return {

    'folder' : Tip.objects.raw("""SELECT  d.id, 
                                        d.author_profile_id as fid, 
                                        d.author_user_id as user, 
                                        d.date as date,  
                                        d.author_name as name,
                                        d.deck_name as deck_name,
                                        fol.id, fol.card_id as card_id, fol.folder_id
                                        FROM wsbodb.perfis_deck d,
                                        wsbodb.perfis_folder fol,
                                        wsbodb.perfis_tip t
                                        WHERE fol.profile_id = %s
                                        AND d.id = fol.folder_id
                                        AND t.id = fol.card_id;""", [request.user.perfil.id]),
            
       
    'decks' : Tip.objects.raw("""SELECT d.id, 
                                        d.author_profile_id as fid, 
                                        d.author_user_id as user, 
                                        d.date as date,  
                                        d.author_name as name,
                                        d.deck_name as deck_name 
                                        FROM wsbodb.perfis_deck d
                                        WHERE d.author_user_id = %s
                                        ORDER BY d.deck_name ASC;""", [request.user.id]),
            
              
    'notifications_all' : Tip.objects.raw("""SELECT n.id, n.referenced_card,
                                            COUNT(*) as howmany
                                            FROM wsbodb.perfis_notifications n
                                            LEFT JOIN wsbodb.perfis_tip t
                                            ON t.id = n.referenced_card
                                            WHERE n.card_id NOT IN (SELECT re.card_id FROM wsbodb.perfis_removed re WHERE re.profile_id=%s) 
                                            AND t.author_profile_id = %s;""", [request.user.id, request.user.perfil.id]),
            
            
    'notifications_count' : Tip.objects.raw("""SELECT n.id, n.referenced_card,
                                            COUNT(*) as howmany
                                            FROM wsbodb.perfis_notifications n
                                            LEFT JOIN wsbodb.perfis_tip t
                                            ON t.id = n.referenced_card
                                            WHERE n.card_id NOT IN (SELECT re.card_id FROM wsbodb.perfis_removed re WHERE re.profile_id=%s) 
                                            AND t.author_profile_id = %s
                                            GROUP BY n.referenced_card;""", [request.user.id, request.user.perfil.id]),
            
    'hotcard' : Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date, p.usuario_id as profile_id, 
                                t.author_user_id as author_user, t.author_name as name, count(fav.tip_id) hot,
                                (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                (t.id IN (SELECT n.referenced_card FROM wsbodb.perfis_notifications n WHERE n.card_id NOT IN (SELECT re.card_id FROM wsbodb.perfis_removed re WHERE re.profile_id=%s) AND t.author_profile_id=%s)) as notified
                                FROM wsbodb.perfis_tip t, wsbodb.perfis_perfil p, wsbodb.perfis_favorites fav 
                                WHERE t.author_user_id = p.usuario_id
                                AND t.author_user_id IN ( SELECT usuario_id FROM wsbodb.perfis_perfil )
                                AND t.author_profile_id = %s
                                AND t.hided = 0
                                AND t.id = fav.tip_id
                                GROUP BY t.id
                                ORDER BY hot DESC
                                LIMIT 1;""", [request.user.perfil.id, request.user.id, request.user.perfil.id, request.user.perfil.id]),

    'others_hotcard' : Tip.objects.raw("""SELECT t.id, t.author_profile_id as author, t.content, t.date, p.usuario_id as profile_id, 
                                t.author_user_id as author_user, t.author_name as name, count(fav.tip_id) hot
                                FROM wsbodb.perfis_tip t, wsbodb.perfis_perfil p, wsbodb.perfis_favorites fav 
                                WHERE t.author_user_id = p.usuario_id
                                AND t.author_user_id IN ( SELECT usuario_id FROM wsbodb.perfis_perfil )
                                AND t.author_profile_id = %s
                                AND t.hided = 0
                                AND t.id = fav.tip_id
                                GROUP BY t.id
                                ORDER BY hot DESC
                                LIMIT 1;""", [request.build_absolute_uri().split('//')[-1].split('/')[-2]]),
  
    'card_on_deck' : Tip.objects.raw("""SELECT d.id,
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
                                        GROUP BY t.id;"""),
            
    'my_background_image' : Tip.objects.raw("""SELECT b.id, b.bkg_upload as bkg_upload, b.user_id,
                                        p.color as color
                                        FROM wsbodb.perfis_background b LEFT JOIN wsbodb.perfis_perfil p
                                        ON(b.user_id = p.usuario_id)
                                        WHERE p.usuario_id = %s;""", [request.user.id]),
            
    'my_avatar_image' : Tip.objects.raw("""SELECT a.id, a.upload as upload, a.user_id
                                        FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                        ON(a.user_id = p.usuario_id)
                                        WHERE p.usuario_id = %s;""", [request.user.id]), 
    
    'chat' : Mensagem.objects.raw("""SELECT *,
                                  p.id as profileID,
                                  a.upload
                                  FROM wsbodb.mensagens_mensagem m,
                                  wsbodb.perfis_perfil p,
                                  wsbodb.perfis_avatar a
                                  WHERE m.origem = p.id
                                  AND p.id = a.profile_id
                                  AND (p.usuario_id = %s or m.destino = %s) 
                                  ORDER BY m.id DESC;""",[request.user.id, request.user.perfil.id]),

 
    
    'chat_all' : Tip.objects.raw("""SELECT m.id, m.outdoor, m.corpo, m.origem,
                                    p.nome, p.type, p.id as profileID,
                                    a.upload,
                                    t.outdoor as imagem, t.slug, t.id as outdoorID
                                    FROM wsbodb.perfis_perfil p,
                                    wsbodb.perfis_avatar a,
                                    wsbodb.mensagens_mensagem m
                                    LEFT JOIN wsbodb.perfis_tip t
                                    ON t.id = m.outdoor
                                    WHERE m.outdoor NOT IN (SELECT re.card_id FROM wsbodb.perfis_removed re WHERE re.profile_id=%s) 
                                    AND m.destino = %s
                                    AND m.origem = p.id
                                    AND p.id = a.profile_id
                                    GROUP BY p.id,t.id
                                    ORDER BY m.criacao DESC;""", [request.user.id, request.user.perfil.id]),   
    
    
    'job' : Jobs.objects.raw("""SELECT  j.id, 
                                        j.jobs_profile_id,
                                        j.company as company,
                                        j.status_work
                                        FROM wsbodb.perfis_jobs j;"""),  
    
    'categories' : Tip.objects.raw("""SELECT d.id, 
                                        d.author_profile_id as fid, 
                                        d.author_user_id as user, 
                                        d.date as date,  
                                        d.author_name as name,
                                        d.deck_name as deck_name 
                                        FROM wsbodb.perfis_deck d,
                                        wsbodb.perfis_tip t,
                                        wsbodb.perfis_folder f
                                        WHERE t.world = 2
                                        AND t.id = f.card_id
                                        AND d.id = f.folder_id
                                        GROUP BY d.deck_name
                                        ORDER BY d.deck_name ASC;"""),            
                    
    }