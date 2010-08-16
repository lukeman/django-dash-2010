from django.http import HttpResponse, HttpResponseServerError
import django.utils.simplejson as simplejson
import elesma.models
from django.contrib.auth.decorators import login_required
from haystack.query import SearchQuerySet

DEFAULT_SUGGESTIONS_COUNT = 5

def api_response(http_code, data):
    if http_code == 200:
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    else:
        return HttpResponseServerError(simplejson.dumps(data), mimetype="application/json")

def suggestions(request):
    def make_result(obj):
        return [x.object.get_absolute_url(), x.name.capitalize(), x.name]

    if request.method == "GET":
        if request.GET.has_key('q'):
            query = request.GET['q']
            count = (request.GET.has_key('count') and request.GET['count']) or DEFAULT_SUGGESTIONS_COUNT
            results = SearchQuerySet().filter(content=query)[:count]
            recipes = { 'title':'Recipes',
                        'results':[make_result(x)  for x in results if x.model_name == 'recipe'],
                        }
            ingredients = { 'title': 'Ingredients',
                            'results':[make_result(x)  for x in results if x.model_name == 'ingredient'],
                            }
            return api_response(200, [recipes, ingredients])
        return api_response(500, {'error': "Search requests must specify parameter q." })
    return api_response(500, {'error': "Search requests must use GET." })

@login_required
def vote(request):
    recipe = elesma.models.Recipe.objects.all()[0]
    if request.method == "POST":
        post = request.POST.copy()
        if post.has_key('slug') and post.has_key('score'):
            try:
                slug = post['slug']
                score = int(post['score'])
                recipe = elesma.models.Recipe.objects.get(slug=slug)
                # don't count two votes on one recipe as multiple votes
                if not recipe.rating.get_rating_for_user(request.user, request.META['REMOTE_ADDR']):
                    profile = request.user.get_profile()
                    profile.votes += 1
                    profile.save()
                recipe.rating.add(score=score, user=request.user, ip_address=request.META['REMOTE_ADDR'])
                return api_response(200, {'score': score, 'slug': slug })
            except ValueError:
                return api_response(500, {'error': "%s is an invalid score." % score })
            except Exception, e:
                return api_response(500, {'error': "Voting failed."})
        else:
            return api_response(500, {'error': "Must specify both 'slug' and 'score'." })
    return api_response(500, {'error': "Voting requests must use POST." })



