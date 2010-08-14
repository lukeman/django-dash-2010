from django.http import HttpResponse, HttpResponseServerError
import django.utils.simplejson as simplejson
import elesma.models
from django.contrib.auth.decorators import login_required


def api_response(http_code, data):
    if http_code == 200:
        data['success'] = True
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    else:
        data['success'] = False
        return HttpResponseServerError(simplejson.dumps(data), mimetype="application/json")

@login_required
def vote(request):
    recipe = elesma.models.Recipe.objects.all()[0]
    if request.method == "POST":
        post = request.POST.copy()
        if post.has_key('recipe') and post.has_key('score'):
            try:
                slug = post['slug']
                score = int(post['score'])
                recipe = elesma.models.Recipe(slug=slug)
                recipe.rating.add(score=score, user=request.user, ip_address=request.META['REMOTE_ADDR'])
                # don't count two votes on one recipe as multiple votes
                if not recipe.rating.get_rating_for_user(request.user, request.META['REMOTE_ADDR']):
                    profile = request.user.get_profile()
                    profile.score += 1
                    profile.save()
                return api_response(200, {'score': score, 'slug': slug })
            except ValueError:
                return api_response(500, {'error': "%s is an invalid score." % score })
            except Exception, e:
                return api_response(500, {'error': "Voting failed."})
        else:
            return api_response(500, {'error': "Must specify both 'recipe' and 'score'." })
    return api_response(500, {'error': "Voting requests must use POST." })



