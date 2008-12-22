from django.conf.urls.defaults import *
from django.contrib import databrowse
from models import *

urlpatterns = patterns('addressbook.views', 
    url(r'^$', 'main', name='addressbook-main'),
    url(r'^contact/(?P<contact_id>\d+)/$', 'contact_detail', name='addressbook-contact-detail'),
)

# databrowse
databrowse.site.register(Contact)
databrowse.site.register(Group)
urlpatterns += patterns('',
    (r'^browse/(.*)', databrowse.site.root),
)