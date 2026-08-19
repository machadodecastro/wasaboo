# connectedin/perfis/urls.py 
from django.conf.urls import patterns, url, include
from django.core.context_processors import request
from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet
from haystack.views import search_view_factory, SearchView, FacetedSearchView

from perfis import views

sqs = SearchQuerySet().order_by('-date')
#sqs = SearchQuerySet().spelling_suggestion('q')


urlpatterns = patterns('',  
    url(r'^home/$', views.public, name='public'),
    url(r'^$', views.how_it_works, name='how_it_works'),
    url(r'^feed/$', views.index, name='index'),
    url(r'^profile/(?P<perfil_id>\d+)/$', views.exibir, name='exibir'),
    url(r'^profile/(?P<perfil_id>\d+)/(?P<tip_pk>\d+)/$', views.exibir, name='exibir'),
    url(r'^profile/(?P<perfil_id>\d+)/convidar$', views.convidar, name='convidar'),
    url(r'^convite/(?P<convite_id>\d+)/aceitar$', views.aceitar, name='aceitar'),
    url(r'^notifications/$', views.notifications, name='notifications'),
    url(r'^contacts/(?P<perfil_id>\d+)/$', views.contacts, name='contacts'),
    url(r'^followers/(?P<perfil_id>\d+)/$', views.followers, name='followers'),
	url(r'^removed_cards/(?P<perfil_id>\d+)$', views.removed_cards, name='removed_cards'),
    url(r'^accepted_cards/(?P<perfil_id>\d+)$', views.accepted_cards, name='accepted_cards'),
    url(r'^config/(?P<perfil_id>\d+)/$', views.config, name='config'),
    url(r'^stats/(?P<perfil_id>\d+)/$', views.stats, name='stats'),
    url(r'^bysubject/(?P<perfil_id>\d+)/(?P<pk>\d+)/$', views.bysubject, name='bysubject'),
    
    #CHANGE PROFILE TYPE
    url(r'^update_type_company/(?P<perfil_id>\d+)/$', views.update_type_company, name='update_type_company'),
    url(r'^update_type_female/(?P<perfil_id>\d+)/$', views.update_type_female, name='update_type_female'),
    url(r'^update_type_male/(?P<perfil_id>\d+)/$', views.update_type_male, name='update_type_male'), 
    
    #ACTIVATE/DEACTIVATE STEALTH MODE
    url(r'^activate_stealth_mode/(?P<perfil_id>\d+)/$', views.activate_stealth_mode, name='activate_stealth_mode'),
    url(r'^deactivate_stealth_mode/(?P<perfil_id>\d+)/$', views.deactivate_stealth_mode, name='deactivate_stealth_mode'), 
        
    #DEACTIVATE ACCOUNT
    url(r'^deactivate_account/(?P<perfil_id>\d+)/$', views.deactivate_account, name='deactivate_account'),
        
    #CAMPAIGNS
    url(r'^decks/(?P<perfil_id>\d+)/$', views.decks, name='decks'), #View all profile folders
    url(r'^deck/(?P<pk>\d+)/$', views.deck, name='deck'), #View into folder 
    url(r'deck/new/$', views.new_deck, name='new_deck'), #Create new folder
    url(r'^update-deck/(?P<pk>\d+)/$', views.update_deck, name='update_deck'), #Action to UPDATE folder name
    url(r'^delete-deck/(?P<pk>\d+)/$', views.delete_deck, name='delete_deck'), #Action to delete folder
    
    
    #OUTDOORS
    url(r'^tip/new/$', views.new_tip, name='new_tip'),
    url(r'^update-card/(?P<pk>\d+)/$', views.update_card, name='update_card'), #Action to update card
    url(r'^update-card-on-profile/(?P<pk>\d+)/$', views.update_card_on_profile, name='update_card_on_profile'), #Action to update card on Profile page
    url(r'^update-card-on-hided/(?P<pk>\d+)/$', views.update_card_on_hided, name='update_card_on_hided'), #Action to update card on Hided page
    url(r'^update-card-on-deck/(?P<pk>\d+)/$', views.update_card_on_deck, name='update_card_on_deck'), #Action to update card on Deck page
    url(r'^update-card-on-card/(?P<pk>\d+)$', views.update_card_on_card, name='update_card_on_card'), #Action to update card on Card page
    url(r'^update-card-on-search/(?P<pk>\d+)$', views.update_card_on_search, name='update_card_on_search'), #Action to update card on Search page
    url(r'^update-card-on-bysubject/(?P<pk>\d+)/$', views.update_card_on_bysubject, name='update_card_on_bysubject'), #Action to update card on BySubject page
    url(r'^delete-tip/(?P<pk>\d+)/$', views.delete_tip, name='delete_tip'), #Action to delete tip
    url(r'^save-into-folder/(?P<pk>\d+)/$', views.save_into_folder, name='save_into_folder'), #Action to save card into folder
    url(r'^remove-from-folder/(?P<pk>\d+)/$', views.remove_from_folder, name='remove_from_folder'), #Action to remove card from folder
    url(r'^(?P<slug>[-\w\d]+)-(?P<pk>\d+)$', views.show_tip, name='show_tip'), #Show single outdoor
    url(r'^connected-to/(?P<slug>[-\w\d]+)-(?P<pk>\d+)$', views.show_connected, name='show_connected'), #Show connected outdoors
    url(r'^remove-upload/(?P<pk>\d+)/$', views.remove_upload, name='remove_upload'), #Action to delete uploaded image from card
    url(r'^delete-notification/(?P<pk>\d+)/$', views.delete_notification, name='delete_notification'), #Action to delete card's notification
    

    #PLAY OUTDOORS
    url(r'^play-card/(?P<pk>\d+)/$', views.play_card, name='play_card'), #Action to play card to other player
    
    url(r'^play-to/(?P<slug>[-\w\d]+)-(?P<pk>\d+)$', views.play_to, name='play_to'), #Play area
    
    
    #HOLD OUTDOORS
    url(r'^hold-card/(?P<pk>\d+)/$', views.hold_card, name='hold_card'), #Action to hold card to your deck
    
    url(r'^hold-to/(?P<slug>[-\w\d]+)-(?P<pk>\d+)$', views.hold_to, name='hold_to'), #Hold area
    
    
    #BUY OUTDOORS
    url(r'^buy/(?P<pk>\d+)/$', views.buy, name='buy'), #Action to buy outdoor
    
    url(r'^buy-action/(?P<slug>[-\w\d]+)-(?P<pk>\d+)$', views.buy_action, name='buy_action'), #Market area
    
    
    #REMOVE OUTDOORS
    url(r'^remove-by-discard/(?P<pk>\d+)/$', views.remove_discard, name='remove_discard'),
    url(r'^remove-by-harassment/(?P<pk>\d+)/$', views.remove_harassment, name='remove_harassment'),
    url(r'^remove-by-spam/(?P<pk>\d+)/$', views.remove_spam, name='remove_spam'),
    url(r'^remove-by-plagiarism/(?P<pk>\d+)/$', views.remove_plagiarism, name='remove_plagiarism'),
    url(r'^remove-by-joke/(?P<pk>\d+)/$', views.remove_joke, name='remove_joke'),
    url(r'^remove-by-out/(?P<pk>\d+)/$', views.remove_out, name='remove_out'),
    url(r'^remove-by-written/(?P<pk>\d+)/$', views.remove_written, name='remove_written'),
    url(r'^remove-by-fake/(?P<pk>\d+)/$', views.remove_fake, name='remove_fake'),
    url(r'^remove-by-image/(?P<pk>\d+)/$', views.remove_image, name='remove_image'),
    url(r'^remove-by-incorrect/(?P<pk>\d+)/$', views.remove_incorrect, name='remove_incorrect'),
    
    
    #RESTORE CARDS
    url(r'^restore/(?P<pk>\d+)/$', views.restore, name='restore'),
    
    
    #WHO_ACCEPTED YOUR CARD
    url(r'^who-accepted/(?P<pk>\d+)/$', views.who_accepted, name='who_accepted'),
    
    
    #FAVORITES
    url(r'^favorites/(?P<perfil_id>\d+)/$', views.favorites, name='favorites'),
    url(r'^tips-favorites/(?P<pk>\d+)/$', views.favorite_tips, name='favorite_tips'),
    url(r'^tips-desfavorites/(?P<pk>\d+)/$', views.desfavorite_tips, name='desfavorite_tips'),
    
    
    
    #HIDED
    url(r'^hided/(?P<perfil_id>\d+)/$', views.hided, name='hided'),
    url(r'^tips-hide/(?P<pk>\d+)/$', views.hide_tips, name='hide_tips'),
    url(r'^tips-show/(?P<pk>\d+)/$', views.show_tips, name='show_tips'),
    
    #LIKES
    url(r'^tips-likes/(?P<pk>\d+)/$', views.like_tips, name='like_tips'),
    
    
    #MY FEED WITHOUT WORLDS
    url(r'^myfeed-on/(?P<pk>\d+)/$', views.myfeed_on, name='myfeed_on'),
    
    #MY FEED WITH WORLDS
    url(r'^world-on/(?P<pk>\d+)/$', views.world_on, name='world_on'),
    url(r'^world-off/(?P<pk>\d+)/$', views.world_off, name='world_off'),
    
    
    #MAPS WORLD
    url(r'^map/$', views.map_init, name='map'),
    url(r'^mapping/(?P<pk>\d+)/$', views.mapping, name='mapping'),
    url(r'^map-on/(?P<pk>\d+)/$', views.map_on, name='map_on'),
    url(r'^map-off/(?P<pk>\d+)/$', views.map_off, name='map_off'),
    
    #FYS WORLD
    url(r'^fys-on/(?P<pk>\d+)/$', views.fys_on, name='fys_on'),
    
    #ADIDAS WORLD
    url(r'^adidas-on/(?P<pk>\d+)/$', views.adidas_on, name='adidas_on'),
    
    
    #UPCARDS
    url(r'^cards-upcards/(?P<pk>\d+)/$', views.upcards_cards, name='upcards_cards'),

    
    #FOLLOWING
    #url(r'^following/(?P<perfil_id>\d+)/$', views.hided, name='hided'),
    #url(r'^tips/hide/(?P<pk>\d+)$', views.hide_tips, name='hide_tips'),
    url(r'^tips-follow/(?P<pk>\d+)/$', views.follow_tips, name='follow_tips'),
    url(r'^tips-nofollow/(?P<pk>\d+)/$', views.no_follow_tips, name='no_follow_tips'),

    
    #CARD MORE
    url(r'^show-references/(?P<pk>\d+)/$', views.show_references, name='show_references'), #Action to show more...
    url(r'^show-content/(?P<pk>\d+)/$', views.show_content, name='show_content'), #Back to tip main content


    #WHO FAVORITED CARD
    url(r'^who-favorited/(?P<pk>\d+)/$', views.who_favorited, name='who_favorited'), #Action to CALL WHO FAVORITED
	url(r'^who-favorited-list/(?P<pk>\d+)/$', views.who_favorited_list, name='who_favorited_list'), #Action to CALL WHO FAVORITED
 
    
    #PROFILE HEADER
    url(r'^edit-profile-name/(?P<pk>\d+)/$', views.update_profile_name, name='update_profile_name'),
    url(r'^publish-short-description/(?P<pk>\d+)/$', views.publish_short_description, name='publish_short_description'),
    url(r'^update-short-description/(?P<pk>\d+)/$', views.update_short_description, name='update_short_description'),
    url(r'^delete-short-description/(?P<pk>\d+)/$', views.delete_short_description, name='delete_short_description'), 
    url(r'^new-profile-picture/(?P<pk>\d+)/$', views.new_profile_picture, name='new_profile_picture'),
    url(r'^new-background-picture/(?P<pk>\d+)/$', views.new_background_picture, name='new_background_picture'),
    url(r'^change-background-default/(?P<pk>\d+)/$', views.change_background_default, name='change_background_default'),
    url(r'^change-white-text/(?P<pk>\d+)/$', views.change_white_text, name='change_white_text'),
    url(r'^change-black-text/(?P<pk>\d+)/$', views.change_black_text, name='change_black_text'),
 
    
    #WHO AM I PROFILE DETAILS
    url(r'^profile/whoami/(?P<perfil_id>\d+)/$', views.whoami, name='whoami'),
    url(r'^update-whoami/(?P<pk>\d+)/$', views.update_whoami, name='update_whoami'), #Action to UPDATE whoami
    url(r'^delete-whoami/(?P<pk>\d+)/$', views.delete_whoami, name='delete_whoami'), #Action to DELETE whoami

    
    #EDUCATION PROFILE DETAILS
    url(r'^profile/education/(?P<perfil_id>\d+)/$', views.education, name='education'),
    url(r'^update-education/(?P<pk>\d+)/$', views.update_education, name='update_education'), #Action to UPDATE Education    
    url(r'^delete-education/(?P<pk>\d+)/$', views.delete_education, name='delete_education'), #Action to DELETE Education


    #KNOWS ABOUT PROFILE DETAILS
    url(r'^profile/knows/(?P<perfil_id>\d+)/$', views.knows, name='knows'),
    url(r'^update-knows/(?P<pk>\d+)/$', views.update_knows, name='update_knows'), #Action to UPDATE Knows    
    url(r'^delete-knows/(?P<pk>\d+)/$', views.delete_knows, name='delete_knows'), #Action to DELETE Knows


    #JOBS PROFILE DETAILS
    url(r'^profile/jobs/(?P<perfil_id>\d+)/$', views.jobs, name='jobs'),
    url(r'^update-jobs/(?P<pk>\d+)/$', views.update_jobs, name='update_jobs'), #Action to UPDATE Jobs    
    url(r'^delete-jobs/(?P<pk>\d+)/$', views.delete_jobs, name='delete_jobs'), #Action to DELETE Jobs
    
    
    #COMPANY - COMPANY PROFILE DETAILS
    url(r'^profile/company/(?P<perfil_id>\d+)/$', views.company, name='company'),
    url(r'^update-company/(?P<pk>\d+)/$', views.update_company, name='update_company'), #Action to UPDATE Company
    url(r'^delete-company/(?P<pk>\d+)/$', views.delete_company, name='delete_company'), #Action to DELETE Company  
    
        
    #LOCATION - COMPANY PROFILE DETAILS
    url(r'^profile/location/(?P<perfil_id>\d+)/$', views.location, name='location'),
    url(r'^update-location/(?P<pk>\d+)/$', views.update_location, name='update_location'), #Action to UPDATE Company Location
    url(r'^delete-location/(?P<pk>\d+)/$', views.delete_location, name='delete_location'), #Action to DELETE Company Location      
    
    
    #PROFILE MODALS - Man & Woman
    url(r'profile/new/whoami/(?P<perfil_id>\d+)/$', views.new_whoami, name='new_whoami'),
    url(r'profile/new/education/(?P<perfil_id>\d+)/$', views.new_education, name='new_education'),
    url(r'profile/new/knows/(?P<perfil_id>\d+)/$', views.new_knows, name='new_knows'),
    url(r'profile/new/jobs/(?P<perfil_id>\d+)/$', views.new_jobs, name='new_jobs'),
    
    
    #PROFILE MODALS - Company
    url(r'profile/new/company/(?P<perfil_id>\d+)/$', views.new_company, name='new_company'),
    url(r'profile/new/location/(?P<perfil_id>\d+)/$', views.new_location, name='new_location'), 
    
        
    #url(r'^search/$', include('haystack.urls')),
    url(r'^search/$', SearchView(searchqueryset=sqs,), name='search'), #by sqs
    #url(r'^$', FacetedSearchView(form_class=FacetedSearchForm, searchqueryset=sqs), name='haystack_search'),
    #url(r'search/$', views.search, name='tip_search'),
    url(r'^autocomplete/', views.autocomplete, name='autocomplete'), 
     
	#MOBILE
    url(r'^mobile_menu/(?P<perfil_id>\d+)/$', views.mobile_menu, name='mobile_menu'), 
	url(r'^mobile_new_card/(?P<perfil_id>\d+)/$', views.mobile_new_card, name='mobile_new_card'),
    
    #CHAT
    url(r'^chat/(?P<pk>\d+)/$', views.chat, name='chat'),  
    url(r'^chat-room/(?P<perfil_id>\d+)/(?P<pk>\d+)/$', views.chat_room, name='chat_room'), 
    
    #WINDY
    url(r'^windy/$', views.windy, name='windy'),
    
)