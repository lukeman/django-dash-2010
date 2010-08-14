# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
import elesma.models
import settings

def random_drink_404(request):
    cocktail = elesma.models.Recipe(name="404 Cocktail",
                                    directions="Carefully check the URL you intended to discover, mix in the ingredients, and go.",
                                    category=elesma.models.Category(name="When-You-Typo Cocktail"),
                                    container=elesma.models.Container(name=request.META.get('HTTP_USER_AGENT', 'Your Browser')),
                                    )
    resp = render_to_response('404.html', {'object': cocktail, 'STATIC_URL': settings.STATIC_URL })
    resp.status_code = 404
    return resp
