import datetime

from haystack import indexes

from perfis.models import Tip, Deck, Avatar


class TipIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    #author_name = indexes.CharField(model_attr='author_name', faceted=True, indexed=True, boost=1.125)
    #content = indexes.CharField(model_attr='content', faceted=True, indexed=True)
    #reference = indexes.CharField(model_attr='reference', faceted=True, indexed=True)
    content = indexes.CharField(model_attr='content', faceted=True, indexed=True)
    outdoor = indexes.CharField(model_attr='outdoor', faceted=True, indexed=True)
    author_name = indexes.CharField(model_attr='author_name',  faceted=True, indexed=True)
    date = indexes.DateTimeField(model_attr='date', faceted=True, indexed=True)
    author_profile_id = indexes.IntegerField(model_attr='author_profile_id',  faceted=True, indexed=True)
    slug = indexes.CharField(model_attr='slug', faceted=True, indexed=True)
    
    suggestions = indexes.FacetCharField()
    
    def prepare(self, obj):
        prepared_data = super(TipIndex, self).prepare(obj)
        prepared_data['suggestions'] = prepared_data['text']
        return prepared_data
    
    def get_model(self):
        return Tip

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(date__lte=datetime.datetime.now())
    

class DeckIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    deck_name = indexes.CharField(model_attr='deck_name',  faceted=True, indexed=True)
    author_name = indexes.CharField(model_attr='author_name',  faceted=True, indexed=True)
    date = indexes.DateTimeField(model_attr='date', faceted=True, indexed=True)
    
    suggestions = indexes.FacetCharField()
    
    def prepare(self, obj):
        prepared_data = super(DeckIndex, self).prepare(obj)
        prepared_data['suggestions'] = prepared_data['text']
        return prepared_data
    
    def get_model(self):
        return Deck

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(date__lte=datetime.datetime.now())
    
    
class AvatarIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    upload = indexes.CharField(model_attr='upload',  faceted=True, indexed=True)
    profile_id = indexes.IntegerField(model_attr='profile_id',  faceted=True, indexed=True)
    
    suggestions = indexes.FacetCharField()
    
    def prepare(self, obj):
        prepared_data = super(AvatarIndex, self).prepare(obj)
        prepared_data['suggestions'] = prepared_data['text']
        return prepared_data
    
    def get_model(self):
        return Avatar

    def index_queryset(self, using=None):
        return self.get_model().objects
