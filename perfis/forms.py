from django import forms
from django.db.models.base import Model
from django.forms.models import ModelForm
from haystack.forms import ModelSearchForm

from perfis.models import  Tip, Favorites, Perfil, Avatar, Whoami, Education, Knows, \
    Jobs, Live, Hobby, Company, Offer, Location, Deck, Background, Mensagem


class DeckForm(ModelForm): 
    class Meta: 
        model = Deck
        
class TipForm(ModelForm): 
    class Meta: 
        model = Tip
        
class PerfilForm(ModelForm): 
    class Meta: 
        model = Perfil        
        
class FavoriteForm(ModelForm): 
    class Meta: 
        model = Favorites   
        
class AvatarForm(ModelForm): 
    class Meta: 
        model = Avatar
        
        
#Profile Classes
class WhoamiForm(ModelForm): 
    class Meta: 
        model = Whoami   
        
class EducationForm(ModelForm): 
    class Meta: 
        model = Education  
        
class KnowsForm(ModelForm): 
    class Meta: 
        model = Knows  
        
class JobsForm(ModelForm): 
    class Meta: 
        model = Jobs      
        
class LiveForm(ModelForm): 
    class Meta: 
        model = Live   
        
class HobbyForm(ModelForm): 
    class Meta: 
        model = Hobby  
        
class CompanyForm(ModelForm): 
    class Meta: 
        model = Company  
        
class OfferForm(ModelForm): 
    class Meta: 
        model = Offer 
        
class LocationForm(ModelForm): 
    class Meta: 
        model = Location        
        
class BackgroundForm(ModelForm): 
    class Meta: 
        model = Background  
        
class MensagemForm(ModelForm): 
    class Meta: 
        model = Mensagem  
        
                                                  