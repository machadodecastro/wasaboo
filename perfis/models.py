# Create your models here.

#from django.contrib.auth.models import User
import base64
import copy
from datetime import date, datetime
from dircache import listdir
from genericpath import isfile
import hashlib
import hmac
from mimetypes import MimeTypes
import os
import sys

from _mysql import connection
from django import forms
from django.conf import settings
from django.core.context_processors import request
from django.core.files.base import File
from django.core.urlresolvers import reverse
from django.db import models
from django.forms.widgets import Textarea
from django.http.response import HttpResponse
from django.template.defaultfilters import join, slugify
from docutils.nodes import reference
from haystack.forms import ModelSearchForm

import _usuarios
from _usuarios.models import User


#class Perfil(object):
#    def __init__(self, nome='', email='', telefone= '', nome_empresa=''):
#        self.nome = nome
#        self.email = email
#        self.telefone = telefone
#        self.nome_empresa = nome_empresa
class Perfil(models.Model):

    nome = models.CharField(max_length=255, null=False)
    #Classe User ja possui email
    #email = models.CharField(max_length=255, null=False)     
    type = models.CharField(max_length=1, null=False)
    stealth = models.CharField(max_length=1, null=False, default='0')
    color = models.CharField(max_length=1, null=False, default='0')
    map = models.CharField(max_length=1, null=False, default='0')
    
    contatos = models.ManyToManyField('self')
    
    usuario = models.OneToOneField(User, related_name="perfil")

    
    @property
    def email(self):
        return self.usuario.email

    def convidar(self, perfil_convidado):
        convite = Convite(solicitante=self, convidado=perfil_convidado)
        convite.save()
    

class Convite(models.Model):
    solicitante = models.ForeignKey(Perfil, related_name='convites_feitos')
    convidado = models.ForeignKey(Perfil, related_name='convites_recebidos') 
    
    def aceitar(self):
        self.convidado.contatos.add(self.solicitante)
        self.solicitante.contatos.add(self.convidado)
        self.delete()
        

class Avatar(models.Model):
    user_id = models.IntegerField(verbose_name="User identification", blank=False)
    profile_id = models.IntegerField(verbose_name="Profile identification", blank=False)
    upload = models.TextField(verbose_name="Avatar", blank=True)


    
    
class Background(models.Model):
    user_id = models.IntegerField(verbose_name="User identification", blank=False)
    profile_id = models.IntegerField(verbose_name="Profile identification", blank=False)
    bkg_upload = models.FileField(upload_to='backgrounds/%Y/%m/%d', verbose_name="Background", blank=True)
    
    
class Deck(models.Model):
    author_user_id = models.IntegerField(verbose_name="Card user owner", blank=False)
    author_profile_id = models.IntegerField(verbose_name="Card profile owner", blank=False)
    author_name = models.CharField(max_length=100, verbose_name="Author name", blank=False)
    deck_name =  models.TextField(verbose_name="Deck name", blank=False)
    date = models.DateTimeField(auto_now=True)
        
            
