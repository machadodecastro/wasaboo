from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import url
from django.contrib.admin.templatetags.admin_list import results
from django.core.files import images
from django.core.paginator import Paginator, InvalidPage
from django.db.models.query_utils import Q
from django.http import Http404, request
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from haystack import query
from haystack.forms import ModelSearchForm, FacetedSearchForm
from haystack.inputs import Raw
from haystack.query import EmptySearchQuerySet, SearchQuerySet

from perfis.models import Tip, Avatar, Favorites
from perfis.views import get_perfil_logado, favorites


RESULTS_PER_PAGE = getattr(settings, 'HAYSTACK_SEARCH_RESULTS_PER_PAGE', 20)


class SearchView(object):
    template = 'search/search.html'
    extra_context = {}
    query = ''
    results = EmptySearchQuerySet()
    request = None
    form = None
    results_per_page = RESULTS_PER_PAGE

    def __init__(self, template=None, load_all=True, form_class=None, searchqueryset=None, context_class=RequestContext, results_per_page=None):
        self.load_all = load_all
        self.form_class = form_class
        self.context_class = context_class
        self.searchqueryset = searchqueryset

        if form_class is None:
            self.form_class = ModelSearchForm

        if not results_per_page is None:
            self.results_per_page = results_per_page

        if template:
            self.template = template

    def __call__(self, request):
        """
        Generates the actual response to the search.

        Relies on internal, overridable methods to construct the response.
        """
        self.request = request

        self.form = self.build_form()
        self.query = self.get_query()
        self.results = self.get_results()

        return self.create_response()

    def build_form(self, form_kwargs=None):
        """
        Instantiates the form the class should use to process the search query.
        """
        data = None
        kwargs = {
            'load_all': self.load_all,
        }
        if form_kwargs:
            kwargs.update(form_kwargs)

        if len(self.request.GET):
            data = self.request.GET

        if self.searchqueryset is not None:
            kwargs['searchqueryset'] = self.searchqueryset

        return self.form_class(data, **kwargs)

    def get_query(self):
        """
        Returns the query provided by the user.

        Returns an empty string if the query is invalid.
        """
        if self.form.is_valid():
            return self.form.cleaned_data['q']

        return ''

    def get_results(self):
        """
        Fetches the results via the form.

        Returns an empty list if there's no query to search with.
        """
        return self.form.search()

    def build_page(self):
        """
        Paginates the results appropriately.

        In case someone does not want to use Django's built-in pagination, it
        should be a simple matter to override this method to do what they would
        like.
        """
        try:
            page_no = int(self.request.GET.get('page', 1))
        except (TypeError, ValueError):
            raise Http404("Not a valid number for page.")

        if page_no < 1:
            raise Http404("Pages should be 1 or greater.")

        start_offset = (page_no - 1) * self.results_per_page
        self.results[start_offset:start_offset + self.results_per_page]

        paginator = Paginator(self.results, self.results_per_page)

        try:
            page = paginator.page(page_no)
        except InvalidPage:
            raise Http404("No such page!")

        return (paginator, page)

    def extra_context(self):
        if self.request.user.is_authenticated():
            context = { 'suggestion': None,
                        'url': '127.0.0.1:8000',
                        'perfil_logado': self.request.user.perfil,
                        'my_profile_image': Tip.objects.raw("""SELECT a.id, a.upload as upload, a.user_id
                                            FROM wsbodb.perfis_avatar a LEFT JOIN wsbodb.perfis_perfil p
                                            ON(a.user_id = p.usuario_id)
                                            WHERE p.usuario_id = %s;""", [self.request.user.id]),
                        'has_profile_image' : Tip.objects.raw("""SELECT a.id, ifnull(a.upload,0) as upload 
                                            FROM wsbodb.perfis_avatar a
                                            WHERE a.profile_id = %s;""", [self.request.user.perfil.id]),
                        'is_contact': Tip.objects.raw("""SELECT t.id, f.followed_id as fid, p.nome as name, t.content, 
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
                                        ORDER BY t.date DESC;""", [self.request.user.id, self.request.user.id, self.request.user.id]),
                        'folder': Tip.objects.raw("""SELECT  d.id, 
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
                                            AND t.id = fol.card_id;""", [self.request.user.perfil.id]),    
                        'decks': Tip.objects.raw("""SELECT  d.id, 
                                            d.author_profile_id as fid, 
                                            d.author_user_id as user, 
                                            d.date as date,  
                                            d.author_name as name,
                                            d.deck_name as deck_name 
                                            FROM wsbodb.perfis_deck d
                                            WHERE d.author_user_id = %s
                                            ORDER BY d.deck_name ASC;""", [self.request.user.id]), 
                        'results': Tip.objects.raw("""SELECT t.id, p.nome as name, t.content, 
                                    t.author_profile_id as author, p.type as type,
                                    (t.id IN (SELECT fold.card_id FROM wsbodb.perfis_folder fold WHERE fold.profile_id=%s)) as saved,
                                    (t.id IN (SELECT r.card_id FROM wsbodb.perfis_removed r WHERE r.profile_id=%s)) as removed,
                                    (t.author_profile_id IN (SELECT p.id FROM wsbodb.perfis_perfil p WHERE p.stealth=1)) as stealthed,
                                    (t.id IN (SELECT n.referenced_card FROM wsbodb.perfis_notifications n WHERE n.card_id NOT IN (SELECT re.card_id FROM wsbodb.perfis_removed re) AND t.author_profile_id=%s)) as notified,
                                    p.usuario_id as profile_id, t.author_name as name,
                                    t.date, ifnull(f.id,0) as isfollowing, ifnull(fav.id,0) as isfav, 
                                    f.followed_id, ifnull(a.upload,0) as upload, t.outdoor
                                    FROM wsbodb.perfis_perfil p, wsbodb.perfis_follow f,
                                    wsbodb.perfis_avatar a,
                                    wsbodb.perfis_deck d,
                                    wsbodb.perfis_tip t LEFT JOIN wsbodb.perfis_favorites fav 
                                    ON (t.id = fav.tip_id AND fav.profile_id = %s)  
                                    WHERE (t.content LIKE trim(%s) OR REPLACE(t.content, ' ', '') = REPLACE(trim(%s), ' ', '')
                                    OR t.author_name LIKE trim(%s) OR REPLACE(t.author_name, ' ', '') = REPLACE(trim(%s), ' ', ''))
                                    AND p.usuario_id = %s                                
                                    AND t.hided = 0
                                    AND t.author_profile_id = a.profile_id
                                    GROUP BY t.id
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""", 
                                    [self.request.user.perfil.id, self.request.user.id, self.request.user.perfil.id, self.request.user.id, '%%'+self.query+'%%', self.query, '%%'+self.query+'%%', self.query, self.request.user.id]),
                                           
                            #Cards Notifications
                            'notifications_count': Tip.objects.raw("""SELECT n.id, n.referenced_card,
                                    COUNT(*) as howmany
                                    FROM wsbodb.perfis_notifications n
                                    LEFT JOIN wsbodb.perfis_tip t
                                    ON t.id = n.referenced_card
                                    WHERE n.card_id NOT IN (SELECT re.card_id FROM wsbodb.perfis_removed re)
                                    AND t.author_profile_id = %s
                                    GROUP BY n.referenced_card;""", [self.request.user.perfil.id])                    
                       }

            
            if self.results.query.backend.include_spelling:
                suggestion = self.form.get_suggestion()
                if suggestion != self.query:
                    context['suggestion'] = suggestion
    
            return context 
        
        else:
            context = { 'suggestion': None,
                        'url': '127.0.0.1:8000',
                        'results': Tip.objects.raw("""SELECT t.id, p.nome as name, t.content, 
                                    t.author_profile_id as author, p.type as type,
                                    p.usuario_id as profile_id, t.author_name as name,
                                    t.date, ifnull(f.id,0) as isfollowing, 
                                    f.followed_id, ifnull(a.upload,0) as upload, t.outdoor
                                    FROM wsbodb.perfis_perfil p, wsbodb.perfis_follow f,
                                    wsbodb.perfis_avatar a,
                                    wsbodb.perfis_tip t
                                    WHERE (t.content LIKE trim(%s) OR REPLACE(t.content, ' ', '') = REPLACE(trim(%s), ' ', '')
                                    OR t.author_name LIKE trim(%s) OR REPLACE(t.author_name, ' ', '') = REPLACE(trim(%s), ' ', ''))
                                    AND t.hided = 0
                                    AND t.author_profile_id = a.profile_id
                                    GROUP BY t.id
                                    ORDER BY ifnull(t.updated_date,t.date) DESC;""", 
                                    ['%%'+self.query+'%%', self.query, '%%'+self.query+'%%', self.query]),
                       }

            
            if self.results.query.backend.include_spelling:
                suggestion = self.form.get_suggestion()
                if suggestion != self.query:
                    context['suggestion'] = suggestion
    
            return context 

    def create_response(self):
        """
        Generates the actual HttpResponse to send back to the user.
        """
        (paginator, page) = self.build_page()

           
        context = {
            'query': self.query,
            'form': self.form,
            'page': page,
            'paginator': paginator,
            'suggestion': None,
        }

        if self.results is not None and hasattr(self.results, 'query') and self.results.query.backend.include_spelling:
        #if self.results is not None and hasattr(self.results, 'query') and self.results.query.backend.include_spelling:
            context['suggestion'] = self.form.get_suggestion()
            

        context.update(self.extra_context())
        return render_to_response(self.template, context, context_instance=self.context_class(self.request))
    


