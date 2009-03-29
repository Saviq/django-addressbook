from django.conf.urls.defaults import *
from django.contrib import databrowse
from models import *

# databrowse
databrowse.site.register(Contact)
databrowse.site.register(Group)
urlpatterns = patterns('',
    (r'^browse/(.*)', databrowse.site.root),
)