class Tip(models.Model):
    author_user_id = models.IntegerField(verbose_name="Card user owner", blank=False)
    author_profile_id = models.IntegerField(verbose_name="Card profile owner", blank=False)
    author_name = models.CharField(max_length=100, verbose_name="Author name", blank=False)
    content =  models.TextField(verbose_name="Card content", blank=True)
    date = models.DateTimeField(auto_now_add=True)
    hided = models.TextField(verbose_name="Hided tips", blank=False)
    reference = models.TextField(verbose_name="References", blank=True, default='')
    link =  models.TextField(verbose_name="Web link", blank=True, default='')
    coin = models.CharField(max_length=1, blank=True)
    price = models.CharField(max_length=100, blank=True)
    local = models.CharField(max_length=100, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    outdoor = models.FileField(upload_to='uploads/%Y/%m/%d', verbose_name="Outdoor", blank=True)
    outdoor2 = models.FileField(upload_to='uploads/%Y/%m/%d', verbose_name="Outdoor2", blank=True)
    outdoor3 = models.FileField(upload_to='uploads/%Y/%m/%d', verbose_name="Outdoor3", blank=True)
    outdoor4 = models.FileField(upload_to='uploads/%Y/%m/%d', verbose_name="Outdoor4", blank=True)
    direction = models.CharField(max_length=1, verbose_name="Image direction", blank=True, default='0')
    direction2 = models.CharField(max_length=1, verbose_name="Image2 direction", blank=True, default='0')
    direction3 = models.CharField(max_length=1, verbose_name="Image3 direction", blank=True, default='0')
    direction4 = models.CharField(max_length=1, verbose_name="Image4 direction", blank=True, default='0')
    hide_image = models.CharField(max_length=1, verbose_name="Hide image", blank=True, default='0')
    hide_image2 = models.CharField(max_length=1, verbose_name="Hide image2", blank=True, default='0')  
    hide_image3 = models.CharField(max_length=1, verbose_name="Hide image3", blank=True, default='0')  
    hide_image4 = models.CharField(max_length=1, verbose_name="Hide image4", blank=True, default='0')    
    slug = models.SlugField(max_length=60, blank=True)
    lat = models.CharField(max_length=100, verbose_name="Lat", blank=True)
    lng = models.CharField(max_length=100, verbose_name="Lng", blank=True)
    world = models.CharField(max_length=1, blank=True, default='0') 
        
    @property
    def is_today(self):
        return datetime.date() == self.date

    def get_absolute_url(self):
        return reverse('show_tip', kwargs={'slug': self.slug, 'id':self.id})
    
    #Then override models save method:
    def save(self, *args, **kwargs):
        if not self.id:
            #Only set the slug when the object is created.
            if self.content:
                self.slug = slugify(self.content)
            else:
                self.slug = slugify('outdoor') #Or whatever you want the slug to use
        else:
            if self.content:
                self.slug = slugify(self.content)
            else:
                self.slug = slugify('outdoor')
        super(Tip, self).save(*args, **kwargs)
        
    @property
    def verify_coin(self):
        if self.coin == '1':
            return 'Dollar'
        elif self.coin == '2':
            return 'Euro'
        else:
            return 'Real'
        
    def docs(self):
        string = "fr-file"
        
        if string in self.reference:
            return self.reference        
        
    
class Image(object):
 
    defaultUploadOptions = {
        "fieldname": "outdoor",
        "validation": {
            "allowedExts": ["gif", "jpeg", "jpg", "png", "svg", "blob"],
            "allowedMimeTypes": ["image/gif", "image/jpeg", "image/pjpeg", "image/x-png", "image/png",
                                 "image/svg+xml"]
        },
        # string resize param from http://docs.wand-py.org/en/0.4.3/guide/resizecrop.html#transform-images
        # Examples: "100x100", "100x100!". Find more on http://www.imagemagick.org/script/command-line-processing.php#geometry
        "resize": None
    }
 
    @staticmethod
    def upload(req, fileRoute, options=None):
        """
        Image upload to disk.
        Parameters:
            req: framework adapter to http request. See BaseAdapter.
            fileRoute: string
            options: dict optional, see defaultUploadOptions attribute
        Return:
            dict: {link: "linkPath"}
        """
 
        if options is None:
            options = Image.defaultUploadOptions
        else:
            options = Utils.merge_dicts(Image.defaultUploadOptions, options)
 
        return Tip.upload(req, fileRoute, options)
 
    @staticmethod
    def delete(src):
        """
        Delete image from disk.
        Parameters:
            src: string
        """
        return Tip.delete(src)
 
    @staticmethod
    def list(folderPath, thumbPath=None):
        """
        List images from disk.
        Parameters:
            folderPath: string
            thumbPath: string
        Return:
            list: list of images dicts. example: [{url: "url", thumb: "thumb", name: "name"}, ...]
        """
 
        if thumbPath == None:
            thumbPath = folderPath
 
        # Array of image objects to return.
        response = []
 
        absoluteFolderPath = Utils.getServerPath() + folderPath
 
        # Image types.
        imageTypes = Image.defaultUploadOptions["validation"]["allowedMimeTypes"]
 
        # Filenames in the uploads folder.
        fnames = [f for f in listdir(absoluteFolderPath) if isfile(join(absoluteFolderPath, f))]
 
        for fname in fnames:
            mime = MimeTypes()
            mimeType = mime.guess_type(absoluteFolderPath + fname)[0]
 
            if mimeType in imageTypes:
                response.append({
                    "url": folderPath + fname,
                    "thumb": thumbPath + fname,
                    "name": fname
                })
 
        return response
 
 
class Utils(object):
    """
    Utils static class.
    """
 
    @staticmethod
    def hmac(key, string, hex=False):
        """
        Calculate hmac.
        Parameters:
            key: string
            string: string
            hex: boolean optional, return in hex, else return in binary
        Return:
            string: hmax in hex or binary
        """
 
        # python 2-3 compatible:
        try:
            hmac256 = hmac.new(key.encode() if isinstance(key, str) else key, msg=string.encode("utf-8") if isinstance(string, str) else string, digestmod=hashlib.sha256) # v3
        except Exception:
            hmac256 = hmac.new(key, msg=string, digestmod=hashlib.sha256) # v2
 
        return hmac256.hexdigest() if hex else hmac256.digest()
 
    @staticmethod
    def merge_dicts(a, b, path=None):
        """
        Deep merge two dicts without modifying them. Source: http://stackoverflow.com/questions/7204805/dictionaries-of-dictionaries-merge/7205107#7205107
        Parameters:
            a: dict
            b: dict
            path: list
        Return:
            dict: Deep merged dict.
        """
 
        aClone = copy.deepcopy(a);
        # Returns deep b into a without affecting the sources.
        if path is None: path = []
        for key in b:
            if key in a:
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    aClone[key] = Utils.merge_dicts(a[key], b[key], path + [str(key)])
                else:
                    aClone[key] = b[key]
            else:
                aClone[key] = b[key]
        return aClone
 
    @staticmethod
    def getExtension(filename):
        """
        Get filename extension.
        Parameters:
            filename: string
        Return:
            string: The extension without the dot.
        """
        return os.path.splitext(filename)[1][1:]
 
    @staticmethod
    def getServerPath():
        """
        Get the path where the server has started.
        Return:
            string: serverPath
        """
        return os.path.abspath(os.path.dirname(sys.argv[0]))
 
    @staticmethod
    def isFileValid(filename, mimetype, allowedExts, allowedMimeTypes):
        """
        Test if a file is valid based on its extension and mime type.
        Parameters:
            filename string
            mimeType string
            allowedExts list
            allowedMimeTypes list
        Return:
            boolean
        """
 
        # Skip if the allowed extensions or mime types are missing.
        if not allowedExts or not allowedMimeTypes:
            return False
 
        extension = Utils.getExtension(filename)
        return extension.lower() in allowedExts and mimetype in allowedMimeTypes
 
    @staticmethod
    def isValid(validation, filePath, mimetype):
        """
        Generic file validation.
        Parameters:
            validation: dict or function
            filePath: string
            mimetype: string
        """
 
        # No validation means you dont want to validate, so return affirmative.
        if not validation:
            return True
 
        # Validation is a function provided by the user.
        if callable(validation):
            return validation(filePath, mimetype)
 
        if isinstance(validation, dict):
            return Utils.isFileValid(filePath, mimetype, validation["allowedExts"], validation["allowedMimeTypes"])
 
        # Else: no specific validating behaviour found.
        return False
 
 
class BaseAdapter(object):
    """
    Interface. Inherit this class to use the lib in your framework.
    """
 
    def __init__(self, request):
        """
        Constructor.
        Parameters:
            request: http request object from some framework.
        """
        self.request = request
 
    def riseError(self):
        """
        Use this when you want to make an abstract method.
        """
        raise NotImplementedError( "Should have implemented this method." )
 
    def getFilename(self, fieldname):
        """
        Get upload filename based on the fieldname.
        Parameters:
            fieldname: string
        Return:
            string: filename
        """
        self.riseError()
 
    def getMimetype(self, fieldname):
        """
        Get upload file mime type based on the fieldname.
        Parameters:
            fieldname: string
        Return:
            string: mimetype
        """
        self.riseError()
 
    def saveFile(self, fieldname, fullNamePath):
        """
        Save the upload file based on the fieldname on the fullNamePath location.
        Parameters:
            fieldname: string
            fullNamePath: string
        """
        self.riseError()
 
 
class DjangoAdapter(BaseAdapter):
    """
    Django Adapter: Check BaseAdapter to see what methods description.
    """
 
    def checkFile(self, fieldname):
        if fieldname not in self.request.FILES:
            raise Exception("File does not exist.")
 
    def getFilename(self, fieldname):
        self.checkFile(fieldname)
        return self.request.FILES[fieldname].name
 
    def getMimetype(self, fieldname):
        self.checkFile(fieldname)
        return self.request.FILES[fieldname].content_type
 
    def saveFile(self, fieldname, fullNamePath):
        print("should save now")
        print("the path" + fullNamePath)
        self.checkFile(fieldname)
 
        with open(fullNamePath, "wb+") as destination:
            for chunk in self.request.FILES[fieldname].chunks():
                destination.write(chunk)   
    
class Favorites(models.Model):
    tip_id = models.ForeignKey(Tip, related_name='favorite_tip')
    profile_id = models.ForeignKey(Perfil, related_name='profile')
    favorite = models.BooleanField(verbose_name="Favotite tips", default=False);
    
class Follow(models.Model):
    follower_id = models.ForeignKey(Perfil, related_name='follower')
    followed_id = models.ForeignKey(Perfil, related_name='followed')
    
class Description(models.Model):
    profile_id = models.ForeignKey(Perfil, related_name='Profile unique')
    description = models.TextField(verbose_name="Short description", blank=False) 
    color = models.CharField(max_length=1, null=False, default='0')
    

class Whoami(models.Model):
    whoami_user_id = models.IntegerField(verbose_name="Who am I User", blank=False)
    whoami_profile_id = models.IntegerField(verbose_name="Who am I Profile", blank=False)
    whoami_name = models.CharField(max_length=100, verbose_name="Who am I profile name", blank=False)
    whoami_content =  models.TextField(verbose_name="Who am I content", blank=False)
    date = models.DateTimeField(auto_now=True)
    
class Education(models.Model):
    education_user_id = models.IntegerField(verbose_name="Education User", blank=False)
    education_profile_id = models.IntegerField(verbose_name="Education Profile ID", blank=False)
    education_name = models.CharField(max_length=100, verbose_name="Education name user", blank=False)
    school =  models.CharField(max_length=100, verbose_name="Education school", blank=False)
    course =  models.CharField(max_length=100, verbose_name="Education concentration", blank=True)
    degree =  models.CharField(max_length=100, verbose_name="Degree Type", blank=True)
    graduation = models.CharField(max_length=10, verbose_name="Graduation year", blank=True)
    date = models.DateTimeField(auto_now=True)   

class Knows(models.Model):
    knows_user_id = models.IntegerField(verbose_name="Knows About User", blank=False)
    knows_profile_id = models.IntegerField(verbose_name="Knows About Profile ID", blank=False)
    topic =  models.CharField(max_length=100, verbose_name="Knows About Topic", blank=False)
    date = models.DateTimeField(auto_now=True)   
    
class Jobs(models.Model):
    jobs_user_id = models.IntegerField(verbose_name="Jobs user", blank=False)
    jobs_profile_id = models.IntegerField(verbose_name="Jobs Profile ID", blank=False)
    company =  models.CharField(max_length=100, verbose_name="Company", blank=False)
    position =  models.CharField(max_length=100, verbose_name="Position in company", blank=True)
    start_year = models.CharField(max_length=10, verbose_name="Start year", blank=True)
    end_year = models.CharField(max_length=10, verbose_name="End year", blank=True)
    status_work = models.BooleanField()
    date = models.DateTimeField(auto_now=True)    
    
class Live(models.Model):
    live_user_id = models.IntegerField(verbose_name="Where user lives", blank=False)
    live_profile_id = models.IntegerField(verbose_name="Where Profile Lives", blank=False)
    location =  models.CharField(max_length=100, verbose_name="Location", blank=False)
    start_year = models.CharField(max_length=10, verbose_name="Start year living", blank=True)
    end_year = models.CharField(max_length=10, verbose_name="End year living", blank=True)
    status_live = models.BooleanField()
    date = models.DateTimeField(auto_now=True)        
        
class Hobby(models.Model):
    hobby_user_id = models.IntegerField(verbose_name="Hobbies User", blank=False)
    hobby_profile_id = models.IntegerField(verbose_name="Hobbies Profile", blank=False)
    hobby_content =  models.TextField(verbose_name="Hobbies content", blank=False)
    date = models.DateTimeField(auto_now=True)   
        
class Company(models.Model):
    company_user_id = models.IntegerField(verbose_name="Company User ID", blank=False)
    company_profile_id = models.IntegerField(verbose_name="Company Profile ID", blank=False)
    company_content =  models.TextField(verbose_name="Company content", blank=False)
    date = models.DateTimeField(auto_now=True)  
    
class Offer(models.Model):
    offer_user_id = models.IntegerField(verbose_name="Job offers ID", blank=False)
    offer_profile_id = models.IntegerField(verbose_name="Job offers Profile ID", blank=False)
    offer_title =  models.CharField(max_length=100, verbose_name="Jof offer title", blank=False)
    offer_skills =  models.TextField(verbose_name="Job offer skills", blank=False)
    offer_benefits =  models.TextField(verbose_name="Job offer benefits", blank=False)
    date = models.DateTimeField(auto_now=True) 
    more =   models.TextField(verbose_name="More about Job offer", blank=True)
    
class Location(models.Model):
    location_user_id = models.IntegerField(verbose_name="Company user id", blank=False)
    location_profile_id = models.IntegerField(verbose_name="Company location profile id", blank=False)
    address =  models.CharField(max_length=100, verbose_name="Company address", blank=False)
    date = models.DateTimeField(auto_now=True)            
    
class Folder(models.Model):
    card_id = models.ForeignKey(Tip, related_name='saved_card_id')
    profile_id = models.ForeignKey(Perfil, related_name='profile_id')
    folder_id = models.ForeignKey(Deck, related_name='folder_id') 
    
class RemovedBy(models.Model):
    card_id = models.ForeignKey(Tip, related_name='card_removed')
    profile_id = models.ForeignKey(Perfil, related_name='profile_removes')
    removed_by = models.CharField(max_length=1, null=False, default=0)  
    
class Mensagem(models.Model):
    outdoor = models.IntegerField(verbose_name="Outdoor ID", blank=False)
    destino = models.CharField(max_length=100, verbose_name="ID do perfil de destino", blank=False)
    origem = models.CharField(max_length=100, verbose_name="ID do perfil de origem", blank=False)
    status = models.CharField(max_length=100, verbose_name="Status", blank=False)
    corpo = models.TextField(verbose_name="Corpo da mensagem", blank=False)
    criacao = models.DateTimeField(default=datetime.now, blank=False)
    
    
