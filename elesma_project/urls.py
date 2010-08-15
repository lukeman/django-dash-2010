from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

from pinax.apps.account.openid_consumer import PinaxConsumer


handler500 = "pinax.views.server_error"
handler404 = "elesma.views.random_drink_404"


urlpatterns = patterns("",
    url(r"^$", direct_to_template, {
        "template": "homepage.html",
    }, name="home"),
    url(r'^recipe/(?P<slug>[-\w]+)/$', "elesma.views.recipe", name="recipe_detail"),
    url(r'^leaderboard/drinkers/$', "elesma.views.user_leaderboard"),
    url(r'^random-drink/$', "elesma.views.random_drink"),
    url(r'^leaderboard/recipes/$', "elesma.views.recipe_leaderboard"),
    url(r"^admin/invite_user/$", "pinax.apps.signup_codes.views.admin_invite_user", name="admin_invite_user"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("pinax.apps.account.urls")),
    url(r"^openid/(.*)", PinaxConsumer()),
    url(r'^search/', include('haystack.urls')),
    url(r'^404.html$', "elesma.views.random_drink_404"),
    url(r'^ajax/', include('elesma.ajax_urls')),

)

if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r"", include("staticfiles.urls")),
    )