def search_view_factory(view_class=SearchView, *args, **kwargs):
    def search_view(request):
        return view_class(*args, **kwargs)(request)
    return search_view


class FacetedSearchView(SearchView):
    def __init__(self, *args, **kwargs):
        # Needed to switch out the default form class.
        if kwargs.get('form_class') is None:
            kwargs['form_class'] = FacetedSearchForm

        super(FacetedSearchView, self).__init__(*args, **kwargs)

    def build_form(self, form_kwargs=None):
        if form_kwargs is None:
            form_kwargs = {}

        # This way the form can always receive a list containing zero or more
        # facet expressions:
        form_kwargs['selected_facets'] = self.request.GET.getlist("selected_facets")

        return super(FacetedSearchView, self).build_form(form_kwargs)

    def extra_context(self):
        extra = super(FacetedSearchView, self).extra_context()
        extra['request'] = self.request
        extra['facets'] = self.results.facet_counts()
        return extra



def basic_search(request, template='search/search.html', load_all=True, form_class=ModelSearchForm, searchqueryset=None, context_class=RequestContext, extra_context=None, results_per_page=None):

    """
    A more traditional view that also demonstrate an alternative
    way to use Haystack.

    Useful as an example of for basing heavily custom views off of.

    Also has the benefit of thread-safety, which the ``SearchView`` class may
    not be.

    Template:: ``search/search.html``
    Context::
        * form
          An instance of the ``form_class``. (default: ``ModelSearchForm``)
        * page
          The current page of search results.
        * paginator
          A paginator instance for the results.
        * query
          The query received by the form.
    """
    query = ''
    results = EmptySearchQuerySet()

    if request.GET.get('q'):
        form = form_class(request.GET, searchqueryset=searchqueryset, load_all=load_all)

        if form.is_valid():
            query = form.cleaned_data['q']
            results = form.search()
    else:
        form = form_class(searchqueryset=searchqueryset, load_all=load_all)

    paginator = Paginator(results, results_per_page or RESULTS_PER_PAGE)

    try:
        page = paginator.page(int(request.GET.get('page', 1)))
    except InvalidPage:
        raise Http404("No such page of results!")

    context = {
        'form': form,
        'page': page,
        'paginator': paginator,
        'query': query,
        'suggestion': None,
    }


    if results.query.backend.include_spelling:
        context['suggestion'] = form.get_suggestion()

    if extra_context:
        context.update(extra_context)

    return render_to_response(template, context, context_instance=context_class(request))



