# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
import elesma.models
import settings
from djangoratings.models import Vote
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm, CheckboxSelectMultiple, ModelMultipleChoiceField
from uni_form.helpers import FormHelper, Submit, Reset, Layout, Fieldset, Row, HTML
from django.template.defaultfilters import slugify
from django.core.exceptions import ObjectDoesNotExist


def user(request, username=None):
    user = get_object_or_404(User, username=username)
    votes = Vote.objects.filter(user=user)
    return render_to_response('elesma/profile.html',
                              { 'object': user,
                                'votes': votes,
                                },
                              context_instance=RequestContext(request))

class RecipeForm(ModelForm):
    ingredients = ModelMultipleChoiceField(queryset=elesma.models.Ingredient.objects.all().order_by('name'),
                                           required=True,
                                           widget=CheckboxSelectMultiple)

    class Meta:
        model = elesma.models.Recipe
        fields = ('name', 'description', 'directions', 'category', 'container', 'ingredients')

    helper = FormHelper()
    layout = Layout(Fieldset('Describe your Drink','name', 'category', 'container', 'description'),
                   Fieldset('Record the Recipe', 'directions','ingredients'),
                   )
    helper.add_layout(layout)
    helper.add_input(Submit('create', 'Create Cocktail'))

@login_required
def create_recipe(request):
    if request.method == 'POST':
        formset = RecipeForm(request.POST, request.FILES)
        if formset.is_valid():
            recipe = formset.save(commit=False)
            recipe.slug = slugify(recipe.name)
            try:
                recipe.save()
            finally:
                return HttpResponseRedirect(reverse('elesma.views.recipe', kwargs={'slug': recipe.slug}))
    else:
        formset = RecipeForm()
    return render_to_response('elesma/create_recipe.html',
                              { 'form': formset,
                                },
                              context_instance=RequestContext(request))

def recipe(request, slug):
    recipe = get_object_or_404(elesma.models.Recipe, slug=slug)
    vote = recipe.rating.get_rating_for_user(request.user, request.META['REMOTE_ADDR'])
    return render_to_response('elesma/recipe.html',
                              { 'object': recipe,
                                'vote': vote,
                                },
                              context_instance=RequestContext(request))

def random_drink(request):
    recipe = elesma.models.Recipe.objects.all().order_by('?')[0]
    return HttpResponseRedirect(reverse('elesma.views.recipe', kwargs={'slug': recipe.slug}))

def ingredient(request):
    # @TODO: handle more than one ingredient
    for ingredient_name in request.GET.getlist('ingredient'):
        ingredient = get_object_or_404(elesma.models.Ingredient, name__iexact=ingredient_name)
        recipes = ingredient.recipe_set.all()
        return render_to_response('elesma/ingredients.html',
                                  { 'objects': [ingredient],
                                    'recipes': recipes,
                                    },
                                  context_instance=RequestContext(request))
    return HttpResponseNotFound()




def user_leaderboard(request):
    profiles = elesma.models.UserProfile.objects.all().order_by('-votes')[:10]
    print profiles
    return render_to_response('elesma/user_leaderboard.html',
                              { 'objects': profiles },
                              context_instance=RequestContext(request))

def recipe_leaderboard(request):
    qs = elesma.models.Recipe.objects.extra(select={
            'rating_rank': '((100/%s*rating_score/(rating_votes+%s))+100)/2' % (elesma.models.Recipe.rating.range,
                                                                           elesma.models.Recipe.rating.weight)
            })
    qs = qs.order_by('-rating_rank')
    return render_to_response('elesma/recipe_leaderboard.html',
                              { 'objects': qs },
                              context_instance=RequestContext(request))

def random_drink_404(request):
    cocktail = elesma.models.Recipe(name="404 Cocktail",
                                    directions="Carefully check the URL you intended to discover, mix in the ingredients, and go.",
                                    category=elesma.models.Category(name="When-You-Typo Cocktail"),
                                    container=elesma.models.Container(name=request.META.get('HTTP_USER_AGENT', 'Your Browser')),
                                    )
    resp = render_to_response('404.html',
                              {'object': cocktail },
                              context_instance=RequestContext(request))
    resp.status_code = 404
    return resp
