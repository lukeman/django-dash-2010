from django.conf import settings
from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
    url(r'^vote$', "elesma.ajax_views.vote"),
)
