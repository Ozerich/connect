from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('main.views',
    (r'^$', 'index'),
    (r'^login$', 'login'),
    (r'^logout$', 'logout'),
    (r'^register$', 'registration'),
    (r'^(?P<userid>\d+)$', 'profile'),
    (r'^friends$', 'friends'),
    (r'^messages$', 'messages'),
    (r'^messages/view/(?P<id>\d+)$', 'viewmsg'),
    (r'^messages/send/(?P<id>\d+)$', 'sendmsg'),
    (r'^messages/delete/(?P<id>\d+)$', 'deletemsg'),
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',    
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '../media'}),
)
   
