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
    (r'^community$', 'community_tree'),
    (r'^community/(?P<id>\d+)$', 'community'),
    (r'^community/join/(?P<id>\d+)$', 'community_join'),
    (r'^community/leave/(?P<id>\d+)$', 'community_leave'),
    (r'^topic/(?P<id>\d+)$', 'topic'),
    (r'^topic/reply$', 'topic_reply'),
    (r'^files$', 'files'),
    (r'^file/download/(?P<id>\d+)$', 'file_download'),
    (r'^file/delete/(?P<id>\d+)$', 'file_delete'),
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',    
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '../media'}),
)
   
