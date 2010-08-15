# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
import elesma.models
import settings


def user(request, username=None):
    user = get_object_or_404(User, username=username)
    return render_to_response('elesma/profile.html',
                              { 'object': user },
                              context_instance=RequestContext(request))

def recipe(request, slug):
    recipe = get_object_or_404(elesma.models.Recipe, slug=slug)
    return render_to_response('elesma/recipe.html',
                              { 'object': recipe },
                              context_instance=RequestContext(request))

def random_drink(request):
    recipe = elesma.models.Recipe.objects.all().order_by('?')[0]
    return HttpResponseRedirect(reverse('elesma.views.recipe', kwargs={'slug': recipe.slug}))

def user_leaderboard(request):
    profiles = elesma.models.UserProfile.objects.all().order_by('-votes')[:10]
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
